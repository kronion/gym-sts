import math

from pydantic import BaseModel


class PotionMetadata(BaseModel):
    id: str
    name: str
    requires_target: bool


class _PotionCatalog:
    _id_to_meta = {
        # Indicates the potion slot does not exist
        "NONE": PotionMetadata(
            id="NONE",
            name="NONE",
            requires_target=False,
        ),
        "Potion Slot": PotionMetadata(
            id="Potion Slot",
            name="Potion Slot",
            requires_target=False,
        ),
        "EntropicBrew": PotionMetadata(
            id="EntropicBrew",
            name="Entropic Brew",
            requires_target=False,
        ),
        "Regen Potion": PotionMetadata(
            id="Regen Potion",
            name="Regen Potion",
            requires_target=False,
        ),
        "AttackPotion": PotionMetadata(
            id="AttackPotion",
            name="Attack Potion",
            requires_target=False,
        ),
        "SkillPotion": PotionMetadata(
            id="SkillPotion",
            name="Skill Potion",
            requires_target=False,
        ),
        "LiquidMemories": PotionMetadata(
            id="LiquidMemories",
            name="Liquid Memories",
            requires_target=False,
        ),
        "SteroidPotion": PotionMetadata(
            id="SteroidPotion",
            name="Flex Potion",
            requires_target=False,
        ),
        "FairyPotion": PotionMetadata(
            id="FairyPotion",
            name="Fairy in a Bottle",
            requires_target=False,
        ),
        "Energy Potion": PotionMetadata(
            id="Energy Potion",
            name="Energy Potion",
            requires_target=False,
        ),
        "EssenceOfSteel": PotionMetadata(
            id="EssenceOfSteel",
            name="Essence of Steel",
            requires_target=False,
        ),
        "GamblersBrew": PotionMetadata(
            id="GamblersBrew",
            name="Gambler's Brew",
            requires_target=False,
        ),
        "PowerPotion": PotionMetadata(
            id="PowerPotion",
            name="Power Potion",
            requires_target=False,
        ),
        "PotionOfCapacity": PotionMetadata(
            id="PotionOfCapacity",
            name="Potion of Capacity",
            requires_target=False,
        ),
        "DuplicationPotion": PotionMetadata(
            id="DuplicationPotion",
            name="Duplication Potion",
            requires_target=False,
        ),
        "BlessingOfTheForge": PotionMetadata(
            id="BlessingOfTheForge",
            name="Blessing of the Forge",
            requires_target=False,
        ),
        "Swift Potion": PotionMetadata(
            id="Swift Potion",
            name="Swift Potion",
            requires_target=False,
        ),
        "CultistPotion": PotionMetadata(
            id="CultistPotion",
            name="Cultist Potion",
            requires_target=False,
        ),
        "StancePotion": PotionMetadata(
            id="StancePotion",
            name="Stance Potion",
            requires_target=False,
        ),
        "Fruit Juice": PotionMetadata(
            id="Fruit Juice",
            name="Fruit Juice",
            requires_target=False,
        ),
        "LiquidBronze": PotionMetadata(
            id="LiquidBronze",
            name="Liquid Bronze",
            requires_target=False,
        ),
        "HeartOfIron": PotionMetadata(
            id="HeartOfIron",
            name="Heart of Iron",
            requires_target=False,
        ),
        "Fire Potion": PotionMetadata(
            id="Fire Potion",
            name="Fire Potion",
            requires_target=True,
        ),
        "Ancient Potion": PotionMetadata(
            id="Ancient Potion",
            name="Ancient Potion",
            requires_target=False,
        ),
        "SmokeBomb": PotionMetadata(
            id="SmokeBomb",
            name="Smoke Bomb",
            requires_target=True,
        ),
        "Block Potion": PotionMetadata(
            id="Block Potion",
            name="Block Potion",
            requires_target=False,
        ),
        "BottledMiracle": PotionMetadata(
            id="BottledMiracle",
            name="Bottled Miracle",
            requires_target=False,
        ),
        "CunningPotion": PotionMetadata(
            id="CunningPotion",
            name="Cunning Potion",
            requires_target=False,
        ),
        "FocusPotion": PotionMetadata(
            id="FocusPotion",
            name="Focus Potion",
            requires_target=False,
        ),
        "EssenceOfDarkness": PotionMetadata(
            id="EssenceOfDarkness",
            name="Essence of Darkness",
            requires_target=False,
        ),
        "GhostInAJar": PotionMetadata(
            id="GhostInAJar",
            name="Ghost in a Jar",
            requires_target=False,
        ),
        "Explosive Potion": PotionMetadata(
            id="Explosive Potion",
            name="Explosive Potion",
            requires_target=True,
        ),
        "FearPotion": PotionMetadata(
            id="FearPotion",
            name="Fear Potion",
            requires_target=True,
        ),
        "SneckoOil": PotionMetadata(
            id="SneckoOil",
            name="Snecko Oil",
            requires_target=False,
        ),
        "Poison Potion": PotionMetadata(
            id="Poison Potion",
            name="Poison Potion",
            requires_target=True,
        ),
        "DistilledChaos": PotionMetadata(
            id="DistilledChaos",
            name="Distilled Chaos",
            requires_target=False,
        ),
        "SpeedPotion": PotionMetadata(
            id="SpeedPotion",
            name="Speed Potion",
            requires_target=False,
        ),
        "Strength Potion": PotionMetadata(
            id="Strength Potion",
            name="Strength Potion",
            requires_target=False,
        ),
        "Weak Potion": PotionMetadata(
            id="Weak Potion",
            name="Weak Potion",
            requires_target=True,
        ),
        "Dexterity Potion": PotionMetadata(
            id="Dexterity Potion",
            name="Dexterity Potion",
            requires_target=False,
        ),
        "ColorlessPotion": PotionMetadata(
            id="ColorlessPotion",
            name="Colorless Potion",
            requires_target=False,
        ),
        "Ambrosia": PotionMetadata(
            id="Ambrosia",
            name="Ambrosia",
            requires_target=False,
        ),
        "BloodPotion": PotionMetadata(
            id="BloodPotion",
            name="Blood Potion",
            requires_target=False,
        ),
        "ElixirPotion": PotionMetadata(
            id="ElixirPotion",
            name="Elixer",
            requires_target=False,
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


PotionCatalog = _PotionCatalog()


NUM_POTIONS = len(PotionCatalog)
LOG_NUM_POTIONS = math.ceil(math.log(NUM_POTIONS, 2))

NUM_POTION_SLOTS = 5
