from __future__ import annotations

from typing import Union

from gym.spaces import Dict, Discrete, MultiBinary, Space, Tuple
from pydantic import BaseModel

import gym_sts.spaces.constants.cards as card_consts
import gym_sts.spaces.constants.shop as shop_consts
from gym_sts.spaces.constants.cards import CardCatalog
from gym_sts.spaces.constants.potions import PotionCatalog
from gym_sts.spaces.constants.relics import RelicCatalog
from gym_sts.spaces.observations import types, utils

from .base import PydanticComponent


class SerializedPurge(BaseModel):
    available: int
    price: types.BinaryArray

    class Config:
        arbitrary_types_allowed = True


class ShopObs(PydanticComponent):
    cards: list[types.ShopCard] = []
    relics: list[types.ShopRelic] = []
    potions: list[types.ShopPotion] = []
    purge_available: bool = False
    purge_cost: int = 0

    @staticmethod
    def space() -> Space:
        return Dict(
            {
                "cards": Tuple(
                    [
                        Dict(
                            {
                                "card": MultiBinary(
                                    card_consts.LOG_NUM_CARDS_WITH_UPGRADES
                                ),
                                "price": MultiBinary(shop_consts.SHOP_LOG_MAX_PRICE),
                            }
                        )
                    ]
                    * shop_consts.SHOP_CARD_COUNT,
                ),
                "relics": Tuple(
                    [types.ShopRelic.space()] * shop_consts.SHOP_RELIC_COUNT
                ),
                "potions": Tuple(
                    [types.ShopPotion.space()] * shop_consts.SHOP_POTION_COUNT
                ),
                "purge": Dict(
                    {
                        "available": Discrete(2),
                        "price": MultiBinary(shop_consts.SHOP_LOG_MAX_PRICE),
                    }
                ),
            }
        )

    def serialize(self) -> dict:
        serialized_cards = [
            types.ShopCard.serialize_empty()
        ] * shop_consts.SHOP_CARD_COUNT
        for i, card in enumerate(self.cards):
            serialized_cards[i] = card.serialize()

        serialized_relics = [
            types.ShopRelic.serialize_empty()
        ] * shop_consts.SHOP_RELIC_COUNT
        for i, relic in enumerate(self.relics):
            serialized_relics[i] = relic.serialize()

        serialized_potions = [
            types.ShopPotion.serialize_empty()
        ] * shop_consts.SHOP_POTION_COUNT
        for i, potion in enumerate(self.potions):
            serialized_potions[i] = potion.serialize()

        serialized_purge = {
            "available": int(self.purge_available),
            "price": utils.to_binary_array(
                self.purge_cost, shop_consts.SHOP_LOG_MAX_PRICE
            ),
        }

        return {
            "cards": serialized_cards,
            "relics": serialized_relics,
            "potions": serialized_potions,
            "purge": serialized_purge,
        }

    class SerializedState(BaseModel):
        cards: list[types.ShopCard.SerializedState]
        relics: list[types.ShopRelic.SerializedState]
        potions: list[types.ShopPotion.SerializedState]
        purge: SerializedPurge

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> ShopObs:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        cards = []
        for serialized_card in data.cards:
            shop_card = types.ShopCard.deserialize(serialized_card)
            if shop_card.id != CardCatalog.NONE.id:
                cards.append(shop_card)

        relics = []
        for serialized_relic in data.relics:
            shop_relic = types.ShopRelic.deserialize(serialized_relic)
            if shop_relic.id != RelicCatalog.NONE.id:
                relics.append(shop_relic)

        potions = []
        for serialized_potion in data.potions:
            shop_potion = types.ShopPotion.deserialize(serialized_potion)
            if shop_potion.id != PotionCatalog.NONE.id:
                potions.append(shop_potion)

        purge_available = bool(data.purge.available)
        purge_cost = utils.from_binary_array(data.purge.price)

        return cls(
            cards=cards,
            relics=relics,
            potions=potions,
            purge_available=purge_available,
            purge_cost=purge_cost,
        )
