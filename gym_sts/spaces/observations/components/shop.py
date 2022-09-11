from gym.spaces import Dict, Discrete, MultiBinary, Tuple
from pydantic import parse_obj_as

from gym_sts.spaces import constants
from gym_sts.spaces.observations import types, utils

from .base import ObsComponent


class ShopObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.cards = []
        self.relics = []
        self.potions = []
        self.purge_available = False
        self.purge_price = 0

        if "game_state" in state:
            game_state = state["game_state"]
            if (
                "screen_type" in game_state
                and game_state["screen_type"] == "SHOP_SCREEN"
            ):
                screen_state = game_state["screen_state"]
                self.cards = parse_obj_as(list[types.ShopCard], screen_state["cards"])
                self.relics = parse_obj_as(
                    list[types.ShopRelic], screen_state["relics"]
                )
                self.potions = parse_obj_as(
                    list[types.ShopPotion], screen_state["potions"]
                )
                self.purge_available = screen_state["purge_available"]
                self.purge_price = screen_state["purge_cost"]

    @staticmethod
    def space():
        return Dict(
            {
                "cards": Tuple(
                    [
                        Dict(
                            {
                                "card": MultiBinary(
                                    constants.LOG_NUM_CARDS_WITH_UPGRADES
                                ),
                                "price": MultiBinary(constants.SHOP_LOG_MAX_PRICE),
                            }
                        )
                    ]
                    * constants.SHOP_CARD_COUNT,
                ),
                "relics": Tuple(
                    [
                        Dict(
                            {
                                "relic": Discrete(constants.NUM_RELICS),
                                "price": MultiBinary(constants.SHOP_LOG_MAX_PRICE),
                            }
                        )
                    ]
                    * constants.SHOP_RELIC_COUNT
                ),
                "potions": Tuple(
                    [
                        Dict(
                            {
                                "potion": Discrete(constants.NUM_POTIONS),
                                "price": MultiBinary(constants.SHOP_LOG_MAX_PRICE),
                            }
                        )
                    ]
                    * constants.SHOP_POTION_COUNT
                ),
                "purge": Dict(
                    {
                        "available": Discrete(2),
                        "price": MultiBinary(constants.SHOP_LOG_MAX_PRICE),
                    }
                ),
            }
        )

    def serialize(self) -> dict:
        serialized_cards = [
            types.ShopCard.serialize_empty()
        ] * constants.SHOP_CARD_COUNT
        for i, card in enumerate(self.cards):
            serialized_cards[i] = card.serialize()

        serialized_relics = [
            {
                "relic": 0,
                "price": utils.to_binary_array(0, constants.SHOP_LOG_MAX_PRICE),
            }
        ] * constants.SHOP_RELIC_COUNT
        for i, relic in enumerate(self.relics):
            serialized = {
                "relic": constants.ALL_RELICS.index(relic.id),
                "price": utils.to_binary_array(
                    relic.price, constants.SHOP_LOG_MAX_PRICE
                ),
            }
            serialized_relics[i] = serialized

        serialized_potions = [
            {
                "potion": 0,
                "price": utils.to_binary_array(0, constants.SHOP_LOG_MAX_PRICE),
            }
        ] * constants.SHOP_POTION_COUNT
        for i, potion in enumerate(self.potions):
            serialized = {
                "potion": constants.ALL_POTIONS.index(potion.id),
                "price": utils.to_binary_array(
                    potion.price, constants.SHOP_LOG_MAX_PRICE
                ),
            }
            serialized_potions[i] = serialized

        serialized_purge = {
            "available": int(self.purge_available),
            "price": utils.to_binary_array(
                self.purge_price, constants.SHOP_LOG_MAX_PRICE
            ),
        }

        return {
            "cards": serialized_cards,
            "relics": serialized_relics,
            "potions": serialized_potions,
            "purge": serialized_purge,
        }
