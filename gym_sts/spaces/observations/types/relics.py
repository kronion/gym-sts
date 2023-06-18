from __future__ import annotations

from typing import Union

import numpy as np
from gymnasium.spaces import Dict, Discrete, MultiBinary
from pydantic import BaseModel, validator

import gym_sts.spaces.constants.relics as relic_consts
import gym_sts.spaces.constants.shop as shop_consts
from gym_sts.spaces.constants.relics import RelicCatalog
from gym_sts.spaces.observations import utils

from .base import BinaryArray, ShopMixin


class RelicBase(BaseModel):
    id: str
    name: str

    @classmethod
    def _serialize(cls, relic_id: str, discrete=False) -> Union[BinaryArray, int]:
        relic_idx = RelicCatalog.ids.index(relic_id)
        if discrete:
            return relic_idx
        else:
            return utils.to_binary_array(relic_idx, relic_consts.LOG_NUM_RELICS)

    @classmethod
    def serialize_empty(cls, discrete=False) -> Union[BinaryArray, int]:
        return cls._serialize(RelicCatalog.NONE.id, discrete=discrete)

    def serialize(self, discrete=False) -> Union[BinaryArray, int]:
        return self._serialize(self.id, discrete=discrete)

    @classmethod
    def deserialize(cls, relic_idx: Union[int, BinaryArray]) -> RelicBase:
        if isinstance(relic_idx, np.ndarray):
            relic_idx = utils.from_binary_array(relic_idx)

        relic_id = RelicCatalog.ids[relic_idx]
        relic_meta: relic_consts.RelicMetadata = getattr(RelicCatalog, relic_id)

        return cls(id=relic_id, name=relic_meta.name)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, RelicBase):
            return NotImplemented

        return self.id < other.id


class Relic(RelicBase):
    counter: int = 0

    @validator("counter", pre=True)
    def must_be_nonnegative(cls, v: int) -> int:
        # STS uses values of -1 and -2 (to indicate the relic has no counter, or that
        # it's exhausted, respectively), so we pad by 3 so all values are positive.
        # The "NONE" relic should have a value of 0.
        return v + 3

    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "id": Discrete(relic_consts.NUM_RELICS),
                "counter": MultiBinary(relic_consts.LOG_MAX_COUNTER),
            }
        )

    @classmethod
    def serialize_empty(cls) -> dict:  # type: ignore[override]
        return {
            "id": super().serialize_empty(discrete=True),
            "counter": utils.to_binary_array(0, relic_consts.LOG_MAX_COUNTER),
        }

    def serialize(self) -> dict:  # type: ignore[override]
        return {
            "id": super().serialize(discrete=True),
            "counter": utils.to_binary_array(
                min(self.counter, relic_consts.MAX_COUNTER),
                relic_consts.LOG_MAX_COUNTER,
            ),
        }

    class SerializedState(BaseModel):
        id: int
        counter: BinaryArray

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(  # type: ignore[override]
        cls, data: Union[dict, SerializedState]
    ) -> Relic:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        relic_base = RelicBase.deserialize(data.id)
        counter = utils.from_binary_array(data.counter) - 3

        return cls(id=relic_base.id, name=relic_base.name, counter=counter)


class ShopRelic(RelicBase, ShopMixin):
    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "relic": MultiBinary(relic_consts.LOG_NUM_RELICS),
                "price": MultiBinary(shop_consts.SHOP_LOG_MAX_PRICE),
            }
        )

    @classmethod
    def serialize_empty(cls) -> dict:  # type: ignore[override]
        return {
            "relic": super().serialize_empty(),
            "price": cls.serialize_empty_price(),
        }

    def serialize(self) -> dict:  # type: ignore[override]
        return {"relic": super().serialize(), "price": self.serialize_price()}

    class SerializedState(BaseModel):
        relic: BinaryArray
        price: BinaryArray

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(  # type: ignore[override]
        cls, data: Union[dict, SerializedState]
    ) -> ShopRelic:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        relic = RelicBase.deserialize(data.relic)
        price = ShopMixin.deserialize_price(data.price)

        return cls(**relic.dict(), price=price)
