from typing import Callable, List

from gym_sts.spaces.observations import Observation

from .base import SlayTheSpireGymEnv
from .utils import single_combat_value


class SingleCombatSTSEnv(SlayTheSpireGymEnv):
    def __init__(
        self,
        *args,
        value_fn: Callable[[Observation], float] = single_combat_value,
        enemies: List[str] = ["3_Sentries"],
        cards: List[str],
        add_relics: List[str],
        **kwargs,
    ):
        super().__init__(*args, value_fn=value_fn, **kwargs)  # type: ignore[misc]
        self.enemies = enemies
        self.cards = cards
        self.add_relics = add_relics

    def reset(self, *args, **kwargs):
        super().reset(*args, **kwargs)  # type: ignore[misc]

        # prng should have already been set in super().reset
        assert self.prng is not None

        self.communicator.basemod("deck remove all")

        for card in self.cards:
            self.communicator.basemod(f"deck add {card}")

        for relic in self.add_relics:
            self.communicator.basemod(f"relic add {relic}")

        enemy = self.prng.choice(self.enemies)
        obs = self.communicator.basemod(f"fight {enemy}")

        assert obs.in_combat
        self.observation_cache.append(obs)

        info = {
            "seed": self.seed,
            "sts_seed": self.sts_seed,
            "rng_state": self.prng.getstate(),
            "observation": obs,
        }
        return obs.serialize(), info

    def step(self, action_id: int):
        ser, reward, should_reset, truncated, info = super().step(action_id)

        # When you test out a new combat, make sure this condition works
        if not info["observation"].in_combat:
            should_reset = True

        return ser, reward, should_reset, truncated, info
