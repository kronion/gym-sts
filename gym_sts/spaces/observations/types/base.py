from __future__ import annotations

from typing import Union

import numpy as np
import numpy.typing as npt
from gymnasium.spaces import Dict, Discrete, MultiBinary
from pydantic import BaseModel, Field, validator

import gym_sts.spaces.constants.base as base_consts
import gym_sts.spaces.constants.combat as combat_consts
import gym_sts.spaces.constants.shop as shop_consts
from gym_sts.spaces.observations import spaces, utils


BinaryArray = npt.NDArray[np.uint]


class ShopMixin(BaseModel):
    price: int = Field(..., ge=0, lt=2**shop_consts.SHOP_LOG_MAX_PRICE)

    @staticmethod
    def serialize_empty_price():
        return utils.to_binary_array(0, shop_consts.SHOP_LOG_MAX_PRICE)

    def serialize_price(self):
        return utils.to_binary_array(self.price, shop_consts.SHOP_LOG_MAX_PRICE)

    @staticmethod
    def deserialize_price(price: BinaryArray) -> int:
        return utils.from_binary_array(price)


class Keys(BaseModel):
    emerald: bool = False
    ruby: bool = False
    sapphire: bool = False

    def serialize(self) -> BinaryArray:
        _keys = [self.ruby, self.emerald, self.sapphire]
        return np.array([int(key) for key in _keys])

    @classmethod
    def deserialize(cls, data: BinaryArray) -> Keys:
        ruby, emerald, sapphire = data
        return cls(ruby=ruby, emerald=emerald, sapphire=sapphire)


class Effect(BaseModel):
    id: str = "EMPTY"  # Placeholder should always be replaced
    amount: int = Field(..., ge=-combat_consts.MAX_EFFECT, le=combat_consts.MAX_EFFECT)

    def serialize(self) -> dict:
        sign = 0
        value = self.amount

        if self.amount < 0:
            sign = 1
            value = -value

        return {
            "sign": sign,
            "value": utils.to_binary_array(value, combat_consts.LOG_MAX_EFFECT),
        }

    @staticmethod
    def serialize_all(effects: list[Effect]) -> list[dict]:
        serialized = []
        effect_map = {effect.id: effect for effect in effects}

        for effect_id in combat_consts.ALL_EFFECTS:
            encoding = {
                "sign": 0,
                "value": utils.to_binary_array(0, combat_consts.LOG_MAX_EFFECT),
            }
            if effect_id in effect_map:
                effect = effect_map[effect_id]
                encoding = effect.serialize()

            serialized.append(encoding)

        return serialized

    class SerializedState(BaseModel):
        sign: int = Field(..., ge=0, le=1)
        value: BinaryArray

        class Config:
            arbitrary_types_allowed = True

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
        return combat_consts.ALL_ORBS.index("NONE")

    def serialize(self) -> int:
        return combat_consts.ALL_ORBS.index(self.id)

    @classmethod
    def deserialize(cls, orb_idx: int) -> Orb:
        orb_id = combat_consts.ALL_ORBS[orb_idx]
        return cls(id=orb_id)


class Health(BaseModel):
    hp: int = Field(..., ge=0, le=base_consts.MAX_HP)
    max_hp: int = Field(..., ge=0, le=base_consts.MAX_HP)

    def serialize(self) -> dict:
        return {
            "hp": utils.to_binary_array(self.hp, base_consts.LOG_MAX_HP),
            "max_hp": utils.to_binary_array(self.max_hp, base_consts.LOG_MAX_HP),
        }

    class SerializedState(BaseModel):
        hp: BinaryArray
        max_hp: BinaryArray

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> Health:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        hp = utils.from_binary_array(data.hp)
        max_hp = utils.from_binary_array(data.max_hp)

        return cls(hp=hp, max_hp=max_hp)


class Attack(BaseModel):
    damage: int = Field(..., ge=0, le=combat_consts.MAX_ATTACK)
    times: int = Field(..., ge=0, lt=combat_consts.MAX_ATTACK_TIMES)

    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "damage": MultiBinary(combat_consts.LOG_MAX_ATTACK),
                "times": MultiBinary(combat_consts.LOG_MAX_ATTACK_TIMES),
            }
        )

    def serialize(self):
        return {
            "damage": utils.to_binary_array(self.damage, combat_consts.LOG_MAX_ATTACK),
            "times": utils.to_binary_array(
                self.times, combat_consts.LOG_MAX_ATTACK_TIMES
            ),
        }

    class SerializedState(BaseModel):
        damage: BinaryArray
        times: BinaryArray

        class Config:
            arbitrary_types_allowed = True

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
    current_hp: int = Field(..., ge=0, le=base_consts.MAX_HP)
    max_hp: int = Field(..., ge=0, le=base_consts.MAX_HP)
    block: int = Field(..., ge=0, le=combat_consts.MAX_BLOCK)
    effects: list[Effect] = Field([], alias="powers")

    # These attribues may not be set if the player has runic dome
    damage: int = Field(
        0, alias="move_adjusted_damage", ge=0, le=combat_consts.MAX_ATTACK
    )
    times: int = Field(0, alias="move_hits", ge=0, le=combat_consts.MAX_ATTACK_TIMES)

    @validator("damage", pre=True)
    def must_be_nonnegative(cls, v: int) -> int:
        return max(0, v)

    @staticmethod
    def space() -> Dict:
        return Dict(
            {
                "id": Discrete(combat_consts.NUM_MONSTER_TYPES),
                "intent": Discrete(combat_consts.NUM_INTENTS),
                "attack": Attack.space(),
                "block": MultiBinary(combat_consts.LOG_MAX_BLOCK),
                "effects": spaces.generate_effect_space(),
                "health": spaces.generate_health_space(),
            }
        )

    @staticmethod
    def serialize_empty() -> dict:
        serialized = {
            "id": 0,
            "intent": 0,
            "attack": Attack(damage=0, times=0).serialize(),
            "block": utils.to_binary_array(0, combat_consts.LOG_MAX_BLOCK),
            "effects": Effect.serialize_all([]),
            "health": Health(hp=0, max_hp=0).serialize(),
        }

        return serialized

    def serialize(self) -> dict:
        serialized = {
            "id": combat_consts.ALL_MONSTER_TYPES.index(self.id),
            "intent": combat_consts.ALL_INTENTS.index(self.intent),
            "attack": Attack(damage=self.damage, times=self.times).serialize(),
            "block": utils.to_binary_array(self.block, combat_consts.LOG_MAX_BLOCK),
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

        class Config:
            arbitrary_types_allowed = True

    @classmethod
    def deserialize(cls, data: Union[dict, SerializedState]) -> Enemy:
        if not isinstance(data, cls.SerializedState):
            data = cls.SerializedState(**data)

        effects = []
        for effect_idx, e in enumerate(data.effects):
            effect = Effect.deserialize(e)
            if effect.amount != 0:
                effect.id = combat_consts.ALL_EFFECTS[effect_idx]
                effects.append(effect)

        health = Health.deserialize(data.health)
        attack = Attack.deserialize(data.attack)

        return cls(
            id=combat_consts.ALL_MONSTER_TYPES[data.id],
            intent=combat_consts.ALL_INTENTS[data.intent],
            block=utils.from_binary_array(data.block),
            powers=effects,
            current_hp=health.hp,
            max_hp=health.max_hp,
            move_adjusted_damage=attack.damage,
            move_hits=attack.times,
        )
