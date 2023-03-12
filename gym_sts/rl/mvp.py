"""Run with rllib."""
import os

import fancyflags as ff
import ray
from absl import app, logging
from gym import spaces
from ray import tune
from ray.air import config
from ray.air.callbacks.wandb import WandbLoggerCallback
from ray.rllib.algorithms import ppo
from ray.rllib.models import preprocessors
from ray.train.rl import RLTrainer

from gym_sts.envs import base, single_combat
from gym_sts.rl import action_masking


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
)

TUNE = ff.DEFINE_dict(
    "tune",
    run=dict(
        name=ff.String("sts-rl", "Name of the ray experiment"),
        local_dir=ff.String(None),  # default is ~/ray_results/
        verbose=ff.Integer(3),
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
    save_checkpoints=ff.Boolean(False),
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
)

SCALING = ff.DEFINE_dict(
    "scaling",
    num_workers=ff.Integer(0),
    use_gpu=ff.Boolean(False),
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
        "framework": "torch",
        "eager_tracing": True,
        # "horizon": 64,  # just for reporting some rewards
        # "soft_horizon": True,
        # "no_done_at_end": True,
    }
    ppo_config.update(rl_config)

    # algorithm = ppo.PPO(ppo_config)
    # algorithm.restore("/home/spdskatr/ray_results/potato/artifacts/checkpoint_sts-rl:v12")
    # raise Exception("hi")

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
    sync_config = tune.SyncConfig(**tune_config["sync_config"])
    checkpoint_config = config.CheckpointConfig(**tune_config["checkpoint_config"])
    run_config = config.RunConfig(
        callbacks=callbacks,
        checkpoint_config=checkpoint_config,
        sync_config=sync_config,
        **tune_config["run"],
    )

    tuner = tune.Tuner(
        trainable=trainer,
        run_config=run_config,
    )

    restore_path = tune_config.get("restore")
    if restore_path:
        tuner = tune.Tuner.restore(restore_path)

    tuner.fit()


if __name__ == "__main__":
    app.run(main)
