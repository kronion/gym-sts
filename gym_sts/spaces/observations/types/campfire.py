from __future__ import annotations

from enum import Enum
from typing import Union

import numpy as np
from gym.spaces import MultiBinary

from gym_sts.spaces.constants.campfire import LOG_NUM_OPTIONS
from gym_sts.spaces.observations import utils

from .base import BinaryArray


class CampfireChoice(str, Enum):
    EMPTY = "EMPTY"  # Indicates the absence of a choice
    REST = "rest"
    SMITH = "smith"
    DIG = "dig"
    LIFT = "lift"
    TOKE = "toke"
    RECALL = "recall"

    @staticmethod
    def space():
        return MultiBinary(LOG_NUM_OPTIONS)

    @classmethod
    def serialize_empty(cls) -> BinaryArray:
        return cls.EMPTY.serialize()

    def serialize(self) -> BinaryArray:
        idx = list(CampfireChoice).index(self)
        return utils.to_binary_array(idx, LOG_NUM_OPTIONS)

    @classmethod
    def deserialize(cls, idx: Union[int, BinaryArray]) -> CampfireChoice:
        if isinstance(idx, np.ndarray):
            idx = utils.from_binary_array(idx)

        return list(cls)[idx]
