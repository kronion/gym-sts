"""Run with rllib."""
import os

import fancyflags as ff
import ray
from absl import app, logging
from gymnasium import spaces
from ray import tune
from ray.air import config
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.rllib.algorithms import ppo
from ray.rllib.models import preprocessors
from ray.train.rl import RLTrainer

from gym_sts.envs import base, single_combat
from gym_sts.rl import action_masking
from gym_sts.rl.metrics import StSCustomMetricCallbacks


def check_rllib_bug(space: spaces.Space):
    # rllib special-cases certain spaces, which we don't want
    if isinstance(space, spaces.Dict):
        for subspace in space.values():
            check_rllib_bug(subspace)
    elif not isinstance(space, (spaces.Discrete, spaces.MultiDiscrete)):
        assert space.shape != preprocessors.ATARI_RAM_OBS_SHAPE


check_rllib_bug(base.OBSERVATION_SPACE)

action_masking.register()

ENV = ff.DEFINE_dict(
    "env",
    lib=ff.String("lib"),
    mods=ff.String("mods"),
    out=ff.String(None),
    headless=ff.Boolean(True),
    animate=ff.Boolean(False),
    ascension=ff.Integer(20),
    build_image=ff.Boolean(False),
    reboot_frequency=ff.Integer(50, "Reboot game every n resets."),
    reboot_on_error=ff.Boolean(False),
    log_states=ff.Boolean(False),
)

TUNE = ff.DEFINE_dict(
    "tune",
    run=dict(
        name=ff.String("sts-rl", "Name of the ray experiment"),
        local_dir=ff.String(None),  # default is ~/ray_results/
        verbose=ff.Integer(3),
    ),
    failure_config=dict(
        max_failures=ff.Integer(0)  # Set to -1 to enable infinite recovery retries
    ),
    checkpoint_config=dict(
        checkpoint_frequency=ff.Integer(20),
        checkpoint_at_end=ff.Boolean(False),
        num_to_keep=ff.Integer(3),
    ),
    restore=ff.String(
        None, "Path to experiment directory to restore from, e.g. ~/ray_results/sts-rl"
    ),
    sync_config=dict(
        upload_dir=ff.String(None, "Path to local or remote folder."),
        syncer=ff.String("auto"),
        sync_on_checkpoint=ff.Boolean(True),
        sync_period=ff.Integer(300),
    ),
)

WANDB = ff.DEFINE_dict(
    "wandb",
    use=ff.Boolean(False),
    entity=ff.String("sts-ai"),
    project=ff.String("sts-rllib"),
    api_key_file=ff.String(None),
    api_key=ff.String(None),
    log_config=ff.Boolean(False),
    upload_checkpoints=ff.Boolean(False),
)

RL = ff.DEFINE_dict(
    "rl",
    rollout_fragment_length=ff.Integer(32),
    train_batch_size=ff.Integer(1024),
    num_workers=ff.Integer(0),
    model=dict(
        custom_model=ff.String("masked"),
        fcnet_hiddens=ff.Sequence([256, 256, 256, 256]),
        fcnet_activation=ff.String("relu"),
    ),
    entropy_coeff=ff.Float(0.0),
)

SCALING = ff.DEFINE_dict(
    "scaling",
    num_workers=ff.Integer(0),
    use_gpu=ff.Boolean(False),
    trainer_resources=dict(CPU=ff.Integer(1), GPU=ff.Integer(0)),
    resources_per_worker=dict(CPU=ff.Integer(1), GPU=ff.Integer(0)),
)

SINGLE_COMBAT = ff.DEFINE_dict(
    "single_combat",
    use=ff.Boolean(False),
    enemies=ff.StringList(["3_Sentries"]),
    cards=ff.StringList(["Strike_B"] * 4 + ["Defend_B"] * 4 + ["Zap"] + ["Dualcast"]),
    add_relics=ff.StringList([]),
)


class Env(base.SlayTheSpireGymEnv):
    def __init__(self, cfg: dict):
        super().__init__(**cfg)


class SingleCombatEnv(single_combat.SingleCombatSTSEnv):
    def __init__(self, cfg: dict):
        super().__init__(**cfg)


def main(_):
    ray.init(address=None)
    # we need abspath's here because the cwd will be different later
    output_dir = ENV.value["out"]
    if output_dir is not None:
        output_dir = os.path.abspath(output_dir)

    env_config = {
        "lib_dir": os.path.abspath(ENV.value["lib"]),
        "mods_dir": os.path.abspath(ENV.value["mods"]),
        "output_dir": output_dir,
    }
    for key in [
        "headless",
        "animate",
        "reboot_frequency",
        "reboot_on_error",
        "ascension",
        "log_states",
    ]:
        env_config[key] = ENV.value[key]

    if SINGLE_COMBAT.value["use"]:
        env_config["enemies"] = SINGLE_COMBAT.value["enemies"]
        env_config["cards"] = SINGLE_COMBAT.value["cards"]
        env_config["add_relics"] = SINGLE_COMBAT.value["add_relics"]

    if ENV.value["build_image"]:
        logging.info("build_image")
        base.SlayTheSpireGymEnv.build_image()

    rl_config = RL.value.copy()

    ppo_config = {
        "env": SingleCombatEnv if SINGLE_COMBAT.value["use"] else Env,
        "env_config": env_config,
        "framework": "tf2",
        "eager_tracing": True,
        # "horizon": 64,  # just for reporting some rewards
        # "soft_horizon": True,
        # "no_done_at_end": True,
    }
    if SINGLE_COMBAT.value["use"]:
        ppo_config["callbacks"] = StSCustomMetricCallbacks

    ppo_config.update(rl_config)

    trainer = RLTrainer(
        scaling_config=config.ScalingConfig(**SCALING.value),
        algorithm=ppo.PPO,
        config=ppo_config,
    )

    callbacks = []
    wandb_config = WANDB.value.copy()
    if wandb_config.pop("use"):
        wandb_callback = WandbLoggerCallback(
            name=TUNE.value["run"]["name"], **wandb_config
        )
        callbacks.append(wandb_callback)

    tune_config = TUNE.value
    # We're doing a lot of direct key-based access of values in these dict flags.
    # The fancyflags docs consider this an antipattern, see:
    #   https://github.com/deepmind/fancyflags#tips.
    sync_config = tune.SyncConfig(**tune_config["sync_config"])
    checkpoint_config = config.CheckpointConfig(**tune_config["checkpoint_config"])
    failure_config = config.FailureConfig(**tune_config["failure_config"])
    run_config = config.RunConfig(
        callbacks=callbacks,
        checkpoint_config=checkpoint_config,
        sync_config=sync_config,
        failure_config=failure_config,
        **tune_config["run"],
    )

    tuner = tune.Tuner(
        trainable=trainer,
        run_config=run_config,
    )

    restore_path = tune_config.get("restore")
    if restore_path:
        tuner = tune.Tuner.restore(restore_path, trainable=trainer, resume_errored=True)

    tuner.fit()


if __name__ == "__main__":
    app.run(main)
