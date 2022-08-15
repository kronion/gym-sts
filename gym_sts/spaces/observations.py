from typing import Optional

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


class ObservationError(Exception):
    pass


class Observation:
    def __init__(self, state: dict):
        # Keep a reference to the raw CommunicationMod response
        self.state = state

    def check_for_error(self) -> None:
        if "error" in self.state:
            raise ObservationError(self.state["error"])

    @property
    def _available_commands(self) -> list[str]:
        self.check_for_error()
        return self.state["available_commands"]

    @property
    def game_over(self) -> bool:
        self.check_for_error()
        return self.screen_type == "GAME_OVER"

    @property
    def in_game(self) -> bool:
        self.check_for_error()
        return self.state["in_game"]

    @property
    def screen_type(self) -> str:
        self.check_for_error()
        if "game_state" in self.state:
            game_state = self.state["game_state"]
            screen_type = game_state["screen_type"]
        else:
            # CommunicationMod doesn't specify a screen type in the main menu
            screen_type = "MAIN_MENU"

        return screen_type

    @property
    def stable(self) -> bool:
        return self.state["ready_for_command"]
