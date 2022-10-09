from dataclasses import dataclass, field

from gym.spaces import Dict, MultiBinary, MultiDiscrete
from pydantic import parse_obj_as

from gym_sts.spaces import constants
from gym_sts.spaces.observations import serializers, spaces, types, utils

from .base import ObsComponent
from .map import MapObs


@dataclass
class PersistentStateObs(ObsComponent):
    # Sane defaults
    floor: int = 0
    hp: int = 0
    max_hp: int = 0
    gold: int = 0
    potions: list[types.Potion] = field(default_factory=list)
    relics: list[types.Relic] = field(default_factory=list)
    deck: list[types.Card] = field(default_factory=list)
    keys: dict = field(default_factory=dict)
    map: MapObs = field(default_factory=MapObs)

    # def from_state(state: dict) -> "PersistentStateObs":
        # self = PersistentStateObs()
    def __init__(self, state: dict):
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

            if "keys" in game_state:
                self.keys = game_state["keys"]

        return self

    @classmethod
    def space(cls):
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
