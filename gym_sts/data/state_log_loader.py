import json
from typing import TextIO

from pydantic import BaseModel

from gym_sts.spaces.actions import ACTIONS
from gym_sts.spaces.observations import Observation


class Step(BaseModel):
    state_before: dict
    action: int
    state_after: dict


class StateLogLoader:
    def __init__(self):
        self.observations = []
        self.steps = []

    def load_file(self, fh: TextIO):
        objs = json.load(fh)

        action_strings = [act.to_command() for act in ACTIONS]

        prev_obs = None

        for obj in objs:
            cur_obs = Observation(obj["state_after"]).serialize()

            self.observations.append(cur_obs)

            # Store step data
            if prev_obs and obj["action"]:
                action = action_strings.index(obj["action"])
                step = Step(state_before=prev_obs, action=action, state_after=cur_obs)
                self.steps.append(step)

            prev_obs = cur_obs
