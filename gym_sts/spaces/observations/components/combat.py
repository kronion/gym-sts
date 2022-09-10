from typing import Optional

from gym_sts.spaces import constants
from gym_sts.spaces.observations import serializers, types, utils

from .base import ObsComponent


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
                "block": utils.to_binary_array(enemy["block"], constants.LOG_MAX_BLOCK),
                "effects": serializers.serialize_effects(enemy["powers"]),
                "health": serializers.serialize_health(
                    enemy["current_hp"], enemy["max_hp"]
                ),
            }
        else:
            serialized = {
                "id": 0,
                "intent": 0,
                "block": utils.to_binary_array(0, constants.LOG_MAX_BLOCK),
                "effects": serializers.serialize_effects([]),
                "health": serializers.serialize_health(0, 0),
            }

        return serialized

    def serialize(self) -> dict:
        turn = utils.to_binary_array(self.turn, constants.LOG_MAX_TURN)
        energy = utils.to_binary_array(self.energy, constants.LOG_MAX_ENERGY)
        block = utils.to_binary_array(self.block, constants.LOG_MAX_BLOCK)

        hand = [0] * constants.HAND_SIZE
        for i, card in enumerate(self.hand):
            card_idx = card.serialize_discrete()
            hand[i] = card_idx

        effects = serializers.serialize_effects(self.effects)
        orbs = serializers.serialize_orbs(self.orbs)

        enemies = []
        for i in range(constants.NUM_ENEMIES):
            enemy = None
            if i < len(self.enemies):
                enemy = self.enemies[i]

            enemies.append(self._serialize_enemy(enemy))

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
