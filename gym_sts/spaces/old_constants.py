import math
from enum import Enum


NUM_FLOORS = 55
LOG_NUM_FLOORS = math.ceil(math.log(NUM_FLOORS, 2))

LOG_MAX_HP = 10
LOG_MAX_GOLD = 12
LOG_MAX_ENERGY = 4
LOG_MAX_ATTACK = 10
LOG_MAX_ATTACK_TIMES = 5
LOG_MAX_BLOCK = 10
LOG_MAX_EFFECT = 10
LOG_MAX_TURN = 8

ALL_MONSTER_TYPES = [
    "NONE",
    "GremlinNob",
    "GremlinTsundere",
    "FungiBeast",
    "GremlinThief",
    "TheGuardian",
    "FuzzyLouseNormal",
    "GremlinWarrior",
    "Looter",
    "Lagavulin",
    "AcidSlime_L",
    "HexaghostOrb",
    "Hexaghost",
    "SlaverBlue",
    "Sentry",
    "AcidSlime_S",
    "SpikeSlime_S",
    "GremlinWizard",
    "FuzzyLouseDefensive",
    "SpikeSlime_M",
    "AcidSlime_M",
    "Cultist",
    "Apology Slime",
    "SlimeBoss",
    "HexaghostBody",
    "SpikeSlime_L",
    "GremlinFat",
    "SlaverRed",
    "JawWorm",
    "BronzeOrb",
    "BookOfStabbing",
    "TheCollector",
    "Snecko",
    "BanditBear",
    "SlaverBoss",
    "TorchHead",
    "Shelled Parasite",
    "Centurion",
    "Chosen",
    "BronzeAutomaton",
    "Healer",
    "BanditChild",
    "BanditLeader",
    "SphericGuardian",
    "SnakePlant",
    "Champ",
    "Mugger",
    "Byrd",
    "GremlinLeader",
    "Serpent",
    "Darkling",
    "Orb Walker",
    "Donu",
    "Maw",
    "Spiker",
    "AwakenedOne",
    "TimeEater",
    "Repulsor",
    "WrithingMass",
    "Deca",
    "Exploder",
    "Reptomancer",
    "Transient",
    "Nemesis",
    "Dagger",
    "GiantHead",
    "SpireShield",
    "SpireSpear",
    "CorruptHeart",
]

ALL_EFFECTS = [
    "Conserve",
    "Sharp Hide",
    "Evolve",
    "Double Tap",
    "Draw Card",
    "Demon Form",
    "Thorns",
    "Wraith Form v2",
    "Angry",
    "Time Warp",
    "IntangiblePlayer",
    "Ritual",
    "Intangible",
    "Flex",
    "Thievery",
    "Metallicize",
    "Fading",
    "BackAttack",
    "Tools Of The Trade",
    "Unawakened",
    "Entangled",
    "Plated Armor",
    "Regenerate",
    "Choked",
    "Storm",
    "Constricted",
    "Feel No Pain",
    "Dexterity",
    "CorpseExplosionPower",
    "Stasis",
    "Panache",
    "Magnetism",
    "After Image",
    "Nullify Attack",
    "RechargingCore",
    "GrowthPower",
    "Flight",
    "Rebound",
    "Confusion",
    "Mode Shift",
    "Curiosity",
    "Double Damage",
    "Artifact",
    "Berserk",
    "Amplify",
    "Anger",
    "Loop",
    "Creative AI",
    "Next Turn Block",
    "Generic Strength Up Power",
    "Rage",
    "Strength",
    "Curl Up",
    "Thousand Cuts",
    "Equilibrium",
    "Sadistic",
    "Painful Stabs",
    "Flame Barrier",
    "Mayhem",
    "Poison",
    "Regeneration",
    "Dark Embrace",
    "Skill Burn",
    "Weakened",
    "Life Link",
    "Draw Reduction",
    "Juggernaut",
    "Pen Nib",
    "Electro",
    "Fire Breathing",
    "Buffer",
    "Rupture",
    "Malleable",
    "Spore Cloud",
    "Vulnerable",
    "StrikeUp",
    "Night Terror",
    "Collect",
    "BlockReturnPower",
    "DevotionPower",
    "EnergyDownPower",
    "BattleHymn",
    "WrathNextTurnPower",
    "MasterRealityPower",
    "Vault",
    "DevaForm",
    "Controlled",
    "OmnisciencePower",
    "PathToVictoryPower",
    "Study",
    "FreeAttackPower",
    "OmegaPower",
    "AngelForm",
    "Adaptation",
    "Nirvana",
    "WireheadingPower",
    "CannotChangeStancePower",
    "NoSkills",
    "LikeWaterPower",
    "EndTurnDeath",
    "EstablishmentPower",
    "Vigor",
    "WaveOfTheHandPower",
    "Mantra",
    "Lockon",
    "Life Link",
    "TheBomb",
    "Compulsive",
    "Hello",
    "Winter",
    "Split",
    "Shifting",
    "Focus",
    "Phantasmal",
    "Attack Burn",
    "Minion",
    "Noxious Fumes",
    "Envenom",
    "Brutality",
    "NoBlockPower",
    "Burst",
    "EnergizedBlue",
    "Explosive",
    "Bias",
    "DuplicationPower",
    "Corruption",
    "StaticDischarge",
    "Slow",
    "Lightning Mastery",
    "Draw",
    "Combust",
    "Hex",
    "Frail",
    "Surrounded",
    "Heatsink",
    "TimeMazePower",
    "DexLoss",
    "Shackled",
    "Retain Cards",
    "Echo Form",
    "Energized",
    "Repair",
    "No Draw",
    "Invincible",
    "FlickPower",
    "AlwaysMad",
    "HotHot",
    "MasterRealityPower",
    "FlowPower",
    "DisciplinePower",
    "DEPRECATEDCondense",
    "EmotionalTurmoilPower",
    "Grounded",
    "Retribution",
    "Serenity",
    "Mastery",
    "Barricade",
    "Blur",
    "BeatOfDeath",
    "Infinite Blades",
    "Accuracy",
]

ALL_ORBS = [
    "NONE",  # Indicates the slot does not exist
    "Empty",
    "Dark",
    "Frost",
    "Lightning",
    "Plasma",
]

ALL_INTENTS = [
    "NONE",
    "ATTACK",
    "ATTACK_BUFF",
    "ATTACK_DEBUFF",
    "ATTACK_DEFEND",
    "BUFF",
    "DEBUFF",
    "STRONG_DEBUFF",
    "DEBUG",
    "DEFEND",
    "DEFEND_DEBUFF",
    "DEFEND_BUFF",
    "ESCAPE",
    "MAGIC",
    "SLEEP",
    "STUN",
    "UNKNOWN",
]
NUM_INTENTS = len(ALL_INTENTS)

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

ALL_KEYS = [
    "EMERALD",
    "RUBY",
    "SAPPHIRE",
]
NUM_KEYS = len(ALL_KEYS)

# I don't know if 15 is enough, I know the card flipping game has at least 12
NUM_CHOICES = 16

NUM_ENEMIES = 8

# I really don't know the number of monster types
NUM_MONSTER_TYPES = len(ALL_MONSTER_TYPES)

HAND_SIZE = 10

NUM_ORBS = len(ALL_ORBS)
MAX_ORB_SLOTS = 10

# Wiki seems to list 108 buffs and debuffs, I may have missed a few
NUM_EFFECTS = len(ALL_EFFECTS)

SHOP_CARD_COUNT = 7
SHOP_RELIC_COUNT = 3
SHOP_POTION_COUNT = 3
SHOP_LOG_MAX_PRICE = 10


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
