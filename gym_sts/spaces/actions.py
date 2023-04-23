from abc import ABC, abstractmethod
from typing import Optional

from gym.spaces import Discrete
from pydantic import BaseModel, PrivateAttr

from gym_sts.spaces import old_constants as constants
from gym_sts.spaces.constants import potions as potion_consts


class Action(BaseModel, ABC):
    _id: int = PrivateAttr(-1)

    @abstractmethod
    def to_command(self) -> str:
        raise RuntimeError("not implemented")

    class Config:
        # Allows model instances to be hashable, e.g. they can be added to sets.
        # See https://pydantic-docs.helpmanual.io/usage/model_config/
        frozen = True


class PickCard(Action):
    card_id: int
    upgraded: bool

    def to_command(self):
        # TODO: Finish this
        raise RuntimeError("not implemented")


class PlayCard(Action):
    # NOTE: Card position starts with 1
    card_position: int
    target_index: Optional[int]

    def to_command(self):
        target = "" if self.target_index is None else self.target_index
        return f"PLAY {self.card_position} {target}"


class PotionAction(Action):
    potion_index: int


class UsePotion(PotionAction):
    target_index: Optional[int] = None

    def to_command(self):
        target = "" if self.target_index is None else self.target_index
        return f"POTION USE {self.potion_index} {target}"


class DiscardPotion(PotionAction):
    def to_command(self):
        return f"POTION DISCARD {self.potion_index}"


class Choose(Action):
    choice_index: int

    def to_command(self):
        return f"CHOOSE {self.choice_index}"


class EndTurn(Action):
    def to_command(self):
        return "END"


class Return(Action):
    def to_command(self):
        return "RETURN"


class Proceed(Action):
    def to_command(self):
        return "PROCEED"


def all_actions() -> list[Action]:
    actions = [EndTurn(), Return(), Proceed()]

    for i in range(constants.NUM_CHOICES):
        actions.append(Choose(choice_index=i))

    for i in range(potion_consts.NUM_POTION_SLOTS):
        actions.append(UsePotion(potion_index=i))
        actions.append(DiscardPotion(potion_index=i))
        for j in range(constants.NUM_ENEMIES):
            actions.append(UsePotion(potion_index=i, target_index=j))

    for i in range(1, constants.HAND_SIZE + 1):
        actions.append(PlayCard(card_position=i))
        for j in range(constants.NUM_ENEMIES):
            actions.append(PlayCard(card_position=i, target_index=j))

    for i, action in enumerate(actions):
        action._id = i

    return actions


ACTIONS = all_actions()
ACTION_SPACE = Discrete(len(ACTIONS))
