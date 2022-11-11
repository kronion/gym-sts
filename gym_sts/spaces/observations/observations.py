import functools

from gym import spaces

from gym_sts.spaces import actions

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
        # TODO: Possibly have Discrete space telling AI what screen it's on
        # (e.g. screen type)
        "valid_action_mask": spaces.MultiBinary(len(actions.ACTIONS)),
    }
)


class Observation:
    def __init__(self, state: dict):
        game_state = state.get("game_state", {})
        try:
            self.persistent_state = components.PersistentStateObs(**game_state)
        except Exception as e:
            breakpoint()
        self.combat_state = components.CombatObs(state)
        self.shop_state = components.ShopObs(state)
        self.campfire_state = components.CampfireObs(state)
        self.card_reward_state = components.CardRewardObs(state)
        self.combat_reward_state = components.CombatRewardObs(state)
        self.event_state = components.EventStateObs(state)

        # Keep a reference to the raw CommunicationMod response
        self.state = state

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
        valid_action_mask = [False] * len(actions.ACTIONS)
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
