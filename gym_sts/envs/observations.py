class Observation:
    def __init__(self, state: dict):
        self.in_game = state["in_game"]
        self.stable = state["ready_for_command"]

        if "game_state" in state:
            game_state = state["game_state"]
            self.screen_type = game_state["screen_type"]
        else:
            # CommunicationMod doesn't specify a screen type in the main menu
            self.screen_type = "MAIN_MENU"
        self.game_over = self.screen_type == "GAME_OVER"

        # Keep a reference to the raw CommunicationMod response
        self._state = state
