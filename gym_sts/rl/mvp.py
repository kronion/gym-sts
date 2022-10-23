"""Run with rllib."""
import os
import typing as tp

from absl import app, flags
from gym import spaces

# from ray import tune
# from ray.rllib import utils
from ray.rllib.algorithms import ppo

from gym_sts.envs import base

_LIB = flags.DEFINE_string("lib", None, "lib dir", required=True)
_MODS = flags.DEFINE_string("mods", None, "mods dir", required=True)
_OUT = flags.DEFINE_string("out", None, "out dir", required=False)


class Env(base.SlayTheSpireGymEnv):
    def __init__(self, cfg: dict):
        super().__init__(**cfg)


def check_space(space: spaces.Space, element: tp.Any):
    if isinstance(space, spaces.Dict):
        assert isinstance(element, tp.Mapping)

        for key, subspace in space.items():
            check_space(subspace, element[key])
    assert space.contains(element)


def main(_):
    # we need abspath's here because the cwd will be different later
    output_dir = _OUT.value
    if output_dir is not None:
        output_dir = os.path.abspath(output_dir)

    env_config = {
        "lib_dir": os.path.abspath(_LIB.value),
        "mods_dir": os.path.abspath(_MODS.value),
        "output_dir": output_dir,
        "headless": True,
    }

    ppo_config = {
        "env": Env,
        "env_config": env_config,
        "num_workers": 0,
        "framework": "torch",
        # "framework": "tf2",
        # "eager_tracing": True,
        "rollout_fragment_length": 32,
        "train_batch_size": 256,
        "horizon": 64,  # just for reporting some rewards
        "soft_horizon": True,
        "no_done_at_end": True,
    }

    # env = Env(env_config)
    # obs = env.reset()
    # check_space(env.observation_space, obs)

    # utils.check_env(env)
    # print('env check done')

    # take a manual step
    algo = ppo.PPO(ppo_config)
    algo.train()

    # tune.run(
    #     ppo.PPO,
    #     config=ppo_config,
    # )


if __name__ == "__main__":
    app.run(main)
