from gym_sts.spaces.constants import *
from gym.spaces import Discrete, MultiBinary, MultiDiscrete, Dict, Tuple

def generate_card_space():
    # Generally beyond some number of cards you don't actually care
    # how many cards you have
    # But this could be optimized
    return MultiDiscrete([5] * NUM_CARDS * 2)

def generate_effect_space():
    return Tuple(
        [Dict({
            "sign": Discrete(2),
            "value": MultiBinary([LOG_MAX_EFFECT])
        })] * NUM_EFFECTS
    )

def generate_health_space():
    return Dict({
        "hp": MultiBinary(LOG_MAX_HP),
        "max_hp": MultiBinary(LOG_MAX_HP)
    })

def generate_enemy_space():
    return Dict({
        "id": Discrete(NUM_MONSTER_TYPES),
        "intent": Discrete(NUM_INTENTS),
        "block": MultiBinary(LOG_MAX_BLOCK),
        "effects": generate_effect_space(),
        "health": generate_health_space()
    })

OBSERVATION_SPACE = Dict({
    "persistent_state": Dict({
        "health": generate_health_space(),
        "gold": MultiBinary(LOG_MAX_GOLD),
        "potions": MultiDiscrete([NUM_POTIONS] * NUM_POTION_SLOTS),
        "relics": MultiBinary(NUM_RELICS),
        "deck": generate_card_space()
        # TODO: Add map
    }),
    "combat_state": Dict({
        "hand": MultiDiscrete([NUM_CARDS] * HAND_SIZE),
        "energy": Dict({
            "current": MultiBinary(LOG_MAX_ENERGY),
            "max": MultiBinary(LOG_MAX_ENERGY)
        }),
        # TODO: Add orbs
        "block": MultiBinary(LOG_MAX_BLOCK),
        "effects": generate_effect_space(),
        "enemies": Tuple(
            [generate_enemy_space()] * NUM_ENEMIES
        ),
        "discard": generate_card_space(),
        "draw": generate_card_space(),
        # TODO: Worry about exhaust pile
    }),
    # TODO: Worry about shop
    # TODO: Possibly have Discrete space telling AI what screen it's on
    # TODO: Worry about random events
})


class Observation:
    def __init__(self, state: dict):
        self.in_game = state["in_game"]
        self.stable = state["ready_for_command"]

        if "game_state" in state:
            game_state = state["game_state"]
            self.screen_type = game_state["screen_type"]
        else:
            # CommunicationMod doesn't specify a screen type in the main menu
            self.screen_type = "MAIN_MENU"
        self.game_over = self.screen_type == "GAME_OVER"

        # Keep a reference to the raw CommunicationMod response
        self._state = state