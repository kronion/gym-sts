import atexit
import datetime
import logging
import pathlib
import random
import shutil
import string
import subprocess
import tempfile
import time
from typing import Callable, Optional, Tuple

import docker
import gymnasium as gym
from docker.models.containers import Container

from gym_sts import constants, exceptions
from gym_sts.communication import Communicator
from gym_sts.data.state_logger import StateLogger
from gym_sts.spaces.actions import ACTION_SPACE, ACTIONS, Action
from gym_sts.spaces.observations import OBSERVATION_SPACE, Observation

from .action_validation import validate
from .types import ResetParams
from .utils import Cache, SeedHelpers, full_game_obs_value


CONTAINER_OUTDIR = "/game/out"
CONTAINER_LIBDIR = "/game/lib"
CONTAINER_MODSDIR = "/game/mods"


logger = logging.getLogger(__name__)


class SlayTheSpireGymEnv(gym.Env):
    def __init__(
        self,
        lib_dir: str,
        mods_dir: str,
        output_dir: Optional[str] = None,
        headless: bool = False,
        animate: bool = True,
        reboot_frequency: Optional[int] = None,
        reboot_on_error: bool = False,
        value_fn: Callable[[Observation], float] = full_game_obs_value,
        ascension: int = 0,
        log_states: bool = False,
        verbose: bool = True,
    ):
        """
        Gym env to interact with the Slay the Spire video game.

        Args:
            lib_dir: The directory containing desktop-1.0.jar and ModTheSpire.jar.
            mods_dir: The directory containing BaseMod.jar and CommunicationMod.jar.
            output_dir: Directory used for communication between env and containers.
                If None, a temporary directory will be created and later cleaned up.
            headless: If True, run the game in a headless Docker container. Otherwise,
                run the game directly on the host (presumably with a visible interface).
            animate: If True, the game UI will update as normal, which costs CPU time.
                If False, the game will stop rendering frames, causing the UI to appear
                frozen in place, but saving CPU.
            reboot_frequency: Reboot the game every n resets. This stops memory leaks.
            reboot_on_error: Reboot the game if an error (e.g. timeout) occurs.
            verbose: Controls the verbosity of CommunicationMod.
        """

        self.lib_dir = pathlib.Path(lib_dir).resolve()
        self.mods_dir = pathlib.Path(mods_dir).resolve()

        self.headless = headless
        self.container_name = None
        if self.headless:
            self.container_name = "sts-" + "".join(
                random.choices(string.ascii_lowercase, k=8)
            )

        self._current_dir = pathlib.Path.cwd()
        self._output_temp_dir = None
        if output_dir is None:
            self._output_temp_dir = tempfile.TemporaryDirectory(prefix="sts-")
            output_dir = self._output_temp_dir.name
        self.output_dir = pathlib.Path(output_dir).resolve()
        if self.container_name:
            self.output_dir = self.output_dir / self.container_name
            self.output_dir.mkdir(exist_ok=True)

        self._gamefile_temp_dir = tempfile.TemporaryDirectory(
            prefix="sts-", suffix="-gamefiles"
        )
        self.gamefile_dir = pathlib.Path(self._gamefile_temp_dir.name).resolve()

        self.input_path = self.output_dir / "stsai_input"
        self.output_path = self.output_dir / "stsai_output"
        self.logfile_path = self.output_dir / "stderr.log"

        # Create screenshots directory
        self.screenshots_dir = pathlib.Path(CONTAINER_OUTDIR) / "screenshots"
        (self.output_dir / "screenshots").mkdir(exist_ok=True)

        self.logfile = self.logfile_path.open("wb")

        self.container: Optional[Container] = None
        self.process: Optional[subprocess.Popen] = None

        self.reboot_frequency = reboot_frequency
        self.reset_count = 0
        self.reboot_on_error = reboot_on_error

        self.verbose = verbose

        # Animation can be toggled at any time using set_animate()
        self.animate = animate

        # The seed used to initialize the env's PRNG, which is used to
        # generate the seeds used by the game itself.
        self.seed: Optional[int] = None

        # Similar to above, typically used to return the PRNG to a previously
        # observed state.
        self.rng_state: Optional[tuple] = None

        self.prng: Optional[random.Random] = None
        self.sts_seed: Optional[str] = None  # The seed used by the game.

        self.action_space = ACTION_SPACE
        self.observation_space = OBSERVATION_SPACE

        self.observation_cache: Cache[Observation] = Cache()

        self.value_fn = value_fn

        self.ascension = ascension

        # Create states directory
        self.log_states = log_states
        self.states_dir = self.output_dir / "states"
        self.states_dir.mkdir(exist_ok=True)
        self.state_logger: StateLogger = StateLogger(self.states_dir)

        atexit.register(self.close)

    @classmethod
    def build_image(cls, verbose: bool = True) -> None:
        cls._generate_communication_mod_config(headless=True, verbose=verbose)

        client = docker.from_env()
        client.images.build(
            path=str(constants.PROJECT_ROOT / "build"), tag=constants.DOCKER_IMAGE_TAG
        )

    @classmethod
    def _generate_communication_mod_config(
        cls,
        headless: bool,
        input_path: pathlib.Path | None = None,
        output_path: pathlib.Path | None = None,
        home_path: pathlib.Path | None = None,
        verbose: bool = True,
    ) -> None:
        """
        Create the config file CommunicationMod uses to start a subprocess.

        WARNING: This function will silently overwrite any existing config file.
        """

        if headless:
            command = "/game/pipe_to_host.sh"
            config_file = pathlib.Path(
                constants.PROJECT_ROOT / "build" / "communication_mod.config.properties"
            ).resolve()
        else:
            if input_path is None:
                raise Exception("input_path is required when not headless")
            if output_path is None:
                raise Exception("output_path is required when not headless")

            if home_path is None:
                home_path = pathlib.Path.home()

            pipe_script = (
                constants.PROJECT_ROOT / "build" / "pipe_locally.sh"
            ).resolve()
            command = f"{pipe_script} {input_path} {output_path}"

            config_file = (
                home_path
                / ".config"
                / "ModTheSpire"
                / "CommunicationMod"
                / "config.properties"
            )
            config_file.parent.mkdir(parents=True, exist_ok=True)

        with config_file.open(mode="w") as f:
            f.write(f"command={command}\n")
            f.write("runAtGameStart=true\n")
            if verbose:
                f.write("verbose=true\n")

    def _generate_superfastmode_config(self, home_path: pathlib.Path | None = None) -> None:
        """
        Create the config file for SuperFastMode.

        WARNING: This function will silently overwrite any existing config file.
        """

        if home_path is None:
            home_path = pathlib.Path.home()

        config_file = (
            home_path
            / ".config"
            / "ModTheSpire"
            / "SuperFastMode"
            / "SuperFastModeConfig.properties"
        )
        config_file.parent.mkdir(parents=True, exist_ok=True)

        with config_file.open(mode="w") as f:
            f.write(
                "isDeltaMultiplied=true\ndeltaMultiplier=100.0\n"
                "EXISTS=YES INDEED I EXIST\nisInstantLerp=true\n"
            )

    def _run_container(self) -> None:
        logger.info("Starting STS in Docker container")
        self.client = docker.from_env()
        try:
            self.client.images.get(constants.DOCKER_IMAGE_TAG)
        except docker.errors.ImageNotFound:
            raise Exception(
                f"{constants.DOCKER_IMAGE_TAG} image not found. "
                "Please build it with SlayTheSpireGymEnv.build_image()"
            )

        self.container = self.client.containers.run(
            image=constants.DOCKER_IMAGE_TAG,
            name=self.container_name,
            remove=True,
            init=True,
            detach=True,
            volumes={
                self.output_dir: dict(bind=CONTAINER_OUTDIR, mode="rw"),
                self.lib_dir: dict(bind=CONTAINER_LIBDIR, mode="ro"),
                self.mods_dir: dict(bind=CONTAINER_MODSDIR, mode="ro"),
            },
        )
        logger.info(f"Started docker container {self.container.name}")
        logger.info(f"To view logs, run `docker logs {self.container.name}`.")

    def _run_locally(self) -> None:
        logger.info("Starting STS on the host machine")

        # Create a sandbox directory where the subprocess will run
        tmp_dir = self.gamefile_dir

        shutil.copytree(str(self.lib_dir), str(tmp_dir), dirs_exist_ok=True)
        shutil.copytree(str(self.mods_dir), str(tmp_dir / "mods"), dirs_exist_ok=True)
        preferences = constants.PROJECT_ROOT / "build" / "preferences"
        shutil.copytree(
            str(preferences), str(tmp_dir / "preferences"), dirs_exist_ok=True
        )

        displayconfig_path = constants.PROJECT_ROOT / "build" / "info.displayconfig"
        shutil.copy(str(displayconfig_path), str(tmp_dir / "info.displayconfig"))

        self._generate_communication_mod_config(
            headless=False,
            input_path=self.input_path,
            output_path=self.output_path,
            home_path=tmp_dir,
            verbose=self.verbose,
        )
        self._generate_superfastmode_config(home_path=tmp_dir)

        self.process = subprocess.Popen(
            [constants.JAVA_INSTALL, f"-Duser.home={tmp_dir}", "-jar", constants.MTS_JAR] + constants.EXTRA_ARGS,
            stdout=self.logfile,
            stderr=self.logfile,
            cwd=tmp_dir,
        )

    def _do_action(self, action: str) -> Observation:
        """
        Manually execute CommunicationMod commands.

        This method can be useful for debugging in development, but it should not be
        used by agents. Please use step() instead.
        """

        return self.communicator._manual_command(action)

    def _end_game(self) -> None:
        obs = self.observe()

        if not obs.in_game:
            return

        # If still alive
        obs = self.communicator.resign()
        assert obs.screen_type == "MAIN_MENU"

    def set_animate(self, animate: bool) -> None:
        self.animate = animate
        self.communicator.render(self.animate)

    def observe(self, add_to_cache: bool = False) -> Observation:
        """
        Fetches the latest game state and returns its observation.

        This method _always_ communicates with the game. It does not return a cached
        observation.

        Args:
            add_to_cache: By default, this method does not add the returned obervation
                to the env's internal cache, since it may be a duplicate. Set
                add_to_cache to True to override that behavior. Adding the result to the
                cache can be useful to fix the behavior of methods like valid_actions()
                in the event of desync.
        """

        stable = False

        for _ in range(100):
            obs = self.communicator.state()

            if obs.stable:
                stable = True
                break

            time.sleep(0.05)

        if not stable:
            raise RuntimeError("Unable to retrieve a stable observation")

        if add_to_cache:
            self.observation_cache.append(obs)

        return obs

    def _ready(self):
        logger.debug("Signalling READY")
        self.start_message = self.communicator.ready()

    def reboot(self) -> None:
        """
        Close and reopen the game process. Also works for the initial boot.
        """
        logger.debug("Rebooting")
        self.stop()
        self.start()

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ) -> Tuple[dict, dict]:
        """
        Args:
            seed: An int used to initialize the env's PRNG. The PRNG is used to
                generate new game seeds on subsequent resets, so you should only need
                to provide this kwarg once.
            options: A dict of additional optional parameters, listed below:
                sts_seed (str): A specific seed for the game to use, in the same format
                    as you'd provide in the game's menu. Useful for (re)playing known
                    scenarios. If this parameter is not provided, the env's PRNG will
                    generate a game seed instead.
                rng_state (object): An object representing the internal state of a PRNG.
                    If provided, this object will be used to set the env's PRNG. Useful
                    for (re)playing known scenarios. If provided, the seed argument must
                    be None.
                reboot (bool): Force a full reboot of the game.
        """

        options = options or {}
        params = ResetParams(seed=seed, **options)

        if params.reboot:
            self.reset_count = 0
        if self.reset_count == 0:
            self.reboot()
        else:
            self._end_game()

        run_type = "local"
        if self.container is not None:
            run_type = f"container {self.container.name}"

        logger.debug(f"Reset {run_type} reset_count={self.reset_count} {repr(params)}")

        self.reset_count += 1
        if self.reset_count == self.reboot_frequency:
            self.reset_count = 0

        if params.rng_state is not None:
            self.rng_state = params.rng_state
            self.seed = None
            self.prng = random.Random()
            self.prng.setstate(self.rng_state)
        elif params.seed is not None:
            self.seed = seed
            self.rng_state = None
            self.prng = random.Random(seed)
        elif self.prng is None:
            # If no seed is specified, set the prng on first run.
            # The same prng should be used across resets unless
            # the caller decides to change the seed.
            self.seed = random.getrandbits(64)
            self.prng = random.Random(self.seed)

        self.observation_cache.reset()

        if params.sts_seed is not None:
            sts_seed = SeedHelpers.validate_seed(params.sts_seed)
        else:
            sts_seed = SeedHelpers.make_seed(self.prng)
        self.sts_seed = sts_seed

        obs = self.communicator.start("DEFECT", self.ascension, self.sts_seed)

        # In my experience the game isn't actually stable here, and we have
        # to wait for a bit before the game actually starts.
        success = False
        for _ in range(10):
            if obs.screen_type == "MAIN_MENU":
                time.sleep(1)
                obs = self.observe()
            else:
                success = True
                break
        if not success:
            raise TimeoutError("Could not get out of MAIN_MENU after game start.")

        assert obs.event_state.event_id == "Neow Event"
        self.observation_cache.append(obs)

        # Send game's starting state to state logger
        if self.log_states:
            self.state_logger.log(None, obs)

        info = {
            "seed": self.seed,
            "sts_seed": self.sts_seed,
            "rng_state": self.prng.getstate(),
            "observation": obs,
        }
        return obs.serialize(), info

    def start(self) -> None:
        if self.headless:
            self._run_container()
        else:
            self._run_locally()

        logger.debug("Opening pipe files...")
        self.communicator = Communicator(self.input_path, self.output_path)
        logger.debug("Opened pipe files.")

        self._ready()
        self.communicator.render(self.animate)

    def step(self, action_id: int) -> Tuple[dict, float, bool, bool, dict]:
        prev_obs = self.observation_cache.get()
        assert prev_obs is not None  # should have been set by reset()

        action = ACTIONS[action_id]
        is_valid = validate(action, prev_obs)

        try:
            obs = self.communicator._manual_command(action.to_command())

            if obs.has_error == is_valid:
                # indicates a mismatch in our action validity checking
                logger.error(
                    "Action was %svalid, but obs %s an error.",
                    "" if is_valid else "in",
                    "had" if obs.has_error else "did not have",
                )
                logger.error(prev_obs.state)
                logger.error(action_id)

            had_error = obs.has_error
            if had_error:
                reward = -1.0
                # Maybe check that the new obs is the same as the old one, modulo
                # the error field?
                obs = prev_obs
            else:
                # Send observation to state logger
                if self.log_states:
                    self.state_logger.log(action, obs)

                success = False
                for _ in range(10):
                    if len(obs.valid_actions) == 0:
                        # this can indicate instability
                        time.sleep(1)
                        obs = self.observe()
                    else:
                        success = True
                        break
                if not success:
                    raise exceptions.StSError("No valid actions.")

                reward = self.value_fn(obs) - self.value_fn(prev_obs)
                self.observation_cache.append(obs)

            info = {
                "observation": obs,
                "had_error": had_error,
            }

            return obs.serialize(), reward, obs.game_over, False, info

        except Exception as e:
            logger.error(e)
            logger.debug(prev_obs.state)
            logger.debug(prev_obs.persistent_state.screen_type)
            from gym_sts.spaces.constants.base import ScreenType

            if prev_obs.persistent_state.screen_type == ScreenType.EVENT:
                logger.debug(f"Event {prev_obs.event_state.event_id}")
            logger.debug(f"Action {action_id} ({action})")

            if self.container is not None:
                logs = self.container.logs()
                self.logfile.write(logs)

            now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

            try:
                self.screenshot(f"error_{now}.png")
            except NotImplementedError:
                pass

            if not self.reboot_on_error:
                raise e

            # Reboot and return done=True to trigger a reset
            self.reboot()
            obs = prev_obs

            info = {
                "observation": obs,
                "had_error": obs.has_error,
                "reboot_error": e,
            }

            return obs.serialize(), 0.0, True, False, info

    def screenshot(self, filename: str) -> None:
        """
        Take a screenshot of the current game. Only works with headless=True.
        """
        if self.container is None:
            raise NotImplementedError("screenshot only works with headless=True")

        # Briefly enable animation ahead of screenshotting
        prev_setting = self.animate
        if not self.animate:
            self.set_animate(True)
        time.sleep(1)

        file_path = self.screenshots_dir / filename
        exit_code, output = self.container.exec_run(
            cmd=["scrot", str(file_path)],
            environment={"DISPLAY": ":99", "XAUTHORITY": "/tmp/sts.xauth"},
        )

        # Return animation state to whatever it was before
        self.set_animate(prev_setting)

        if exit_code != 0:
            raise RuntimeError(
                "Failed to take a screenshot. Output: " + output.decode("utf-8")
            )

    def stop(self) -> None:
        """
        Terminate the current game process.
        """

        if self.headless:
            if self.container is not None:
                logger.debug(f"Stopping container {self.container.name}")
                self.container.rename(f"{self.container.name}-stopping")
                self.container.stop()
                self.container.wait()
                self.container = None
            else:
                logger.debug("No container to stop")

        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None

    def valid_actions(self) -> list[Action]:
        latest_obs = self.observation_cache.get()
        if latest_obs is None:
            raise RuntimeError("Game not started?")
        return latest_obs.valid_actions

    def save_artifact(self, file_name):
        # TODO: Implement uploading to WandB
        raise NotImplementedError("Not implemented")

    def close(self) -> None:
        """
        Stops the env and cleans up temp files
        """

        self.stop()

        # if self._output_temp_dir is not None:
        #     self._output_temp_dir.cleanup()
        #     self._output_temp_dir = None
        #
        # if self._gamefile_temp_dir is not None:
        #     self._gamefile_temp_dir.cleanup()
        #     self._gamefile_temp_dir = None
