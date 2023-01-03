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
