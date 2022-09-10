from gym_sts.spaces import constants
from gym_sts.spaces.observations import types

from .base import ObsComponent


class CombatRewardState(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.rewards: list[types.Reward] = []

        game_state = state.get("game_state")
        if game_state is None:
            return

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
                types.RelicReward(value=types.Relic(**relic))
                for relic in screen_state["relics"]
            ]

    @staticmethod
    def _parse_reward(reward: dict):
        reward_type = reward["reward_type"]

        if reward_type == "GOLD":
            return types.GoldReward(value=reward["gold"])
        elif reward_type == "POTION":
            potion = types.Potion(**reward["potion"])
            return types.PotionReward(value=potion)
        elif reward_type == "RELIC":
            relic = types.Relic(**reward["relic"])
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
        serialized = [types.Reward.serialize_empty()] * constants.MAX_NUM_REWARDS
        for i, reward in enumerate(self.rewards):
            serialized[i] = reward.serialize()
        return serialized
