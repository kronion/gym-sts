from __future__ import annotations

from typing import Union

import numpy as np
from gymnasium.spaces import Dict, Discrete, MultiBinary, Tuple
from pydantic import BaseModel, Field, root_validator, validator

import gym_sts.spaces.constants.potions as potion_consts
import gym_sts.spaces.constants.relics as relic_consts
from gym_sts.spaces import old_constants as constants
from gym_sts.spaces.constants.cards import CardCatalog, CardMetadata
from gym_sts.spaces.observations import serializers, spaces, types, utils

from .base import PydanticComponent


class PersistentStateObs(PydanticComponent):
    floor: int = 0
    hp: int = Field(0, alias="current_hp")
    max_hp: int = 0
    gold: int = 0
    potions: list[types.Potion] = []
    relics: list[types.Relic] = []
    deck: list[types.Card] = []
    keys: types.Keys = types.Keys()
    map: types.Map = types.Map()
    screen_type: constants.ScreenType = constants.ScreenType.EMPTY

    @root_validator(pre=True)
    def combine_map_inputs(cls, values):
        """
        CommunicationMod provides the map nodes and act boss separately, but we'd
        rather combine them into one Pydantic model. To do this, we restructure the
        input so our Pydantic model will deserialize it properly.
        """

        try:
            map = values["map"]
            if not isinstance(map, types.Map):
                restructured_map = {
                    "nodes": map,
                    "boss": values["act_boss"],
                }
                values["map"] = restructured_map
        except KeyError:
            pass

        return values

    @validator("deck")
    def ensure_deck_sorted(cls, v: list[types.Card]) -> list[types.Card]:
        v.sort()
        return v

    @validator("relics")
    def ensure_relics_sorted(cls, v: list[types.Relic]) -> list[types.Relic]:
        v.sort()
        return v

    @staticmethod
    def space():
        return Dict(
            {
                "floor": MultiBinary(constants.LOG_NUM_FLOORS),
                "health": spaces.generate_health_space(),
                "gold": MultiBinary(constants.LOG_MAX_GOLD),
                "potions": Tuple(
                    [types.Potion.space()] * potion_consts.NUM_POTION_SLOTS
                ),
                "relics": Tuple(
                    [MultiBinary(relic_consts.LOG_MAX_COUNTER)]
                    * relic_consts.NUM_RELICS
                ),
                "deck": spaces.generate_card_space(),
                "keys": MultiBinary(constants.NUM_KEYS),
                "map": types.Map.space(),
                "screen_type": Discrete(len(constants.ScreenType.__members__)),
            }
        )

    def serialize(self) -> dict:
        floor = utils.to_binary_array(self.floor, constants.LOG_NUM_FLOORS)
        health = types.Health(hp=self.hp, max_hp=self.max_hp).serialize()
        gold = utils.to_binary_array(self.gold, constants.LOG_MAX_GOLD)

        potions = [types.Potion.serialize_empty()] * potion_consts.NUM_POTION_SLOTS

        for i, potion in enumerate(self.potions):
            potions[i] = potion.serialize()

        relics = [
            np.zeros(relic_consts.LOG_MAX_COUNTER, dtype=bool)
        ] * relic_consts.NUM_RELICS

        for relic in self.relics:
            ser = relic.serialize()
            relics[ser["id"]] = ser["counter"]

        deck = serializers.serialize_cards(self.deck)

        keys = self.keys.serialize()
        map = self.map.serialize()

        response = {
            "floor": floor,
            "health": health,
            "gold": gold,
            "potions": potions,
            "relics": relics,
            "deck": deck,
            "keys": keys,
            "map": map,
            "screen_type": list(constants.ScreenType.__members__).index(
                self.screen_type.value
            ),
        }

        return response

    class SerializedState(BaseModel):
        floor: types.BinaryArray
        health: types.Health.SerializedState
        gold: types.BinaryArray
        potions: list[types.Potion.SerializedState]
        relics: list[types.BinaryArray]
        deck: types.BinaryArray
        keys: types.BinaryArray
        map: types.Map.SerializedState
        screen_type: int

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> PersistentStateObs:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        floor = utils.from_binary_array(data.floor)
        hp = utils.from_binary_array(data.health.hp)
        max_hp = utils.from_binary_array(data.health.max_hp)
        gold = utils.from_binary_array(data.gold)

        potions = []
        for p in data.potions:
            potion = types.Potion.deserialize(p)
            if potion.id != "NONE":
                potions.append(potion)

        relics = []
        for idx, r in enumerate(data.relics):
            relic_data = {
                "id": idx,
                "counter": r,
            }
            relic = types.Relic.deserialize(relic_data)
            if relic.id != relic_consts.RelicCatalog.NONE.id and relic.counter > 0:
                relics.append(relic)

        deck = []
        for _card_idx, count in enumerate(data.deck):
            card_idx, upgrade_bit = divmod(_card_idx, 2)
            card_id = CardCatalog.ids[card_idx]
            if card_id != CardCatalog.NONE.id and count > 0:
                card_meta: CardMetadata = getattr(CardCatalog, card_id)
                card_props = card_meta.upgraded if upgrade_bit else card_meta.unupgraded

                for _ in range(count):
                    card = types.Card(
                        id=card_id,
                        name=card_meta.name,
                        # TODO may be wrong because we don't currently serialize cost
                        cost=card_props.default_cost,
                        exhausts=card_props.exhausts,
                        ethereal=card_props.ethereal,
                        has_target=card_props.has_target,
                        # TODO may be wrong for cards that can be upgraded 2+ times
                        upgrades=upgrade_bit,
                    )
                    deck.append(card)

        keys = types.Keys.deserialize(data.keys)
        map = types.Map.deserialize(data.map)
        screen_type_str = list(constants.ScreenType.__members__)[data.screen_type]
        screen_type = constants.ScreenType(screen_type_str)

        return cls(
            floor=floor,
            current_hp=hp,
            max_hp=max_hp,
            gold=gold,
            potions=potions,
            relics=relics,
            deck=deck,
            keys=keys,
            map=map,
            screen_type=screen_type,
        )
