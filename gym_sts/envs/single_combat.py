from .base import SlayTheSpireGymEnv


class SingleCombatSTSEnv(SlayTheSpireGymEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def reset(self, *args, **kwargs):
        res = super().reset(*args, **kwargs)

        obs = self.communicator.basemod("fight Gremlin_Nob")
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
