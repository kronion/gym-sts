import math

from pydantic import BaseModel


class RelicMetadata(BaseModel):
    id: str
    name: str


class _RelicCatalog:
    _id_to_meta = {
        # Indicates the absence of a relic
        "NONE": RelicMetadata(
            id="NONE",
            name="NONE",
        ),
        "CaptainsWheel": RelicMetadata(
            id="CaptainsWheel",
            name="Captain's Wheel",
        ),
        "SsserpentHead": RelicMetadata(
            id="SsserpentHead",
            name="Ssserpent Head",
        ),
        "Orrery": RelicMetadata(
            id="Orrery",
            name="Orrery",
        ),
        "Nloth's Gift": RelicMetadata(
            id="Nloth's Gift",
            name="N'loth's Gift",
        ),
        "Mark of the Bloom": RelicMetadata(
            id="Mark of the Bloom",
            name="Mark of the Bloom",
        ),
        "Snecko Eye": RelicMetadata(
            id="Snecko Eye",
            name="Snecko Eye",
        ),
        "Brimstone": RelicMetadata(
            id="Brimstone",
            name="Brimstone",
        ),
        "Astrolabe": RelicMetadata(
            id="Astrolabe",
            name="Astrolabe",
        ),
        "Peace Pipe": RelicMetadata(
            id="Peace Pipe",
            name="Peace Pipe",
        ),
        "Thread and Needle": RelicMetadata(
            id="Thread and Needle",
            name="Thread and Needle",
        ),
        "Bloody Idol": RelicMetadata(
            id="Bloody Idol",
            name="Bloody Idol",
        ),
        "Tiny Chest": RelicMetadata(
            id="Tiny Chest",
            name="Tiny Chest",
        ),
        "Incense Burner": RelicMetadata(
            id="Incense Burner",
            name="Incense Burner",
        ),
        "Self Forming Clay": RelicMetadata(
            id="Self Forming Clay",
            name="Self-Forming Clay",
        ),
        "Ring of the Snake": RelicMetadata(
            id="Ring of the Snake",
            name="Ring of the Snake",
        ),
        "ClockworkSouvenir": RelicMetadata(
            id="ClockworkSouvenir",
            name="Clockwork Souvenir",
        ),
        "Bottled Flame": RelicMetadata(
            id="Bottled Flame",
            name="Bottled Flame",
        ),
        "Burning Blood": RelicMetadata(
            id="Burning Blood",
            name="Burning Blood",
        ),
        "InkBottle": RelicMetadata(
            id="InkBottle",
            name="Ink Bottle",
        ),
        "Ninja Scroll": RelicMetadata(
            id="Ninja Scroll",
            name="Ninja Scroll",
        ),
        "War Paint": RelicMetadata(
            id="War Paint",
            name="War Paint",
        ),
        "Pandora's Box": RelicMetadata(
            id="Pandora's Box",
            name="Pandora's Box",
        ),
        "Red Skull": RelicMetadata(
            id="Red Skull",
            name="Red Skull",
        ),
        "Bag of Preparation": RelicMetadata(
            id="Bag of Preparation",
            name="Bag of Preparation",
        ),
        "Ice Cream": RelicMetadata(
            id="Ice Cream",
            name="Ice Cream",
        ),
        "PrismaticShard": RelicMetadata(
            id="PrismaticShard",
            name="Prismatic Shard",
        ),
        "Sling": RelicMetadata(
            id="Sling",
            name="Sling of Courage",
        ),
        "Gremlin Horn": RelicMetadata(
            id="Gremlin Horn",
            name="Gremlin Horn",
        ),
        "Inserter": RelicMetadata(
            id="Inserter",
            name="Inserter",
        ),
        "Torii": RelicMetadata(
            id="Torii",
            name="Torii",
        ),
        "Sozu": RelicMetadata(
            id="Sozu",
            name="Sozu",
        ),
        "Toolbox": RelicMetadata(
            id="Toolbox",
            name="Toolbox",
        ),
        "Boot": RelicMetadata(
            id="Boot",
            name="The Boot",
        ),
        "Vajra": RelicMetadata(
            id="Vajra",
            name="Vajra",
        ),
        "White Beast Statue": RelicMetadata(
            id="White Beast Statue",
            name="White Beast Statue",
        ),
        "Girya": RelicMetadata(
            id="Girya",
            name="Girya",
        ),
        "TwistedFunnel": RelicMetadata(
            id="TwistedFunnel",
            name="Twisted Funnel",
        ),
        "Singing Bowl": RelicMetadata(
            id="Singing Bowl",
            name="Singing Bowl",
        ),
        "Juzu Bracelet": RelicMetadata(
            id="Juzu Bracelet",
            name="Juzu Bracelet",
        ),
        "Medical Kit": RelicMetadata(
            id="Medical Kit",
            name="Medical Kit",
        ),
        "Eternal Feather": RelicMetadata(
            id="Eternal Feather",
            name="Eternal Feather",
        ),
        "Pen Nib": RelicMetadata(
            id="Pen Nib",
            name="Pen Nib",
        ),
        "GremlinMask": RelicMetadata(
            id="GremlinMask",
            name="Gremlin Visage",
        ),
        "Mango": RelicMetadata(
            id="Mango",
            name="Mango",
        ),
        "Nilry's Codex": RelicMetadata(
            id="Nilry's Codex",
            name="Nilry's Codex",
        ),
        "Anchor": RelicMetadata(
            id="Anchor",
            name="Anchor",
        ),
        "Tiny House": RelicMetadata(
            id="Tiny House",
            name="Tiny House",
        ),
        "Nunchaku": RelicMetadata(
            id="Nunchaku",
            name="Nunchaku",
        ),
        "GoldenEye": RelicMetadata(
            id="GoldenEye",
            name="Golden Eye",
        ),
        "Unceasing Top": RelicMetadata(
            id="Unceasing Top",
            name="Unceasing Top",
        ),
        "Black Blood": RelicMetadata(
            id="Black Blood",
            name="Black Blood",
        ),
        "Frozen Eye": RelicMetadata(
            id="Frozen Eye",
            name="Frozen Eye",
        ),
        "Happy Flower": RelicMetadata(
            id="Happy Flower",
            name="Happy Flower",
        ),
        "TeardropLocket": RelicMetadata(
            id="TeardropLocket",
            name="Teardrop Locket",
        ),
        "Art of War": RelicMetadata(
            id="Art of War",
            name="Art of War",
        ),
        "Mercury Hourglass": RelicMetadata(
            id="Mercury Hourglass",
            name="Mercury Hourglass",
        ),
        "Coffee Dripper": RelicMetadata(
            id="Coffee Dripper",
            name="Coffee Dripper",
        ),
        "Calipers": RelicMetadata(
            id="Calipers",
            name="Calipers",
        ),
        "Frozen Egg 2": RelicMetadata(
            id="Frozen Egg 2",
            name="Frozen Egg",
        ),
        "Sundial": RelicMetadata(
            id="Sundial",
            name="Sundial",
        ),
        "Bird Faced Urn": RelicMetadata(
            id="Bird Faced Urn",
            name="Bird-Faced Urn",
        ),
        "CeramicFish": RelicMetadata(
            id="CeramicFish",
            name="Ceramic Fish",
        ),
        "Damaru": RelicMetadata(
            id="Damaru",
            name="Damaru",
        ),
        "StrikeDummy": RelicMetadata(
            id="StrikeDummy",
            name="Strike Dummy",
        ),
        "PureWater": RelicMetadata(
            id="PureWater",
            name="Pure Water",
        ),
        "Turnip": RelicMetadata(
            id="Turnip",
            name="Turnip",
        ),
        "CultistMask": RelicMetadata(
            id="CultistMask",
            name="Cultist Headpiece",
        ),
        "Snake Skull": RelicMetadata(
            id="Snake Skull",
            name="Snecko Skull",
        ),
        "Pocketwatch": RelicMetadata(
            id="Pocketwatch",
            name="Pocketwatch",
        ),
        "Blue Candle": RelicMetadata(
            id="Blue Candle",
            name="Blue Candle",
        ),
        "Old Coin": RelicMetadata(
            id="Old Coin",
            name="Old Coin",
        ),
        "Runic Pyramid": RelicMetadata(
            id="Runic Pyramid",
            name="Runic Pyramid",
        ),
        "Spirit Poop": RelicMetadata(
            id="Spirit Poop",
            name="Spirit Poop",
        ),
        "VioletLotus": RelicMetadata(
            id="VioletLotus",
            name="Violet Lotus",
        ),
        "Champion Belt": RelicMetadata(
            id="Champion Belt",
            name="Champion Belt",
        ),
        "Omamori": RelicMetadata(
            id="Omamori",
            name="Omamori",
        ),
        "Philosopher's Stone": RelicMetadata(
            id="Philosopher's Stone",
            name="Philosopher's Stone",
        ),
        "Runic Capacitor": RelicMetadata(
            id="Runic Capacitor",
            name="Runic Capacitor",
        ),
        "Yang": RelicMetadata(
            id="Yang",
            name="Duality",
        ),
        "Pear": RelicMetadata(
            id="Pear",
            name="Pear",
        ),
        "Mark of Pain": RelicMetadata(
            id="Mark of Pain",
            name="Mark of Pain",
        ),
        "Bag of Marbles": RelicMetadata(
            id="Bag of Marbles",
            name="Bag of Marbles",
        ),
        "Orichalcum": RelicMetadata(
            id="Orichalcum",
            name="Orichalcum",
        ),
        "Du-Vu Doll": RelicMetadata(
            id="Du-Vu Doll",
            name="Du-Vu Doll",
        ),
        "Ornamental Fan": RelicMetadata(
            id="Ornamental Fan",
            name="Ornamental Fan",
        ),
        "Tingsha": RelicMetadata(
            id="Tingsha",
            name="Tingsha",
        ),
        "Charon's Ashes": RelicMetadata(
            id="Charon's Ashes",
            name="Charon's Ashes",
        ),
        "SacredBark": RelicMetadata(
            id="SacredBark",
            name="Sacred Bark",
        ),
        "Kunai": RelicMetadata(
            id="Kunai",
            name="Kunai",
        ),
        "HoveringKite": RelicMetadata(
            id="HoveringKite",
            name="Hovering Kite",
        ),
        "Empty Cage": RelicMetadata(
            id="Empty Cage",
            name="Empty Cage",
        ),
        "HornCleat": RelicMetadata(
            id="HornCleat",
            name="Horn Cleat",
        ),
        "Darkstone Periapt": RelicMetadata(
            id="Darkstone Periapt",
            name="Darkstone Periapt",
        ),
        "Paper Frog": RelicMetadata(
            id="Paper Frog",
            name="Paper Phrog",
        ),
        "Cracked Core": RelicMetadata(
            id="Cracked Core",
            name="Cracked Core",
        ),
        "Symbiotic Virus": RelicMetadata(
            id="Symbiotic Virus",
            name="Symbiotic Virus",
        ),
        "HandDrill": RelicMetadata(
            id="HandDrill",
            name="Hand Drill",
        ),
        "Meat on the Bone": RelicMetadata(
            id="Meat on the Bone",
            name="Meat on the Bone",
        ),
        "Shovel": RelicMetadata(
            id="Shovel",
            name="Shovel",
        ),
        "DataDisk": RelicMetadata(
            id="DataDisk",
            name="Data Disk",
        ),
        "Oddly Smooth Stone": RelicMetadata(
            id="Oddly Smooth Stone",
            name="Oddly Smooth Stone",
        ),
        "Ancient Tea Set": RelicMetadata(
            id="Ancient Tea Set",
            name="Ancient Tea Set",
        ),
        "Bronze Scales": RelicMetadata(
            id="Bronze Scales",
            name="Bronze Scales",
        ),
        "Nuclear Battery": RelicMetadata(
            id="Nuclear Battery",
            name="Nuclear Battery",
        ),
        "TheAbacus": RelicMetadata(
            id="TheAbacus",
            name="The Abacus",
        ),
        "NeowsBlessing": RelicMetadata(
            id="NeowsBlessing",
            name="Neow's Lament",
        ),
        "Whetstone": RelicMetadata(
            id="Whetstone",
            name="Whetstone",
        ),
        "Membership Card": RelicMetadata(
            id="Membership Card",
            name="Membership Card",
        ),
        "HolyWater": RelicMetadata(
            id="HolyWater",
            name="Holy Water",
        ),
        "Letter Opener": RelicMetadata(
            id="Letter Opener",
            name="Letter Opener",
        ),
        "Dead Branch": RelicMetadata(
            id="Dead Branch",
            name="Dead Branch",
        ),
        "Tough Bandages": RelicMetadata(
            id="Tough Bandages",
            name="Tough Bandages",
        ),
        "Blood Vial": RelicMetadata(
            id="Blood Vial",
            name="Blood Vial",
        ),
        "SlaversCollar": RelicMetadata(
            id="SlaversCollar",
            name="Slaver's Collar",
        ),
        "Ginger": RelicMetadata(
            id="Ginger",
            name="Ginger",
        ),
        "WarpedTongs": RelicMetadata(
            id="WarpedTongs",
            name="Warped Tongs",
        ),
        "Shuriken": RelicMetadata(
            id="Shuriken",
            name="Shuriken",
        ),
        "Odd Mushroom": RelicMetadata(
            id="Odd Mushroom",
            name="Odd Mushroom",
        ),
        "Bottled Lightning": RelicMetadata(
            id="Bottled Lightning",
            name="Bottled Lightning",
        ),
        "The Specimen": RelicMetadata(
            id="The Specimen",
            name="The Specimen",
        ),
        "Lee's Waffle": RelicMetadata(
            id="Lee's Waffle",
            name="Lee's Waffle",
        ),
        "Red Mask": RelicMetadata(
            id="Red Mask",
            name="Red Mask",
        ),
        "Potion Belt": RelicMetadata(
            id="Potion Belt",
            name="Potion Belt",
        ),
        "Regal Pillow": RelicMetadata(
            id="Regal Pillow",
            name="Regal Pillow",
        ),
        "Magic Flower": RelicMetadata(
            id="Magic Flower",
            name="Magic Flower",
        ),
        "Lizard Tail": RelicMetadata(
            id="Lizard Tail",
            name="Lizard Tail",
        ),
        "Golden Idol": RelicMetadata(
            id="Golden Idol",
            name="Golden Idol",
        ),
        "Question Card": RelicMetadata(
            id="Question Card",
            name="Question Card",
        ),
        "Enchiridion": RelicMetadata(
            id="Enchiridion",
            name="Enchiridion",
        ),
        "Velvet Choker": RelicMetadata(
            id="Velvet Choker",
            name="Velvet Choker",
        ),
        "Calling Bell": RelicMetadata(
            id="Calling Bell",
            name="Calling Bell",
        ),
        "Paper Crane": RelicMetadata(
            id="Paper Crane",
            name="Paper Krane",
        ),
        "Centennial Puzzle": RelicMetadata(
            id="Centennial Puzzle",
            name="Centennial Puzzle",
        ),
        "MawBank": RelicMetadata(
            id="MawBank",
            name="Maw Bank",
        ),
        "PreservedInsect": RelicMetadata(
            id="PreservedInsect",
            name="Preserved Insect",
        ),
        "The Courier": RelicMetadata(
            id="The Courier",
            name="The Courier",
        ),
        "Melange": RelicMetadata(
            id="Melange",
            name="Melange",
        ),
        "Prayer Wheel": RelicMetadata(
            id="Prayer Wheel",
            name="Prayer Wheel",
        ),
        "Smiling Mask": RelicMetadata(
            id="Smiling Mask",
            name="Smiling Mask",
        ),
        "Toxic Egg 2": RelicMetadata(
            id="Toxic Egg 2",
            name="Toxic Egg",
        ),
        "OrangePellets": RelicMetadata(
            id="OrangePellets",
            name="Orange Pellets",
        ),
        "TungstenRod": RelicMetadata(
            id="TungstenRod",
            name="Tungsten Rod",
        ),
        "Pantograph": RelicMetadata(
            id="Pantograph",
            name="Pantograph",
        ),
        "Circlet": RelicMetadata(
            id="Circlet",
            name="Circlet",
        ),
        "Black Star": RelicMetadata(
            id="Black Star",
            name="Black Star",
        ),
        "Mummified Hand": RelicMetadata(
            id="Mummified Hand",
            name="Mummified Hand",
        ),
        "Ectoplasm": RelicMetadata(
            id="Ectoplasm",
            name="Ectoplasm",
        ),
        "FaceOfCleric": RelicMetadata(
            id="FaceOfCleric",
            name="Face Of Cleric",
        ),
        "Gambling Chip": RelicMetadata(
            id="Gambling Chip",
            name="Gambling Chip",
        ),
        "Matryoshka": RelicMetadata(
            id="Matryoshka",
            name="Matryoshka",
        ),
        "FrozenCore": RelicMetadata(
            id="FrozenCore",
            name="Frozen Core",
        ),
        "Bottled Tornado": RelicMetadata(
            id="Bottled Tornado",
            name="Bottled Tornado",
        ),
        "Cables": RelicMetadata(
            id="Cables",
            name="Gold-Plated Cables",
        ),
        "DollysMirror": RelicMetadata(
            id="DollysMirror",
            name="Dolly's Mirror",
        ),
        "Busted Crown": RelicMetadata(
            id="Busted Crown",
            name="Busted Crown",
        ),
        "MutagenicStrength": RelicMetadata(
            id="MutagenicStrength",
            name="Mutagenic Strength",
        ),
        "NlothsMask": RelicMetadata(
            id="NlothsMask",
            name="N'loth's Hungry Face",
        ),
        "Runic Dome": RelicMetadata(
            id="Runic Dome",
            name="Runic Dome",
        ),
        "Toy Ornithopter": RelicMetadata(
            id="Toy Ornithopter",
            name="Toy Ornithopter",
        ),
        "MealTicket": RelicMetadata(
            id="MealTicket",
            name="Meal Ticket",
        ),
        "Lantern": RelicMetadata(
            id="Lantern",
            name="Lantern",
        ),
        "Fusion Hammer": RelicMetadata(
            id="Fusion Hammer",
            name="Fusion Hammer",
        ),
        "WingedGreaves": RelicMetadata(
            id="WingedGreaves",
            name="Wing Boots",
        ),
        "Emotion Chip": RelicMetadata(
            id="Emotion Chip",
            name="Emotion Chip",
        ),
        "Cursed Key": RelicMetadata(
            id="Cursed Key",
            name="Cursed Key",
        ),
        "WristBlade": RelicMetadata(
            id="WristBlade",
            name="Wrist Blade",
        ),
        "Strawberry": RelicMetadata(
            id="Strawberry",
            name="Strawberry",
        ),
        "FossilizedHelix": RelicMetadata(
            id="FossilizedHelix",
            name="Fossilized Helix",
        ),
        "Dream Catcher": RelicMetadata(
            id="Dream Catcher",
            name="Dream Catcher",
        ),
        "StoneCalendar": RelicMetadata(
            id="StoneCalendar",
            name="Stone Calendar",
        ),
        "Necronomicon": RelicMetadata(
            id="Necronomicon",
            name="Necronomicon",
        ),
        "Akabeko": RelicMetadata(
            id="Akabeko",
            name="Akabeko",
        ),
        "Ring of the Serpent": RelicMetadata(
            id="Ring of the Serpent",
            name="Ring of the Serpent",
        ),
        "Runic Cube": RelicMetadata(
            id="Runic Cube",
            name="Runic Cube",
        ),
        "CloakClasp": RelicMetadata(
            id="CloakClasp",
            name="Cloak Clasp",
        ),
        "Chemical X": RelicMetadata(
            id="Chemical X",
            name="Chemical X",
        ),
        "Cauldron": RelicMetadata(
            id="Cauldron",
            name="Cauldron",
        ),
        "Strange Spoon": RelicMetadata(
            id="Strange Spoon",
            name="Strange Spoon",
        ),
        "Molten Egg 2": RelicMetadata(
            id="Molten Egg 2",
            name="Molten Egg",
        ),
    }

    def __getattr__(self, attr):
        data = self._id_to_meta.get(attr)

        if data is None:
            raise AttributeError

        return data

    def __len__(self) -> int:
        return len(self._id_to_meta)

    @property
    def ids(self) -> list:
        return list(self._id_to_meta.keys())


RelicCatalog = _RelicCatalog()


# I count 179 relics on the STS wiki, including the Circlet
NUM_RELICS = len(RelicCatalog)
LOG_NUM_RELICS = math.ceil(math.log(NUM_RELICS, 2))

# Counter values never need to be greater than 10
MAX_COUNTER = 15
LOG_MAX_COUNTER = math.ceil(math.log(MAX_COUNTER, 2))
