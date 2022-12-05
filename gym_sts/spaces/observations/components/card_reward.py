from __future__ import annotations

from typing import Union

from gym.spaces import Dict, Discrete, MultiBinary, Tuple
from pydantic import BaseModel, Field

import gym_sts.spaces.constants.cards as card_consts
from gym_sts.spaces import old_constants as constants
from gym_sts.spaces.constants.cards import CardCatalog
from gym_sts.spaces.observations import types

from .base import PydanticComponent


class CardRewardObs(PydanticComponent):
    cards: list[types.Card] = []
    singing_bowl: bool = Field(False, alias="bowl_available")
    skippable: bool = Field(False, alias="skip_available")

    @staticmethod
    def space():
        return Dict(
            {
                # At most 4 cards may be offered (due to Question Card relic).
                "cards": Tuple(
                    (
                        MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                        MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                        MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                        MultiBinary(card_consts.LOG_NUM_CARDS_WITH_UPGRADES),
                    )
                ),
                "singing_bowl": Discrete(2),
                "skippable": Discrete(2),
            }
        )

    def serialize(self) -> dict:
        serialized_cards = [
            types.Card.serialize_empty_binary()
        ] * constants.REWARD_CARD_COUNT
        for i, card in enumerate(self.cards):
            serialized_cards[i] = card.serialize_binary()

        return {
            "cards": serialized_cards,
            "singing_bowl": int(self.singing_bowl),
            "skippable": int(self.skippable),
        }

    class SerializedState(BaseModel):
        cards: list[types.BinaryArray]
        singing_bowl: int
        skippable: int

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> CardRewardObs:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        cards = []
        for c in data.cards:
            card = types.Card.deserialize_binary(c)
            if card.id != CardCatalog.NONE.id:
                cards.append(card)

        singing_bowl = bool(data.singing_bowl)
        skippable = bool(data.skippable)

        return cls(cards=cards, bowl_available=singing_bowl, skip_available=skippable)
