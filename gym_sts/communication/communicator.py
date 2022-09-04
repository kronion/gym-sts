import os
from pathlib import Path

from gym_sts.communication.receiver import Receiver
from gym_sts.communication.sender import Sender
from gym_sts.spaces.observations import Observation


def init_fifos(filenames):
    # Create fifos for communication
    for f in filenames:
        if os.path.exists(f):
            os.remove(f)
        os.mkfifo(f)


class Communicator:
    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        init_fifos([self.input_path, self.output_path])
        self.receiver = Receiver(self.output_path)
        self.sender = Sender(self.input_path)

    def _manual_command(self, action: str) -> Observation:
        self.receiver.empty_fifo()
        self.sender._send_message(action)
        state = self.receiver.receive_game_state()
        return Observation(state)

    def ready(self) -> None:
        self.sender.send_ready()

    def choose(self, choice) -> Observation:
        self.receiver.empty_fifo()
        self.sender.send_choose(choice)
        state = self.receiver.receive_game_state()
        return Observation(state)

    def click(self, x: int, y: int, left: bool = True) -> Observation:
        self.receiver.empty_fifo()
        self.sender.send_click(x, y, left=left)
        state = self.receiver.receive_game_state()
        return Observation(state)

    def end(self) -> Observation:
        self.receiver.empty_fifo()
        self.sender.send_end()
        state = self.receiver.receive_game_state()
        return Observation(state)

    def potion(self, action, slot, target) -> Observation:
        self.receiver.empty_fifo()
        self.sender.send_potion(action, slot, target)
        state = self.receiver.receive_game_state()
        return Observation(state)

    def proceed(self) -> Observation:
        self.receiver.empty_fifo()
        self.sender.send_proceed()
        state = self.receiver.receive_game_state()
        return Observation(state)

    def start(self, player_class: str, ascension: int, seed: str) -> Observation:
        self.receiver.empty_fifo()
        self.sender.send_start(player_class, ascension, seed)
        state = self.receiver.receive_game_state()
        return Observation(state)

    def state(self) -> Observation:
        """
        Get the JSON representation of the current game state, regardless of whether or
        not the game is "stable." This method is valid in all game states.
        """

        self.receiver.empty_fifo()
        self.sender.send_state()
        state = self.receiver.receive_game_state()
        return Observation(state)

    def wait(self, frames: int) -> Observation:
        self.receiver.empty_fifo()
        self.sender.send_wait(frames)
        state = self.receiver.receive_game_state()
        return Observation(state)
