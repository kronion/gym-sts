from __future__ import annotations

import functools
from typing import Union

import numpy as np
from gymnasium import spaces
from pydantic import BaseModel

from gym_sts.spaces import actions
from gym_sts.spaces.constants.base import ScreenType

from . import components


class ObservationError(Exception):
    pass


OBSERVATION_SPACE = spaces.Dict(
    {
        "persistent_state": components.PersistentStateObs.space(),
        "combat_state": components.CombatObs.space(),
        "shop_state": components.ShopObs.space(),
        "campfire_state": components.CampfireObs.space(),
        "card_reward_state": components.CardRewardObs.space(),
        "combat_reward_state": components.CombatRewardObs.space(),
        "event_state": components.EventStateObs.space(),
        "valid_action_mask": spaces.MultiBinary(len(actions.ACTIONS)),
    }
)


class Observation:
    class SerializedState(BaseModel):
        campfire_state: components.CampfireObs.SerializedState
        card_reward_state: components.CardRewardObs.SerializedState
        combat_state: components.CombatObs.SerializedState
        combat_reward_state: components.CombatRewardObs.SerializedState
        persistent_state: components.PersistentStateObs.SerializedState
        shop_state: components.ShopObs.SerializedState

    def __init__(self, state: Union[dict, SerializedState]):
        if isinstance(state, dict):
            game_state = state.get("game_state", {})
            screen_type = game_state.get("screen_type", ScreenType.NONE)
            screen_state = game_state.get("screen_state", {})

            self.persistent_state = components.PersistentStateObs(**game_state)

            self.combat_state = components.CombatObs(game_state)
            self.combat_reward_state = components.CombatRewardObs(game_state)

            shop_state = screen_state if screen_type == ScreenType.SHOP_SCREEN else {}
            self.shop_state = components.ShopObs(**shop_state)

            campfire_state = screen_state if screen_type == ScreenType.REST else {}
            self.campfire_state = components.CampfireObs(**campfire_state)

            card_reward_state = (
                screen_state if screen_type == ScreenType.CARD_REWARD else {}
            )
            self.card_reward_state = components.CardRewardObs(**card_reward_state)

            self.event_state = components.EventStateObs(state)

            # Keep a reference to the raw CommunicationMod response
            self.state = state
        else:
            self.campfire_state = components.CampfireObs.deserialize(
                state.campfire_state
            )
            self.card_reward_state = components.CardRewardObs.deserialize(
                state.card_reward_state
            )
            self.combat_state = components.CombatObs.deserialize(state.combat_state)
            self.combat_reward_state = components.CombatRewardObs.deserialize(
                state.combat_reward_state
            )
            self.persistent_state = components.PersistentStateObs.deserialize(
                state.persistent_state
            )
            self.shop_state = components.ShopObs.deserialize(state.shop_state)

            # TODO this doesn't really work because we assume the keys will be present
            # replace with a pydantic model?
            self.state = {}

    @property
    def has_error(self) -> bool:
        return "error" in self.state

    def check_for_error(self) -> None:
        if self.has_error:
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

    @functools.cached_property
    def valid_actions(self) -> list[actions.Action]:
        # avoid circular import
        from gym_sts.envs.action_validation import get_valid

        return get_valid(self)

    def serialize(self) -> dict:
        valid_action_mask = np.zeros([len(actions.ACTIONS)], dtype=bool)
        for action in self.valid_actions:
            valid_action_mask[action._id] = True

        return {
            "persistent_state": self.persistent_state.serialize(),
            "combat_state": self.combat_state.serialize(),
            "shop_state": self.shop_state.serialize(),
            "campfire_state": self.campfire_state.serialize(),
            "card_reward_state": self.card_reward_state.serialize(),
            "combat_reward_state": self.combat_reward_state.serialize(),
            "event_state": self.event_state.serialize(),
            "valid_action_mask": valid_action_mask,
        }

    @classmethod
    def deserialize(cls, raw_data: dict) -> Observation:
        data = cls.SerializedState(**raw_data)
        return cls(data)
