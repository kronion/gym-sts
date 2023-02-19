import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional, Union

from gym_sts.spaces.actions import Action
from gym_sts.spaces.observations import Observation


class StateLogger:
    def __init__(self, logdir: Union[str, Path], batch_size: int = 100):
        self.logdir = Path(logdir)
        self.batch_size = batch_size

        self.unlogged_actions: List[Dict] = []

    def log(self, action: Optional[Action], after_obs: Observation) -> None:
        self.unlogged_actions.append(
            {
                "action": action.to_command() if action else None,
                "state_after": after_obs.state,
            }
        )

        if len(self.unlogged_actions) >= self.batch_size:
            self.flush_actions()

    def flush_actions(self) -> None:
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        with open(self.logdir / f"states_{now}.json", "w") as f:
            f.write(json.dumps(self.unlogged_actions))

        self.unlogged_actions = []

        # TODO: Implement writing to WandB

        print("Actions flushed.")
