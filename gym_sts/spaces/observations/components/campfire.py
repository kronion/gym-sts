from __future__ import annotations

from typing import Union

from gym.spaces import Dict, Discrete, Space
from pydantic import BaseModel

from .base import ObsComponent


class CampfireObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.rest = False
        self.smith = False
        self.lift = False
        self.toke = False
        self.dig = False
        self.recall = False

        if state.get("has_rested"):
            return

        rest_options = state.get("rest_options", [])
        possible_options = ["rest", "smith", "lift", "toke", "dig", "recall"]

        for option in possible_options:
            if option in rest_options:
                setattr(self, option, True)

    @staticmethod
    def space() -> Space:
        return Dict(
            {
                "rest": Discrete(2),
                "smith": Discrete(2),
                "lift": Discrete(2),
                "toke": Discrete(2),
                "dig": Discrete(2),
                "recall": Discrete(2),
            }
        )

    def serialize(self) -> dict:
        return {
            "rest": int(self.rest),
            "smith": int(self.smith),
            "lift": int(self.lift),
            "toke": int(self.toke),
            "dig": int(self.dig),
            "recall": int(self.recall),
        }

    class SerializedState(BaseModel):
        rest: int
        smith: int
        lift: int
        toke: int
        dig: int
        recall: int

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> CampfireObs:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        # Instantiate with empty data and update attributes individually,
        # rather than trying to recreate CommunicationMod's weird data shape.
        instance = cls({})

        instance.rest = bool(data.rest)
        instance.smith = bool(data.smith)
        instance.lift = bool(data.lift)
        instance.toke = bool(data.toke)
        instance.dig = bool(data.dig)
        instance.recall = bool(data.recall)

        return instance

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CampfireObs):
            return False

        attrs = [
            "rest",
            "smith",
            "lift",
            "toke",
            "dig",
            "recall",
        ]

        for attr in attrs:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True
