from abc import ABC, abstractmethod

from pydantic import BaseModel

from gym_sts.spaces import constants

from .utils import to_binary_array


class Card(BaseModel):
    exhausts: bool
    cost: int
    name: str
    id: str
    ethereal: bool
    upgrades: int
    has_target: bool


class HandCard(Card):
    is_playable: bool


class Potion(BaseModel):
    requires_target: bool
    can_use: bool
    can_discard: bool
    name: str
    id: str


class Relic(BaseModel):
    name: str
    id: str
    counter: int


class ShopMixin(BaseModel):
    price: int


class ShopCard(Card, ShopMixin):
    pass


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
