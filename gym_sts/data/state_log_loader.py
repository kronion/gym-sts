import json
from typing import TextIO

from gym_sts.spaces.actions import ACTIONS
from gym_sts.spaces.observations import Observation


class StateLogLoader:
    def __init__(self):
        self.state_data = []
        self.step_data = {"state_before": [], "action": [], "state_after": []}

    def load_file(self, fh: TextIO):
        objs = json.load(fh)

        action_strings = [act.to_command() for act in ACTIONS]

        prev_obs = None

        for obj in objs:
            cur_obs = Observation(obj["state_after"]).serialize()

            self.state_data.append(cur_obs)

            # Store step data
            if prev_obs and obj["action"]:
                self.step_data["state_before"].append(prev_obs)
                self.step_data["action"].append(action_strings.index(obj["action"]))
                self.step_data["state_after"].append(cur_obs)

            prev_obs = cur_obs
