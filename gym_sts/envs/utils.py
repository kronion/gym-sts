import random
import typing as tp
from typing import Optional

import numpy as np

from gym_sts.spaces.observations import Observation


class SeedHelpers:
    char_set = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"  # Note no O

    @classmethod
    def make_seed_str(cls, seed_long: int) -> str:
        """
        Based on code from com/megacrit/cardcrawl/helpers/SeedHelper.java
        """

        base = len(cls.char_set)

        seed_str = ""
        while seed_long != 0:
            seed_long, remainder = divmod(seed_long, base)
            char = cls.char_set[remainder]
            seed_str = char + seed_str

        return seed_str

    @classmethod
    def make_seed(cls, rng: random.Random) -> str:
        unsigned_long = 2**64
        seed_long = rng.randrange(unsigned_long)

        return cls.make_seed_str(seed_long)

    @classmethod
    def validate_seed(cls, seed: str) -> str:
        """
        Returns the seed if it's valid, raises a ValueError otherwise.
        """

        seed = seed.upper()
        for char in seed:
            if char not in cls.char_set:
                raise ValueError(f"Seed contains illegal character '{char}'")

        return seed


T = tp.TypeVar("T")


class Cache(tp.Generic[T]):
    def __init__(self, size: int = 10):
        self.size = size
        self.index = 0
        self.cache: list[Optional[T]] = [None] * self.size

    def append(self, obs: T):
        self.cache[self.index] = obs
        self.index = (self.index + 1) % self.size

    def get(self, ago: int = 0) -> Optional[T]:
        """
        Args:
            ago: The number of items back to retrieve (zero indexed).
                The value must be less than the cache size.
        """

        if ago >= self.size:
            raise ValueError(f"ago must be less than the cache size ({self.size})")

        index = (self.index - ago - 1) % self.size
        return self.cache[index]

    def reset(self) -> None:
        self.cache = [None] * self.size


def obs_value(obs: Observation) -> float:
    """Useful for creating a reward function."""
    value = float(obs.persistent_state.floor)
    value += obs.persistent_state.hp / 100
    return value


def single_combat_value(obs: Observation) -> float:
    max_hp = sum(e.max_hp for e in obs.combat_state.enemies)
    enemy_hp = sum(e.current_hp for e in obs.combat_state.enemies)

    self_hp = obs.persistent_state.hp
    self_max_hp = obs.persistent_state.max_hp

    if max_hp == 0:
        enemy_hp = 0
        max_hp = 1

    p_damage = (max_hp - enemy_hp) / max_hp
    p_hp = self_hp / self_max_hp

    return float(np.prod([p_hp, p_damage]) + p_damage * 0.01)
