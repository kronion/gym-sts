from communication.sender import Sender
from communication.receiver import Receiver
from settings import *

import atexit
import subprocess

# Class is not quite gym-env compatible but should be good starting point
class GameState:
    def __init__(self):
        print("Starting STS")
        self.process = subprocess.Popen([JAVA_INSTALL, "-jar" , MTS_PATH] + EXTRA_ARGS, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        atexit.register(lambda: self.process.kill())

        print("Opening pipe files...")
        self.sender = Sender(INPUT_FILE)
        self.receiver = Receiver(OUTPUT_FILE)

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