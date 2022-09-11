from gym.spaces import Dict, Discrete

from .base import ObsComponent


class CampfireObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.rest = False
        self.smith = False
        self.lift = False
        self.toke = False
        self.dig = False
        self.recall = False
        self.num_options = 0

        if "game_state" in state:
            game_state = state["game_state"]
            if "screen_type" in game_state and game_state["screen_type"] == "REST":
                screen_state = game_state["screen_state"]
                if screen_state["has_rested"]:
                    return

                rest_options = screen_state["rest_options"]
                possible_options = ["rest", "smith", "lift", "toke", "dig", "recall"]

                for option in possible_options:
                    if option in rest_options:
                        setattr(self, option, True)
                        self.num_options += 1

    @staticmethod
    def space():
        return Dict(
            {
                "rest": Discrete(2),
                "smith": Discrete(2),
                "lift": Discrete(2),
                "toke": Discrete(2),
                "dig": Discrete(2),
                "recall": Discrete(2),
            }
        )

    def serialize(self) -> dict:
        return {
            "rest": int(self.rest),
            "smith": int(self.smith),
            "lift": int(self.lift),
            "toke": int(self.toke),
            "dig": int(self.dig),
            "recall": int(self.recall),
        }
