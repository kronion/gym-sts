from gym.spaces import Dict

from . import components


class ObservationError(Exception):
    pass


OBSERVATION_SPACE = Dict(
    {
        "persistent_state": components.PersistentStateObs.space(),
        "combat_state": components.CombatObs.space(),
        "shop_state": components.ShopObs.space(),
        "campfire_state": components.CampfireObs.space(),
        "card_reward_state": components.CardRewardObs.space(),
        "combat_reward_space": components.CombatRewardObs.space(),
        # TODO: Possibly have Discrete space telling AI what screen it's on
        # (e.g. screen type)
        # TODO: Worry about random events
    }
)


class Observation:
    def __init__(self, state: dict):
        self.persistent_state = components.PersistentStateObs(state)
        self.combat_state = components.CombatObs(state)
        self.shop_state = components.ShopObs(state)
        self.campfire_state = components.CampfireObs(state)
        self.card_reward_state = components.CardRewardObs(state)
        self.combat_reward_state = components.CombatRewardObs(state)

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
