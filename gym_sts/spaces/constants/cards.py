import math
from enum import Enum
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field


class CardType(str, Enum):
    ATTACK = "Attack"
    POWER = "Power"
    SKILL = "Skill"
    CURSE = "Curse"
    STATUS = "Status"


# TODO add innate and retain?
class CardProperties(BaseModel):
    default_cost: Union[int, Literal["X"], Literal["U"]]
    ethereal: bool = False
    exhausts: bool = False
    has_target: bool


class CardMetadata(BaseModel):
    id: str
    name: str
    card_type: Optional[CardType] = Field(...)
    unupgraded: CardProperties
    upgraded: CardProperties


class _CardCatalog:
    _id_to_meta = {
        # Indicates the absence of a card
        "NONE": CardMetadata(
            id="NONE",
            name="NONE",
            card_type=None,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        # Ironclad cards (alphabetically)
        "Anger": CardMetadata(
            id="Anger",
            name="Anger",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Armaments": CardMetadata(
            id="Armaments",
            name="Armaments",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Barricade": CardMetadata(
            id="Barricade",
            name="Barricade",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Bash": CardMetadata(
            id="Bash",
            name="Bash",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Battle Trance": CardMetadata(
            id="Battle Trance",
            name="Battle Trance",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Berserk": CardMetadata(
            id="Berserk",
            name="Berserk",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Blood for Blood": CardMetadata(
            id="Blood for Blood",
            name="Blood for Blood",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=4,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=True,
            ),
        ),
        "Bloodletting": CardMetadata(
            id="Bloodletting",
            name="Bloodletting",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Bludgeon": CardMetadata(
            id="Bludgeon",
            name="Bludgeon",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=True,
            ),
        ),
        "Body Slam": CardMetadata(
            id="Body Slam",
            name="Body Slam",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Brutality": CardMetadata(
            id="Brutality",
            name="Brutality",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Burning Pact": CardMetadata(
            id="Burning Pact",
            name="Burning Pact",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Carnage": CardMetadata(
            id="Carnage",
            name="Carnage",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                ethereal=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                ethereal=True,
                has_target=True,
            ),
        ),
        "Clash": CardMetadata(
            id="Clash",
            name="Clash",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Cleave": CardMetadata(
            id="Cleave",
            name="Cleave",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Clothesline": CardMetadata(
            id="Clothesline",
            name="Clothesline",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Combust": CardMetadata(
            id="Combust",
            name="Combust",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Corruption": CardMetadata(
            id="Corruption",
            name="Corruption",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Dark Embrace": CardMetadata(
            id="Dark Embrace",
            name="Dark Embrace",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Defend_R": CardMetadata(
            id="Defend_R",
            name="Defend",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Demon Form": CardMetadata(
            id="Demon Form",
            name="Demon Form",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
        ),
        "Disarm": CardMetadata(
            id="Disarm",
            name="Disarm",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Double Tap": CardMetadata(
            id="Double Tap",
            name="Double Tap",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Dropkick": CardMetadata(
            id="Dropkick",
            name="Dropkick",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Dual Wield": CardMetadata(
            id="Dual Wield",
            name="Dual Wield",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Entrench": CardMetadata(
            id="Entrench",
            name="Entrench",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Evolve": CardMetadata(
            id="Evolve",
            name="Evolve",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Exhume": CardMetadata(
            id="Exhume",
            name="Exhume",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Feed": CardMetadata(
            id="Feed",
            name="Feed",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Feel No Pain": CardMetadata(
            id="Feel No Pain",
            name="Feel No Pain",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Fiend Fire": CardMetadata(
            id="Fiend Fire",
            name="Fiend Fire",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Fire Breathing": CardMetadata(
            id="Fire Breathing",
            name="Fire Breathing",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Flame Barrier": CardMetadata(
            id="Flame Barrier",
            name="Flame Barrier",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Flex": CardMetadata(
            id="Flex",
            name="Flex",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Ghostly Armor": CardMetadata(
            id="Ghostly Armor",
            name="Ghostly Armor",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                ethereal=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                ethereal=True,
                has_target=False,
            ),
        ),
        "Havoc": CardMetadata(
            id="Havoc",
            name="Havoc",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Headbutt": CardMetadata(
            id="Headbutt",
            name="Headbutt",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Heavy Blade": CardMetadata(
            id="Heavy Blade",
            name="Heavy Blade",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Hemokinesis": CardMetadata(
            id="Hemokinesis",
            name="Hemokinesis",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Immolate": CardMetadata(
            id="Immolate",
            name="Immolate",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Impervious": CardMetadata(
            id="Impervious",
            name="Impervious",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Infernal Blade": CardMetadata(
            id="Infernal Blade",
            name="Infernal Blade",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Inflame": CardMetadata(
            id="Inflame",
            name="Inflame",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Intimidate": CardMetadata(
            id="Intimidate",
            name="Intimidate",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Iron Wave": CardMetadata(
            id="Iron Wave",
            name="Iron Wave",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Juggernaut": CardMetadata(
            id="Juggernaut",
            name="Juggernaut",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Limit Break": CardMetadata(
            id="Limit Break",
            name="Limit Break",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Metallicize": CardMetadata(
            id="Metallicize",
            name="Metallicize",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Offering": CardMetadata(
            id="Offering",
            name="Offering",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Perfected Strike": CardMetadata(
            id="Perfected Strike",
            name="Perfected Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Pommel Strike": CardMetadata(
            id="Pommel Strike",
            name="Pommel Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Power Through": CardMetadata(
            id="Power Through",
            name="Power Through",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Pummel": CardMetadata(
            id="Pummel",
            name="Pummel",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Rage": CardMetadata(
            id="Rage",
            name="Rage",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Rampage": CardMetadata(
            id="Rampage",
            name="Rampage",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Reaper": CardMetadata(
            id="Reaper",
            name="Reaper",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Reckless Charge": CardMetadata(
            id="Reckless Charge",
            name="Reckless Charge",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Rupture": CardMetadata(
            id="Rupture",
            name="Rupture",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Searing Blow": CardMetadata(
            id="Searing Blow",
            name="Searing Blow",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Second Wind": CardMetadata(
            id="Second Wind",
            name="Second Wind",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Seeing Red": CardMetadata(
            id="Seeing Red",
            name="Seeing Red",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Sentinel": CardMetadata(
            id="Sentinel",
            name="Sentinel",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Sever Soul": CardMetadata(
            id="Sever Soul",
            name="Sever Soul",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Shockwave": CardMetadata(
            id="Shockwave",
            name="Shockwave",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Shrug It Off": CardMetadata(
            id="Shrug It Off",
            name="Shrug It Off",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Spot Weakness": CardMetadata(
            id="Spot Weakness",
            name="Spot Weakness",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Strike_R": CardMetadata(
            id="Strike_R",
            name="Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Sword Boomerang": CardMetadata(
            id="Sword Boomerang",
            name="Sword Boomerang",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Thunderclap": CardMetadata(
            id="Thunderclap",
            name="Thunderclap",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "True Grit": CardMetadata(
            id="True Grit",
            name="True Grit",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Twin Strike": CardMetadata(
            id="Twin Strike",
            name="Twin Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Uppercut": CardMetadata(
            id="Uppercut",
            name="Uppercut",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Warcry": CardMetadata(
            id="Warcry",
            name="Warcry",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Whirlwind": CardMetadata(
            id="Whirlwind",
            name="Whirlwind",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost="X",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="X",
                has_target=False,
            ),
        ),
        "Wild Strike": CardMetadata(
            id="Wild Strike",
            name="Wild Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        # Silent cards (alphabetically)
        "A Thousand Cuts": CardMetadata(
            id="A Thousand Cuts",
            name="A Thousand Cuts",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Accuracy": CardMetadata(
            id="Accuracy",
            name="Accuracy",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Acrobatics": CardMetadata(
            id="Acrobatics",
            name="Acrobatics",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Adrenaline": CardMetadata(
            id="Adrenaline",
            name="Adrenaline",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "After Image": CardMetadata(
            id="After Image",
            name="After Image",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "All Out Attack": CardMetadata(
            id="All Out Attack",
            name="All-Out Attack",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Backflip": CardMetadata(
            id="Backflip",
            name="Backflip",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Backstab": CardMetadata(
            id="Backstab",
            name="Backstab",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Bane": CardMetadata(
            id="Bane",
            name="Bane",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Blade Dance": CardMetadata(
            id="Blade Dance",
            name="Blade Dance",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Blur": CardMetadata(
            id="Blur",
            name="Blur",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Bouncing Flask": CardMetadata(
            id="Bouncing Flask",
            name="Bouncing Flask",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Bullet Time": CardMetadata(
            id="Bullet Time",
            name="Bullet Time",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Burst": CardMetadata(
            id="Burst",
            name="Burst",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Calculated Gamble": CardMetadata(
            id="Calculated Gamble",
            name="Calculated Gamble",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Caltrops": CardMetadata(
            id="Caltrops",
            name="Caltrops",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Catalyst": CardMetadata(
            id="Catalyst",
            name="Catalyst",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Choke": CardMetadata(
            id="Choke",
            name="Choke",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Cloak And Dagger": CardMetadata(
            id="Cloak And Dagger",
            name="Cloak and Dagger",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Concentrate": CardMetadata(
            id="Concentrate",
            name="Concentrate",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Corpse Explosion": CardMetadata(
            id="Corpse Explosion",
            name="Corpse Explosion",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Crippling Poison": CardMetadata(
            id="Crippling Poison",
            name="Crippling Cloud",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Dagger Spray": CardMetadata(
            id="Dagger Spray",
            name="Dagger Spray",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Dagger Throw": CardMetadata(
            id="Dagger Throw",
            name="Dagger Throw",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Dash": CardMetadata(
            id="Dash",
            name="Dash",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Deadly Poison": CardMetadata(
            id="Deadly Poison",
            name="Deadly Poison",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Defend_G": CardMetadata(
            id="Defend_G",
            name="Defend",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Deflect": CardMetadata(
            id="Deflect",
            name="Deflect",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Die Die Die": CardMetadata(
            id="Die Die Die",
            name="Die Die Die",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Distraction": CardMetadata(
            id="Distraction",
            name="Distraction",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Dodge and Roll": CardMetadata(
            id="Dodge and Roll",
            name="Dodge and Roll",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Doppelganger": CardMetadata(
            id="Doppelganger",
            name="Doppelganger",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
        ),
        "Endless Agony": CardMetadata(
            id="Endless Agony",
            name="Endless Agony",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Envenom": CardMetadata(
            id="Envenom",
            name="Envenom",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Escape Plan": CardMetadata(
            id="Escape Plan",
            name="Escape Plan",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Eviscerate": CardMetadata(
            id="Eviscerate",
            name="Eviscerate",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=True,
            ),
        ),
        "Expertise": CardMetadata(
            id="Expertise",
            name="Expertise",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Finisher": CardMetadata(
            id="Finisher",
            name="Finisher",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Flechettes": CardMetadata(
            id="Flechettes",
            name="Flechettes",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Flying Knee": CardMetadata(
            id="Flying Knee",
            name="Flying Knee",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Footwork": CardMetadata(
            id="Footwork",
            name="Footwork",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Glass Knife": CardMetadata(
            id="Glass Knife",
            name="Glass Knife",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Grand Finale": CardMetadata(
            id="Grand Finale",
            name="Grand Finale",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Heel Hook": CardMetadata(
            id="Heel Hook",
            name="Heel Hook",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Infinite Blades": CardMetadata(
            id="Infinite Blades",
            name="Infinite Blades",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Leg Sweep": CardMetadata(
            id="Leg Sweep",
            name="Leg Sweep",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Malaise": CardMetadata(
            id="Malaise",
            name="Malaise",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=True,
            ),
        ),
        "Masterful Stab": CardMetadata(
            id="Masterful Stab",
            name="Masterful Stab",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Neutralize": CardMetadata(
            id="Neutralize",
            name="Neutralize",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Night Terror": CardMetadata(
            id="Night Terror",
            name="Nightmare",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=3,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Noxious Fumes": CardMetadata(
            id="Noxious Fumes",
            name="Noxious Fumes",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Outmaneuver": CardMetadata(
            id="Outmaneuver",
            name="Outmaneuver",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Phantasmal Killer": CardMetadata(
            id="Phantasmal Killer",
            name="Phantasmal Killer",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "PiercingWail": CardMetadata(
            id="PiercingWail",
            name="Piercing Wail",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Poisoned Stab": CardMetadata(
            id="Poisoned Stab",
            name="Poisoned Stab",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Predator": CardMetadata(
            id="Predator",
            name="Predator",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Prepared": CardMetadata(
            id="Prepared",
            name="Prepared",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Quick Slash": CardMetadata(
            id="Quick Slash",
            name="Quick Slash",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Reflex": CardMetadata(
            id="Reflex",
            name="Reflex",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Riddle With Holes": CardMetadata(
            id="Riddle With Holes",
            name="Riddle With Holes",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Setup": CardMetadata(
            id="Setup",
            name="Setup",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Skewer": CardMetadata(
            id="Skewer",
            name="Skewer",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost="X",
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost="X",
                has_target=True,
            ),
        ),
        "Slice": CardMetadata(
            id="Slice",
            name="Slice",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Storm of Steel": CardMetadata(
            id="Storm of Steel",
            name="Storm of Steel",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Strike_G": CardMetadata(
            id="Strike_G",
            name="Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Sucker Punch": CardMetadata(
            id="Sucker Punch",
            name="Sucker Punch",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Survivor": CardMetadata(
            id="Survivor",
            name="Survivor",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Tactician": CardMetadata(
            id="Tactician",
            name="Tactician",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Terror": CardMetadata(
            id="Terror",
            name="Terror",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Tools of the Trade": CardMetadata(
            id="Tools of the Trade",
            name="Tools of the Trade",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Underhanded Strike": CardMetadata(
            id="Underhanded Strike",
            name="Sneaky Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Unload": CardMetadata(
            id="Unload",
            name="Unload",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Venomology": CardMetadata(
            id="Venomology",
            name="Alchemize",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Well Laid Plans": CardMetadata(
            id="Well Laid Plans",
            name="Well Laid Plans",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Wraith Form v2": CardMetadata(
            id="Wraith Form v2",
            name="Wraith Form",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
        ),
        # Defect cards (alphabetically)
        "Aggregate": CardMetadata(
            id="Aggregate",
            name="Aggregate",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "All For One": CardMetadata(
            id="All For One",
            name="All for One",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Amplify": CardMetadata(
            id="Amplify",
            name="Amplify",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Auto Shields": CardMetadata(
            id="Auto Shields",
            name="Auto-Shields",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Ball Lightning": CardMetadata(
            id="Ball Lightning",
            name="Ball Lightning",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Barrage": CardMetadata(
            id="Barrage",
            name="Barrage",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Beam Cell": CardMetadata(
            id="Beam Cell",
            name="Beam Cell",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Biased Cognition": CardMetadata(
            id="Biased Cognition",
            name="Biased Cognition",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Blizzard": CardMetadata(
            id="Blizzard",
            name="Blizzard",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "BootSequence": CardMetadata(
            id="BootSequence",
            name="Boot Sequence",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Buffer": CardMetadata(
            id="Buffer",
            name="Buffer",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Capacitor": CardMetadata(
            id="Capacitor",
            name="Capacitor",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Chaos": CardMetadata(
            id="Chaos",
            name="Chaos",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Chill": CardMetadata(
            id="Chill",
            name="Chill",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Cold Snap": CardMetadata(
            id="Cold Snap",
            name="Cold Snap",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Compile Driver": CardMetadata(
            id="Compile Driver",
            name="Compile Driver",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Conserve Battery": CardMetadata(
            id="Conserve Battery",
            name="Charge Battery",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Consume": CardMetadata(
            id="Consume",
            name="Consume",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Coolheaded": CardMetadata(
            id="Coolheaded",
            name="Coolheaded",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Core Surge": CardMetadata(
            id="Core Surge",
            name="Core Surge",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Creative AI": CardMetadata(
            id="Creative AI",
            name="Creative AI",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Darkness": CardMetadata(
            id="Darkness",
            name="Darkness",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Defend_B": CardMetadata(
            id="Defend_B",
            name="Defend",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Defragment": CardMetadata(
            id="Defragment",
            name="Defragment",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Doom and Gloom": CardMetadata(
            id="Doom and Gloom",
            name="Doom and Gloom",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Double Energy": CardMetadata(
            id="Double Energy",
            name="Double Energy",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Dualcast": CardMetadata(
            id="Dualcast",
            name="Dualcast",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Echo Form": CardMetadata(
            id="Echo Form",
            name="Echo Form",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=3,
                ethereal=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
        ),
        "Electrodynamics": CardMetadata(
            id="Electrodynamics",
            name="Electrodynamics",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Fission": CardMetadata(
            id="Fission",
            name="Fission",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Force Field": CardMetadata(
            id="Force Field",
            name="Force Field",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=4,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=4,
                has_target=False,
            ),
        ),
        "FTL": CardMetadata(
            id="FTL",
            name="FTL",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Fusion": CardMetadata(
            id="Fusion",
            name="Fusion",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Gash": CardMetadata(
            id="Gash",
            name="Claw",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Genetic Algorithm": CardMetadata(
            id="Genetic Algorithm",
            name="Genetic Algorithm",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Glacier": CardMetadata(
            id="Glacier",
            name="Glacier",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Go for the Eyes": CardMetadata(
            id="Go for the Eyes",
            name="Go for the Eyes",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Heatsinks": CardMetadata(
            id="Heatsinks",
            name="Heatsinks",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Hello World": CardMetadata(
            id="Hello World",
            name="Hello World",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Hologram": CardMetadata(
            id="Hologram",
            name="Hologram",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Hyperbeam": CardMetadata(
            id="Hyperbeam",
            name="Hyperbeam",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Leap": CardMetadata(
            id="Leap",
            name="Leap",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Loop": CardMetadata(
            id="Loop",
            name="Loop",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Lockon": CardMetadata(
            id="Lockon",
            name="Bullseye",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Machine Learning": CardMetadata(
            id="Machine Learning",
            name="Machine Learning",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Melter": CardMetadata(
            id="Melter",
            name="Melter",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Meteor Strike": CardMetadata(
            id="Meteor Strike",
            name="Meteor Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=5,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=5,
                has_target=True,
            ),
        ),
        "Multi-Cast": CardMetadata(
            id="Multi-Cast",
            name="Multi-Cast",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="X",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="X",
                has_target=False,
            ),
        ),
        "Rainbow": CardMetadata(
            id="Rainbow",
            name="Rainbow",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Reboot": CardMetadata(
            id="Reboot",
            name="Reboot",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Rebound": CardMetadata(
            id="Rebound",
            name="Rebound",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Recycle": CardMetadata(
            id="Recycle",
            name="Recycle",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Redo": CardMetadata(
            id="Redo",
            name="Recursion",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Reinforced Body": CardMetadata(
            id="Reinforced Body",
            name="Reinforced Body",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="X",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="X",
                has_target=False,
            ),
        ),
        "Reprogram": CardMetadata(
            id="Reprogram",
            name="Reprogram",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Rip and Tear": CardMetadata(
            id="Rip and Tear",
            name="Rip and Tear",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Scrape": CardMetadata(
            id="Scrape",
            name="Scrape",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Seek": CardMetadata(
            id="Seek",
            name="Seek",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Self Repair": CardMetadata(
            id="Self Repair",
            name="Self Repair",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Skim": CardMetadata(
            id="Skim",
            name="Skim",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Stack": CardMetadata(
            id="Stack",
            name="Stack",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Static Discharge": CardMetadata(
            id="Static Discharge",
            name="Static Discharge",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Steam": CardMetadata(
            id="Steam",
            name="Steam Barrier",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Steam Power": CardMetadata(
            id="Steam Power",
            name="Overclock",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Storm": CardMetadata(
            id="Storm",
            name="Storm",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Streamline": CardMetadata(
            id="Streamline",
            name="Streamline",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Strike_B": CardMetadata(
            id="Strike_B",
            name="Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Sunder": CardMetadata(
            id="Sunder",
            name="Sunder",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=True,
            ),
        ),
        "Sweeping Beam": CardMetadata(
            id="Sweeping Beam",
            name="Sweeping Beam",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Tempest": CardMetadata(
            id="Tempest",
            name="Tempest",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
        ),
        "Thunder Strike": CardMetadata(
            id="Thunder Strike",
            name="Thunder Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
        ),
        "Turbo": CardMetadata(
            id="Turbo",
            name="TURBO",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Undo": CardMetadata(
            id="Undo",
            name="Equilibrium",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "White Noise": CardMetadata(
            id="White Noise",
            name="White Noise",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Zap": CardMetadata(
            id="Zap",
            name="Zap",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        # Colorless cards (alphabetically)
        "Apotheosis": CardMetadata(
            id="Apotheosis",
            name="Apotheosis",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Bandage Up": CardMetadata(
            id="Bandage Up",
            name="Bandage Up",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Bite": CardMetadata(
            id="Bite",
            name="Bite",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Blind": CardMetadata(
            id="Blind",
            name="Blind",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Chrysalis": CardMetadata(
            id="Chrysalis",
            name="Chrysalis",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Dark Shackles": CardMetadata(
            id="Dark Shackles",
            name="Dark Shackles",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Deep Breath": CardMetadata(
            id="Deep Breath",
            name="Deep Breath",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Discovery": CardMetadata(
            id="Discovery",
            name="Discovery",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Dramatic Entrance": CardMetadata(
            id="Dramatic Entrance",
            name="Dramatic Entrance",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Enlightenment": CardMetadata(
            id="Enlightenment",
            name="Enlightenment",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Finesse": CardMetadata(
            id="Finesse",
            name="Finesse",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Flash of Steel": CardMetadata(
            id="Flash of Steel",
            name="Flash of Steel",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "Forethought": CardMetadata(
            id="Forethought",
            name="Forethought",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Ghostly": CardMetadata(
            id="Ghostly",
            name="Apparition",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                ethereal=True,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Good Instincts": CardMetadata(
            id="Good Instincts",
            name="Good Instincts",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "HandOfGreed": CardMetadata(
            id="HandOfGreed",
            name="Hand of Greed",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Impatience": CardMetadata(
            id="Impatience",
            name="Impatience",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "J.A.X.": CardMetadata(
            id="J.A.X.",
            name="J.A.X.",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Jack Of All Trades": CardMetadata(
            id="Jack Of All Trades",
            name="Jack of All Trades",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Madness": CardMetadata(
            id="Madness",
            name="Madness",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Magnetism": CardMetadata(
            id="Magnetism",
            name="Magnetism",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Master of Strategy": CardMetadata(
            id="Master of Strategy",
            name="Master of Strategy",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Mayhem": CardMetadata(
            id="Mayhem",
            name="Mayhem",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Metamorphosis": CardMetadata(
            id="Metamorphosis",
            name="Metamorphosis",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Mind Blast": CardMetadata(
            id="Mind Blast",
            name="Mind Blast",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Panacea": CardMetadata(
            id="Panacea",
            name="Panacea",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Panache": CardMetadata(
            id="Panache",
            name="Panache",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "PanicButton": CardMetadata(
            id="PanicButton",
            name="Panic Button",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Purity": CardMetadata(
            id="Purity",
            name="Purity",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "RitualDagger": CardMetadata(
            id="RitualDagger",
            name="Ritual Dagger",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Sadistic Nature": CardMetadata(
            id="Sadistic Nature",
            name="Sadistic Nature",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Secret Technique": CardMetadata(
            id="Secret Technique",
            name="Secret Technique",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Secret Weapon": CardMetadata(
            id="Secret Weapon",
            name="Secret Weapon",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Swift Strike": CardMetadata(
            id="Swift Strike",
            name="Swift Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "The Bomb": CardMetadata(
            id="The Bomb",
            name="The Bomb",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Thinking Ahead": CardMetadata(
            id="Thinking Ahead",
            name="Thinking Ahead",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Transmutation": CardMetadata(
            id="Transmutation",
            name="Transmutation",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
        ),
        "Trip": CardMetadata(
            id="Trip",
            name="Trip",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Violence": CardMetadata(
            id="Violence",
            name="Violence",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        # Watcher cards (alphabetically)
        "Adaptation": CardMetadata(
            id="Adaptation",
            name="Rushdown",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Alpha": CardMetadata(
            id="Alpha",
            name="Alpha",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "BattleHymn": CardMetadata(
            id="BattleHymn",
            name="Battle Hymn",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Blasphemy": CardMetadata(
            id="Blasphemy",
            name="Blasphemy",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "BowlingBash": CardMetadata(
            id="BowlingBash",
            name="Bowling Bash",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Brilliance": CardMetadata(
            id="Brilliance",
            name="Brilliance",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "CarveReality": CardMetadata(
            id="CarveReality",
            name="Carve Reality",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "ClearTheMind": CardMetadata(
            id="ClearTheMind",
            name="Tranquility",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Collect": CardMetadata(
            id="Collect",
            name="Collect",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
        ),
        "Conclude": CardMetadata(
            id="Conclude",
            name="Conclude",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "ConjureBlade": CardMetadata(
            id="ConjureBlade",
            name="Conjure Blade",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="X",
                exhausts=True,
                has_target=False,
            ),
        ),
        "Consecrate": CardMetadata(
            id="Consecrate",
            name="Consecrate",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Crescendo": CardMetadata(
            id="Crescendo",
            name="Crescendo",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "CrushJoints": CardMetadata(
            id="CrushJoints",
            name="Crush Joints",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "CutThroughFate": CardMetadata(
            id="CutThroughFate",
            name="Cut Through Fate",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "DeceiveReality": CardMetadata(
            id="DeceiveReality",
            name="Deceive Reality",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Defend_P": CardMetadata(
            id="Defend_P",
            name="Defend",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "DeusExMachina": CardMetadata(
            id="DeusExMachina",
            name="Deus Ex Machina",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
        ),
        "DevaForm": CardMetadata(
            id="DevaForm",
            name="Deva Form",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=3,
                ethereal=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
        ),
        "Devotion": CardMetadata(
            id="Devotion",
            name="Devotion",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "EmptyBody": CardMetadata(
            id="EmptyBody",
            name="Empty Body",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "EmptyFist": CardMetadata(
            id="EmptyFist",
            name="Empty Fist",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "EmptyMind": CardMetadata(
            id="EmptyMind",
            name="Empty Mind",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Eruption": CardMetadata(
            id="Eruption",
            name="Eruption",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Establishment": CardMetadata(
            id="Establishment",
            name="Establishment",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Evaluate": CardMetadata(
            id="Evaluate",
            name="Evaluate",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Fasting2": CardMetadata(
            id="Fasting2",
            name="Fasting",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "FearNoEvil": CardMetadata(
            id="FearNoEvil",
            name="Fear No Evil",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "FlurryOfBlows": CardMetadata(
            id="FlurryOfBlows",
            name="Flurry Of Blows",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "FlyingSleeves": CardMetadata(
            id="FlyingSleeves",
            name="Flying Sleeves",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "FollowUp": CardMetadata(
            id="FollowUp",
            name="Follow-Up",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "ForeignInfluence": CardMetadata(
            id="ForeignInfluence",
            name="Foreign Influence",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Halt": CardMetadata(
            id="Halt",
            name="Halt",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Indignation": CardMetadata(
            id="Indignation",
            name="Indignation",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "InnerPeace": CardMetadata(
            id="InnerPeace",
            name="Inner Peace",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Judgement": CardMetadata(
            id="Judgement",
            name="Judgement",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "JustLucky": CardMetadata(
            id="JustLucky",
            name="Just Lucky",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "LessonLearned": CardMetadata(
            id="LessonLearned",
            name="Lesson Learned",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=True,
            ),
        ),
        "LikeWater": CardMetadata(
            id="LikeWater",
            name="Like Water",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "MasterReality": CardMetadata(
            id="MasterReality",
            name="Master Reality",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Meditate": CardMetadata(
            id="Meditate",
            name="Meditate",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "MentalFortress": CardMetadata(
            id="MentalFortress",
            name="Mental Fortress",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Nirvana": CardMetadata(
            id="Nirvana",
            name="Nirvana",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Omniscience": CardMetadata(
            id="Omniscience",
            name="Omniscience",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=4,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                exhausts=True,
                has_target=False,
            ),
        ),
        "PathToVictory": CardMetadata(
            id="PathToVictory",
            name="Pressure Points",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Perseverance": CardMetadata(
            id="Perseverance",
            name="Perseverance",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Pray": CardMetadata(
            id="Pray",
            name="Pray",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Prostrate": CardMetadata(
            id="Prostrate",
            name="Prostrate",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=False,
            ),
        ),
        "Protect": CardMetadata(
            id="Protect",
            name="Protect",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Ragnarok": CardMetadata(
            id="Ragnarok",
            name="Ragnarok",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
        ),
        "ReachHeaven": CardMetadata(
            id="ReachHeaven",
            name="Reach Heaven",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Sanctity": CardMetadata(
            id="Sanctity",
            name="Sanctity",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "SandsOfTime": CardMetadata(
            id="SandsOfTime",
            name="Sands of Time",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=4,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=4,
                has_target=True,
            ),
        ),
        "SashWhip": CardMetadata(
            id="SashWhip",
            name="Sash Whip",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Scrawl": CardMetadata(
            id="Scrawl",
            name="Scrawl",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "SignatureMove": CardMetadata(
            id="SignatureMove",
            name="Signature Move",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "SpiritShield": CardMetadata(
            id="SpiritShield",
            name="Spirit Shield",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Strike_P": CardMetadata(
            id="Strike_P",
            name="Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Study": CardMetadata(
            id="Study",
            name="Study",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Swivel": CardMetadata(
            id="Swivel",
            name="Swivel",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "TalkToTheHand": CardMetadata(
            id="TalkToTheHand",
            name="Talk to the Hand",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Tantrum": CardMetadata(
            id="Tantrum",
            name="Tantrum",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "ThirdEye": CardMetadata(
            id="ThirdEye",
            name="Third Eye",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Vault": CardMetadata(
            id="Vault",
            name="Vault",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=3,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Vengeance": CardMetadata(
            id="Vengeance",
            name="Simmering Fury",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Vigilance": CardMetadata(
            id="Vigilance",
            name="Vigilance",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "Wallop": CardMetadata(
            id="Wallop",
            name="Wallop",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "WaveOfTheHand": CardMetadata(
            id="WaveOfTheHand",
            name="Wave of the Hand",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Weave": CardMetadata(
            id="Weave",
            name="Weave",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                has_target=True,
            ),
        ),
        "WheelKick": CardMetadata(
            id="WheelKick",
            name="Wheel Kick",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "WindmillStrike": CardMetadata(
            id="WindmillStrike",
            name="Windmill Strike",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=True,
            ),
        ),
        "Wireheading": CardMetadata(
            id="Wireheading",
            name="Foresight",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        "Wish": CardMetadata(
            id="Wish",
            name="Wish",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=3,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Worship": CardMetadata(
            id="Worship",
            name="Worship",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=2,
                has_target=False,
            ),
        ),
        "WreathOfFlame": CardMetadata(
            id="WreathOfFlame",
            name="Wreath of Flame",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=False,
            ),
        ),
        # Status cards (alphabetically)
        "Burn": CardMetadata(
            id="Burn",
            name="Burn",
            card_type=CardType.STATUS,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Dazed": CardMetadata(
            id="Dazed",
            name="Dazed",
            card_type=CardType.STATUS,
            unupgraded=CardProperties(
                default_cost="U",
                ethereal=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                ethereal=True,
                has_target=False,
            ),
        ),
        "Slimed": CardMetadata(
            id="Slimed",
            name="Slimed",
            card_type=CardType.STATUS,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Void": CardMetadata(
            id="Void",
            name="Void",
            card_type=CardType.STATUS,
            unupgraded=CardProperties(
                default_cost="U",
                ethereal=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                ethereal=True,
                has_target=False,
            ),
        ),
        "Wound": CardMetadata(
            id="Wound",
            name="Wound",
            card_type=CardType.STATUS,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        # Curse cards (alphabetically)
        "AscendersBane": CardMetadata(
            id="AscendersBane",
            name="Ascender's Bane",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                ethereal=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                ethereal=True,
                has_target=False,
            ),
        ),
        "Clumsy": CardMetadata(
            id="Clumsy",
            name="Clumsy",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                ethereal=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                ethereal=True,
                has_target=False,
            ),
        ),
        "CurseOfTheBell": CardMetadata(
            id="CurseOfTheBell",
            name="Curse of the Bell",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Decay": CardMetadata(
            id="Decay",
            name="Decay",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Doubt": CardMetadata(
            id="Doubt",
            name="Doubt",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Injury": CardMetadata(
            id="Injury",
            name="Injury",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Necronomicurse": CardMetadata(
            id="Necronomicurse",
            name="Necronomicurse",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Normality": CardMetadata(
            id="Normality",
            name="Normality",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Pain": CardMetadata(
            id="Pain",
            name="Pain",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Parasite": CardMetadata(
            id="Parasite",
            name="Parasite",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Pride": CardMetadata(
            id="Pride",
            name="Pride",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Regret": CardMetadata(
            id="Regret",
            name="Regret",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Shame": CardMetadata(
            id="Shame",
            name="Shame",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        "Writhe": CardMetadata(
            id="Writhe",
            name="Writhe",
            card_type=CardType.CURSE,
            unupgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                has_target=False,
            ),
        ),
        # "Temporary" cards (alphabetically)
        "Beta": CardMetadata(
            id="Beta",
            name="Beta",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=2,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Expunger": CardMetadata(
            id="Expunger",
            name="Expunger",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                has_target=True,
            ),
        ),
        "Insight": CardMetadata(
            id="Insight",
            name="Insight",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Miracle": CardMetadata(
            id="Miracle",
            name="Miracle",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Omega": CardMetadata(
            id="Omega",
            name="Omega",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=3,
                has_target=False,
            ),
        ),
        "Safety": CardMetadata(
            id="Safety",
            name="Safety",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=False,
            ),
        ),
        "Shiv": CardMetadata(
            id="Shiv",
            name="Shiv",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
        ),
        "Smite": CardMetadata(
            id="Smite",
            name="Smite",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=1,
                exhausts=True,
                has_target=True,
            ),
        ),
        "ThroughViolence": CardMetadata(
            id="ThroughViolence",
            name="Through Violence",
            card_type=CardType.ATTACK,
            unupgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
            upgraded=CardProperties(
                default_cost=0,
                exhausts=True,
                has_target=True,
            ),
        ),
        # "Option" cards (alphabetically)
        # One of the Wish rewards
        "BecomeAlmighty": CardMetadata(
            id="BecomeAlmighty",
            name="Become Almighty",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
        ),
        # One of the choices when drinking a stance potion
        "Calm": CardMetadata(
            id="Calm",
            name="Calm",
            card_type=CardType.STATUS,
            unupgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
        ),
        # One of the Wish rewards
        "FameAndFortune": CardMetadata(
            id="FameAndFortune",
            name="Fame and Fortune",
            card_type=CardType.SKILL,
            unupgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
        ),
        # One of the Wish rewards
        "LiveForever": CardMetadata(
            id="LiveForever",
            name="Live Forever",
            card_type=CardType.POWER,
            unupgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
        ),
        # One of the choices when drinking a stance potion
        "Wrath": CardMetadata(
            id="Wrath",
            name="Wrath",
            card_type=CardType.STATUS,
            unupgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
            upgraded=CardProperties(
                default_cost="U",
                exhausts=True,
                has_target=False,
            ),
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


CardCatalog = _CardCatalog()


NUM_CARDS = len(CardCatalog)
NUM_CARDS_WITH_UPGRADES = NUM_CARDS * 2
LOG_NUM_CARDS = math.ceil(math.log(NUM_CARDS, 2))
LOG_NUM_CARDS_WITH_UPGRADES = LOG_NUM_CARDS + 1  # Use one more bit to indicate upgrade

# There's no real limit in the game, but this value greatly impacts the size
# of the observation space.
MAX_COPIES_OF_CARD = 5
