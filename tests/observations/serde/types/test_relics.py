from typing import Union

from hypothesis import given
from hypothesis import strategies as st

from gym_sts.spaces.constants.relics import RelicCatalog
from gym_sts.spaces.observations.types import Relic, RelicBase, ShopRelic


@st.composite
def create_relic_base(draw, relic_ids=st.sampled_from(RelicCatalog.ids)):
    relic_id = draw(relic_ids)
    relic_metadata = getattr(RelicCatalog, relic_id)

    return draw(
        st.builds(
            RelicBase,
            id=st.just(relic_id),
            name=st.just(relic_metadata.name),
        )
    )


@given(create_relic_base())
def test_relic_base_serde_binary(relic: RelicBase):
    ser = relic.serialize()
    de = relic.deserialize(ser)

    assert relic == de


@given(create_relic_base())
def test_relic_base_serde_discrete(relic: RelicBase):
    ser = relic.serialize(discrete=True)
    de = relic.deserialize(ser)

    assert relic == de


def test_relic_base_serde_empty_binary():
    ser = RelicBase.serialize_empty()
    de = RelicBase.deserialize(ser)

    assert de.id == RelicCatalog.NONE.id


def test_relic_base_serde_empty_discrete():
    ser = RelicBase.serialize_empty(discrete=True)
    de = RelicBase.deserialize(ser)

    assert de.id == RelicCatalog.NONE.id


def create_relic_subclass(Model: Union[type[Relic], type[ShopRelic]]):
    @st.composite
    def create_subclass(draw, relic_bases=create_relic_base()):
        relic_base = draw(relic_bases)

        return draw(
            st.builds(
                Model,
                id=st.just(relic_base.id),
                name=st.just(relic_base.name),
            )
        )

    return create_subclass()


@given(create_relic_subclass(Relic))
def test_relic_serde(relic: Relic):
    ser = relic.serialize()
    de = relic.deserialize(ser)

    assert relic == de


def test_relic_serde_empty():
    ser = Relic.serialize_empty()
    de = Relic.deserialize(ser)

    assert de.id == RelicCatalog.NONE.id


@given(create_relic_subclass(ShopRelic))
def test_shop_relic_serde(relic: ShopRelic):
    ser = relic.serialize()
    de = relic.deserialize(ser)

    assert relic == de


def test_shop_relic_serde_empty():
    ser = ShopRelic.serialize_empty()
    de = ShopRelic.deserialize(ser)

    assert de.id == RelicCatalog.NONE.id
    assert de.price == 0
