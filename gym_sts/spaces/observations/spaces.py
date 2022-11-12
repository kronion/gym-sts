from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete, Tuple

import gym_sts.spaces.constants.cards as card_consts
from gym_sts.spaces import old_constants as constants


def generate_card_space():
    # Generally beyond some number of cards you don't actually care
    # how many cards you have
    # But this could be optimized
    return MultiDiscrete(
        [card_consts.MAX_COPIES_OF_CARD + 1] * card_consts.NUM_CARDS_WITH_UPGRADES
    )


def generate_effect_space():
    return Tuple(
        [Dict({"sign": Discrete(2), "value": MultiBinary([constants.LOG_MAX_EFFECT])})]
        * constants.NUM_EFFECTS
    )


def generate_health_space():
    return Dict(
        {
            "hp": MultiBinary(constants.LOG_MAX_HP),
            "max_hp": MultiBinary(constants.LOG_MAX_HP),
        }
    )
