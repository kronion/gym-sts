import atexit
import pathlib
import random
import subprocess
from typing import Optional

import gym

from gym_sts.communication import Communicator
from gym_sts.envs.observations import Observation
from gym_sts.settings import *


class SlayTheSpireGymEnv(gym.Env):
    def __init__(self, output_dir: str):
        print("Starting STS in Docker container")
        self.output_dir = pathlib.Path(output_dir)
        self.logfile_path = self.output_dir / "stderr.log"
        self.input_path = self.output_dir / "stsai_input"
        self.output_path = self.output_dir / "stsai_output"

        self.logfile = self.logfile_path.open("w")

        # docker_args = ["docker", "run", "--rm", "-v", f"{self.output_dir}:/out", "--device", "/dev/snd", "--init", "sts"]
        # mts_args = [JAVA_INSTALL, "-jar" , MTS_PATH] + EXTRA_ARGS
        # self.process = subprocess.Popen(docker_args + mts_args,
        #     stdin=subprocess.DEVNULL,
        #     stdout=self.logfile,
        #     stderr=self.logfile)
        self.process = subprocess.Popen([JAVA_INSTALL, "-jar" , MTS_PATH] + EXTRA_ARGS, stdout=self.logfile, stderr=self.logfile)
        atexit.register(lambda: self.process.kill())

        print("Opening pipe files...")
        self.communicator = Communicator(self.input_path, self.output_path)

        self.ready()

        # Set on first reset
        self.seed = None
        self.prng = None

    def _end_game(self) -> None:
        obs = self.observe()

        if not obs.in_game:
            return

        # If still alive
        if not obs.game_over:
            self.communicator.click(1900, 10)
            self.communicator.click(1500, 240)
            self.communicator.click(1500, 240)
            self.communicator.click(830, 700)
            self.communicator.click(830, 700)
            self.communicator.click(950, 920)
            self.communicator.click(950, 920)
            self.communicator.click(950, 950)
            self.communicator.click(950, 950)
        else:
            self.communicator.click(950, 920)
            self.communicator.click(950, 920)
            self.communicator.click(950, 950)
            self.communicator.click(950, 950)

        # TODO have a loop limit to prevent infinite loop
        while True:
            obs = self.observe()
            if not obs.in_game:
                break

    def observe(self) -> Observation:
        # TODO need to return from a cached value, calling
        # receive_game_state() gets the next message from the fifo
        obs = self.communicator.state()

        # TODO if this assertion ever fails, we should take it as an indication that
        # the send_state() call needs to be retried.
        assert obs.stable

        return obs

    def ready(self):
        print("Signalling READY")
        self.start_message = self.communicator.ready()
        # print("Waiting for game to be stable...")
        # self.start_message = self.receiver.receive_game_state()

    def reset(self, seed: Optional[int] = None, return_info: bool = False):
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

        # TODO use prng to generate seed
        obs = self.communicator.start("IRONCLAD", 0, 42)

        if return_info:
            return obs, {}
        else:
            return obs

    def step(self, action):
        obs = self.communicator.end()

        return obs
