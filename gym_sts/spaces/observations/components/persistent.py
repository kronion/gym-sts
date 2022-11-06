from gym.spaces import Dict, Discrete, MultiBinary, MultiDiscrete
from pydantic import parse_obj_as

from gym_sts.spaces import constants
from gym_sts.spaces.observations import serializers, spaces, types, utils

from .base import ObsComponent
from .map import MapObs


class PersistentStateObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.floor = 0
        self.hp = 0
        self.max_hp = 0
        self.gold = 0
        self.potions = []
        self.relics = []
        self.deck = []
        self.keys = {}
        self.map = MapObs()
        self.screen_type = "EMPTY"

        if "game_state" in state:
            game_state = state["game_state"]
            self.floor = game_state["floor"]
            self.hp = game_state["current_hp"]
            self.max_hp = game_state["max_hp"]
            self.gold = game_state["gold"]
            self.potions = parse_obj_as(list[types.Potion], game_state["potions"])
            self.relics = parse_obj_as(list[types.Relic], game_state["relics"])
            self.deck = parse_obj_as(list[types.Card], game_state["deck"])
            self.map = MapObs(state)
            self.screen_type = game_state["screen_type"]

            if "keys" in game_state:
                self.keys = game_state["keys"]

    @staticmethod
    def space():
        return Dict(
            {
                "health": spaces.generate_health_space(),
                "gold": MultiBinary(constants.LOG_MAX_GOLD),
                "potions": MultiDiscrete(
                    [constants.NUM_POTIONS] * constants.NUM_POTION_SLOTS
                ),
                # TODO add counters and usages (e.g. lizard tail) to relics
                "relics": MultiBinary(constants.NUM_RELICS),
                "deck": spaces.generate_card_space(),
                "keys": MultiBinary(constants.NUM_KEYS),
                "map": MapObs.space(),
                "screen_type": Discrete(len(constants.ALL_SCREEN_TYPES)),
            }
        )

    def serialize(self) -> dict:
        health = serializers.serialize_health(self.hp, self.max_hp)
        gold = utils.to_binary_array(self.gold, constants.LOG_MAX_GOLD)

        potions = [0] * constants.NUM_POTION_SLOTS

        for i, potion in enumerate(self.potions):
            potions[i] = constants.ALL_POTIONS.index(potion.id)

        _relics = [False] * constants.NUM_RELICS
        for relic in self.relics:
            _relics[constants.ALL_RELICS.index(relic.id)] = True
        relics = [int(relic) for relic in _relics]

        deck = serializers.serialize_cards(self.deck)

        _keys = [False] * constants.NUM_KEYS
        for i, key in enumerate(["ruby", "emerald", "sapphire"]):
            if key in self.keys:
                _keys[i] = self.keys[key]
        keys = [int(key) for key in _keys]

        screen_type = constants.ALL_SCREEN_TYPES.index(self.screen_type)

        response = {
            "health": health,
            "gold": gold,
            "potions": potions,
            "relics": relics,
            "deck": deck,
            "keys": keys,
            "map": self.map.serialize(),
            "screen_type": screen_type,
        }

        return response
