from gym.spaces import Dict, Discrete, MultiBinary, Tuple
from pydantic import parse_obj_as

import gym_sts.spaces.constants.cards as card_consts
from gym_sts.spaces import old_constants as constants
from gym_sts.spaces.observations import types

from .base import ObsComponent


class CardRewardObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.cards = []
        self.singing_bowl = False
        self.skippable = False

        if "game_state" in state:
            game_state = state["game_state"]
            if (
                "screen_type" in game_state
                and game_state["screen_type"] == "CARD_REWARD"
            ):

                screen_state = game_state["screen_state"]
                self.cards = parse_obj_as(list[types.Card], screen_state["cards"])
                self.singing_bowl = screen_state["bowl_available"]
                self.skippable = screen_state["skip_available"]

    @staticmethod
    def space():
        return Dict(
            {
                # At most 4 cards may be offered (due to Question Card relic).
                "cards": Tuple(
                    (
                        MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                        MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                        MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                        MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                    )
                ),
                "singing_bowl": Discrete(2),
                "skippable": Discrete(2),
            }
        )

    def serialize(self) -> dict:
        serialized_cards = [
            types.Card.serialize_empty_binary()
        ] * constants.REWARD_CARD_COUNT
        for i, card in enumerate(self.cards):
            serialized_cards[i] = card.serialize_binary()

        return {
            "cards": serialized_cards,
            "singing_bowl": int(self.singing_bowl),
            "skippable": int(self.skippable),
        }
