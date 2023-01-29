from __future__ import annotations

from typing import Union

from gym.spaces import Tuple

import gym_sts.spaces.constants.rewards as reward_consts
from gym_sts.spaces.observations import types

from .base import ObsComponent


class CombatRewardObs(ObsComponent):
    def __init__(self, game_state: dict):
        # Sane defaults
        self.rewards: list[types.Reward] = []

        screen_type = game_state.get("screen_type")
        if screen_type is None:
            return

        screen_state = game_state["screen_state"]
        if screen_type == "COMBAT_REWARD":
            self.rewards = [
                self._parse_reward(reward) for reward in screen_state["rewards"]
            ]
        elif screen_type == "BOSS_REWARD":
            self.rewards = [
                types.RelicReward(value=types.RelicBase(**relic))
                for relic in screen_state["relics"]
            ]

    @staticmethod
    def space():
        return Tuple([types.Reward.space()] * reward_consts.MAX_NUM_REWARDS)

    @staticmethod
    def _parse_reward(reward: dict):
        reward_type = reward["reward_type"]

        if reward_type in ["GOLD", "STOLEN_GOLD"]:
            return types.GoldReward(value=reward["gold"])
        elif reward_type == "POTION":
            potion = types.PotionBase(**reward["potion"])
            return types.PotionReward(value=potion)
        elif reward_type == "RELIC":
            relic = types.RelicBase(**reward["relic"])
            return types.RelicReward(value=relic)
        elif reward_type == "CARD":
            return types.CardReward()
        elif reward_type in ["EMERALD_KEY", "SAPPHIRE_KEY"]:
            # TODO is it important to encode the "link" info for the sapphire key?
            key_type = reward_type.split("_")[0]
            return types.KeyReward(value=key_type)
        else:
            raise ValueError(f"Unrecognized reward type {reward_type}")

    def serialize(self) -> list[dict]:
        serialized = [types.Reward.serialize_empty()] * reward_consts.MAX_NUM_REWARDS
        for i, reward in enumerate(self.rewards):
            serialized[i] = reward.serialize()
        return serialized

    SerializedState = list[types.Reward.SerializedState]

    @classmethod
    def deserialize(cls, data: Union[list[dict], SerializedState]) -> CombatRewardObs:
        rewards = []
        for r in data:
            try:
                reward = types.Reward.deserialize(r)
            except types.Reward.NotDeserializable:
                continue
            rewards.append(reward)

        instance = cls({})
        instance.rewards = rewards

        return instance

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CombatRewardObs):
            return False

        attrs = ["rewards"]

        for attr in attrs:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True
