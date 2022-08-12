from communication import init_fifos
from communication.sender import Sender
from communication.receiver import Receiver
from settings import *

import atexit
import subprocess
import pathlib

# Class is not quite gym-env compatible but should be good starting point
class BaseGameState:
    def ready(self):
        print("Signalling READY")
        self.sender.send_ready()
        print("Waiting for game to be stable...")
        self.start_message = self.receiver.receive_game_state()

    def begin(self, seed):
        """
        Start a new game, from a reset state.
        """
        print("Starting a new game")
        self.sender.send_start("IRONCLAD", 0, seed)
        return self.receiver.receive_game_state()

    def do_action(self, action):
        self.sender.send_message(action)
        return self.receiver.receive_game_state()

    def reset(self):
        self.sender.send_click(1900, 10)
        self.receiver.receive_game_state()
        self.sender.send_click(1500, 240)
        self.sender.send_click(1500, 240)
        self.receiver.receive_game_state()
        self.sender.send_click(830, 700)
        self.sender.send_click(830, 700)
        self.receiver.receive_game_state()
        self.sender.send_click(950, 920)
        self.sender.send_click(950, 920)
        self.receiver.receive_game_state()
        self.sender.send_click(950, 950)
        self.sender.send_click(950, 950)
        while True:
            state = self.receiver.receive_game_state()
            if not state["in_game"]:
                self.sender.send_start("IRONCLAD", 0, 42)
                break

class LegacyGameState(BaseGameState):
    def __init__(self):
        super().__init__()
        init_fifos([INPUT_FILE, OUTPUT_FILE])
        print("Starting STS")
        self.logfile = open(LOG_FILE, "w")
        self.process = subprocess.Popen([JAVA_INSTALL, "-jar" , MTS_PATH] + EXTRA_ARGS, stdout=self.logfile, stderr=self.logfile)
        atexit.register(lambda: self.process.kill())

        print("Opening pipe files...")
        self.receiver = Receiver(OUTPUT_FILE)
        self.sender = Sender(INPUT_FILE)

        self.ready()


class DockerGameState(BaseGameState):
    def __init__(self, output_dir):
        super().__init__()
        print("Starting STS in Docker container")
        self.output_dir = pathlib.Path(output_dir)
        self.logfile_path = self.output_dir / "stderr.log"
        self.input_file_path = self.output_dir / "stsai_input"
        self.output_file_path = self.output_dir / "stsai_output"

        init_fifos([self.input_file_path, self.output_file_path])
        self.logfile = self.logfile_path.open("w")
 
        docker_args = ["docker", "run", "--rm", "-v", f"{self.output_dir}:/out", "--device", "/dev/snd", "--init", "sts"]
        mts_args = [JAVA_INSTALL, "-jar" , MTS_PATH] + EXTRA_ARGS
        self.process = subprocess.Popen(docker_args + mts_args,
            stdin=subprocess.DEVNULL,
            stdout=self.logfile,
            stderr=self.logfile)
        atexit.register(lambda: self.process.kill())

        print("Opening pipe files...")
        self.sender = Sender(self.input_file_path)
        self.receiver = Receiver(self.output_file_path)

        self.ready()
