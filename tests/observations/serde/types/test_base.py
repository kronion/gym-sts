from hypothesis import given
from hypothesis import strategies as st

import gym_sts.spaces.old_constants as constants
from gym_sts.spaces.observations.types.base import (
    Effect,
    Enemy,
    Health,
    Keys,
    Orb,
    ShopMixin,
)


@given(st.builds(Effect, id=st.sampled_from(constants.ALL_EFFECTS)))
def test_effect_serde(effect: Effect):
    ser = effect.serialize()
    de = effect.deserialize(ser)

    # Note that the effect ID isn't serialized, so it's not recovered
    # TODO serialize ID as well and then discard if unwanted
    assert effect.amount == de.amount


@given(
    st.builds(
        Enemy,
        id=st.sampled_from(constants.ALL_MONSTER_TYPES),
        intent=st.sampled_from(constants.ALL_INTENTS),
    )
)
def test_enemy_serde(enemy: Enemy):
    ser = enemy.serialize()
    de = enemy.deserialize(ser)

    assert enemy == de


@given(st.builds(Health))
def test_health_serde(health: Health):
    ser = health.serialize()
    de = health.deserialize(ser)

    assert health == de


@given(st.builds(Keys))
def test_keys_serde(keys: Keys):
    ser = keys.serialize()
    de = Keys.deserialize(ser)
    assert keys == de


@given(st.builds(Orb, id=st.sampled_from(constants.ALL_ORBS)))
def test_orb_serde(orb: Orb):
    ser = orb.serialize()
    de = orb.deserialize(ser)

    assert orb == de


@given(st.builds(ShopMixin))
def test_shop_mixin_serde(mixin: ShopMixin):
    ser = mixin.serialize_price()
    de = ShopMixin.deserialize_price(ser)

    assert mixin.price == de


def test_shop_mixin_serde_empty():
    ser = ShopMixin.serialize_empty_price()
    de = ShopMixin.deserialize_price(ser)

    assert de == 0
