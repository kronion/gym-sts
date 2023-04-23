from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from gym.spaces import Dict, Discrete, MultiBinary
from pydantic import BaseModel, Field

import gym_sts.spaces.constants.base as base_consts
import gym_sts.spaces.constants.rewards as reward_consts
from gym_sts.spaces.constants.relics import RelicCatalog
from gym_sts.spaces.observations import utils

from .base import BinaryArray
from .potions import PotionBase
from .relics import RelicBase


class Reward(BaseModel, ABC):
    @staticmethod
    def space():
        return Dict(
            {
                "type": Discrete(reward_consts.NUM_REWARD_TYPES),
                # Could be a gold value, a relic ID, the color of a key, or a potion ID
                "value": MultiBinary(reward_consts.COMBAT_REWARD_LOG_MAX_ID),
            }
        )

    @abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError("Unimplemented")

    @staticmethod
    def serialize_empty():
        return {
            "type": reward_consts.RewardType.NONE,
            "value": utils.to_binary_array(0, reward_consts.COMBAT_REWARD_LOG_MAX_ID),
        }

    class SerializedState(BaseModel):
        type: int
        value: BinaryArray

        class Config:
            arbitrary_types_allowed = True

    class NotDeserializable(Exception):
        pass

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> Reward:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        reward_type = reward_consts.RewardType(data.type)

        if reward_type == reward_consts.RewardType.GOLD:
            return GoldReward.deserialize(data)
        elif reward_type == reward_consts.RewardType.POTION:
            return PotionReward.deserialize(data)
        elif reward_type == reward_consts.RewardType.RELIC:
            return RelicReward.deserialize(data)
        elif reward_type == reward_consts.RewardType.CARD:
            return CardReward.deserialize(data)
        elif reward_type == reward_consts.RewardType.KEY:
            return KeyReward.deserialize(data)
        elif reward_type == reward_consts.RewardType.NONE:
            raise cls.NotDeserializable()
        else:
            raise ValueError(f"Unrecognized reward type {reward_type}")


class GoldReward(Reward):
    value: int = Field(..., ge=0, lt=2**reward_consts.COMBAT_REWARD_LOG_MAX_ID)

    def serialize(self) -> dict:
        return {
            "type": reward_consts.RewardType.GOLD,
            "value": utils.to_binary_array(
                self.value, reward_consts.COMBAT_REWARD_LOG_MAX_ID
            ),
        }

    @classmethod
    def deserialize(cls, data: Union[dict, Reward.SerializedState]) -> GoldReward:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        value = utils.from_binary_array(data.value)

        return cls(value=value)


class PotionReward(Reward):
    value: PotionBase

    def serialize(self) -> dict:
        potion_idx = self.value.serialize(discrete=True)
        assert isinstance(potion_idx, int)

        return {
            "type": reward_consts.RewardType.POTION,
            "value": utils.to_binary_array(
                potion_idx, reward_consts.COMBAT_REWARD_LOG_MAX_ID
            ),
        }

    @classmethod
    def deserialize(cls, data: Union[dict, Reward.SerializedState]) -> PotionReward:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        potion_idx = utils.from_binary_array(data.value)
        potion = PotionBase.deserialize(potion_idx)

        return cls(value=potion)


class RelicReward(Reward):
    value: RelicBase

    def serialize(self) -> dict:
        relic_idx = RelicCatalog.ids.index(self.value.id)
        return {
            "type": reward_consts.RewardType.RELIC,
            "value": utils.to_binary_array(
                relic_idx, reward_consts.COMBAT_REWARD_LOG_MAX_ID
            ),
        }

    @classmethod
    def deserialize(cls, data: Union[dict, Reward.SerializedState]) -> RelicReward:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        relic_idx = utils.from_binary_array(data.value)
        relic = RelicBase.deserialize(relic_idx)

        return cls(value=relic)


class CardReward(Reward):
    def serialize(self) -> dict:
        return {
            "type": reward_consts.RewardType.CARD,
            "value": utils.to_binary_array(0, reward_consts.COMBAT_REWARD_LOG_MAX_ID),
        }

    @classmethod
    def deserialize(cls, data: Union[dict, Reward.SerializedState]) -> CardReward:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        return cls()


class KeyReward(Reward):
    value: str

    def serialize(self) -> dict:
        key_idx = base_consts.ALL_KEYS.index(self.value)
        return {
            "type": reward_consts.RewardType.KEY,
            "value": utils.to_binary_array(
                key_idx, reward_consts.COMBAT_REWARD_LOG_MAX_ID
            ),
        }

    @classmethod
    def deserialize(cls, data: Union[dict, Reward.SerializedState]) -> KeyReward:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        key_idx = utils.from_binary_array(data.value)
        key = base_consts.ALL_KEYS[key_idx]

        return cls(value=key)
