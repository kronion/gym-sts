from __future__ import annotations

from typing import Union

import numpy as np
from gym.spaces import Dict, Discrete, MultiBinary
from pydantic import BaseModel

import gym_sts.spaces.constants.potions as potion_consts
import gym_sts.spaces.constants.shop as shop_consts
from gym_sts.spaces.constants.potions import PotionCatalog
from gym_sts.spaces.observations import utils

from .base import BinaryArray, ShopMixin


class PotionBase(BaseModel):
    id: str
    name: str
    requires_target: bool

    @classmethod
    def _serialize(cls, potion_id: str, discrete=False) -> Union[BinaryArray, int]:
        potion_idx = PotionCatalog.ids.index(potion_id)
        if discrete:
            return potion_idx
        else:
            return utils.to_binary_array(potion_idx, potion_consts.LOG_NUM_POTIONS)

    @classmethod
    def serialize_empty(cls, discrete=False) -> Union[BinaryArray, int]:
        return cls._serialize(PotionCatalog.NONE.id, discrete=discrete)

    def serialize(self, discrete=False) -> Union[BinaryArray, int]:
        return self._serialize(self.id, discrete=discrete)

    @classmethod
    def deserialize(cls, potion_idx: Union[int, BinaryArray]) -> PotionBase:
        # Can't check if instance of BinaryArray, because it's not a real class?
        if isinstance(potion_idx, np.ndarray):
            potion_idx = utils.from_binary_array(potion_idx)

        potion_id = PotionCatalog.ids[potion_idx]
        potion_meta: potion_consts.PotionMetadata = getattr(PotionCatalog, potion_id)

        return cls(
            id=potion_id,
            name=potion_meta.name,
            requires_target=potion_meta.requires_target,
        )


class Potion(PotionBase):
    can_use: bool
    can_discard: bool

    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "id": MultiBinary(potion_consts.LOG_NUM_POTIONS),
                "can_use": Discrete(2),
                "can_discard": Discrete(2),
            }
        )

    @classmethod
    def serialize_empty(cls) -> dict:  # type: ignore[override]
        return {
            "id": super().serialize_empty(),
            "can_use": 0,
            "can_discard": 0,
        }

    def serialize(self) -> dict:  # type: ignore[override]
        return {
            "id": super().serialize(),
            "can_use": int(self.can_use),
            "can_discard": int(self.can_discard),
        }

    class SerializedState(BaseModel):
        id: BinaryArray
        can_use: int
        can_discard: int

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(  # type: ignore[override]
        cls, data: Union[dict, SerializedState]
    ) -> Potion:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        potion_base = PotionBase.deserialize(data.id)
        can_use = bool(data.can_use)
        can_discard = bool(data.can_discard)

        return cls(
            id=potion_base.id,
            name=potion_base.name,
            requires_target=potion_base.requires_target,
            can_use=can_use,
            can_discard=can_discard,
        )


class ShopPotion(PotionBase, ShopMixin):
    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "potion": MultiBinary(potion_consts.LOG_NUM_POTIONS),
                "price": MultiBinary(shop_consts.SHOP_LOG_MAX_PRICE),
            }
        )

    @classmethod
    def serialize_empty(cls) -> dict:  # type: ignore[override]
        return {
            "potion": super().serialize_empty(),
            "price": cls.serialize_empty_price(),
        }

    def serialize(self) -> dict:  # type: ignore[override]
        return {"potion": super().serialize(), "price": self.serialize_price()}

    class SerializedState(BaseModel):
        potion: BinaryArray
        price: BinaryArray

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(  # type: ignore[override]
        cls, data: Union[dict, SerializedState]
    ) -> ShopPotion:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        potion = PotionBase.deserialize(data.potion)
        price = ShopMixin.deserialize_price(data.price)

        return cls(**potion.dict(), price=price)
