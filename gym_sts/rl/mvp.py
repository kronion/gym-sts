"""Run with rllib."""
import os
import typing as tp

from absl import app, logging
import fancyflags as ff
from gym import spaces

from ray import tune
from ray.air.callbacks.wandb import WandbLoggerCallback
# from ray.tune.integration.wandb import WandbLoggerCallback
# # from ray.rllib import utils
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

ENV = ff.DEFINE_dict(
    'env',
    lib=ff.String('lib'),
    mods=ff.String('mods'),
    out=ff.String(None),
    headless=ff.Boolean(True),
    animate=ff.Boolean(False),
    build_image=ff.Boolean(False),
)

TUNE = ff.DEFINE_dict(
    'tune',
    checkpoint_freq=ff.Integer(20),
    keep_checkpoints_num=ff.Integer(3),
    checkpoint_at_end=ff.Boolean(False),
    restore=ff.String(None, 'path to checkpoint to restore from'),
    resume=ff.Enum(None, ["LOCAL", "REMOTE", "PROMPT", "ERRORED_ONLY", "AUTO"]),
    sync_config=dict(
        upload_dir=ff.String(None, 'Path to local or remote folder.'),
        syncer=ff.String('auto'),
        sync_on_checkpoint=ff.Boolean(True),
        sync_period=ff.Integer(300),
    ),
    verbose=ff.Integer(3),
)

WANDB = ff.DEFINE_dict(
    'wandb',
    use=ff.Boolean(False),
    entity=ff.String('sts-ai'),
    project=ff.String('sts-rllib'),
    api_key_file=ff.String("~/.wandb"),
    log_config=ff.Boolean(False),
    save_checkpoints=ff.Boolean(False),
)

RL = ff.DEFINE_dict(
    'rl',
    num_workers=ff.Integer(0),
    rollout_fragment_length=ff.Integer(32),
    train_batch_size=ff.Integer(1024),
)

class Env(base.SlayTheSpireGymEnv):
    def __init__(self, cfg: dict):
        super().__init__(**cfg)


def main(_):
    # we need abspath's here because the cwd will be different later
    output_dir = ENV.value['out']
    if output_dir is not None:
        output_dir = os.path.abspath(output_dir)

    env_config = {
        "lib_dir": os.path.abspath(ENV.value['lib']),
        "mods_dir": os.path.abspath(ENV.value['mods']),
        "output_dir": output_dir,
        "headless": ENV.value['headless'],
        "animate": ENV.value['animate'],
    }

    if ENV.value['build_image']:
        logging.info('build_image')
        base.SlayTheSpireGymEnv.build_image()

    ppo_config = {
        "env": Env,
        "env_config": env_config,
        # "framework": "torch",
        "framework": "tf2",
        "eager_tracing": True,
        # "horizon": 64,  # just for reporting some rewards
        # "soft_horizon": True,
        # "no_done_at_end": True,
        "model": {
            "custom_model": "masked",
        },
    }
    ppo_config.update(RL.value)

    tune_config = TUNE.value
    tune_config['sync_config'] = tune.SyncConfig(**tune_config['sync_config'])

    callbacks = []

    wandb_config = WANDB.value.copy()
    if wandb_config.pop('use'):
        wandb_callback = WandbLoggerCallback(**wandb_config)
        callbacks.append(wandb_callback)

    tune.run(
        ppo.PPO,
        config=ppo_config,
        # stop={"episode_reward_mean": 1},
        callbacks=callbacks,
        **tune_config,
    )

if __name__ == "__main__":
    app.run(main)
