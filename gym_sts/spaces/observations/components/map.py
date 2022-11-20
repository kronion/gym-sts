from typing import Optional

import numpy as np

from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete
from gym_sts.spaces import constants

from .base import ObsComponent


class MapObs(ObsComponent):
    def __init__(self, state: Optional[dict] = None):
        self.nodes = []
        self.boss = "NONE"

        if state is not None:
            game_state = state["game_state"]
            self.nodes = game_state["map"]
            self.boss = game_state["act_boss"]

    @staticmethod
    def space():
        return Dict(
            {
                "nodes": MultiDiscrete(
                    [constants.NUM_MAP_LOCATIONS] * constants.NUM_MAP_NODES
                ),
                "edges": MultiBinary(constants.NUM_MAP_EDGES),
                "boss": Discrete(constants.NUM_NORMAL_BOSSES),
            }
        )

    def serialize(self) -> dict:
        empty_node = constants.ALL_MAP_LOCATIONS.index("NONE")
        nodes = np.full([constants.NUM_MAP_NODES], empty_node, dtype=np.uint8)
        edges = np.zeros([constants.NUM_MAP_EDGES], dtype=bool)

        for node in self.nodes:
            x, y = node["x"], node["y"]
            node_index = constants.NUM_MAP_NODES_PER_ROW * y + x
            symbol = node["symbol"]

            if symbol == "E":
                # Depends on json field added in our CommunicationMod fork
                if "is_burning" in node and node["is_burning"]:
                    symbol = "B"

            node_type = constants.ALL_MAP_LOCATIONS.index(symbol)
            nodes[node_index] = node_type

            if y < constants.NUM_MAP_ROWS - 1:
                edge_index = node_index * constants.NUM_MAP_EDGES_PER_NODE

                child_x_coords = [child["x"] for child in node["children"]]

                for coord in [x - 1, x, x + 1]:
                    if coord in child_x_coords:
                        edges[edge_index] = True
                    edge_index += 1

        boss = constants.NORMAL_BOSSES.index(self.boss)
        return {
            "nodes": nodes,
            "edges": edges,
            "boss": boss,
        }
