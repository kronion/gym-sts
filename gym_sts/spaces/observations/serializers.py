import numpy as np
import numpy.typing as npt

from gym_sts.spaces import old_constants as constants
from gym_sts.spaces.constants import cards as card_consts
from gym_sts.spaces.observations import types


def serialize_cards(cards: list[types.Card]) -> npt.NDArray[np.uint]:
    # TODO handle Searing Blow, which can be upgraded unlimited times
    serialized = [0] * card_consts.NUM_CARDS_WITH_UPGRADES
    for card in cards:
        card_idx = card.serialize(discrete=True)

        if serialized[card_idx] < card_consts.MAX_COPIES_OF_CARD:
            serialized[card_idx] += 1

    return np.array(serialized, dtype=np.uint8)


def serialize_orbs(orbs: list[types.Orb]) -> npt.NDArray[np.uint]:
    serialized = np.array([types.Orb.serialize_empty()] * constants.MAX_ORB_SLOTS)

    for i, orb in enumerate(orbs):
        serialized[i] = orb.serialize()

    return serialized


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
