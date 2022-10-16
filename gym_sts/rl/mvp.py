"""Run with rllib."""
import os

import click
import ray
from gym import spaces
from ray import air, tune

# from ray.rllib import utils
from ray.rllib.algorithms import ppo
from ray.rllib.models import preprocessors

from gym_sts.envs import base
from gym_sts.rl import models_tf


def check_rllib_bug(space: spaces.Space):
    # rllib special-cases certain spaces, which we don't want
    if isinstance(space, spaces.Dict):
        for subspace in space.values():
            check_rllib_bug(subspace)
    elif not isinstance(space, (spaces.Discrete, spaces.MultiDiscrete)):
        assert space.shape != preprocessors.ATARI_RAM_OBS_SHAPE


check_rllib_bug(base.OBSERVATION_SPACE)

models_tf.register()


class Env(base.SlayTheSpireGymEnv):
    def __init__(self, cfg: dict):
        super().__init__(**cfg)


@click.command()
@click.argument("lib")
@click.argument("mods")
@click.argument("out")
@click.option("--headless/--headful", default=True)
@click.option("--animate/--no-animate", default=False)
@click.option("--restore/--no-restore", default=False)
def main(lib, mods, out, headless, animate, restore):

    ray.init(address=None)

    # we need abspath's here because the cwd will be different later
    if out is not None:
        output_dir = os.path.abspath(out)

    env_config = {
        "lib_dir": os.path.abspath(lib),
        "mods_dir": os.path.abspath(mods),
        "output_dir": output_dir,
        "headless": headless,
        "animate": animate,
    }

    ppo_config = {
        "env": Env,
        "env_config": env_config,
        "num_workers": 0,
        # "framework": "torch",
        "framework": "tf2",
        "eager_tracing": True,
        "rollout_fragment_length": 128,
        "train_batch_size": 1024,
        # "horizon": 64,  # just for reporting some rewards
        # "soft_horizon": True,
        # "no_done_at_end": True,
        "model": {
            "custom_model": "masked",
        },
    }

    # env = Env(env_config)
    # obs = env.reset()
    # utils.assert_contains(env.observation_space, obs)

    # utils.check_env(env)
    # print('env check done')

    # take a manual step
    # algo = ppo.PPO(ppo_config)
    # while True:
    #   algo.train()

    # tune.run(
    #     ppo.PPO,
    #     config=ppo_config,
    # )

    if restore:
        tuner = tune.Tuner.restore(
            "~/ray_results/SlayTheSpireRL",
            resume_unfinished=True,
            resume_errored=True,
            restart_errored=False,
        )
    else:
        tuner = tune.Tuner(
            ppo.PPO,
            param_space=ppo_config,
            run_config=air.RunConfig(
                name="SlayTheSpireRL",
                sync_config=tune.SyncConfig(
                    syncer=None  # Disable syncing, we store checkpoints locally
                ),
                checkpoint_config=air.config.CheckpointConfig(
                    # Only keep this many checkpoints.
                    num_to_keep=2,
                    checkpoint_frequency=1,
                ),
            ),
        )

    tuner.fit()


if __name__ == "__main__":
    main()
