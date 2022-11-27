from __future__ import annotations

from typing import Union

from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete
from pydantic import BaseModel, Field

from gym_sts.spaces import old_constants as constants
from gym_sts.spaces.constants.cards import CardCatalog, CardMetadata
from gym_sts.spaces.observations import serializers, spaces, types, utils

from .base import PydanticComponent

# from .map import MapObs


class SerializedMap(BaseModel):
    nodes: list[int]
    edges: types.BinaryArray
    boss: int


def serialize_map(nodes: list[types.Node], boss: str) -> dict:
    empty_node = constants.ALL_MAP_LOCATIONS.index("NONE")
    _nodes = [empty_node] * constants.NUM_MAP_NODES
    edges = [0] * constants.NUM_MAP_EDGES

    for node in nodes:
        x, y = node.x, node.y
        index = constants.NUM_MAP_NODES_PER_ROW * y + x
        symbol = node.symbol

        if symbol == "E":
            # Depends on json field added in our CommunicationMod fork
            if isinstance(node, types.EliteNode) and node.is_burning:
                symbol = "B"

        node_type = constants.ALL_MAP_LOCATIONS.index(symbol)
        _nodes[index] = node_type

        if y < constants.NUM_MAP_ROWS - 1:
            edge_index = (
                constants.NUM_MAP_NODES_PER_ROW * y + x
            ) * constants.NUM_MAP_EDGES_PER_NODE

            child_x_coords = [child.x for child in node.children]

            for coord in [x - 1, x, x + 1]:
                if coord in child_x_coords:
                    edges[edge_index] = 1
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

    @staticmethod
    def space():
        return Dict(
            {
                "floor": MultiBinary(constants.LOG_NUM_FLOORS),
                "health": spaces.generate_health_space(),
                "gold": MultiBinary(constants.LOG_MAX_GOLD),
                "potions": MultiDiscrete(
                    [constants.NUM_POTIONS] * constants.NUM_POTION_SLOTS
                ),
                # TODO @kronion add counters and usages (e.g. lizard tail) to relics
                "relics": MultiBinary(constants.NUM_RELICS),
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

        potions = [0] * constants.NUM_POTION_SLOTS

        for i, potion in enumerate(self.potions):
            potions[i] = constants.ALL_POTIONS.index(potion.id)

        _relics = [False] * constants.NUM_RELICS
        for relic in self.relics:
            _relics[constants.ALL_RELICS.index(relic.id)] = True
        relics = [int(relic) for relic in _relics]

        deck = serializers.serialize_cards(self.deck)

        _keys = [self.keys.ruby, self.keys.emerald, self.keys.sapphire]
        keys = [int(key) for key in _keys]

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
        potions: list[int]
        relics: types.BinaryArray
        deck: list[int]
        keys: types.BinaryArray
        act_map: SerializedMap = Field(..., alias="map")
        screen_type: int

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
        for r in data.relics:
            relic = types.Relic.deserialize(r)
            if relic.id != "NONE":
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

        ruby, emerald, sapphire = data.keys
        keys = types.Keys(ruby=ruby, emerald=emerald, sapphire=sapphire)
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
