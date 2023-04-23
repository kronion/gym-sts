import math
from enum import Enum


MAX_HP = 999
NUM_FLOORS = 55

LOG_MAX_GOLD = 12
LOG_MAX_HP = math.ceil(math.log(MAX_HP, 2))
LOG_NUM_FLOORS = math.ceil(math.log(NUM_FLOORS, 2))

ALL_KEYS = [
    "EMERALD",
    "RUBY",
    "SAPPHIRE",
]
NUM_KEYS = len(ALL_KEYS)

# I don't know if 15 is enough, I know the card flipping game has at least 12
NUM_CHOICES = 16


class ScreenType(str, Enum):
    EMPTY = "EMPTY"  # Indicates the absence of a screen type
    BOSS_REWARD = "BOSS_REWARD"  # The contents of the boss chest
    CARD_REWARD = "CARD_REWARD"
    CHEST = "CHEST"
    COMBAT_REWARD = "COMBAT_REWARD"
    EVENT = "EVENT"
    FTUE = "FTUE"
    GAME_OVER = "GAME_OVER"
    GRID = "GRID"  # The contents of card piles, e.g. the discard
    HAND_SELECT = "HAND_SELECT"
    MAIN_MENU = "MAIN_MENU"
    MAP = "MAP"
    NONE = "NONE"  # Has several meanings, e.g. combat
    REST = "REST"
    SHOP_ROOM = "SHOP_ROOM"  # The room containing the merchant
    SHOP_SCREEN = "SHOP_SCREEN"  # The actual shopping menu
