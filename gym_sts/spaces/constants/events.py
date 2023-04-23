ALL_EVENTS = [
    "NONE",  # Indicates the absence of an event
    "Shining Light",
    "World of Goop",
    "Mushrooms",
    "The Cleric",
    "Dead Adventurer",
    "Living Wall",
    "Big Fish",
    "Liars Game",
    "Scrap Ooze",
    "Golden Wing",
    "Golden Idol",
    "Beggar",
    "Colosseum",
    "The Mausoleum",
    "The Library",
    "Addict",
    "Cursed Tome",
    "The Joust",
    "Forgotten Altar",
    "Masked Bandits",
    "Drug Dealer",
    "Knowing Skull",
    "Back to Basics",
    "Vampires",
    "Nest",
    "Ghosts",
    "Mysterious Sphere",
    "Tomb of Lord Red Mask",
    "SecretPortal",
    "The Moai Head",
    "Spire Heart",
    "SensoryStone",
    "MindBloom",
    "Falling",
    "Winding Halls",
    "Golden Shrine",
    "Accursed Blacksmith",
    "Designer",
    "Fountain of Cleansing",
    "Wheel of Change",
    "Duplicator",
    "The Woman in Blue",
    "Match and Keep!",
    "NoteForYourself",
    "WeMeetAgain",
    "Transmorgrifier",
    "N'loth",
    "Bonfire Elementals",
    "Purifier",
    "Upgrade Shrine",
    "Lab",
    "FaceTrader",
    "Neow Event",
]
NUM_EVENTS = len(ALL_EVENTS)

# Most (if not all) numbers in random events occur in the middle of the text, so spaces
# are enough to match the left word boundary
# It's a feature that the right word boundary is intentionally omitted so e.g. "1" and
# "10" still match "100%"
GLOBALLY_CHECKED_TEXTS = [f" {x}" for x in range(100)]

NUM_GLOBALLY_CHECKED_TEXTS = len(GLOBALLY_CHECKED_TEXTS)
MAX_NUM_CUSTOM_TEXTS = 30
MAX_NUM_TEXTS = MAX_NUM_CUSTOM_TEXTS + NUM_GLOBALLY_CHECKED_TEXTS
