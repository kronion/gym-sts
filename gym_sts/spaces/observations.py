from abc import ABC, abstractmethod
from typing import Optional

from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete, Tuple

from gym_sts.spaces import constants


def generate_card_space():
    # Generally beyond some number of cards you don't actually care
    # how many cards you have
    # But this could be optimized
    return MultiDiscrete([constants.MAX_COPIES_OF_CARD] * constants.NUM_CARDS * 2)


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


def generate_combat_space():
    return Dict(
        {
            "turn": MultiBinary(constants.LOG_MAX_TURN),
            # Every card + upgrade, or no card
            "hand": MultiDiscrete([constants.NUM_CARDS * 2 + 1] * constants.HAND_SIZE),
            "energy": MultiBinary(constants.LOG_MAX_ENERGY),
            "orbs": MultiDiscrete([constants.NUM_ORBS] * constants.MAX_ORB_SLOTS),
            "block": MultiBinary(constants.LOG_MAX_BLOCK),
            "effects": generate_effect_space(),
            "enemies": Tuple([generate_enemy_space()] * constants.NUM_ENEMIES),
            "discard": generate_card_space(),
            "draw": generate_card_space(),
            "exhaust": generate_card_space(),
        }
    )


def generate_shop_space():
    return Dict(
        {
            "cards": Tuple(
                [
                    Dict(
                        {
                            # Every card + upgrade, or no card
                            "card": Discrete(constants.NUM_CARDS * 2 + 1),
                            "cost": MultiBinary([constants.SHOP_LOG_MAX_COST]),
                        }
                    )
                ]
                * constants.SHOP_CARD_COUNT,
            ),
            "relics": Tuple(
                [
                    Dict(
                        {
                            # Every relic, or no relic
                            "relic": Discrete(constants.NUM_RELICS + 1),
                            "cost": MultiBinary([constants.SHOP_LOG_MAX_COST]),
                        }
                    )
                ]
                * constants.SHOP_RELIC_COUNT
            ),
            "potions": Tuple(
                [
                    Dict(
                        {
                            "potion": Discrete(constants.NUM_POTIONS),
                            "cost": MultiBinary([constants.SHOP_LOG_MAX_COST]),
                        }
                    )
                ]
                * constants.SHOP_POTION_COUNT
            ),
            "purge": Dict(
                {
                    "available": Discrete(2),
                    "cost": MultiBinary([constants.SHOP_LOG_MAX_COST]),
                }
            ),
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
        "combat_state": generate_combat_space(),
        "shop_state": generate_shop_space(),
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


def _serialize_card(card: dict) -> int:
    # TODO update constant so adding 1 isn't needed
    card_idx = constants.ALL_CARDS.index(card["id"]) * 2 + 1
    if card["upgrades"] > 0:
        card_idx += 1

    return card_idx


def _serialize_cards(cards: list) -> list[int]:
    # TODO handle Searing Blow, which can be upgraded unlimited times
    serialized = [0] * constants.NUM_CARDS * 2
    for card in cards:
        card_idx = _serialize_card(card)

        if serialized[card_idx] < constants.MAX_COPIES_OF_CARD:
            serialized[card_idx] += 1

    return serialized


def _serialize_health(hp: int, max_hp: int) -> dict[str, list[int]]:
    return {
        "hp": to_binary_array(hp, constants.LOG_MAX_HP),
        "max_hp": to_binary_array(max_hp, constants.LOG_MAX_HP),
    }


def _serialize_effects(effects: list) -> list[dict]:
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


def _serialize_orbs(orbs: list) -> list:
    serialized = [0] * constants.MAX_ORB_SLOTS
    for i, orb in enumerate(orbs):
        if "id" in orb:
            orb_idx = constants.ALL_ORBS.index(orb["id"])
        else:
            # STS seems to have a bug where empty orbs sometimes have no ID
            orb_idx = constants.ALL_ORBS.index("Empty")

        serialized[i] = orb_idx

    return serialized


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

    def serialize(self) -> dict:
        health = _serialize_health(self.hp, self.max_hp)
        gold = to_binary_array(self.gold, constants.LOG_MAX_GOLD)

        potions = [
            constants.ALL_POTIONS.index("Potion Slot")
        ] * constants.NUM_POTION_SLOTS

        for i, potion in enumerate(self.potions):
            potions[i] = constants.ALL_POTIONS.index(potion["id"])

        _relics = [False] * constants.NUM_RELICS
        for relic in self.relics:
            _relics[constants.ALL_RELICS.index(relic["id"])] = True
        relics = [int(relic) for relic in _relics]

        deck = _serialize_cards(self.deck)

        _keys = [False] * constants.NUM_KEYS
        for i, key in enumerate(["ruby", "emerald", "sapphire"]):
            if key in self.keys:
                _keys[i] = self.keys[key]
        keys = [int(key) for key in _keys]

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


class CombatStateObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.turn = 0

        self.hand = []
        self.discard = []
        self.draw = []
        self.exhaust = []

        self.enemies = []

        self.energy = 0
        self.block = 0
        self.effects = []
        self.orbs = []

        if "game_state" in state:
            game_state = state["game_state"]
            if "combat_state" in game_state:
                combat_state = game_state["combat_state"]

                self.turn = combat_state["turn"]

                self.hand = combat_state["hand"]
                self.discard = combat_state["discard_pile"]
                self.draw = combat_state["draw_pile"]
                self.exhaust = combat_state["exhaust_pile"]

                self.enemies = combat_state["monsters"]

                player_state = combat_state["player"]
                self.block = player_state["block"]
                self.energy = player_state["energy"]
                self.effects = player_state["powers"]
                self.orbs = player_state["orbs"]

    def _serialize_enemy(self, enemy: Optional[dict]) -> dict:
        if enemy is not None:
            serialized = {
                "id": constants.ALL_MONSTER_TYPES.index(enemy["id"]),
                "intent": constants.ALL_INTENTS.index(enemy["intent"]),
                "block": to_binary_array(enemy["block"], constants.LOG_MAX_BLOCK),
                "effects": _serialize_effects(enemy["powers"]),
                "health": _serialize_health(enemy["current_hp"], enemy["max_hp"]),
            }
        else:
            serialized = {
                "id": 0,
                "intent": 0,
                "block": to_binary_array(0, constants.LOG_MAX_BLOCK),
                "effects": _serialize_effects([]),
                "health": _serialize_health(0, 0),
            }

        return serialized

    def serialize(self) -> dict:
        turn = to_binary_array(self.turn, constants.LOG_MAX_TURN)
        energy = to_binary_array(self.energy, constants.LOG_MAX_ENERGY)
        block = to_binary_array(self.block, constants.LOG_MAX_BLOCK)

        # TODO handle Searing Blow, which can be upgraded unlimited times
        hand = [0] * constants.HAND_SIZE
        for i, card in enumerate(self.hand):
            # Add 1 so the 0 index is reserved for no card
            card_id = constants.ALL_CARDS.index(card["id"]) * 2 + 1
            if card["upgrades"] > 0:
                card_id += 1

            hand[i] = card_id

        effects = _serialize_effects(self.effects)
        orbs = _serialize_orbs(self.orbs)

        enemies = []
        for i in range(constants.NUM_ENEMIES):
            enemy = None
            if i < len(self.enemies):
                enemy = self.enemies[i]

            enemies.append(self._serialize_enemy(enemy))

        discard = _serialize_cards(self.discard)
        draw = _serialize_cards(self.draw)
        exhaust = _serialize_cards(self.exhaust)

        response = {
            "turn": turn,
            "hand": hand,
            "energy": energy,
            "block": block,
            "effects": effects,
            "orbs": orbs,
            "enemies": enemies,
            "discard": discard,
            "draw": draw,
            "exhaust": exhaust,
        }

        return response


class ShopStateObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.cards = []
        self.relics = []
        self.potions = []
        self.purge_available = False
        self.purge_cost = 0

        if "game_state" in state:
            game_state = state["game_state"]
            if (
                "screen_type" in game_state
                and game_state["screen_type"] == "SHOP_SCREEN"
            ):
                screen_state = game_state["screen_state"]
                self.cards = screen_state["cards"]
                self.relics = screen_state["relics"]
                self.potions = screen_state["potions"]
                self.purge_available = screen_state["purge_available"]
                self.purge_cost = screen_state["purge_cost"]

    def serialize(self) -> dict:
        serialized_cards = [
            {
                "card": 0,
                "cost": to_binary_array(0, constants.SHOP_LOG_MAX_COST),
            }
        ] * constants.SHOP_CARD_COUNT
        for i, card in enumerate(self.cards):
            serialized = {
                "card": _serialize_card(card),
                "cost": to_binary_array(card["price"], constants.SHOP_LOG_MAX_COST),
            }
            serialized_cards[i] = serialized

        serialized_relics = [
            {
                "relic": 0,
                "cost": to_binary_array(0, constants.SHOP_LOG_MAX_COST),
            }
        ] * constants.SHOP_RELIC_COUNT
        for i, relic in enumerate(self.relics):
            serialized = {
                # TODO eliminate need to pad by 1
                "relic": constants.ALL_RELICS.index(relic["id"]) + 1,
                "cost": to_binary_array(relic["price"], constants.SHOP_LOG_MAX_COST),
            }
            serialized_relics[i] = serialized

        serialized_potions = [
            {
                "potion": 0,
                "cost": to_binary_array(0, constants.SHOP_LOG_MAX_COST),
            }
        ] * constants.SHOP_POTION_COUNT
        for i, potion in enumerate(self.potions):
            serialized = {
                # TODO eliminate need to pad by 1
                "potion": constants.ALL_POTIONS.index(potion["id"]),
                "cost": to_binary_array(potion["price"], constants.SHOP_LOG_MAX_COST),
            }
            serialized_potions[i] = serialized

        serialized_purge = {
            "available": int(self.purge_available),
            "price": to_binary_array(self.purge_cost, constants.SHOP_LOG_MAX_COST),
        }

        return {
            "cards": serialized_cards,
            "relics": serialized_relics,
            "potions": serialized_potions,
            "purge": serialized_purge,
        }


class Observation:
    def __init__(self, state: dict):
        self.persistent_state = PersistentStateObs(state)
        self.combat_state = CombatStateObs(state)
        self.shop_state = ShopStateObs(state)

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

    def serialize(self) -> dict:
        return {
            "persistent_state": self.persistent_state.serialize(),
            "combat_state": self.combat_state.serialize(),
            "shop_state": self.shop_state.serialize(),
        }
