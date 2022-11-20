import numpy as np
from gym.spaces import Dict, Discrete, MultiBinary

from gym_sts.spaces import constants
from gym_sts.spaces.data import EVENT_DATA

from .base import ObsComponent

# Processing text is annoying, especially when text is the only real indicator for event
# state and the numbers can sometimes change.
# So, each text fragment (extracted from game files) has an individual bit flag that
# indicates whether the given text is present in the current event.


class EventStateObs(ObsComponent):
    def __init__(self, state: dict):
        self.event_id = "NONE"
        self.raw_text = ""
        self.text_matches = []

        if "game_state" in state:
            game_state = state["game_state"]
            if "screen_type" in game_state and game_state["screen_type"] == "EVENT":
                screen_state = game_state["screen_state"]
                self.event_id = screen_state["event_id"]
                self.find_raw_text(screen_state)

                self.text_matches = EVENT_DATA.find_matches(
                    self.event_id, self.raw_text
                )

    def find_raw_text(self, screen_state):
        texts = [screen_state["body_text"]]

        for opt in screen_state["options"]:
            texts.append(opt["text"])

        self.raw_text = "".join(texts)

    @staticmethod
    def space():
        return Dict(
            {
                "event_id": Discrete(constants.NUM_EVENTS),
                "text": MultiBinary(constants.MAX_NUM_TEXTS),
            }
        )

    def serialize(self) -> dict:
        text = [flag for _, flag in self.text_matches]
        text.extend([False] * (constants.MAX_NUM_TEXTS - len(text)))
        return {
            "event_id": constants.ALL_EVENTS.index(self.event_id),
            "text": np.array(text),
        }
