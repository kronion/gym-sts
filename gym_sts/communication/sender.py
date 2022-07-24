class Sender:
    def __init__(self, fn):
        self.fh = open(fn, "w")

    def send_message(self, msg):
        self.fh.write(f"{msg}\n")
        self.fh.flush()

    def send_ready(self):
        self.send_message("READY")

    def send_start(self, player_class, ascension, seed):
        self.send_message(f"START {player_class} {ascension} {seed}")

    def send_proceed(self):
        self.send_message("PROCEED")

    def send_choose(self, choice):
        self.send_message(f"CHOOSE {choice}")

    def send_play(self, index, target):
        # NOTE: Card index argument is indexed from 1, with 0 representing position 10.
        # Indices can change in the middle of a game.
        # Target argument is indexed from 0.
        self.send_message(f"PLAY {index} {target}")

    def send_end(self):
        self.send_meesage("END")

    def send_potion(self, action, slot, target):
        self.send_message(f"POTION {action} {slot} {target}")