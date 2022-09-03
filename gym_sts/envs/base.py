import atexit
import os
import pathlib
import random
import shutil
import subprocess
import time
from typing import Optional, Tuple, Union

import docker
from docker.models.containers import Container

import gym
from gym_sts import constants
from gym_sts.communication import Communicator
from gym_sts.spaces.actions import ACTION_SPACE, ACTIONS, Action
from gym_sts.spaces.observations import OBSERVATION_SPACE, Observation, ObservationCache

from .utils import ActionValidators

CONTAINER_OUTDIR = "/game/out"
CONTAINER_LIBDIR = "/game/lib"
CONTAINER_MODSDIR = "/game/mods"


class SlayTheSpireGymEnv(gym.Env):
    def __init__(
        self, lib_dir: str, mods_dir: str, output_dir: str, headless: bool = False
    ):
        """
        Gym env to interact with the Slay the Spire video game.

        Args:
            lib_dir: The directory containing desktop-1.0.jar and ModTheSpire.jar.
            mods_dir: The directory containing BaseMod.jar and CommunicationMod.jar.
            output_dir: Directory used for communication between env and containers.
            headless: If True, run the game in a headless Docker container. Otherwise,
                run the game directly on the host (presumably with a visible interface).
        """

        self.lib_dir = pathlib.Path(lib_dir).resolve()
        self.mods_dir = pathlib.Path(mods_dir).resolve()

        self.output_dir = pathlib.Path(output_dir).resolve()
        self.input_path = self.output_dir / "stsai_input"
        self.output_path = self.output_dir / "stsai_output"
        self.logfile_path = self.output_dir / "stderr.log"

        self.logfile = self.logfile_path.open("w")

        if headless:
            self._run_container()
        else:
            self._run_locally()

        print("Opening pipe files...")
        self.communicator = Communicator(self.input_path, self.output_path)
        print("Opened pipe files.")

        self.ready()

        # Set on first reset
        self.seed: Optional[int] = None
        self.prng: Optional[random.Random] = None

        self.action_space = ACTION_SPACE
        self.observation_space = OBSERVATION_SPACE

        self.observation_cache = ObservationCache()

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

        self.container: Container = self.client.containers.run(
            image=constants.DOCKER_IMAGE_TAG,
            remove=True,
            devices=["/dev/snd"],
            init=True,
            detach=True,
            volumes={
                self.output_dir.resolve(): dict(bind=CONTAINER_OUTDIR, mode="rw"),
                self.lib_dir: dict(bind=CONTAINER_LIBDIR, mode="ro"),
                self.mods_dir: dict(bind=CONTAINER_MODSDIR, mode="ro"),
            },
        )
        print(f"started docker container {self.container.name}")
        print(f"To view logs, run `docker logs {self.container.name}`.")
        atexit.register(self.container.stop)

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

        self._generate_communication_mod_config()

        os.chdir("tmp")

        self.process = subprocess.Popen(
            [constants.JAVA_INSTALL, "-jar", constants.MTS_JAR] + constants.EXTRA_ARGS,
            stdout=self.logfile,
            stderr=self.logfile,
        )
        atexit.register(lambda: self.process.kill())

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
        # TODO(collin): document/clean this up
        if not obs.game_over:
            # Open the menu in the upper right of the screen
            self.communicator.click(1900, 10)

            # Click "abandon run"
            self.communicator.click(1500, 240)
            self.communicator.click(1500, 240)

            # Confirm
            self.communicator.click(830, 700)
            self.communicator.click(830, 700)

            # Acknowledge death
            self.communicator.click(950, 920)
            self.communicator.click(950, 920)

            # Return to main menu
            self.communicator.click(950, 950)
            self.communicator.click(950, 950)
        else:
            # Acknowledge death
            self.communicator.click(950, 920)
            self.communicator.click(950, 920)

            # Return to main menu
            self.communicator.click(950, 950)
            self.communicator.click(950, 950)

        # TODO have a loop limit to prevent infinite loop
        while True:
            obs = self.observe()
            if not obs.in_game:
                break

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

    def ready(self):
        print("Signalling READY")
        self.start_message = self.communicator.ready()
        # print("Waiting for game to be stable...")
        # self.start_message = self.receiver.receive_game_state()

    def reset(
        self,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ) -> Union[Observation, Tuple[Observation, dict]]:
        self._end_game()

        if seed is not None:
            self.seed = seed
            self.prng = random.Random(seed)
        elif self.prng is None:
            # If no seed is specified, set the prng on first run.
            # The same prng should be used across resets unless
            # the caller decides to change the seed.
            self.seed = random.getrandbits(64)
            self.prng = random.Random(self.seed)

        self.observation_cache.reset()

        # TODO use prng to generate seed
        obs = self.communicator.start("DEFECT", 0, 42)
        self.observation_cache.append(obs)

        if return_info:
            return obs, {}
        else:
            return obs

    def step(self, action_id: int) -> Tuple[Observation, float, bool, dict]:
        action = ACTIONS[action_id]
        obs = self.communicator._manual_command(action.to_command())
        self.observation_cache.append(obs)

        reward = 1

        return obs, reward, obs.game_over, {"observation": obs}

    def screenshot(self, filename: str) -> None:
        """
        Take a screenshot of the current game. Only works with headless=True.
        """
        file_path = pathlib.Path(CONTAINER_OUTDIR) / filename
        exit_code, output = self.container.exec_run(
            cmd=["scrot", str(file_path)],
            environment={"DISPLAY": ":99", "XAUTHORITY": "/tmp/sts.xauth"},
        )
        if exit_code != 0:
            raise RuntimeError(
                "Failed to take a screenshot. Output: " + output.decode("utf-8")
            )

    def valid_actions(self) -> list[Action]:
        latest_obs = self.observation_cache.get()
        if latest_obs is None:
            raise RuntimeError("Game not started?")

        valid_actions = []
        for action in ACTIONS:
            if ActionValidators.validate(action, latest_obs):
                valid_actions.append(action)

        return valid_actions
