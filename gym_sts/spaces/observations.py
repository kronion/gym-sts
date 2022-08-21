from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete, Tuple

from gym_sts.spaces import constants


def generate_card_space():
    # Generally beyond some number of cards you don't actually care
    # how many cards you have
    # But this could be optimized
    return MultiDiscrete([5] * constants.NUM_CARDS * 2)


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


def generate_enemy_space():
    return Dict(
        {
            "id": Discrete(constants.NUM_MONSTER_TYPES),
            "intent": Discrete(constants.NUM_INTENTS),
            "block": MultiBinary(constants.LOG_MAX_BLOCK),
            "effects": generate_effect_space(),
            "health": generate_health_space(),
        }
    )


OBSERVATION_SPACE = Dict(
    {
        "persistent_state": Dict(
            {
                "health": generate_health_space(),
                "gold": MultiBinary(constants.LOG_MAX_GOLD),
                "potions": MultiDiscrete(
                    [constants.NUM_POTIONS] * constants.NUM_POTION_SLOTS
                ),
                "relics": MultiBinary(constants.NUM_RELICS),
                "deck": generate_card_space()
                # TODO: Add map
                # TODO: Add keys
            }
        ),
        "combat_state": Dict(
            {
                "hand": MultiDiscrete([constants.NUM_CARDS] * constants.HAND_SIZE),
                "energy": Dict(
                    {
                        "current": MultiBinary(constants.LOG_MAX_ENERGY),
                        "max": MultiBinary(constants.LOG_MAX_ENERGY),
                    }
                ),
                # TODO: Add orbs
                "block": MultiBinary(constants.LOG_MAX_BLOCK),
                "effects": generate_effect_space(),
                "enemies": Tuple([generate_enemy_space()] * constants.NUM_ENEMIES),
                "discard": generate_card_space(),
                "draw": generate_card_space(),
                # TODO: Worry about exhaust pile
            }
        ),
        # TODO: Worry about shop
        # TODO: Possibly have Discrete space telling AI what screen it's on (e.g. screen type)
        # TODO: Worry about random events
    }
)


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
