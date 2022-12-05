import numpy as np
from hypothesis import given
from hypothesis import strategies as st

import gym_sts.spaces.old_constants as constants
from gym_sts.spaces.constants.cards import CardCatalog
from gym_sts.spaces.observations import types


def test_card_empty_binary_serde():
    initial_ser = types.Card.serialize_empty_binary()
    card = types.Card.deserialize_binary(initial_ser)
    final_ser = card.serialize_binary()

    assert np.array_equal(initial_ser, final_ser)


@given(st.builds(types.Card, id=st.sampled_from(CardCatalog.ids)))
def test_card_binary_serde(card: types.Card):
    ser = card.serialize_binary()
    de = card.deserialize_binary(ser)

    assert card.id == de.id

    # Really de.upgrades should equal card.upgrades, but it doesn't because our current
    # serialization doesn't support more than one upgrades
    assert card.upgrades == de.upgrades == 0 or card.upgrades > 0 and de.upgrades > 0


@given(st.builds(types.HandCard, id=st.sampled_from(CardCatalog.ids)))
def test_hand_card_serde(card: types.HandCard):
    ser = card.serialize()
    de = card.deserialize(ser)

    assert card.id == de.id
    assert card.is_playable == de.is_playable

    # Really de.upgrades should equal card.upgrades, but it doesn't because our current
    # serialization doesn't support more than one upgrades
    assert card.upgrades == de.upgrades == 0 or card.upgrades > 0 and de.upgrades > 0


@given(st.builds(types.Potion, id=st.sampled_from(constants.ALL_POTIONS)))
def test_potion_serde(potion: types.Potion):
    ser = potion.serialize()
    de = potion.deserialize(ser)

    assert potion.id == de.id


@given(st.builds(types.Relic, id=st.sampled_from(constants.ALL_RELICS)))
def test_relic_serde(relic: types.Relic):
    ser = relic.serialize()
    de = relic.deserialize(ser)

    assert relic.id == de.id


@given(st.builds(types.ShopCard, id=st.sampled_from(CardCatalog.ids)))
def test_shop_card_serde(card: types.ShopCard):
    ser = card.serialize()
    de = card.deserialize(ser)

    assert card.id == de.id
    assert card.price == de.price

    # Really de.upgrades should equal card.upgrades, but it doesn't because our current
    # serialization doesn't support more than one upgrades
    assert card.upgrades == de.upgrades == 0 or card.upgrades > 0 and de.upgrades > 0


@given(st.builds(types.ShopPotion, id=st.sampled_from(constants.ALL_POTIONS)))
def test_shop_potion_serde(potion: types.ShopPotion):
    ser = potion.serialize()
    de = potion.deserialize(ser)

    assert potion.id == de.id
    assert potion.price == de.price


@given(st.builds(types.ShopRelic, id=st.sampled_from(constants.ALL_RELICS)))
def test_shop_relic_serde(relic: types.ShopRelic):
    ser = relic.serialize()
    de = relic.deserialize(ser)

    assert relic.id == de.id
    assert relic.price == de.price


@given(st.builds(types.Effect, id=st.sampled_from(constants.ALL_EFFECTS)))
def test_effect_serde(effect: types.Effect):
    ser = effect.serialize()
    de = effect.deserialize(ser)

    # Note that the effect ID isn't serialized, so it's not recovered
    assert effect.amount == de.amount


@given(st.builds(types.Orb, id=st.sampled_from(constants.ALL_ORBS)))
def test_orb_serde(orb: types.Orb):
    ser = orb.serialize()
    de = orb.deserialize(ser)

    assert orb == de


@given(st.builds(types.Health))
def test_health_serde(health: types.Health):
    ser = health.serialize()
    de = health.deserialize(ser)

    assert health == de


@given(
    st.builds(
        types.Enemy,
        id=st.sampled_from(constants.ALL_MONSTER_TYPES),
        intent=st.sampled_from(constants.ALL_INTENTS),
    )
)
def test_enemy_serde(enemy: types.Enemy):
    ser = enemy.serialize()
    de = enemy.deserialize(ser)

    assert enemy == de


@given(st.builds(types.GoldReward))
def test_gold_reward_serde(reward: types.GoldReward):
    ser = reward.serialize()
    de = reward.deserialize(ser)

    assert reward == de


@st.composite
def create_potion_reward(
    draw, elements=st.builds(types.Potion, id=st.sampled_from(constants.ALL_POTIONS))
):
    potion = draw(elements)
    return types.PotionReward(value=potion)


@given(create_potion_reward())
def test_potion_reward_serde(reward: types.PotionReward):
    ser = reward.serialize()
    de = reward.deserialize(ser)

    assert reward == de


@st.composite
def create_relic_reward(
    draw, elements=st.builds(types.Relic, id=st.sampled_from(constants.ALL_RELICS))
):
    relic = draw(elements)
    return types.RelicReward(value=relic)


@given(create_relic_reward())
def test_relic_reward_serde(reward: types.RelicReward):
    ser = reward.serialize()
    de = reward.deserialize(ser)

    assert reward == de


@given(st.builds(types.CardReward))
def test_card_reward_serde(reward: types.CardReward):
    ser = reward.serialize()
    de = reward.deserialize(ser)

    assert reward == de


@given(st.builds(types.KeyReward, value=st.sampled_from(constants.ALL_KEYS)))
def test_key_reward_serde(reward: types.KeyReward):
    ser = reward.serialize()
    de = reward.deserialize(ser)

    assert reward == de
