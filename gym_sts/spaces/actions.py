from dataclasses import dataclass

from gym.spaces import Discrete

from gym_sts.spaces import constants


@dataclass
class PickCard:
    card_id: int
    upgraded: bool

    def to_command(self, last_observation):
        # TODO: Finish this
        raise RecursionError("not implemented")


@dataclass
class PlayCardUntargeted:
    card_position: int

    def to_command(self, last_observation):
        return f"PLAY {self.card_position}"


@dataclass
class PlayCardTargeted:
    # NOTE: Card position starts from 1
    card_position: int
    target: int

    def to_command(self, last_observation):
        return f"PLAY {self.card_position} {self.target}"


@dataclass
class UsePotionUntargeted:
    potion_index: int

    def to_command(self, last_observation):
        return f"POTION USE {self.potion_index}"


@dataclass
class UsePotionTargeted:
    potion_index: int
    target_index: int

    def to_command(self):
        return f"POTION USE {self.potion_index} {self.target_index}"


@dataclass
class DiscardPotion:
    potion_index: int

    def to_command(self):
        return f"POTION DISCARD {self.potion_index}"


@dataclass
class Choose:
    choice_index: int

    def to_command(self):
        return f"CHOOSE {self.choice_index}"


@dataclass
class EndTurn:
    def to_command(self):
        return "END"


@dataclass
class Return:
    def to_command(self):
        return "RETURN"


@dataclass
class Proceed:
    def to_command(self):
        return "PROCEED"


def all_actions():
    actions = [EndTurn(), Return(), Proceed()]

    for i in range(constants.NUM_CHOICES):
        actions.append(Choose(i))

    for i in range(constants.NUM_POTION_SLOTS):
        actions.append(UsePotionUntargeted(i))
        actions.append(DiscardPotion(i))
        for j in range(constants.NUM_ENEMIES):
            actions.append(UsePotionTargeted(i, j))

    for i in range(1, constants.HAND_SIZE + 1):
        actions.append(PlayCardUntargeted(i))
        for j in range(constants.NUM_ENEMIES):
            actions.append(PlayCardTargeted(i, j))

    return actions


ACTIONS = all_actions()

ACTION_SPACE = Discrete(len(ACTIONS))
