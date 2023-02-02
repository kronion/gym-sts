from gym_sts.spaces.observations import Observation

from .base import SlayTheSpireGymEnv


class SingleCombatSTSEnv(SlayTheSpireGymEnv):
    def __init__(self, *args, enemy: str = "3_Sentries", **kwargs):
        if "value_fn" not in kwargs:
            kwargs["value_fn"] = single_combat_value
        super().__init__(*args, **kwargs)
        self.enemy = enemy

    def reset(self, *args, **kwargs):
        res = super().reset(*args, **kwargs)

        obs = self.communicator.basemod(f"fight {self.enemy}")
        assert obs.in_combat
        self.observation_cache.append(obs)

        if type(res) == tuple and len(res) == 2:
            # params.return_info is set to true
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

        if (
            not info["observation"].in_combat
            or info["observation"].screen_type != "NONE"
        ):
            should_reset = True

        return ser, reward, should_reset, info


def single_combat_value(obs: Observation) -> float:
    max_hp = sum(e.max_hp for e in obs.combat_state.enemies)
    enemy_hp = sum(e.current_hp for e in obs.combat_state.enemies)

    self_hp = obs.persistent_state.hp

    if max_hp == 0:
        enemy_hp = 1
        max_hp = 1

    return ((max_hp - enemy_hp) / max_hp) * 100 + self_hp
