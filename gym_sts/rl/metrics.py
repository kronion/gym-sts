from typing import Dict

from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.env import BaseEnv
from ray.rllib.evaluation import Episode, RolloutWorker
from ray.rllib.policy import Policy

from gym_sts.spaces.observations import Observation


class StSCustomMetricCallbacks(DefaultCallbacks):
    def on_episode_end(
        self,
        *,
        worker: RolloutWorker,
        base_env: BaseEnv,
        policies: Dict[str, Policy],
        episode: Episode,
        env_index: int,
        **kwargs
    ):
        obs = Observation.deserialize(episode.last_raw_obs_for())
        self_hp = obs.persistent_state.hp
        episode.custom_metrics["win_rate"] = 1 if self_hp > 0 else 0
