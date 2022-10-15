import atexit
import logging
import os
import pathlib
import random
import shutil
import subprocess
import tempfile
import time
from typing import Optional, Tuple, Union

import docker
import gym
from docker.models.containers import Container

from gym_sts import constants, exceptions
from gym_sts.communication import Communicator
from gym_sts.spaces.actions import ACTION_SPACE, ACTIONS, Action
from gym_sts.spaces.observations import OBSERVATION_SPACE, Observation

from .action_validation import validate
from .utils import Cache, SeedHelpers, obs_value

CONTAINER_OUTDIR = "/game/out"
CONTAINER_LIBDIR = "/game/lib"
CONTAINER_MODSDIR = "/game/mods"


class SlayTheSpireGymEnv(gym.Env):
    def __init__(
        self,
        lib_dir: str,
        mods_dir: str,
        output_dir: Optional[str] = None,
        headless: bool = False,
        animate: bool = True,
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
        """

        self.lib_dir = pathlib.Path(lib_dir).resolve()
        self.mods_dir = pathlib.Path(mods_dir).resolve()

        self._temp_dir = None
        if output_dir is None:
            self._temp_dir = tempfile.TemporaryDirectory(prefix="sts-")
            output_dir = self._temp_dir.name
        self.output_dir = pathlib.Path(output_dir).resolve()
        self.input_path = self.output_dir / "stsai_input"
        self.output_path = self.output_dir / "stsai_output"
        self.logfile_path = self.output_dir / "stderr.log"

        self.logfile = self.logfile_path.open("w")

        self.container: Optional[Container] = None
        self.process: Optional[subprocess.Popen] = None

        if headless:
            self._run_container()
        else:
            self._run_locally()

        print("Opening pipe files...")
        self.communicator = Communicator(self.input_path, self.output_path)
        print("Opened pipe files.")

        self._ready()

        # Animation can be toggled at any time using set_animate()
        self.animate = animate
        self.communicator.render(self.animate)

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

        atexit.register(self.close)

    @classmethod
    def build_image(cls) -> None:
        client = docker.from_env()
        client.images.build(
            path=str(constants.PROJECT_ROOT / "build"), tag=constants.DOCKER_IMAGE_TAG
        )

    def _generate_communication_mod_config(self) -> None:
        """
        Create the config file CommunicationMod uses to start a subprocess.

        WARNING: This function will silently overwrite any existing config file.
        """

        pipe_script = (constants.PROJECT_ROOT / "build" / "pipe_locally.sh").resolve()
        command = f"{pipe_script} {self.input_path} {self.output_path}"
        config_file = pathlib.Path(
            "~/.config/ModTheSpire/CommunicationMod/config.properties"
        ).expanduser()

        with config_file.open(mode="w") as f:
            f.write(f"command={command}\n")
            f.write("runAtGameStart=true\n")

    def _generate_superfastmode_config(self) -> None:
        """
        Create the config file for SuperFastMode.

        WARNING: This function will silently overwrite any existing config file.
        """

        config_file = pathlib.Path(
            "~/.config/ModTheSpire/SuperFastMode/SuperFastModeConfig.properties"
        ).expanduser()

        with config_file.open(mode="w") as f:
            f.write(
                "isDeltaMultiplied=true\ndeltaMultiplier=100.0\n"
                "EXISTS=YES INDEED I EXIST\nisInstantLerp=true\n"
            )

    def _run_container(self) -> None:
        print("Starting STS in Docker container")
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
            remove=True,
            devices=["/dev/snd"],
            init=True,
            detach=True,
            volumes={
                self.output_dir: dict(bind=CONTAINER_OUTDIR, mode="rw"),
                self.lib_dir: dict(bind=CONTAINER_LIBDIR, mode="ro"),
                self.mods_dir: dict(bind=CONTAINER_MODSDIR, mode="ro"),
            },
        )
        print(f"started docker container {self.container.name}")
        print(f"To view logs, run `docker logs {self.container.name}`.")

    def _run_locally(self) -> None:
        print("Starting STS on the host machine")

        # Create a sandbox directory where the subprocess will run
        try:
            shutil.copytree(str(self.lib_dir), "tmp")
        except FileExistsError:
            pass
        shutil.copytree(str(self.mods_dir), "tmp/mods", dirs_exist_ok=True)
        preferences = constants.PROJECT_ROOT / "build" / "preferences"
        shutil.copytree(str(preferences), "tmp/preferences", dirs_exist_ok=True)

        displayconfig_path = constants.PROJECT_ROOT / "build" / "info.displayconfig"
        shutil.copy(str(displayconfig_path), "tmp/info.displayconfig")

        self._generate_communication_mod_config()
        self._generate_superfastmode_config()

        os.chdir("tmp")

        self.process = subprocess.Popen(
            [constants.JAVA_INSTALL, "-jar", constants.MTS_JAR] + constants.EXTRA_ARGS,
            stdout=self.logfile,
            stderr=self.logfile,
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

        for i in range(100):
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
        print("Signalling READY")
        self.start_message = self.communicator.ready()

    def reset(
        self,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ) -> Union[dict, Tuple[dict, dict]]:
        """
        Args:
            seed: An int used to initialize the env's PRNG. The PRNG is used to
                generate new game seeds on subsequent resets, so you should only need
                to provide this kwarg once.
            return_info: Whether or not to return a dict of miscellaneous context, for
                parity with step()'s return signature.
            options: A dict of additional optional parameters, listed below:
                sts_seed (str): A specific seed for the game to use, in the same format
                    as you'd provide in the game's menu. Useful for (re)playing known
                    scenarios. If this parameter is not provided, the env's PRNG will
                    generate a game seed instead.
                rng_state (object): An object representing the internal state of a PRNG.
                    If provided, this object will be used to set the env's PRNG. Useful
                    for (re)playing known scenarios. If provided, the seed argument must
                    be None.
        """

        self._end_game()

        # TODO @kronion: validate options with pydantic

        if options is not None and "rng_state" in options:
            if seed is not None:
                raise ValueError("seed and rng_state cannot both be provided")
            self.rng_state = options["rng_state"]
            assert self.rng_state is not None
            self.seed = None
            self.prng = random.Random()
            self.prng.setstate(self.rng_state)
        elif seed is not None:
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

        if options is not None and "sts_seed" in options:
            sts_seed = SeedHelpers.validate_seed(options["sts_seed"])
        else:
            sts_seed = SeedHelpers.make_seed(self.prng)
        self.sts_seed = sts_seed

        obs = self.communicator.start("DEFECT", 0, sts_seed)

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

        if return_info:
            info = {
                "seed": self.seed,
                "sts_seed": self.sts_seed,
                "rng_state": self.prng.getstate(),
                "observation": obs,
            }
            return obs.serialize(), info
        else:
            return obs.serialize()

    def step(self, action_id: int) -> Tuple[dict, float, bool, dict]:
        prev_obs = self.observation_cache.get()
        assert prev_obs is not None  # should have been set by reset()

        action = ACTIONS[action_id]
        is_valid = validate(action, prev_obs)

        try:
            obs = self.communicator._manual_command(action.to_command())
        except exceptions.StSError as e:
            print(prev_obs)
            print(action_id)
            self.screenshot("error.png")
            raise e

        if obs.has_error == is_valid:
            # indicates a mismatch in our action validity checking
            logging.error(
                "Action was %svalid, but obs %s an error.",
                "" if is_valid else "not ",
                "had" if obs.has_error else "did not have",
            )

        had_error = obs.has_error
        if had_error:
            reward = -1.0
            # Maybe check that the new obs is the same as the old one, modulo
            # the error field?
            obs = prev_obs
        else:
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

            reward = obs_value(obs) - obs_value(prev_obs)
            self.observation_cache.append(obs)

        info = {
            "observation": obs,
            "had_error": had_error,
        }

        return obs.serialize(), reward, obs.game_over, info

    def screenshot(self, filename: str) -> None:
        """
        Take a screenshot of the current game. Only works with headless=True.
        """
        if self.container is None:
            raise NotImplementedError("screenshot only works with headless=True")

        # Briefly enable animation ahead of screenshotting
        if not self.animate:
            self.set_animate(True)

        file_path = pathlib.Path(CONTAINER_OUTDIR) / filename
        exit_code, output = self.container.exec_run(
            cmd=["scrot", str(file_path)],
            environment={"DISPLAY": ":99", "XAUTHORITY": "/tmp/sts.xauth"},
        )

        # Return animation state to whatever it was before
        self.set_animate(self.animate)

        if exit_code != 0:
            raise RuntimeError(
                "Failed to take a screenshot. Output: " + output.decode("utf-8")
            )

    def valid_actions(self) -> list[Action]:
        latest_obs = self.observation_cache.get()
        if latest_obs is None:
            raise RuntimeError("Game not started?")
        return latest_obs.valid_actions

    def close(self):
        if self._temp_dir is not None:
            self._temp_dir.cleanup()
            self._temp_dir = None

        if self.container is not None:
            self.container.stop()
            self.container = None

        if self.process is not None:
            self.process.terminate()
            self.process = None
