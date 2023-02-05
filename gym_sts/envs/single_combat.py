from typing import Callable

from gym_sts.spaces.observations import Observation

from .base import SlayTheSpireGymEnv
from .utils import single_combat_value


class SingleCombatSTSEnv(SlayTheSpireGymEnv):
    def __init__(
        self,
        *args,
        value_fn: Callable[[Observation], float] = single_combat_value,
        enemy: str = "3_Sentries",
        **kwargs,
    ):
        super().__init__(*args, value_fn=value_fn, **kwargs)  # type: ignore[misc]
        self.enemy = enemy

    def reset(self, *args, return_info: bool = False, **kwargs):
        super().reset(*args, return_info=return_info, **kwargs)  # type: ignore[misc]

        obs = self.communicator.basemod(f"fight {self.enemy}")
        assert obs.in_combat
        self.observation_cache.append(obs)

        if return_info:
            # prng should have already been set in super().reset
            assert self.prng is not None
            info = {
                "seed": self.seed,
                "sts_seed": self.sts_seed,
                "rng_state": self.prng.getstate(),
                "observation": obs,
            }
            return obs.serialize(), info
        else:
            return obs.serialize()

    def step(self, action_id: int):
        ser, reward, should_reset, info = super().step(action_id)

        # When you test out a new combat, make sure this condition works
        if not info["observation"].in_combat:
            should_reset = True

        return ser, reward, should_reset, info
