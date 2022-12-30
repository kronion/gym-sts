from __future__ import annotations

from typing import Literal, Union

import numpy as np
from gym.spaces import Dict, Discrete, MultiBinary
from pydantic import BaseModel, Field, NonNegativeInt

import gym_sts.spaces.constants.cards as card_consts
from gym_sts.spaces.constants.cards import CardCatalog
from gym_sts.spaces.observations import utils

from .base import BinaryArray, ShopMixin


class Card(BaseModel):
    exhausts: bool
    cost: Union[NonNegativeInt, Literal["U", "X"]]
    name: str
    id: str
    ethereal: bool
    upgrades: NonNegativeInt
    has_target: bool

    @classmethod
    def _serialize(
        cls, card_id: str, upgrades: int, discrete=False
    ) -> Union[BinaryArray, int]:
        card_idx = CardCatalog.ids.index(card_id)
        if discrete:
            card_idx *= 2
            if upgrades > 0:
                card_idx += 1

            return card_idx

        else:
            array = utils.to_binary_array(card_idx, card_consts.LOG_NUM_CARDS)

            # TODO support more than 1 upgrade
            upgrade_bit = [0]
            if upgrades > 0:
                upgrade_bit = [1]

            array = np.concatenate([upgrade_bit, array], axis=0)

            return array

    @classmethod
    def serialize_empty(cls, discrete=False) -> Union[BinaryArray, int]:
        upgrades = 0
        return cls._serialize(CardCatalog.NONE.id, upgrades, discrete=discrete)

    def serialize(self, discrete=False) -> Union[BinaryArray, int]:
        return self._serialize(self.id, self.upgrades, discrete=discrete)

    @classmethod
    def deserialize(cls, ser_data: Union[int, BinaryArray]) -> Card:
        if isinstance(ser_data, np.ndarray):
            if len(ser_data) != card_consts.LOG_NUM_CARDS + 1:
                raise ValueError("Card encoding has unexpected length")

            upgraded = ser_data[0]
            card_bits = ser_data[1:]
            card_idx = utils.from_binary_array(card_bits)
        else:
            card_idx, upgraded = divmod(ser_data, 2)

        card_id = card_consts.CardCatalog.ids[card_idx]
        card_meta: card_consts.CardMetadata = getattr(card_consts.CardCatalog, card_id)
        card_props = card_meta.upgraded if upgraded else card_meta.unupgraded

        return cls(
            id=card_id,
            name=card_meta.name,
            # TODO may be wrong because we don't currently serialize cost
            cost=card_props.default_cost,
            exhausts=card_props.exhausts,
            ethereal=card_props.ethereal,
            has_target=card_props.has_target,
            # TODO may be wrong for cards that can be upgraded 2+ times
            upgrades=upgraded,
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented

        if self.id != other.id:
            return self.id < other.id

        return self.upgrades < other.upgrades


class HandCard(Card):
    is_playable: bool

    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "card": MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                "is_playable": Discrete(2),
            }
        )

    @classmethod
    def serialize_empty(cls) -> dict:  # type: ignore[override]
        return {
            "card": super().serialize_empty(),
            "is_playable": 0,
        }

    def serialize(self) -> dict:  # type: ignore[override]
        return {
            "card": super().serialize(),
            "is_playable": int(self.is_playable),
        }

    class SerializedState(BaseModel):
        card: BinaryArray
        is_playable: int = Field(..., ge=0, le=1)

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(  # type: ignore[override]
        cls, data: Union[dict, SerializedState]
    ) -> HandCard:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        card = Card.deserialize(data.card)
        return cls(**card.dict(), is_playable=bool(data.is_playable))


class ShopCard(Card, ShopMixin):
    @classmethod
    def serialize_empty(cls) -> dict:  # type: ignore[override]
        return {
            "card": super().serialize_empty(),
            "price": cls.serialize_empty_price(),
        }

    def serialize(self) -> dict:  # type: ignore[override]
        return {"card": super().serialize(), "price": self.serialize_price()}

    class SerializedState(BaseModel):
        card: BinaryArray
        price: BinaryArray

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(  # type: ignore[override]
        cls, data: Union[dict, SerializedState]
    ) -> ShopCard:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        card = Card.deserialize(data.card)
        price = ShopMixin.deserialize_price(data.price)

        return cls(**card.dict(), price=price)
