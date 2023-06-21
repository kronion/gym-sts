from gymnasium.spaces import Dict, Discrete, MultiBinary, MultiDiscrete, Tuple

import gym_sts.spaces.constants.base as base_consts
import gym_sts.spaces.constants.cards as card_consts
import gym_sts.spaces.constants.combat as combat_consts


def generate_card_space():
    # Generally beyond some number of cards you don't actually care
    # how many cards you have
    # But this could be optimized
    return MultiDiscrete(
        [card_consts.MAX_COPIES_OF_CARD + 1] * card_consts.NUM_CARDS_WITH_UPGRADES
    )


def generate_effect_space():
    effect_space = Dict(
        {
            "sign": Discrete(2),
            "value": MultiBinary(combat_consts.LOG_MAX_EFFECT),
        }
    )
    return Tuple([effect_space] * combat_consts.NUM_EFFECTS)


def generate_health_space():
    return Dict(
        {
            "hp": MultiBinary(base_consts.LOG_MAX_HP),
            "max_hp": MultiBinary(base_consts.LOG_MAX_HP),
        }
    )
