from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete, Tuple

from gym_sts.spaces import constants

from . import components


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


class Observation:
    def __init__(self, state: dict):
        self.persistent_state = components.PersistentStateObs(state)
        self.combat_state = components.CombatStateObs(state)
        self.shop_state = components.ShopStateObs(state)
        self.campfire_state = components.CampfireStateObs(state)
        self.card_reward_state = components.CardRewardStateObs(state)
        self.combat_reward_state = components.CombatRewardState(state)

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
