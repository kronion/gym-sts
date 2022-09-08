import random
from typing import Optional

from gym_sts.spaces import actions
from gym_sts.spaces.observations import Observation


class ActionValidators:
    @staticmethod
    def validate_end_turn(action: actions.EndTurn, observation: Observation) -> bool:
        return "end" in observation._available_commands

    @staticmethod
    def validate_return(action: actions.Return, observation: Observation) -> bool:
        for word in ["cancel", "leave", "return", "skip"]:
            if word in observation._available_commands:
                return True

        return False

    @staticmethod
    def validate_proceed(action: actions.Proceed, observation: Observation) -> bool:
        for word in ["confirm", "proceed"]:
            if word in observation._available_commands:
                return True

        return False

    @staticmethod
    def _validate_choice(action: actions.Choose, observation: Observation) -> bool:
        return action.choice_index < len(observation.choice_list)

    @classmethod
    def validate_choose(cls, action: actions.Choose, observation: Observation) -> bool:
        if "choose" not in observation._available_commands:
            return False

        if observation.in_combat:
            if observation.screen_type == "HAND_SELECT":
                return cls._validate_choice(action, observation)
            else:
                # TODO determine if there are any other choices that could
                # be made mid-combat, such as picking from deck/discard/exhaust,
                # or scrying.
                print("NOT IMPLEMENTED")
                return False
        elif observation.screen_type in [
            "CARD_REWARD",
            "CHEST",
            "COMBAT_REWARD",
            "MAP",
            "REST",
            "SHOP_ROOM",
            "SHOP_SCREEN",
        ]:
            return cls._validate_choice(action, observation)
        else:
            # TODO handle choices outside of combat, like events
            print("NOT IMPLEMENTED")
            return True

    @staticmethod
    def validate_play(action: actions.PlayCard, observation: Observation) -> bool:
        if "play" not in observation._available_commands:
            return False

        if not observation.in_combat or observation.screen_type != "NONE":
            return False

        # Choices correspond to playing cards
        hand = observation.combat_state.hand
        index = action.card_position
        # Adjust to account for CommunicationMod's odd indexing scheme.
        index -= 1
        if index < 0:
            index += 10

        if index >= len(hand):
            return False

        card = hand[index]

        target_index = action.target_index
        if target_index is not None and not card.has_target:
            return False
        if target_index is None and card.has_target:
            return False

        enemies = observation.combat_state.enemies
        if target_index is not None and target_index >= len(enemies):
            return False

        return card.is_playable

    @staticmethod
    def _validate_potion(
        action: actions.PotionAction, observation: Observation, prop: str
    ) -> bool:
        if "potion" not in observation._available_commands:
            return False

        index = action.potion_index
        potions = observation.persistent_state.potions
        if index >= len(potions):
            return False

        potion = potions[index]
        return getattr(potion, prop)

    @classmethod
    def validate_use_potion(
        cls, action: actions.UsePotion, observation: Observation
    ) -> bool:
        if not cls._validate_potion(action, observation, "can_use"):
            return False

        index = action.potion_index
        potions = observation.persistent_state.potions
        potion = potions[index]

        target_index = action.target_index
        if target_index is not None and not potion.requires_target:
            return False
        if target_index is None and potion.requires_target:
            return False

        enemies = observation.combat_state.enemies
        if target_index is not None and target_index >= len(enemies):
            return False

        return True

    @classmethod
    def validate_discard_potion(
        cls, action: actions.DiscardPotion, observation: Observation
    ) -> bool:
        return cls._validate_potion(action, observation, "can_discard")

    @classmethod
    def validate(cls, action: actions.Action, observation: Observation) -> bool:
        if isinstance(action, actions.EndTurn):
            return cls.validate_end_turn(action, observation)

        elif isinstance(action, actions.Return):
            return cls.validate_return(action, observation)

        elif isinstance(action, actions.Proceed):
            return cls.validate_proceed(action, observation)

        elif isinstance(action, actions.Choose):
            return cls.validate_choose(action, observation)

        elif isinstance(action, actions.UsePotion):
            return cls.validate_use_potion(action, observation)

        elif isinstance(action, actions.DiscardPotion):
            return cls.validate_discard_potion(action, observation)

        elif isinstance(action, actions.PlayCard):
            return cls.validate_play(action, observation)

        raise ValueError("Unrecognized action type")


class SeedHelpers:
    char_set = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"  # Note no O

    @classmethod
    def make_seed_str(cls, seed_long: int) -> str:
        """
        Based on code from com/megacrit/cardcrawl/helpers/SeedHelper.java
        """

        base = len(cls.char_set)

        seed_str = ""
        while seed_long != 0:
            seed_long, remainder = divmod(seed_long, base)
            char = cls.char_set[remainder]
            seed_str = char + seed_str

        return seed_str

    @classmethod
    def make_seed(cls, rng: random.Random) -> str:
        unsigned_long = 2**64
        seed_long = rng.randrange(unsigned_long)

        return cls.make_seed_str(seed_long)

    @classmethod
    def validate_seed(cls, seed: str) -> str:
        """
        Returns the seed if it's valid, raises a ValueError otherwise.
        """

        seed = seed.upper()
        for char in seed:
            if char not in cls.char_set:
                raise ValueError(f"Seed contains illegal character '{char}'")

        return seed


class ObservationCache:
    def __init__(self, size: int = 10):
        self.size = size
        self.index = 0
        self.cache: list[Optional[Observation]] = [None] * self.size

    def append(self, obs: Observation):
        self.cache[self.index] = obs
        self.index = (self.index + 1) % self.size

    def get(self, ago: int = 0) -> Optional[Observation]:
        """
        Args:
            ago: The number of observations back to retrieve (zero indexed).
                The value must be less than the cache size.
        """

        if ago >= self.size:
            raise ValueError(f"ago must be less than the cache size ({self.size})")

        index = (self.index - ago - 1) % self.size
        return self.cache[index]

    def reset(self) -> None:
        self.cache = [None] * self.size
