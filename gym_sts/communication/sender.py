class Sender:
    def __init__(self, fn):
        self.fh = open(fn, "w")

    def _send_message(self, msg: str) -> None:
        self.fh.write(f"{msg}\n")
        self.fh.flush()

    def send_ready(self) -> None:
        self._send_message("READY")

    def send_start(self, player_class: str, ascension: int, seed: str) -> None:
        self._send_message(f"START {player_class} {ascension} {seed}")

    def send_proceed(self) -> None:
        self._send_message("PROCEED")

    def send_choose(self, choice) -> None:
        self._send_message(f"CHOOSE {choice}")

    def send_click(self, x: int, y: int, left: bool = True) -> None:
        side = "left" if left else "right"
        self._send_message(f"CLICK {side} {x} {y}")

    def send_play(self, index, target) -> None:
        # NOTE: Card index argument is indexed from 1, with 0 representing position 10.
        # Indices can change in the middle of a game.
        # Target argument is indexed from 0.
        self._send_message(f"PLAY {index} {target}")

    def send_end(self) -> None:
        self._send_message("END")

    def send_potion(self, action, slot, target) -> None:
        self._send_message(f"POTION {action} {slot} {target}")

    def send_resign(self) -> None:
        self._send_message("RESIGN")

    def send_wait(self, frames: int) -> None:
        self._send_message(f"WAIT {frames}")

    def send_state(self) -> None:
        """
        Get the JSON representation of the current game state, regardless of whether or
        not the game is "stable." This method is valid in all game states.
        """

        self._send_message("STATE")

    def send_basemod(self, command: str) -> None:
        self._send_message(f"BASEMOD {command}")
