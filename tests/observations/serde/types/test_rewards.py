from hypothesis import given
from hypothesis import strategies as st

import gym_sts.spaces.constants.base as base_consts
from gym_sts.spaces.observations import types

from .test_potions import create_potion_base
from .test_relics import create_relic_base


@given(st.builds(types.GoldReward))
def test_gold_reward_serde(reward: types.GoldReward):
    ser = reward.serialize()
    de = reward.deserialize(ser)

    assert reward == de


@st.composite
def create_potion_reward(draw, potions=create_potion_base()):
    potion = draw(potions)
    return types.PotionReward(value=potion)


@given(create_potion_reward())
def test_potion_reward_serde(reward: types.PotionReward):
    ser = reward.serialize()
    de = reward.deserialize(ser)

    assert reward == de


@st.composite
def create_relic_reward(draw, relics=create_relic_base()):
    relic = draw(relics)
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


@given(st.builds(types.KeyReward, value=st.sampled_from(base_consts.ALL_KEYS)))
def test_key_reward_serde(reward: types.KeyReward):
    ser = reward.serialize()
    de = reward.deserialize(ser)

    assert reward == de
