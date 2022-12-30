import math
from enum import IntEnum

from .potions import NUM_POTIONS
from .relics import NUM_RELICS


class RewardType(IntEnum):
    NONE = 0  # An empty reward slot
    CARD = 1
    GOLD = 2
    KEY = 3
    POTION = 4
    RELIC = 5


NUM_REWARD_TYPES = len(RewardType)

REWARD_CARD_COUNT = 4  # Default of 3, +1 for Question Card

# Boss gold reward max * golden idol bonus * buffer in case I'm wrong
_COMBAT_REWARD_MAX_GOLD = int(105 * 1.25 * 1.25)
_COMBAT_REWARD_MAX_POTION = NUM_POTIONS
_COMBAT_REWARD_MAX_RELIC = NUM_RELICS
_COMBAT_REWARD_MAX_ID = max(
    _COMBAT_REWARD_MAX_GOLD, _COMBAT_REWARD_MAX_POTION, _COMBAT_REWARD_MAX_RELIC
)
COMBAT_REWARD_LOG_MAX_ID = math.ceil(math.log(_COMBAT_REWARD_MAX_ID, 2))

# (Card + gold + potion + 2 relics (black star) + key) * buffer in case I'm wrong
MAX_NUM_REWARDS = int((1 + 1 + 1 + 2 + 1) * 1.25)
