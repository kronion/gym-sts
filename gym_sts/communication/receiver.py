import fcntl
import json
import os
import time


class Receiver:
    def __init__(self, fn, timeout: float = 50):
        self.fh = open(fn, "r")

        # Reading the pipe does not block if there are no contents
        flag = fcntl.fcntl(self.fh, fcntl.F_GETFD)
        fcntl.fcntl(self.fh, fcntl.F_SETFL, flag | os.O_NONBLOCK)

        self.timeout = timeout
        self.sleep_time = 0.05
        self.num_steps = int(timeout / self.sleep_time)

    def empty_fifo(self) -> None:
        """
        Read and discard all pipe content.

        Typically the caller would do this to ensure that the next message on the fifo
        corresponds to the result of the next action sent to the game.
        """

        self.fh.readlines()

    def receive_game_state(self) -> dict:
        """
        Continues reading game state until the game is waiting for action from
        the agent
        """
        print("Waiting to receive game state...")

        for _ in range(self.num_steps):
            message = self.fh.readline()
            if len(message) > 0:
                state = json.loads(message)
                if state["ready_for_command"]:
                    return state

            time.sleep(self.sleep_time)

        raise TimeoutError(
            f"Waited {self.timeout} seconds for game state to be ready "
            "for command, but it didn't happen."
        )
