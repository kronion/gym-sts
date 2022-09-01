LOG_MAX_HP = 10
LOG_MAX_GOLD = 12
LOG_MAX_ENERGY = 4
LOG_MAX_BLOCK = 10
LOG_MAX_EFFECT = 10
LOG_MAX_TURN = 8

# All cards and relics for mapping purposes
ALL_CARDS = [
    "NONE",  # Indicates the absence of a card
    "Whirlwind",
    "Anger",
    "Feel No Pain",
    "Immolate",
    "Bloodletting",
    "Shockwave",
    "Warcry",
    "Pommel Strike",
    "Impervious",
    "Dark Embrace",
    "Bash",
    "Offering",
    "Demon Form",
    "Searing Blow",
    "Entrench",
    "Uppercut",
    "Limit Break",
    "Flame Barrier",
    "Sever Soul",
    "Rampage",
    "Ghostly Armor",
    "Thunderclap",
    "Seeing Red",
    "True Grit",
    "Brutality",
    "Body Slam",
    "Juggernaut",
    "Carnage",
    "Double Tap",
    "Bludgeon",
    "Berserk",
    "Reaper",
    "Corruption",
    "Combust",
    "Fiend Fire",
    "Rage",
    "Clothesline",
    "Flex",
    "Sentinel",
    "Twin Strike",
    "Evolve",
    "Shrug It Off",
    "Battle Trance",
    "Wild Strike",
    "Heavy Blade",
    "Hemokinesis",
    "Havoc",
    "Cleave",
    "Armaments",
    "Perfected Strike",
    "Clash",
    "Dropkick",
    "Burning Pact",
    "Metallicize",
    "Exhume",
    "Blood for Blood",
    "Rupture",
    "Barricade",
    "Power Through",
    "Headbutt",
    "Fire Breathing",
    "Iron Wave",
    "Intimidate",
    "Sword Boomerang",
    "Spot Weakness",
    "Reckless Charge",
    "Disarm",
    "Infernal Blade",
    "Second Wind",
    "Strike_R",
    "Inflame",
    "Defend_R",
    "Dual Wield",
    "Feed",
    "Pummel",
    "Endless Agony",
    "Eviscerate",
    "Infinite Blades",
    "Backstab",
    "Storm of Steel",
    "Adrenaline",
    "PiercingWail",
    "Malaise",
    "Flying Knee",
    "Heel Hook",
    "Choke",
    "Predator",
    "Footwork",
    "Blade Dance",
    "Terror",
    "Masterful Stab",
    "Reflex",
    "Wraith Form v2",
    "Leg Sweep",
    "Expertise",
    "Neutralize",
    "Cloak And Dagger",
    "A Thousand Cuts",
    "Escape Plan",
    "All Out Attack",
    "Deflect",
    "Sucker Punch",
    "Unload",
    "Grand Finale",
    "Tools of the Trade",
    "Prepared",
    "Die Die Die",
    "Dash",
    "Strike_G",
    "Deadly Poison",
    "Quick Slash",
    "Underhanded Strike",
    "Bouncing Flask",
    "Finisher",
    "Envenom",
    "Backflip",
    "Skewer",
    "Outmaneuver",
    "Venomology",
    "Corpse Explosion",
    "Calculated Gamble",
    "Defend_G",
    "Survivor",
    "Well Laid Plans",
    "Poisoned Stab",
    "Noxious Fumes",
    "Blur",
    "Slice",
    "Dagger Throw",
    "After Image",
    "Tactician",
    "Burst",
    "Setup",
    "Flechettes",
    "Acrobatics",
    "Phantasmal Killer",
    "Riddle With Holes",
    "Catalyst",
    "Dodge and Roll",
    "Night Terror",
    "Bane",
    "Concentrate",
    "Glass Knife",
    "Crippling Poison",
    "Doppelganger",
    "Accuracy",
    "Bullet Time",
    "Distraction",
    "Caltrops",
    "Dagger Spray",
    "Shiv",
    "Safety",
    "Smite",
    "Insight",
    "Expunger",
    "ThroughViolence",
    "Omega",
    "Miracle",
    "Beta",
    "Chill",
    "Hello World",
    "Machine Learning",
    "Heatsinks",
    "Electrodynamics",
    "Tempest",
    "Beam Cell",
    "Sweeping Beam",
    "Multi-Cast",
    "Recycle",
    "Amplify",
    "Zap",
    "Biased Cognition",
    "Fission",
    "Compile Driver",
    "Genetic Algorithm",
    "Conserve Battery",
    "All For One",
    "Defragment",
    "Ball Lightning",
    "Barrage",
    "Redo",
    "Doom and Gloom",
    "Steam Power",
    "Scrape",
    "Darkness",
    "Lockon",
    "Hyperbeam",
    "Rainbow",
    "Chaos",
    "Double Energy",
    "Rebound",
    "Reprogram",
    "Undo",
    "Rip and Tear",
    "Static Discharge",
    "Buffer",
    "Thunder Strike",
    "Coolheaded",
    "Seek",
    "Turbo",
    "White Noise",
    "Glacier",
    "Stack",
    "Leap",
    "Melter",
    "Aggregate",
    "Streamline",
    "Core Surge",
    "Blizzard",
    "Reinforced Body",
    "Self Repair",
    "Reboot",
    "Dualcast",
    "Sunder",
    "Impulse",
    "Creative AI",
    "Loop",
    "Go for the Eyes",
    "Cold Snap",
    "Steam",
    "Hologram",
    "Defend_B",
    "Storm",
    "BootSequence",
    "FTL",
    "Consume",
    "Strike_B",
    "Gash",
    "Meteor Strike",
    "Capacitor",
    "Skim",
    "Force Field",
    "Auto Shields",
    "Fusion",
    "Echo Form",
    "Secret Weapon",
    "Forethought",
    "Deep Breath",
    "Bite",
    "Metamorphosis",
    "Violence",
    "Dark Shackles",
    "Transmutation",
    "Jack Of All Trades",
    "Magnetism",
    "PanicButton",
    "Panacea",
    "Dramatic Entrance",
    "Bandage Up",
    "HandOfGreed",
    "Mayhem",
    "The Bomb",
    "RitualDagger",
    "Impatience",
    "Master of Strategy",
    "Discovery",
    "Good Instincts",
    "Finesse",
    "Secret Technique",
    "Panache",
    "Swift Strike",
    "Mind Blast",
    "Purity",
    "Flash of Steel",
    "J.A.X.",
    "Enlightenment",
    "Sadistic Nature",
    "Blind",
    "Ghostly",
    "Chrysalis",
    "Trip",
    "Apotheosis",
    "Thinking Ahead",
    "Madness",
    "Necronomicurse",
    "Doubt",
    "Normality",
    "Regret",
    "Clumsy",
    "Pain",
    "Shame",
    "Decay",
    "Parasite",
    "Pride",
    "Writhe",
    "CurseOfTheBell",
    "Injury",
    "AscendersBane",
    "FameAndFortune",
    "BecomeAlmighty",
    "Wrath",
    "Calm",
    "LiveForever",
    "Perseverance",
    "Adaptation",
    "FearNoEvil",
    "LikeWater",
    "ForeignInfluence",
    "Discipline",
    "Judgement",
    "PathToVictory",
    "MasterReality",
    "CutThroughFate",
    "SignatureMove",
    "TalkToTheHand",
    "Ragnarok",
    "Omniscience",
    "Prostrate",
    "EmptyBody",
    "LessonLearned",
    "Worship",
    "WheelKick",
    "ReachHeaven",
    "Fasting2",
    "Nirvana",
    "Crescendo",
    "Establishment",
    "Strike_P",
    "Halt",
    "JustLucky",
    "ConjureBlade",
    "SashWhip",
    "DevaForm",
    "InnerPeace",
    "Collect",
    "CrushJoints",
    "Indignation",
    "Consecrate",
    "Eruption",
    "EmptyFist",
    "Vigilance",
    "Study",
    "Meditate",
    "FollowUp",
    "ThirdEye",
    "Wish",
    "Wireheading",
    "WreathOfFlame",
    "BattleHymn",
    "WaveOfTheHand",
    "Unraveling",
    "Scrawl",
    "SandsOfTime",
    "Protect",
    "Blasphemy",
    "SpiritShield",
    "ClearTheMind",
    "Swivel",
    "Tantrum",
    "Alpha",
    "Devotion",
    "Brilliance",
    "MentalFortress",
    "DeusExMachina",
    "Wallop",
    "FlurryOfBlows",
    "Conclude",
    "Defend_P",
    "DeceiveReality",
    "Sanctity",
    "CarveReality",
    "Evaluate",
    "Weave",
    "Vengeance",
    "WindmillStrike",
    "FlyingSleeves",
    "EmptyMind",
    "Vault",
    "Pray",
    "BowlingBash",
    "Serenity",
    "AlwaysMad",
    "Blessed",
    "FlowState",
    "DEPRECATEDFlicker",
    "Truth",
    "Confront",
    "SimmeringRage",
    "Flare",
    "BigBrain",
    "Wisdom",
    "BrillianceAura",
    "Polymath",
    "Calm",
    "DEPRECATEDBalancedViolence",
    "MasterReality",
    "Smile",
    "Punishment",
    "PerfectedForm",
    "PathToVictory",
    "Swipe",
    "Flick",
    "Torrent",
    "Grounded",
    "Wrath",
    "Peace",
    "Nothingness",
    "AwakenedStrike",
    "Survey",
    "SublimeSlice",
    "Experienced",
    "RetreatingHand",
    "TemperTantrum",
    "FlameMastery",
    "CleanseEvil",
    "Contemplate",
    "Metaphysics",
    "Causality",
    "HotHot",
    "Flow",
    "SoothingAura",
    "Condense",
    "Eruption",
    "Mastery",
    "ChallengeAccepted",
    "Retribution",
    "Prediction",
    "Bliss",
    "FuryAura",
    "Clarity",
    "Joy",
    "Fury",
    "CrescentKick",
    "Calm",
    "WardAura",
    "Transcendence",
    "LetFateDecide",
    "AndCarryOn",
    "PalmThatRestrains",
    "StepAndStrike",
    "Introspection",
    "Windup",
    "Stomp",
    "Dazed",
    "Burn",
    "Void",
    "Wound",
    "Slimed",
]

ALL_RELICS = [
    "NONE",  # Indicates the absence of a relic
    "CaptainsWheel",
    "SsserpentHead",
    "Orrery",
    "Nloth's Gift",
    "Mark of the Bloom",
    "Snecko Eye",
    "Brimstone",
    "Astrolabe",
    "Peace Pipe",
    "Thread and Needle",
    "Bloody Idol",
    "Tiny Chest",
    "Incense Burner",
    "Self Forming Clay",
    "Ring of the Snake",
    "Red Circlet",
    "ClockworkSouvenir",
    "Bottled Flame",
    "Burning Blood",
    "InkBottle",
    "Ninja Scroll",
    "War Paint",
    "Pandora's Box",
    "Red Skull",
    "Bag of Preparation",
    "Ice Cream",
    "PrismaticShard",
    "Sling",
    "Gremlin Horn",
    "Inserter",
    "Torii",
    "Sozu",
    "Toolbox",
    "Boot",
    "Vajra",
    "White Beast Statue",
    "Girya",
    "TwistedFunnel",
    "Singing Bowl",
    "Juzu Bracelet",
    "Medical Kit",
    "Eternal Feather",
    "Pen Nib",
    "GremlinMask",
    "Mango",
    "Nilry's Codex",
    "Anchor",
    "Tiny House",
    "Nunchaku",
    "GoldenEye",
    "Unceasing Top",
    "Black Blood",
    "Frozen Eye",
    "Happy Flower",
    "TeardropLocket",
    "Art of War",
    "Mercury Hourglass",
    "Coffee Dripper",
    "Calipers",
    "Frozen Egg 2",
    "Sundial",
    "Bird Faced Urn",
    "CeramicFish",
    "Damaru",
    "StrikeDummy",
    "PureWater",
    "Turnip",
    "CultistMask",
    "Snake Skull",
    "Pocketwatch",
    "Blue Candle",
    "Old Coin",
    "Runic Pyramid",
    "Spirit Poop",
    "VioletLotus",
    "Champion Belt",
    "Omamori",
    "Philosopher's Stone",
    "Runic Capacitor",
    "Yang",
    "Pear",
    "Mark of Pain",
    "Test 4",
    "Bag of Marbles",
    "Orichalcum",
    "Du-Vu Doll",
    "Ornamental Fan",
    "Tingsha",
    "Charon's Ashes",
    "SacredBark",
    "Kunai",
    "HoveringKite",
    "Empty Cage",
    "HornCleat",
    "Discerning Monocle",
    "Darkstone Periapt",
    "Paper Frog",
    "Cracked Core",
    "Symbiotic Virus",
    "HandDrill",
    "Test 3",
    "Meat on the Bone",
    "Shovel",
    "DataDisk",
    "Oddly Smooth Stone",
    "Ancient Tea Set",
    "Bronze Scales",
    "Nuclear Battery",
    "TheAbacus",
    "NeowsBlessing",
    "Whetstone",
    "Membership Card",
    "HolyWater",
    "Letter Opener",
    "Dead Branch",
    "Tough Bandages",
    "Blood Vial",
    "SlaversCollar",
    "Ginger",
    "WarpedTongs",
    "Shuriken",
    "Odd Mushroom",
    "Bottled Lightning",
    "The Specimen",
    "Lee's Waffle",
    "Red Mask",
    "Potion Belt",
    "Regal Pillow",
    "Magic Flower",
    "Test 1",
    "Lizard Tail",
    "Golden Idol",
    "Question Card",
    "Enchiridion",
    "Velvet Choker",
    "Calling Bell",
    "Paper Crane",
    "Centennial Puzzle",
    "MawBank",
    "PreservedInsect",
    "The Courier",
    "Melange",
    "Prayer Wheel",
    "Smiling Mask",
    "Toxic Egg 2",
    "OrangePellets",
    "Test 6",
    "TungstenRod",
    "Pantograph",
    "Circlet",
    "Black Star",
    "Mummified Hand",
    "Ectoplasm",
    "FaceOfCleric",
    "Gambling Chip",
    "Matryoshka",
    "FrozenCore",
    "Bottled Tornado",
    "Cables",
    "DollysMirror",
    "Busted Crown",
    "MutagenicStrength",
    "Test 5",
    "NlothsMask",
    "Runic Dome",
    "Toy Ornithopter",
    "MealTicket",
    "Lantern",
    "Fusion Hammer",
    "WingedGreaves",
    "Emotion Chip",
    "Cursed Key",
    "WristBlade",
    "Strawberry",
    "FossilizedHelix",
    "Dream Catcher",
    "StoneCalendar",
    "Necronomicon",
    "Akabeko",
    "Ring of the Serpent",
    "Runic Cube",
    "CloakClasp",
    "Yin",
    "Dark Core",
    "Derp Rock",
    "Dodecahedron",
    "Chemical X",
    "Cauldron",
    "Strange Spoon",
    "Molten Egg 2",
]

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

ALL_POTIONS = [
    "NONE",  # Indicates the slot does not exist
    "Potion Slot",
    "EntropicBrew",
    "Regen Potion",
    "AttackPotion",
    "SkillPotion",
    "LiquidMemories",
    "SteroidPotion",
    "FairyPotion",
    "Energy Potion",
    "EssenceOfSteel",
    "GamblersBrew",
    "PowerPotion",
    "PotionOfCapacity",
    "DuplicationPotion",
    "BlessingOfTheForge",
    "Swift Potion",
    "CultistPotion",
    "StancePotion",
    "Fruit Juice",
    "LiquidBronze",
    "HeartOfIron",
    "Fire Potion",
    "Ancient Potion",
    "SmokeBomb",
    "Block Potion",
    "BottledMiracle",
    "CunningPotion",
    "FocusPotion",
    "EssenceOfDarkness",
    "GhostInAJar",
    "Explosive Potion",
    "FearPotion",
    "SneckoOil",
    "Poison Potion",
    "DistilledChaos",
    "SpeedPotion",
    "Strength Potion",
    "Weak Potion",
    "Dexterity Potion",
    "ColorlessPotion",
    "Ambrosia",
    "BloodPotion",
    "ElixirPotion",
]
NUM_POTIONS = len(ALL_POTIONS)
NUM_POTION_SLOTS = 5

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
]

ALL_MAP_LOCATIONS = [
    "NONE",  # Indicates the absence of node
    "M",  # Monster
    "?",  # Unknown
    "$",  # Shop
    "E",  # Elite
    "B",  # Burning Elite. Note that this symbol isn't actually used by the game.
    "T",  # Treasure
    "R",  # Rest site
]
NUM_MAP_LOCATIONS = len(ALL_MAP_LOCATIONS)
NUM_MAP_NODES_PER_ROW = 7
NUM_MAP_ROWS = 15
NUM_MAP_NODES = NUM_MAP_NODES_PER_ROW * NUM_MAP_ROWS
NUM_MAP_EDGES_PER_NODE = 3  # Max branching factor from one layer to the next
NUM_MAP_EDGES = NUM_MAP_NODES_PER_ROW * NUM_MAP_EDGES_PER_NODE * (NUM_MAP_ROWS - 1)

NORMAL_BOSSES = [
    "NONE",  # A placeholder for an "empty" observation
    "The Guardian",
    "Hexaghost",
    "Slime Boss",
    "Collector",
    "Automaton",
    "Champ",
    "Awakened One",
    "Time Eater",
    "Donu and Deca",
]
NUM_NORMAL_BOSSES = len(NORMAL_BOSSES)

# I don't know if 15 is enough, I know the card flipping game has at least 12
NUM_CHOICES = 15

# I count 179 relics on the STS wiki, including the Circlet
NUM_RELICS = len(ALL_RELICS)

NUM_ENEMIES = 6

# I really don't know the number of monster types
NUM_MONSTER_TYPES = len(ALL_MONSTER_TYPES)

# I estimate at most 400 excluding upgrades
NUM_CARDS = len(ALL_CARDS)
NUM_CARDS_WITH_UPGRADES = NUM_CARDS * 2

HAND_SIZE = 10

# There's no real limit in the game, but this value greatly impacts the size
# of the observation space.
MAX_COPIES_OF_CARD = 5

NUM_ORBS = len(ALL_ORBS)
MAX_ORB_SLOTS = 10

# Wiki seems to list 108 buffs and debuffs, I may have missed a few
NUM_EFFECTS = len(ALL_EFFECTS)

NUM_KEYS = 3

SHOP_CARD_COUNT = 7
SHOP_RELIC_COUNT = 3
SHOP_POTION_COUNT = 3
SHOP_LOG_MAX_COST = 10
