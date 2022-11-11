from abc import ABC, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel, Field

from gym_sts.spaces import constants
from gym_sts.spaces.constants import ScreenType

from .utils import to_binary_array


class Card(BaseModel):
    exhausts: bool
    cost: int
    name: str
    id: str
    ethereal: bool
    upgrades: int
    has_target: bool

    @staticmethod
    def _serialize_binary(card_idx: int, upgrades: int) -> list[int]:
        array = to_binary_array(card_idx, constants.LOG_NUM_CARDS)

        upgrade_bit = [0]
        if upgrades > 0:
            upgrade_bit = [1]

        array = upgrade_bit + array

        return array

    @classmethod
    def serialize_empty_binary(cls) -> list[int]:
        return cls._serialize_binary(0, 0)

    def serialize_discrete(self) -> int:
        card_idx = constants.ALL_CARDS.index(self.id) * 2
        if self.upgrades > 0:
            card_idx += 1

        return card_idx

    def serialize_binary(self) -> list[int]:
        card_idx = constants.ALL_CARDS.index(self.id)
        return self._serialize_binary(card_idx, self.upgrades)


class HandCard(Card):
    is_playable: bool


class Potion(BaseModel):
    id: str
    requires_target: Optional[bool]
    can_use: Optional[bool]
    can_discard: Optional[bool]
    name: Optional[str]


class Relic(BaseModel):
    id: str
    name: Optional[str]
    counter: Optional[int]


class ShopMixin(BaseModel):
    price: int


class ShopCard(Card, ShopMixin):
    def serialize_discrete(self):
        raise NotImplementedError("Use serialize() instead")

    def serialize_binary(self):
        raise NotImplementedError("Use serialize() instead")

    @classmethod
    def serialize_empty(cls) -> dict[str, list[int]]:
        card_array = Card.serialize_empty_binary()
        price_array = to_binary_array(0, constants.SHOP_LOG_MAX_PRICE)

        return {
            "card": card_array,
            "price": price_array,
        }

    def serialize(self) -> dict[str, list[int]]:
        card_array = super().serialize_binary()
        price_array = to_binary_array(self.price, constants.SHOP_LOG_MAX_PRICE)

        return {
            "card": card_array,
            "price": price_array,
        }


class ShopPotion(Potion, ShopMixin):
    pass


class ShopRelic(Relic, ShopMixin):
    pass


class Reward(BaseModel, ABC):
    @abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError("Unimplemented")

    @staticmethod
    def serialize_empty():
        return {
            "type": constants.ALL_REWARD_TYPES.index("NONE"),
            "value": to_binary_array(0, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class GoldReward(Reward):
    value: int

    def serialize(self) -> dict:
        return {
            "type": constants.ALL_REWARD_TYPES.index("GOLD"),
            "value": to_binary_array(self.value, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class PotionReward(Reward):
    value: Potion

    def serialize(self) -> dict:
        potion_idx = constants.ALL_POTIONS.index(self.value.id)
        return {
            "type": constants.ALL_REWARD_TYPES.index("POTION"),
            "value": to_binary_array(potion_idx, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class RelicReward(Reward):
    value: Relic

    def serialize(self) -> dict:
        relic_idx = constants.ALL_RELICS.index(self.value.id)
        return {
            "type": constants.ALL_REWARD_TYPES.index("RELIC"),
            "value": to_binary_array(relic_idx, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class CardReward(Reward):
    def serialize(self) -> dict:
        return {
            "type": constants.ALL_REWARD_TYPES.index("CARD"),
            "value": to_binary_array(0, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class KeyReward(Reward):
    value: str

    def serialize(self) -> dict:
        key_idx = constants.ALL_KEYS.index(self.value)
        return {
            "type": constants.ALL_REWARD_TYPES.index("KEY"),
            "value": to_binary_array(key_idx, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class Keys(BaseModel):
    emerald: bool = False
    ruby: bool = False
    sapphire: bool = False


class MapCoordinates(BaseModel):
    x: int
    y: int


class StandardNode(MapCoordinates):
    symbol: str
    children: list[MapCoordinates]


class EliteNode(StandardNode):
    is_burning: bool


Node = Union[StandardNode, EliteNode]
