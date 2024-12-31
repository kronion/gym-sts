import datetime
import json
from pathlib import Path

from gym_sts.spaces.actions import Action
from gym_sts.spaces.observations import Observation


class StateLogger:
    def __init__(self, logdir, batch_size: int = 100, indent: int | None = None):
        self.logdir = Path(logdir)
        self.batch_size = batch_size
        self.indent = indent

        # TODO: Set this to true in the RL runner,
        # or make it configurable (which requires more plumbing)
        self.write_wandb = False

        self.unlogged_actions: list[dict] = []

    def log(self, action: Action | None, reward: float | None, after_obs: Observation):
        self.unlogged_actions.append(
            {
                "action": action.to_command() if action else None,
                "reward": reward,
                "state_after": after_obs.state,
            }
        )

        if len(self.unlogged_actions) >= self.batch_size:
            self.flush_actions()

    def flush_actions(self):
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        outpath = self.logdir / f"states_{now}.json"
        with open(outpath, "w") as f:
            f.write(json.dumps(self.unlogged_actions, indent=self.indent))

        self.unlogged_actions = []

        # TODO: Implement writing to WandB

        print("Actions logged to", outpath)
