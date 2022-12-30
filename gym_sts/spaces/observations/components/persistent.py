from __future__ import annotations

from typing import Union

import numpy as np
from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete, Tuple
from pydantic import BaseModel, Field, validator

import gym_sts.spaces.constants.relics as relic_consts
from gym_sts.spaces import old_constants as constants
from gym_sts.spaces.constants.cards import CardCatalog, CardMetadata
from gym_sts.spaces.observations import serializers, spaces, types, utils

from .base import PydanticComponent


# from .map import MapObs


class SerializedMap(BaseModel):
    nodes: types.BinaryArray
    edges: types.BinaryArray
    boss: int

    class Config:
        arbitrary_types_allowed = True


def serialize_map(nodes: list[types.Node], boss: str) -> dict:
    empty_node = constants.ALL_MAP_LOCATIONS.index("NONE")
    _nodes = np.full([constants.NUM_MAP_NODES], empty_node, dtype=np.uint8)
    edges = np.zeros([constants.NUM_MAP_EDGES], dtype=bool)

    for node in nodes:
        x, y = node.x, node.y
        node_index = constants.NUM_MAP_NODES_PER_ROW * y + x
        symbol = node.symbol

        if symbol == "E":
            # Depends on json field added in our CommunicationMod fork
            if isinstance(node, types.EliteNode) and node.is_burning:
                symbol = "B"

        node_type = constants.ALL_MAP_LOCATIONS.index(symbol)
        _nodes[node_index] = node_type

        if y < constants.NUM_MAP_ROWS - 1:
            edge_index = node_index * constants.NUM_MAP_EDGES_PER_NODE

            child_x_coords = [child.x for child in node.children]

            for coord in [x - 1, x, x + 1]:
                if coord in child_x_coords:
                    edges[edge_index] = True
                edge_index += 1

    _boss = constants.NORMAL_BOSSES.index(boss)
    return {
        "nodes": _nodes,
        "edges": edges,
        "boss": _boss,
    }


def deserialize_map(data: SerializedMap):
    nodes = []
    for pos, node in enumerate(data.nodes):
        node_type = constants.ALL_MAP_LOCATIONS[node]

        if node_type == "NONE":
            continue

        y, x = divmod(pos, constants.NUM_MAP_NODES_PER_ROW)
        children = []

        if y < constants.NUM_MAP_ROWS - 1:
            edge_index = (
                constants.NUM_MAP_NODES_PER_ROW * y + x
            ) * constants.NUM_MAP_EDGES_PER_NODE

            for i, coord in enumerate([x - 1, x, x + 1]):
                if data.edges[edge_index + i]:
                    children.append({"x": coord, "y": y + 1})
        else:
            children.append({"x": 3, "y": y + 2})

        nodes.append({"symbol": node_type, "children": children, "x": x, "y": y})

    boss = constants.NORMAL_BOSSES[data.boss]

    return nodes, boss


class PersistentStateObs(PydanticComponent):
    floor: int = 0
    hp: int = Field(0, alias="current_hp")
    max_hp: int = 0
    gold: int = 0
    potions: list[types.Potion] = []
    relics: list[types.Relic] = []
    deck: list[types.Card] = []
    keys: types.Keys = types.Keys()
    act_map: list[types.Node] = Field([], alias="map")
    act_boss: str = "NONE"  # TODO use enum
    screen_type: constants.ScreenType = constants.ScreenType.EMPTY

    @validator("deck")
    def ensure_sorted(cls, v: list[types.Card]) -> list[types.Card]:
        v.sort()
        return v

    @staticmethod
    def space():
        return Dict(
            {
                "floor": MultiBinary(constants.LOG_NUM_FLOORS),
                "health": spaces.generate_health_space(),
                "gold": MultiBinary(constants.LOG_MAX_GOLD),
                "potions": Tuple([types.Potion.space()] * constants.NUM_POTION_SLOTS),
                # TODO @kronion add counters and usages (e.g. lizard tail) to relics
                "relics": MultiBinary(
                    [relic_consts.NUM_RELICS, relic_consts.LOG_MAX_COUNTER]
                ),
                "deck": spaces.generate_card_space(),
                "keys": MultiBinary(constants.NUM_KEYS),
                "map": Dict(
                    {
                        "nodes": MultiDiscrete(
                            [constants.NUM_MAP_LOCATIONS] * constants.NUM_MAP_NODES
                        ),
                        "edges": MultiBinary(constants.NUM_MAP_EDGES),
                        "boss": Discrete(constants.NUM_NORMAL_BOSSES),
                    }
                ),
                "screen_type": Discrete(len(constants.ScreenType.__members__)),
            }
        )

    def serialize(self) -> dict:
        floor = utils.to_binary_array(self.floor, constants.LOG_NUM_FLOORS)
        health = types.Health(hp=self.hp, max_hp=self.max_hp).serialize()
        gold = utils.to_binary_array(self.gold, constants.LOG_MAX_GOLD)

        potions = [types.Potion.serialize_empty()] * constants.NUM_POTION_SLOTS

        for i, potion in enumerate(self.potions):
            potions[i] = potion.serialize()

        relics = np.zeros(
            [relic_consts.NUM_RELICS, relic_consts.LOG_MAX_COUNTER], dtype=bool
        )

        for relic in self.relics:
            ser = relic.serialize()
            relics[ser["id"]] = ser["counter"]

        deck = serializers.serialize_cards(self.deck)

        keys = self.keys.serialize()

        response = {
            "floor": floor,
            "health": health,
            "gold": gold,
            "potions": potions,
            "relics": relics,
            "deck": deck,
            "keys": keys,
            "map": serialize_map(self.act_map, self.act_boss),
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
        relics: types.BinaryArray
        deck: types.BinaryArray
        keys: types.BinaryArray
        act_map: SerializedMap = Field(..., alias="map")
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
        relic_df = data.relics.reshape((relic_consts.NUM_RELICS, -1))
        for idx, r in enumerate(relic_df):
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
        act_map, act_boss = deserialize_map(data.act_map)
        screen_type = list(constants.ScreenType.__members__)[data.screen_type]

        return cls(
            floor=floor,
            current_hp=hp,
            max_hp=max_hp,
            gold=gold,
            potions=potions,
            relics=relics,
            deck=deck,
            keys=keys,
            map=act_map,
            act_boss=act_boss,
            screen_type=screen_type,
        )
