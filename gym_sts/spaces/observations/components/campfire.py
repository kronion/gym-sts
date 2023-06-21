from __future__ import annotations

from typing import Union

from gymnasium.spaces import Dict, Discrete, Space, Tuple
from pydantic import BaseModel, Field

import gym_sts.spaces.constants.campfire as campfire_consts
from gym_sts.spaces.observations import types

from .base import PydanticComponent


class CampfireObs(PydanticComponent):
    options: list[types.CampfireChoice] = Field([], alias="rest_options")
    has_rested: bool = False

    @staticmethod
    def space() -> Space:
        return Dict(
            {
                "options": Tuple(
                    [types.CampfireChoice.space()] * campfire_consts.MAX_NUM_OPTIONS
                ),
                "has_rested": Discrete(2),
            }
        )

    def serialize(self) -> dict:
        options = [
            types.CampfireChoice.serialize_empty()
        ] * campfire_consts.MAX_NUM_OPTIONS
        for i, option in enumerate(self.options):
            options[i] = option.serialize()

        return {
            "options": options,
            "has_rested": int(self.has_rested),
        }

    class SerializedState(BaseModel):
        options: list[types.BinaryArray]
        has_rested: int

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> CampfireObs:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        options = []
        for o in data.options:
            option = types.CampfireChoice.deserialize(o)
            if option != types.CampfireChoice.EMPTY:
                options.append(option)

        has_rested = bool(data.has_rested)

        return cls(rest_options=options, has_rested=has_rested)
