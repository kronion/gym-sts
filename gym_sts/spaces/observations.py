from abc import ABC, abstractmethod

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
                "deck": generate_card_space(),
                "keys": MultiBinary(constants.NUM_KEYS),
                # TODO: Add map
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
        # TODO: Possibly have Discrete space telling AI what screen it's on
        # (e.g. screen type)
        # TODO: Worry about random events
    }
)


class ObservationError(Exception):
    pass


class ObsComponent(ABC):
    @abstractmethod
    def serialize(self):
        raise RuntimeError("Not implemented")


def to_binary_array(n: int, digits: int) -> list[int]:
    array = [0] * digits

    idx = 0
    n_copy = n
    while n_copy > 0:
        if idx >= digits:
            raise ValueError(
                f"{n} is too large to represent with {digits} binary digits"
            )

        n_copy, r = divmod(n_copy, 2)
        if r > 0:
            array[idx] = 1
        idx += 1

    return array


def _serialize_health(hp: int, max_hp: int) -> dict[str, list[int]]:
    return {
        "hp": to_binary_array(hp, constants.LOG_MAX_HP),
        "max_hp": to_binary_array(max_hp, constants.LOG_MAX_HP),
    }


class PersistentStateObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.hp = 0
        self.max_hp = 0
        self.gold = 0
        self.potions = []
        self.relics = []
        self.deck = []
        self.keys = {}

        if "game_state" in state:
            game_state = state["game_state"]
            self.hp = game_state["current_hp"]
            self.max_hp = game_state["max_hp"]
            self.gold = game_state["gold"]
            self.potions = game_state["potions"]
            self.relics = game_state["relics"]
            self.deck = game_state["deck"]

            if "keys" in game_state:
                self.keys = game_state["keys"]

    def serialize(self):
        health = _serialize_health(self.hp, self.max_hp)
        gold = to_binary_array(self.gold, constants.LOG_MAX_GOLD)

        potions = [
            constants.ALL_POTIONS.index("Potion Slot")
        ] * constants.NUM_POTION_SLOTS

        for i, potion in enumerate(self.potions):
            potions[i] = constants.ALL_POTIONS.index(potion["id"])

        relics = [False] * constants.NUM_RELICS
        for relic in self.relics:
            relics[constants.ALL_RELICS.index(relic["id"])] = True
        relics = [int(relic) for relic in relics]

        # TODO handle Searing Blow, which can be upgraded unlimited times
        deck = [0] * constants.NUM_CARDS * 2
        for card in self.deck:
            card_idx = constants.ALL_CARDS.index(card["id"]) * 2
            if card["upgrades"] > 0:
                card_idx += 1

            deck[card_idx] += 1

        keys = [False] * constants.NUM_KEYS
        for i, key in enumerate(["ruby", "emerald", "sapphire"]):
            if key in self.keys:
                keys[i] = self.keys[key]
        keys = [int(key) for key in keys]

        response = {
            "health": health,
            "gold": gold,
            "potions": potions,
            "relics": relics,
            "deck": deck,
            "keys": keys,
            # TODO: Add map
        }

        return response


class Observation:
    def __init__(self, state: dict):
        self.persistent_state = PersistentStateObs(state)

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

    def serialize(self):
        return {"persistent_state": self.persistent_state.serialize()}
