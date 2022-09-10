from typing import Optional

from gym_sts.spaces import constants

from .base import ObsComponent


class MapStateObs(ObsComponent):
    def __init__(self, state: Optional[dict] = None):
        self.nodes = []
        self.boss = "NONE"

        if state is not None:
            game_state = state["game_state"]
            self.nodes = game_state["map"]
            self.boss = game_state["act_boss"]

    def serialize(self) -> dict:
        empty_node = constants.ALL_MAP_LOCATIONS.index("NONE")
        nodes = [empty_node] * constants.NUM_MAP_NODES
        edges = [0] * constants.NUM_MAP_EDGES

        for node in self.nodes:
            x, y = node["x"], node["y"]
            index = constants.NUM_MAP_NODES_PER_ROW * y + x
            symbol = node["symbol"]

            if symbol == "E":
                # Depends on json field added in our CommunicationMod fork
                if "is_burning" in node and node["is_burning"]:
                    symbol = "B"

            node_type = constants.ALL_MAP_LOCATIONS.index(symbol)
            nodes[index] = node_type

            if y < constants.NUM_MAP_ROWS - 1:
                edge_index = (
                    constants.NUM_MAP_NODES_PER_ROW * y + x
                ) * constants.NUM_MAP_EDGES_PER_NODE

                child_x_coords = [child["x"] for child in node["children"]]

                for coord in [x - 1, x, x + 1]:
                    if coord in child_x_coords:
                        edges[edge_index] = 1
                    edge_index += 1

        boss = constants.NORMAL_BOSSES.index(self.boss)
        return {
            "nodes": nodes,
            "edges": edges,
            "boss": boss,
        }
