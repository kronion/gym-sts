from __future__ import annotations

from typing import Union

import numpy as np
from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete
from pydantic import BaseModel

import gym_sts.spaces.constants.map as map_consts

from .base import BinaryArray


class MapCoordinates(BaseModel):
    x: int
    y: int


class StandardNode(MapCoordinates):
    symbol: str
    children: list[MapCoordinates]


class EliteNode(StandardNode):
    is_burning: bool


Node = Union[StandardNode, EliteNode]


class Map(BaseModel):
    nodes: list[Node] = []
    boss: str = "NONE"  # TODO use enum

    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "nodes": MultiDiscrete(
                    [map_consts.NUM_MAP_LOCATIONS] * map_consts.NUM_MAP_NODES
                ),
                "edges": MultiBinary(map_consts.NUM_MAP_EDGES),
                "boss": Discrete(map_consts.NUM_NORMAL_BOSSES),
            }
        )

    def serialize(self) -> dict:
        empty_node = map_consts.ALL_MAP_LOCATIONS.index("NONE")
        _nodes = np.full([map_consts.NUM_MAP_NODES], empty_node, dtype=np.uint8)
        edges = np.zeros([map_consts.NUM_MAP_EDGES], dtype=bool)

        for node in self.nodes:
            x, y = node.x, node.y
            node_index = map_consts.NUM_MAP_NODES_PER_ROW * y + x
            symbol = node.symbol

            if symbol == "E":
                # Depends on json field added in our CommunicationMod fork
                if isinstance(node, EliteNode) and node.is_burning:
                    symbol = "B"

            node_type = map_consts.ALL_MAP_LOCATIONS.index(symbol)
            _nodes[node_index] = node_type

            if y < map_consts.NUM_MAP_ROWS - 1:
                edge_index = node_index * map_consts.NUM_MAP_EDGES_PER_NODE

                child_x_coords = [child.x for child in node.children]

                for coord in [x - 1, x, x + 1]:
                    if coord in child_x_coords:
                        edges[edge_index] = True
                    edge_index += 1

        _boss = map_consts.NORMAL_BOSSES.index(self.boss)
        return {
            "nodes": _nodes,
            "edges": edges,
            "boss": _boss,
        }

    class SerializedState(BaseModel):
        nodes: BinaryArray
        edges: BinaryArray
        boss: int

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(cls, data: SerializedState) -> Map:
        nodes = []
        for pos, node in enumerate(data.nodes):
            node_type = map_consts.ALL_MAP_LOCATIONS[node]

            if node_type == "NONE":
                continue

            y, x = divmod(pos, map_consts.NUM_MAP_NODES_PER_ROW)
            children = []

            if y < map_consts.NUM_MAP_ROWS - 1:
                edge_index = (
                    map_consts.NUM_MAP_NODES_PER_ROW * y + x
                ) * map_consts.NUM_MAP_EDGES_PER_NODE

                for i, coord in enumerate([x - 1, x, x + 1]):
                    if data.edges[edge_index + i]:
                        children.append({"x": coord, "y": y + 1})
            else:
                children.append({"x": 3, "y": y + 2})

            nodes.append({"symbol": node_type, "children": children, "x": x, "y": y})

        boss = map_consts.NORMAL_BOSSES[data.boss]

        return cls(nodes=nodes, boss=boss)
