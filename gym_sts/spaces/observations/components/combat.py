from __future__ import annotations

from typing import Union

import numpy as np
import numpy.typing as npt
from gym.spaces import Dict, MultiBinary, MultiDiscrete, Tuple
from pydantic import BaseModel

from gym_sts.spaces import old_constants as constants
from gym_sts.spaces.constants.cards import CardCatalog
from gym_sts.spaces.observations import serializers, spaces, types, utils

from .base import ObsComponent


class CombatObs(ObsComponent):
    def __init__(self, state: dict):
        # Sane defaults
        self.turn = 0

        self.hand: list[types.HandCard] = []
        self.discard: list[types.Card] = []
        self.draw: list[types.Card] = []
        self.exhaust: list[types.Card] = []

        self.enemies: list[types.Enemy] = []

        self.energy = 0
        self.block = 0
        self.effects: list[types.Effect] = []
        self.orbs: list[types.Orb] = []

        # TODO make selections part of observation space?
        self.hand_selects = []
        self.max_selects = 0
        self.can_pick_zero = False

        if "combat_state" in state:
            combat_state = state["combat_state"]

            self.turn = combat_state["turn"]

            self.hand = [types.HandCard(**card) for card in combat_state["hand"]]
            self.discard = [types.Card(**card) for card in combat_state["discard_pile"]]
            self.discard.sort()
            self.draw = [types.Card(**card) for card in combat_state["draw_pile"]]
            self.draw.sort()
            self.exhaust = [types.Card(**card) for card in combat_state["exhaust_pile"]]
            self.exhaust.sort()

            self.enemies = [types.Enemy(**enemy) for enemy in combat_state["monsters"]]

            player_state = combat_state["player"]
            self.block = player_state["block"]
            self.energy = player_state["energy"]
            self.effects = [types.Effect(**effect) for effect in player_state["powers"]]
            self.orbs = [types.Orb(**orb) for orb in player_state["orbs"]]

            if state["screen_type"] == constants.ScreenType.HAND_SELECT:
                screen_state = state["screen_state"]
                self.hand_selects = screen_state["selected"]
                self.max_selects = screen_state["max_cards"]
                self.can_pick_zero = screen_state["can_pick_zero"]

    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "turn": MultiBinary(constants.LOG_MAX_TURN),
                "hand": Tuple([types.HandCard.space()] * constants.HAND_SIZE),
                "energy": MultiBinary(constants.LOG_MAX_ENERGY),
                "orbs": MultiDiscrete([constants.NUM_ORBS] * constants.MAX_ORB_SLOTS),
                "block": MultiBinary(constants.LOG_MAX_BLOCK),
                "effects": spaces.generate_effect_space(),
                "enemies": Tuple([types.Enemy.space()] * constants.NUM_ENEMIES),
                "discard": spaces.generate_card_space(),
                "draw": spaces.generate_card_space(),
                "exhaust": spaces.generate_card_space(),
            }
        )

    def serialize(self) -> dict:
        turn = utils.to_binary_array(self.turn, constants.LOG_MAX_TURN)
        energy = utils.to_binary_array(self.energy, constants.LOG_MAX_ENERGY)
        block = utils.to_binary_array(self.block, constants.LOG_MAX_BLOCK)

        hand = [types.HandCard.serialize_empty()] * constants.HAND_SIZE
        for i, card in enumerate(self.hand):
            card_idx = card.serialize()
            hand[i] = card_idx

        effects = types.Effect.serialize_all(self.effects)
        orbs = serializers.serialize_orbs(self.orbs)

        enemies = [types.Enemy.serialize_empty()] * constants.NUM_ENEMIES
        for i, enemy in enumerate(self.enemies):
            enemies[i] = enemy.serialize()

        discard = serializers.serialize_cards(self.discard)
        draw = serializers.serialize_cards(self.draw)
        exhaust = serializers.serialize_cards(self.exhaust)

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

    class SerializedState(BaseModel):
        turn: types.BinaryArray
        hand: list[types.HandCard.SerializedState]
        energy: types.BinaryArray
        block: types.BinaryArray
        effects: list[dict]
        orbs: npt.NDArray[np.uint]
        enemies: list[dict]
        discard: npt.NDArray[np.uint]
        draw: npt.NDArray[np.uint]
        exhaust: npt.NDArray[np.uint]

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> CombatObs:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        # Instantiate with empty data and update attributes individually,
        # rather than trying to recreate CommunicationMod's weird data shape.
        instance = cls({})

        instance.turn = utils.from_binary_array(data.turn)
        instance.energy = utils.from_binary_array(data.energy)
        instance.block = utils.from_binary_array(data.block)

        instance.effects = []
        for effect_idx, e in enumerate(data.effects):
            effect = types.Effect.deserialize(e)
            if effect.amount != 0:
                effect.id = constants.ALL_EFFECTS[effect_idx]
                instance.effects.append(effect)

        instance.orbs = []
        for o in data.orbs:
            orb = types.Orb.deserialize(o)
            if orb.id != "NONE":
                instance.orbs.append(orb)

        instance.enemies = []
        for e in data.enemies:
            enemy = types.Enemy.deserialize(e)
            if enemy.id != "NONE":
                instance.enemies.append(enemy)

        instance.hand = []
        for hc in data.hand:
            hand_card = types.HandCard.deserialize(hc)
            if hand_card.id != CardCatalog.NONE.id:
                instance.hand.append(hand_card)

        instance.discard = []
        for discard_idx, count in enumerate(data.discard):
            discard = types.Card.deserialize(discard_idx)
            if discard.id != CardCatalog.NONE.id:
                for _ in range(count):
                    instance.discard.append(discard)

        instance.draw = []
        for draw_idx, count in enumerate(data.draw):
            draw = types.Card.deserialize(draw_idx)
            if draw.id != CardCatalog.NONE.id:
                for _ in range(count):
                    instance.draw.append(draw)

        instance.exhaust = []
        for exhaust_idx, count in enumerate(data.exhaust):
            exhaust = types.Card.deserialize(exhaust_idx)
            if exhaust.id != CardCatalog.NONE.id:
                for _ in range(count):
                    instance.exhaust.append(exhaust)

        return instance

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CombatObs):
            return False

        attrs = [
            "turn",
            "hand",
            "energy",
            "block",
            "effects",
            "orbs",
            "enemies",
            "discard",
            "draw",
            "exhaust",
        ]

        for attr in attrs:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True
