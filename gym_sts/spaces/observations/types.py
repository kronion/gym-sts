from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, NonNegativeInt

import gym_sts.spaces.constants.cards as card_consts
from gym_sts.spaces import old_constants as constants

from . import utils

BinaryArray = list[int]


class Card(BaseModel):
    exhausts: bool
    cost: Union[NonNegativeInt, Literal["U", "X"]]
    name: str
    id: str
    ethereal: bool
    upgrades: NonNegativeInt
    has_target: bool

    @staticmethod
    def _serialize_binary(card_idx: int, upgrades: int) -> list[int]:
        array = utils.to_binary_array(card_idx, card_consts.LOG_NUM_CARDS)

        # TODO support more than 1 upgrade
        upgrade_bit = [0]
        if upgrades > 0:
            upgrade_bit = [1]

        array = upgrade_bit + array

        return array

    @classmethod
    def serialize_empty_binary(cls) -> list[int]:
        return cls._serialize_binary(0, 0)

    def serialize_discrete(self) -> int:
        card_idx = card_consts.CardCatalog.ids.index(self.id) * 2
        if self.upgrades > 0:
            card_idx += 1

        return card_idx

    def serialize_binary(self) -> list[int]:
        card_idx = card_consts.CardCatalog.ids.index(self.id)
        return self._serialize_binary(card_idx, self.upgrades)

    @classmethod
    def deserialize_discrete(cls, raw_data: int) -> Card:
        pass

    @classmethod
    def deserialize_binary(cls, raw_data: BinaryArray) -> Card:
        if len(raw_data) != card_consts.LOG_NUM_CARDS + 1:
            raise ValueError("Card encoding has unexpected length")

        upgrade_bit = raw_data[0]
        card_bits = raw_data[1:]

        card_idx = utils.from_binary_array(card_bits)

        card_id = card_consts.CardCatalog.ids[card_idx]
        card_meta: card_consts.CardMetadata = getattr(card_consts.CardCatalog, card_id)
        card_props = card_meta.upgraded if upgrade_bit else card_meta.unupgraded

        return cls(
            id=card_id,
            name=card_meta.name,
            # TODO may be wrong because we don't currently serialize cost
            cost=card_props.default_cost,
            exhausts=card_props.exhausts,
            ethereal=card_props.ethereal,
            has_target=card_props.has_target,
            # TODO may be wrong for cards that can be upgraded 2+ times
            upgrades=upgrade_bit,
        )


class HandCard(Card):
    is_playable: bool


class Potion(BaseModel):
    id: str
    requires_target: Optional[bool]
    can_use: Optional[bool]
    can_discard: Optional[bool]
    name: Optional[str]

    def serialize(self) -> int:
        return constants.ALL_POTIONS.index(self.id)

    @classmethod
    def deserialize(cls, potion_idx: int) -> Potion:
        # TODO add metadata file to recover more state
        potion_id = constants.ALL_POTIONS[potion_idx]

        return cls(id=potion_id)


class Relic(BaseModel):
    id: str
    name: Optional[str]
    counter: Optional[int]

    def serialize(self) -> int:
        return constants.ALL_RELICS.index(self.id)

    @classmethod
    def deserialize(cls, relic_idx: int) -> Relic:
        # TODO add metadata file to recover more state
        relic_id = constants.ALL_RELICS[relic_idx]

        return cls(id=relic_id)


class ShopMixin(BaseModel):
    price: int = Field(..., ge=0, lt=2**constants.SHOP_LOG_MAX_PRICE)

    @staticmethod
    def serialize_empty_price():
        return utils.to_binary_array(0, constants.SHOP_LOG_MAX_PRICE)

    def serialize_price(self):
        return utils.to_binary_array(self.price, constants.SHOP_LOG_MAX_PRICE)

    @staticmethod
    def deserialize_price(price: BinaryArray) -> int:
        return utils.from_binary_array(price)


class ShopCard(Card, ShopMixin):
    def serialize_discrete(self):
        raise NotImplementedError("Use serialize() instead")

    def serialize_binary(self):
        raise NotImplementedError("Use serialize() instead")

    @classmethod
    def serialize_empty(cls) -> dict[str, list[int]]:
        return {
            "card": Card.serialize_empty_binary(),
            "price": cls.serialize_empty_price(),
        }

    def serialize(self) -> dict[str, list[int]]:
        return {"card": super().serialize_binary(), "price": self.serialize_price()}

    class SerializedState(BaseModel):
        card: BinaryArray
        price: BinaryArray

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> ShopCard:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        card = Card.deserialize_binary(data.card)
        price = ShopMixin.deserialize_price(data.price)

        return cls(**card.dict(), price=price)


class ShopPotion(Potion, ShopMixin):
    @classmethod
    def serialize_empty(cls) -> dict:
        return {"potion": 0, "price": cls.serialize_empty_price()}

    def serialize(self) -> dict:  # type: ignore[override]
        return {"potion": super().serialize(), "price": self.serialize_price()}

    class SerializedState(BaseModel):
        potion: int
        price: BinaryArray

    @classmethod
    def deserialize(  # type: ignore[override]
        cls, data: Union[dict, SerializedState]
    ) -> ShopPotion:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        potion = Potion.deserialize(data.potion)
        price = ShopMixin.deserialize_price(data.price)

        return cls(**potion.dict(), price=price)


class ShopRelic(Relic, ShopMixin):
    @classmethod
    def serialize_empty(cls) -> dict:
        return {"relic": 0, "price": cls.serialize_empty_price()}

    def serialize(self) -> dict:  # type: ignore[override]
        return {"relic": super().serialize(), "price": self.serialize_price()}

    class SerializedState(BaseModel):
        relic: int
        price: BinaryArray

    @classmethod
    def deserialize(  # type: ignore[override]
        cls, data: Union[dict, SerializedState]
    ) -> ShopRelic:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        relic = Relic.deserialize(data.relic)
        price = ShopMixin.deserialize_price(data.price)

        return cls(**relic.dict(), price=price)


class Reward(BaseModel, ABC):
    @abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError("Unimplemented")

    @staticmethod
    def serialize_empty():
        return {
            "type": constants.ALL_REWARD_TYPES.index("NONE"),
            "value": utils.to_binary_array(0, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class GoldReward(Reward):
    value: int

    def serialize(self) -> dict:
        return {
            "type": constants.ALL_REWARD_TYPES.index("GOLD"),
            "value": utils.to_binary_array(
                self.value, constants.COMBAT_REWARD_LOG_MAX_ID
            ),
        }


class PotionReward(Reward):
    value: Potion

    def serialize(self) -> dict:
        potion_idx = constants.ALL_POTIONS.index(self.value.id)
        return {
            "type": constants.ALL_REWARD_TYPES.index("POTION"),
            "value": utils.to_binary_array(
                potion_idx, constants.COMBAT_REWARD_LOG_MAX_ID
            ),
        }


class RelicReward(Reward):
    value: Relic

    def serialize(self) -> dict:
        relic_idx = constants.ALL_RELICS.index(self.value.id)
        return {
            "type": constants.ALL_REWARD_TYPES.index("RELIC"),
            "value": utils.to_binary_array(
                relic_idx, constants.COMBAT_REWARD_LOG_MAX_ID
            ),
        }


class CardReward(Reward):
    def serialize(self) -> dict:
        return {
            "type": constants.ALL_REWARD_TYPES.index("CARD"),
            "value": utils.to_binary_array(0, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class KeyReward(Reward):
    value: str

    def serialize(self) -> dict:
        key_idx = constants.ALL_KEYS.index(self.value)
        return {
            "ty  # e.g. charge battery's effectpe": constants.ALL_REWARD_TYPES.index(
                "KEY"
            ),
            "value": utils.to_binary_array(key_idx, constants.COMBAT_REWARD_LOG_MAX_ID),
        }


class Keys(BaseModel):
    emerald: bool = False
    ruby: bool = False
    sapphire: bool = False


class MapCoordinates(BaseModel):
    x: int
    y: int


class StandardNode(MapCoordinates):
    symbol: str
    children: list[MapCoordinates]


class EliteNode(StandardNode):
    is_burning: bool


Node = Union[StandardNode, EliteNode]


class Effect(BaseModel):
    id: str = "EMPTY"  # Placeholder should always be replaced
    amount: int = Field(
        ..., gt=-(2**constants.LOG_MAX_EFFECT), lt=2**constants.LOG_MAX_EFFECT
    )

    def serialize(self) -> dict:
        sign = 0
        value = self.amount

        if self.amount < 0:
            sign = 1
            value = -value

        return {
            "sign": sign,
            "value": utils.to_binary_array(value, constants.LOG_MAX_EFFECT),
        }

    @staticmethod
    def serialize_all(effects: list[Effect]) -> list[dict]:
        serialized = []
        effect_map = {effect.id: effect for effect in effects}

        for effect_id in constants.ALL_EFFECTS:
            encoding = {
                "sign": 0,
                "value": utils.to_binary_array(0, constants.LOG_MAX_EFFECT),
            }
            if effect_id in effect_map:
                effect = effect_map[effect_id]
                encoding = effect.serialize()

            serialized.append(encoding)

        return serialized

    class SerializedState(BaseModel):
        sign: int = Field(..., ge=0, le=1)
        value: BinaryArray

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> Effect:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        amount = utils.from_binary_array(data.value)
        if data.sign:
            amount = -amount

        return cls(amount=amount)


class Orb(BaseModel):
    id: str = "Empty"  # STS seems to have a bug where empty orbs sometimes have no ID

    @staticmethod
    def serialize_empty() -> int:
        return constants.ALL_ORBS.index("NONE")

    def serialize(self) -> int:
        return constants.ALL_ORBS.index(self.id)

    @classmethod
    def deserialize(cls, orb_idx: int) -> Orb:
        orb_id = constants.ALL_ORBS[orb_idx]
        return cls(id=orb_id)


class Health(BaseModel):
    hp: int = Field(..., ge=0, lt=2**constants.LOG_MAX_HP)
    max_hp: int = Field(..., ge=0, lt=2**constants.LOG_MAX_HP)

    def serialize(self) -> dict:
        return {
            "hp": utils.to_binary_array(self.hp, constants.LOG_MAX_HP),
            "max_hp": utils.to_binary_array(self.max_hp, constants.LOG_MAX_HP),
        }

    class SerializedState(BaseModel):
        hp: BinaryArray
        max_hp: BinaryArray

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> Health:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        hp = utils.from_binary_array(data.hp)
        max_hp = utils.from_binary_array(data.max_hp)

        return cls(hp=hp, max_hp=max_hp)


class Attack(BaseModel):
    damage: int = Field(..., ge=0, lt=2**constants.LOG_MAX_ATTACK)
    times: int = Field(..., ge=0, lt=2**constants.LOG_MAX_ATTACK_TIMES)

    def serialize(self):
        return {
            "damage": utils.to_binary_array(self.damage, constants.LOG_MAX_ATTACK),
            "times": utils.to_binary_array(self.times, constants.LOG_MAX_ATTACK_TIMES),
        }

    class SerializedState(BaseModel):
        damage: BinaryArray
        times: BinaryArray

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> Attack:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        return cls(
            damage=utils.from_binary_array(data.damage),
            times=utils.from_binary_array(data.times),
        )


class Enemy(BaseModel):
    id: str
    intent: str
    current_hp: int = Field(..., ge=0, lt=2**constants.LOG_MAX_HP)
    max_hp: int = Field(..., ge=0, lt=2**constants.LOG_MAX_HP)
    block: int = Field(..., ge=0, lt=2**constants.LOG_MAX_BLOCK)
    effects: list[Effect] = Field([], alias="powers")
    is_gone: bool = False  # TODO serialize?

    # These attribues may not be set if the player has runic dome
    damage: int = Field(
        0, alias="move_adjusted_damage", ge=0, lt=2**constants.LOG_MAX_ATTACK
    )
    times: int = Field(
        0, alias="move_hits", ge=0, lt=2**constants.LOG_MAX_ATTACK_TIMES
    )

    @staticmethod
    def serialize_empty() -> dict:
        serialized = {
            "id": 0,
            "intent": 0,
            "attack": Attack(damage=0, times=0).serialize(),
            "block": utils.to_binary_array(0, constants.LOG_MAX_BLOCK),
            "effects": Effect.serialize_all([]),
            "health": Health(hp=0, max_hp=0).serialize(),
        }

        return serialized

    def serialize(self) -> dict:
        serialized = {
            "id": constants.ALL_MONSTER_TYPES.index(self.id),
            "intent": constants.ALL_INTENTS.index(self.intent),
            "attack": Attack(damage=self.damage, times=self.times).serialize(),
            "block": utils.to_binary_array(self.block, constants.LOG_MAX_BLOCK),
            "effects": Effect.serialize_all(self.effects),
            "health": Health(hp=self.current_hp, max_hp=self.max_hp).serialize(),
        }

        return serialized

    class SerializedState(BaseModel):
        id: int
        intent: int
        attack: Attack.SerializedState
        block: BinaryArray
        effects: list[dict]
        health: Health.SerializedState

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> Enemy:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        effects = []
        for effect_idx, e in enumerate(data.effects):
            effect = Effect.deserialize(e)
            if effect.amount != 0:
                effect.id = constants.ALL_EFFECTS[effect_idx]
                effects.append(effect)

        health = Health.deserialize(data.health)
        attack = Attack.deserialize(data.attack)

        return cls(
            id=constants.ALL_MONSTER_TYPES[data.id],
            intent=constants.ALL_INTENTS[data.intent],
            block=utils.from_binary_array(data.block),
            effects=effects,
            current_hp=health.hp,
            max_hp=health.max_hp,
            damage=attack.damage,
            times=attack.times,
        )
