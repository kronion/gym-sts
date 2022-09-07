from abc import ABC, abstractmethod
from typing import Optional

from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete, Tuple
from pydantic import BaseModel, parse_obj_as

from gym_sts.spaces import constants


class Card(BaseModel):
    exhausts: bool
    cost: int
    name: str
    id: str
    ethereal: bool
    upgrades: int
    has_target: bool


class HandCard(Card):
    is_playable: bool


class ShopMixin(BaseModel):
    price: int


class ShopCard(Card, ShopMixin):
    pass


class Potion(BaseModel):
    requires_target: bool
    can_use: bool
    can_discard: bool
    name: str
    id: str


class ShopPotion(Potion, ShopMixin):
    pass


class Relic(BaseModel):
    name: str
    id: str
    counter: int


class ShopRelic(Relic, ShopMixin):
    pass


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
                            "card": Discrete(constants.NUM_CARDS_WITH_UPGRADES),
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
                            "relic": Discrete(constants.NUM_RELICS),
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


def _serialize_card(card: Card) -> int:
    card_idx = constants.ALL_CARDS.index(card.id) * 2
    if card.upgrades > 0:
        card_idx += 1

    return card_idx


def _serialize_cards(cards: list[Card]) -> list[int]:
    # TODO handle Searing Blow, which can be upgraded unlimited times
    serialized = [0] * constants.NUM_CARDS_WITH_UPGRADES
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


class MapStateObs(ObsComponent):
    def __init__(self, state: Optional[dict] = None):
        self.nodes = []
        self.boss = "NONE"

        if state is not None:
            game_state = state["game_state"]
            self.nodes = game_state["map"]
            self.boss = game_state["act_boss"]

    def serialize(self) -> dict:
        empty_node = constants.ALL_MAP_LOCATIONS.index("NONE")
        nodes = [empty_node] * constants.NUM_MAP_NODES
        edges = [0] * constants.NUM_MAP_EDGES

        for node in self.nodes:
            x, y = node["x"], node["y"]
            index = constants.NUM_MAP_NODES_PER_ROW * y + x
            symbol = node["symbol"]

            if symbol == "E":
                # Depends on json field added in our CommunicationMod fork
                if "is_burning" in node and node["is_burning"]:
                    symbol = "B"

            node_type = constants.ALL_MAP_LOCATIONS.index(symbol)
            nodes[index] = node_type

            if y < constants.NUM_MAP_ROWS - 1:
                edge_index = (
                    constants.NUM_MAP_NODES_PER_ROW * y + x
                ) * constants.NUM_MAP_EDGES_PER_NODE

                child_x_coords = [child["x"] for child in node["children"]]

                for coord in [x - 1, x, x + 1]:
                    if coord in child_x_coords:
                        edges[edge_index] = 1
                    edge_index += 1

        boss = constants.NORMAL_BOSSES.index(self.boss)
        return {
            "nodes": nodes,
            "edges": edges,
            "boss": boss,
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
        self.map = MapStateObs()

        if "game_state" in state:
            game_state = state["game_state"]
            self.hp = game_state["current_hp"]
            self.max_hp = game_state["max_hp"]
            self.gold = game_state["gold"]
            self.potions = parse_obj_as(list[Potion], game_state["potions"])
            self.relics = parse_obj_as(list[Relic], game_state["relics"])
            self.deck = parse_obj_as(list[Card], game_state["deck"])
            self.map = MapStateObs(state)

            if "keys" in game_state:
                self.keys = game_state["keys"]

    def serialize(self) -> dict:
        health = _serialize_health(self.hp, self.max_hp)
        gold = to_binary_array(self.gold, constants.LOG_MAX_GOLD)

        potions = [0] * constants.NUM_POTION_SLOTS

        for i, potion in enumerate(self.potions):
            potions[i] = constants.ALL_POTIONS.index(potion.id)

        _relics = [False] * constants.NUM_RELICS
        for relic in self.relics:
            _relics[constants.ALL_RELICS.index(relic.id)] = True
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
            "map": self.map.serialize(),
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

        # TODO make selections part of observation space?
        self.hand_selects = []
        self.max_selects = 0
        self.can_pick_zero = False

        if "game_state" in state:
            game_state = state["game_state"]
            if "combat_state" in game_state:
                combat_state = game_state["combat_state"]

                self.turn = combat_state["turn"]

                self.hand = [HandCard(**card) for card in combat_state["hand"]]
                self.discard = [Card(**card) for card in combat_state["discard_pile"]]
                self.draw = [Card(**card) for card in combat_state["draw_pile"]]
                self.exhaust = [Card(**card) for card in combat_state["exhaust_pile"]]

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

        hand = [0] * constants.HAND_SIZE
        for i, card in enumerate(self.hand):
            card_idx = _serialize_card(card)
            hand[i] = card_idx

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
                self.cards = parse_obj_as(list[ShopCard], screen_state["cards"])
                self.relics = parse_obj_as(list[ShopRelic], screen_state["relics"])
                self.potions = parse_obj_as(list[ShopPotion], screen_state["potions"])
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
                "cost": to_binary_array(card.price, constants.SHOP_LOG_MAX_COST),
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
                "relic": constants.ALL_RELICS.index(relic.id),
                "cost": to_binary_array(relic.price, constants.SHOP_LOG_MAX_COST),
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
                "potion": constants.ALL_POTIONS.index(potion.id),
                "cost": to_binary_array(potion.price, constants.SHOP_LOG_MAX_COST),
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


class Reward(BaseModel, ABC):
    @abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError("Unimplemented")

    @staticmethod
    def serialize_empty():
        return {
            "type": constants.ALL_REWARD_TYPES.index("NONE"),
            "value": to_binary_array(0, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class GoldReward(Reward):
    value: int

    def serialize(self) -> dict:
        return {
            "type": constants.ALL_REWARD_TYPES.index("GOLD"),
            "value": to_binary_array(self.value, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class PotionReward(Reward):
    value: Potion

    def serialize(self) -> dict:
        potion_idx = constants.ALL_POTIONS.index(self.value.id)
        return {
            "type": constants.ALL_REWARD_TYPES.index("POTION"),
            "value": to_binary_array(potion_idx, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class RelicReward(Reward):
    value: Relic

    def serialize(self) -> dict:
        relic_idx = constants.ALL_RELICS.index(self.value.id)
        return {
            "type": constants.ALL_REWARD_TYPES.index("RELIC"),
            "value": to_binary_array(relic_idx, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class CardReward(Reward):
    def serialize(self) -> dict:
        return {
            "type": constants.ALL_REWARD_TYPES.index("CARD"),
            "value": to_binary_array(0, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class KeyReward(Reward):
    value: str

    def serialize(self) -> dict:
        key_idx = constants.ALL_KEYS.index(self.value)
        return {
            "type": constants.ALL_REWARD_TYPES.index("KEY"),
            "value": to_binary_array(key_idx, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class CombatRewardState(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.rewards: list[Reward] = []

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
                RelicReward(value=Relic(**relic)) for relic in screen_state["relics"]
            ]

    @staticmethod
    def _parse_reward(reward: dict):
        reward_type = reward["reward_type"]

        if reward_type == "GOLD":
            return GoldReward(value=reward["gold"])
        elif reward_type == "POTION":
            potion = Potion(**reward["potion"])
            return PotionReward(value=potion)
        elif reward_type == "RELIC":
            relic = Relic(**reward["relic"])
            return RelicReward(value=relic)
        elif reward_type == "CARD":
            return CardReward()
        elif reward_type in ["EMERALD_KEY", "SAPPHIRE_KEY"]:
            # TODO is it important to encode the "link" info for the sapphire key?
            key_type = reward_type.split("_")[0]
            return KeyReward(value=key_type)
        else:
            raise ValueError(f"Unrecognized reward type {reward_type}")

    def serialize(self) -> list[dict]:
        serialized = [Reward.serialize_empty()] * constants.MAX_NUM_REWARDS
        for i, reward in enumerate(self.rewards):
            serialized[i] = reward.serialize()
        return serialized


class Observation:
    def __init__(self, state: dict):
        self.persistent_state = PersistentStateObs(state)
        self.combat_state = CombatStateObs(state)
        self.shop_state = ShopStateObs(state)
        self.campfire_state = CampfireStateObs(state)
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
