from pydantic import BaseModel

from gym_sts.spaces import constants
from gym_sts.spaces.observations import types

from .utils import to_binary_array


def serialize_cards(cards: list[types.Card]) -> list[int]:
    # TODO handle Searing Blow, which can be upgraded unlimited times
    serialized = [0] * constants.NUM_CARDS_WITH_UPGRADES
    for card in cards:
        card_idx = card.serialize_discrete()

        if serialized[card_idx] < constants.MAX_COPIES_OF_CARD:
            serialized[card_idx] += 1

    return serialized


def serialize_health(hp: int, max_hp: int) -> dict[str, list[int]]:
    return {
        "hp": to_binary_array(hp, constants.LOG_MAX_HP),
        "max_hp": to_binary_array(max_hp, constants.LOG_MAX_HP),
    }


def serialize_effects(effects: list) -> list[dict]:
    serialized = []
    effect_map = {effect["id"]: effect for effect in effects}

    for effect in constants.ALL_EFFECTS:
        encoding = {
            "sign": 0,
            "value": to_binary_array(0, constants.LOG_MAX_EFFECT),
        }
        if effect in effect_map:
            value = effect_map[effect]["amount"]

            if value < 0:
                encoding["sign"] = 1
                value = -value

            encoding["value"] = to_binary_array(value, constants.LOG_MAX_EFFECT)

        serialized.append(encoding)

    return serialized


def serialize_orbs(orbs: list) -> list:
    serialized = [0] * constants.MAX_ORB_SLOTS
    for i, orb in enumerate(orbs):
        if "id" in orb:
            orb_idx = constants.ALL_ORBS.index(orb["id"])
        else:
            # STS seems to have a bug where empty orbs sometimes have no ID
            orb_idx = constants.ALL_ORBS.index("Empty")

        serialized[i] = orb_idx

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
