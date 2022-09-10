from abc import ABC, abstractmethod
from typing import Optional

from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete, Tuple
from pydantic import parse_obj_as

from gym_sts.spaces import constants

from . import components, serializers, types
from .utils import to_binary_array


def generate_card_space():
    # Generally beyond some number of cards you don't actually care
    # how many cards you have
    # But this could be optimized
    return MultiDiscrete(
        [constants.MAX_COPIES_OF_CARD] * constants.NUM_CARDS_WITH_UPGRADES
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


def generate_map_space():
    return Dict(
        {
            "nodes": MultiDiscrete(
                [constants.NUM_MAP_LOCATIONS] * constants.NUM_MAP_NODES
            ),
            "edges": MultiBinary(constants.NUM_MAP_EDGES),
            "boss": Discrete(constants.NUM_NORMAL_BOSSES),
        }
    )


def generate_persistent_space():
    return Dict(
        {
            "health": generate_health_space(),
            "gold": MultiBinary(constants.LOG_MAX_GOLD),
            "potions": MultiDiscrete(
                [constants.NUM_POTIONS] * constants.NUM_POTION_SLOTS
            ),
            # TODO add counters and usages (e.g. lizard tail) to relics
            "relics": MultiBinary(constants.NUM_RELICS),
            "deck": generate_card_space(),
            "keys": MultiBinary(constants.NUM_KEYS),
            "map": generate_map_space(),
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
            "hand": MultiDiscrete(
                [constants.NUM_CARDS_WITH_UPGRADES] * constants.HAND_SIZE
            ),
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
                            "card": MultiBinary(constants.LOG_NUM_CARDS_WITH_UPGRADES),
                            "price": MultiBinary(constants.SHOP_LOG_MAX_PRICE),
                        }
                    )
                ]
                * constants.SHOP_CARD_COUNT,
            ),
            "relics": Tuple(
                [
                    Dict(
                        {
                            "relic": Discrete(constants.NUM_RELICS),
                            "price": MultiBinary(constants.SHOP_LOG_MAX_PRICE),
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
                            "price": MultiBinary(constants.SHOP_LOG_MAX_PRICE),
                        }
                    )
                ]
                * constants.SHOP_POTION_COUNT
            ),
            "purge": Dict(
                {
                    "available": Discrete(2),
                    "price": MultiBinary(constants.SHOP_LOG_MAX_PRICE),
                }
            ),
        }
    )


def generate_campfire_space():
    return Dict(
        {
            "rest": Discrete(2),
            "smith": Discrete(2),
            "lift": Discrete(2),
            "toke": Discrete(2),
            "dig": Discrete(2),
            "recall": Discrete(2),
        }
    )


def generate_card_reward_space():
    return Dict(
        {
            # At most 4 cards may be offered (due to Question Card relic).
            "cards": Tuple(
                (
                    MultiBinary(constants.LOG_NUM_CARDS_WITH_UPGRADES),
                    MultiBinary(constants.LOG_NUM_CARDS_WITH_UPGRADES),
                    MultiBinary(constants.LOG_NUM_CARDS_WITH_UPGRADES),
                    MultiBinary(constants.LOG_NUM_CARDS_WITH_UPGRADES),
                )
            ),
            "singing_bowl": Discrete(2),
            "skippable": Discrete(2),
        }
    )


def generate_combat_reward_space():
    combat_reward_item = Dict(
        {
            "type": Discrete(constants.NUM_REWARD_TYPES),
            # Could be an amount of gold, a relic ID, the color of a key, or a potion ID
            "value": MultiBinary(constants.COMBAT_REWARD_LOG_MAX_ID),
        }
    )
    return Tuple([combat_reward_item] * constants.MAX_NUM_REWARDS)


OBSERVATION_SPACE = Dict(
    {
        "persistent_state": generate_persistent_space(),
        "combat_state": generate_combat_space(),
        "shop_state": generate_shop_space(),
        "campfire_state": generate_campfire_space(),
        "card_reward_state": generate_card_reward_space(),
        "combat_reward_space": generate_combat_reward_space(),
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

        # TODO make selections part of observation space?
        self.hand_selects = []
        self.max_selects = 0
        self.can_pick_zero = False

        if "game_state" in state:
            game_state = state["game_state"]
            if "combat_state" in game_state:
                combat_state = game_state["combat_state"]

                self.turn = combat_state["turn"]

                self.hand = [types.HandCard(**card) for card in combat_state["hand"]]
                self.discard = [
                    types.Card(**card) for card in combat_state["discard_pile"]
                ]
                self.draw = [types.Card(**card) for card in combat_state["draw_pile"]]
                self.exhaust = [
                    types.Card(**card) for card in combat_state["exhaust_pile"]
                ]

                self.enemies = combat_state["monsters"]

                player_state = combat_state["player"]
                self.block = player_state["block"]
                self.energy = player_state["energy"]
                self.effects = player_state["powers"]
                self.orbs = player_state["orbs"]

                if game_state["screen_type"] == "HAND_SELECT":
                    screen_state = game_state["screen_state"]
                    self.hand_selects = screen_state["selected"]
                    self.max_selects = screen_state["max_cards"]
                    self.can_pick_zero = screen_state["can_pick_zero"]

    def _serialize_enemy(self, enemy: Optional[dict]) -> dict:
        if enemy is not None:
            serialized = {
                "id": constants.ALL_MONSTER_TYPES.index(enemy["id"]),
                "intent": constants.ALL_INTENTS.index(enemy["intent"]),
                "block": to_binary_array(enemy["block"], constants.LOG_MAX_BLOCK),
                "effects": _serialize_effects(enemy["powers"]),
                "health": serializers._serialize_health(enemy["current_hp"], enemy["max_hp"]),
            }
        else:
            serialized = {
                "id": 0,
                "intent": 0,
                "block": to_binary_array(0, constants.LOG_MAX_BLOCK),
                "effects": _serialize_effects([]),
                "health": serializers._serialize_health(0, 0),
            }

        return serialized

    def serialize(self) -> dict:
        turn = to_binary_array(self.turn, constants.LOG_MAX_TURN)
        energy = to_binary_array(self.energy, constants.LOG_MAX_ENERGY)
        block = to_binary_array(self.block, constants.LOG_MAX_BLOCK)

        hand = [0] * constants.HAND_SIZE
        for i, card in enumerate(self.hand):
            card_idx = card.serialize_discrete()
            hand[i] = card_idx

        effects = _serialize_effects(self.effects)
        orbs = _serialize_orbs(self.orbs)

        enemies = []
        for i in range(constants.NUM_ENEMIES):
            enemy = None
            if i < len(self.enemies):
                enemy = self.enemies[i]

            enemies.append(self._serialize_enemy(enemy))

        discard = serializers._serialize_cards(self.discard)
        draw = serializers._serialize_cards(self.draw)
        exhaust = serializers._serialize_cards(self.exhaust)

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
        self.purge_price = 0

        if "game_state" in state:
            game_state = state["game_state"]
            if (
                "screen_type" in game_state
                and game_state["screen_type"] == "SHOP_SCREEN"
            ):
                screen_state = game_state["screen_state"]
                self.cards = parse_obj_as(list[types.ShopCard], screen_state["cards"])
                self.relics = parse_obj_as(
                    list[types.ShopRelic], screen_state["relics"]
                )
                self.potions = parse_obj_as(
                    list[types.ShopPotion], screen_state["potions"]
                )
                self.purge_available = screen_state["purge_available"]
                self.purge_price = screen_state["purge_cost"]

    def serialize(self) -> dict:
        serialized_cards = [ShopCard.serialize_empty()] * constants.SHOP_CARD_COUNT
        for i, card in enumerate(self.cards):
            serialized_cards[i] = card.serialize()

        serialized_relics = [
            {
                "relic": 0,
                "price": to_binary_array(0, constants.SHOP_LOG_MAX_PRICE),
            }
        ] * constants.SHOP_RELIC_COUNT
        for i, relic in enumerate(self.relics):
            serialized = {
                "relic": constants.ALL_RELICS.index(relic.id),
                "price": to_binary_array(relic.price, constants.SHOP_LOG_MAX_PRICE),
            }
            serialized_relics[i] = serialized

        serialized_potions = [
            {
                "potion": 0,
                "price": to_binary_array(0, constants.SHOP_LOG_MAX_PRICE),
            }
        ] * constants.SHOP_POTION_COUNT
        for i, potion in enumerate(self.potions):
            serialized = {
                "potion": constants.ALL_POTIONS.index(potion.id),
                "price": to_binary_array(potion.price, constants.SHOP_LOG_MAX_PRICE),
            }
            serialized_potions[i] = serialized

        serialized_purge = {
            "available": int(self.purge_available),
            "price": to_binary_array(self.purge_price, constants.SHOP_LOG_MAX_PRICE),
        }

        return {
            "cards": serialized_cards,
            "relics": serialized_relics,
            "potions": serialized_potions,
            "purge": serialized_purge,
        }


class CampfireStateObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.rest = False
        self.smith = False
        self.lift = False
        self.toke = False
        self.dig = False
        self.recall = False
        self.num_options = 0

        if "game_state" in state:
            game_state = state["game_state"]
            if "screen_type" in game_state and game_state["screen_type"] == "REST":
                screen_state = game_state["screen_state"]
                if screen_state["has_rested"]:
                    return

                rest_options = screen_state["rest_options"]
                possible_options = ["rest", "smith", "lift", "toke", "dig", "recall"]

                for option in possible_options:
                    if option in rest_options:
                        setattr(self, option, True)
                        self.num_options += 1

    def serialize(self) -> dict:
        return {
            "rest": int(self.rest),
            "smith": int(self.smith),
            "lift": int(self.lift),
            "toke": int(self.toke),
            "dig": int(self.dig),
            "recall": int(self.recall),
        }


class CardRewardStateObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.cards = []
        self.singing_bowl = False
        self.skippable = False

        if "game_state" in state:
            game_state = state["game_state"]
            if (
                "screen_type" in game_state
                and game_state["screen_type"] == "CARD_REWARD"
            ):

                screen_state = game_state["screen_state"]
                self.cards = parse_obj_as(list[types.Card], screen_state["cards"])
                self.singing_bowl = screen_state["bowl_available"]
                self.skippable = screen_state["skip_available"]

    def serialize(self) -> dict:
        serialized_cards = [
            types.Card.serialize_empty_binary()
        ] * constants.REWARD_CARD_COUNT
        for i, card in enumerate(self.cards):
            serialized_cards[i] = card.serialize_binary()

        return {
            "cards": serialized_cards,
            "singing_bowl": int(self.singing_bowl),
            "skippable": int(self.skippable),
        }


class CombatRewardState(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.rewards: list[types.Reward] = []

        game_state = state.get("game_state")
        if game_state is None:
            return

        screen_type = game_state.get("screen_type")
        if screen_type is None:
            return

        screen_state = game_state["screen_state"]
        if screen_type == "COMBAT_REWARD":
            self.rewards = [
                self._parse_reward(reward) for reward in screen_state["rewards"]
            ]
        elif screen_type == "BOSS_REWARD":
            self.rewards = [
                types.RelicReward(value=types.Relic(**relic))
                for relic in screen_state["relics"]
            ]

    @staticmethod
    def _parse_reward(reward: dict):
        reward_type = reward["reward_type"]

        if reward_type == "GOLD":
            return types.GoldReward(value=reward["gold"])
        elif reward_type == "POTION":
            potion = types.Potion(**reward["potion"])
            return types.PotionReward(value=potion)
        elif reward_type == "RELIC":
            relic = types.Relic(**reward["relic"])
            return types.RelicReward(value=relic)
        elif reward_type == "CARD":
            return types.CardReward()
        elif reward_type in ["EMERALD_KEY", "SAPPHIRE_KEY"]:
            # TODO is it important to encode the "link" info for the sapphire key?
            key_type = reward_type.split("_")[0]
            return types.KeyReward(value=key_type)
        else:
            raise ValueError(f"Unrecognized reward type {reward_type}")

    def serialize(self) -> list[dict]:
        serialized = [types.Reward.serialize_empty()] * constants.MAX_NUM_REWARDS
        for i, reward in enumerate(self.rewards):
            serialized[i] = reward.serialize()
        return serialized


class Observation:
    def __init__(self, state: dict):
        self.persistent_state = PersistentStateObs(state)
        self.combat_state = CombatStateObs(state)
        self.shop_state = ShopStateObs(state)
        self.campfire_state = CampfireStateObs(state)
        self.card_reward_state = CardRewardStateObs(state)
        self.combat_reward_state = CombatRewardState(state)

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
    def choice_list(self) -> list[str]:
        self.check_for_error()
        if "choose" not in self._available_commands:
            return []

        game_state = self.state.get("game_state")
        if game_state is None:
            return []

        return game_state.get("choice_list", [])

    @property
    def game_over(self) -> bool:
        self.check_for_error()
        return self.screen_type == "GAME_OVER"

    @property
    def in_combat(self) -> bool:
        self.check_for_error()
        if "game_state" not in self.state:
            return False

        return "combat_state" in self.state["game_state"]

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
            "campfire_state": self.campfire_state.serialize(),
            "combat_reward_state": self.combat_reward_state.serialize(),
        }
