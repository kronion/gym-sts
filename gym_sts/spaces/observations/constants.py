from enum import Enum


class ScreenType(str, Enum):
    # WARNING this enum may not be exhaustive
    CARD_REWARD = "CARD_REWARD"
    CHEST = "CHEST"
    COMBAT_REWARD = "COMBAT_REWARD"
    HAND_SELECT = "HAND_SELECT"
    REST = "REST"
    SHOP_ROOM = "SHOP_ROOM"
    SHOP_SCREEN = "SHOP_SCREEN"
