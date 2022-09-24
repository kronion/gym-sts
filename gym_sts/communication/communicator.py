import os
import time
import typing as tp
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


ObsType = tp.TypeVar("ObsType")


class GenericCommunicator(tp.Generic[ObsType]):
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        state_wrapper: tp.Callable[[dict], ObsType],
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.wrapper = state_wrapper
        init_fifos([self.input_path, self.output_path])
        self.receiver = Receiver(self.output_path)
        self.sender = Sender(self.input_path)

    def _manual_command(self, action: str) -> ObsType:
        self.receiver.empty_fifo()
        self.sender._send_message(action)
        state = self.receiver.receive_game_state()
        return self.wrapper(state)

    def ready(self) -> None:
        self.sender.send_ready()

    def choose(self, choice) -> ObsType:
        self.receiver.empty_fifo()
        self.sender.send_choose(choice)
        state = self.receiver.receive_game_state()
        return self.wrapper(state)

    def click(self, x: int, y: int, left: bool = True) -> ObsType:
        self.receiver.empty_fifo()
        self.sender.send_click(x, y, left=left)
        state = self.receiver.receive_game_state()
        return self.wrapper(state)

    def end(self) -> ObsType:
        self.receiver.empty_fifo()
        self.sender.send_end()
        state = self.receiver.receive_game_state()
        return self.wrapper(state)

    def potion(self, action, slot, target) -> ObsType:
        self.receiver.empty_fifo()
        self.sender.send_potion(action, slot, target)
        state = self.receiver.receive_game_state()
        return self.wrapper(state)

    def proceed(self) -> ObsType:
        self.receiver.empty_fifo()
        self.sender.send_proceed()
        state = self.receiver.receive_game_state()
        return self.wrapper(state)

    def resign(self) -> Observation:
        self.receiver.empty_fifo()
        self.sender.send_resign()
        state = self.receiver.receive_game_state()
        return Observation(state)

    def start(self, player_class: str, ascension: int, seed: str) -> ObsType:
        self.receiver.empty_fifo()
        self.sender.send_start(player_class, ascension, seed)

        tries = 3
        for _ in range(tries):
            state = self.receiver.receive_game_state()
            if state["in_game"]:
                return self.wrapper(state)

            time.sleep(0.05)

        raise TimeoutError("Waited for game to start, but it didn't happen.")

    def state(self) -> ObsType:
        """
        Get the JSON representation of the current game state, regardless of whether or
        not the game is "stable." This method is valid in all game states.
        """

        self.receiver.empty_fifo()
        self.sender.send_state()
        state = self.receiver.receive_game_state()
        return self.wrapper(state)

    def wait(self, frames: int) -> ObsType:
        self.receiver.empty_fifo()
        self.sender.send_wait(frames)
        state = self.receiver.receive_game_state()
        return self.wrapper(state)


class Communicator(GenericCommunicator[Observation]):
    def __init__(self, input_path: Path, output_path: Path):
        super().__init__(input_path, output_path, state_wrapper=Observation)
