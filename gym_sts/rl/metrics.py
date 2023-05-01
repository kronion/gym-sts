from typing import Dict

from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.env import BaseEnv
from ray.rllib.evaluation import Episode, RolloutWorker
from ray.rllib.policy import Policy


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
        subenvs = base_env.get_sub_environments()
        assert len(subenvs) == 1

        obs = subenvs[0].observe()

        max_hp = sum(e.max_hp for e in obs.combat_state.enemies)
        enemy_hp = sum(e.current_hp for e in obs.combat_state.enemies)
        self_hp = obs.persistent_state.hp
        self_max_hp = obs.persistent_state.max_hp

        if self_hp == 0 or enemy_hp == 0:
            episode.custom_metrics["win_rate"] = 1 if self_hp > 0 else 0

        if enemy_hp == 0:
            episode.custom_metrics["win_remaining_hp"] = self_hp / self_max_hp
        else:
            episode.custom_metrics["lose_enemy_hp"] = (
                enemy_hp / max_hp if max_hp > 0 else 0
            )
