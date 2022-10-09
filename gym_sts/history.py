from dataclasses import dataclass, field
import typing as tp

# from pydantic import BaseModel

from gym_sts.spaces.observations import Observation
from gym_sts.spaces.actions import Action

@dataclass
class History:
    seed: int
    states: tp.List[Observation] = field(default_factory=list)
    actions: tp.List[Action] = field(default_factory=list)
