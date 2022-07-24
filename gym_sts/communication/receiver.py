import json

class Receiver:
    def __init__(self, fn):
        self.fh = open(fn, "r")

    def receive_game_state(self):
        """
        Continues reading game state until the game is waiting for action from
        the agent
        """
        print("Waiting to receive game state...")
        for i in range(1000):
            state = json.loads(self.fh.readline())
            if state["ready_for_command"]:
                return state
        
        raise Exception("Waited 1000 messages for game state to be ready for command, but it didn't happen.")