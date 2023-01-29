from typing import Union

from hypothesis import given
from hypothesis import strategies as st

from gym_sts.spaces.constants.potions import PotionCatalog
from gym_sts.spaces.observations.types import Potion, PotionBase, ShopPotion


@st.composite
def create_potion_base(draw, potion_id=st.sampled_from(PotionCatalog.ids)):
    potion_id = draw(potion_id)
    potion_metadata = getattr(PotionCatalog, potion_id)

    return draw(
        st.builds(
            PotionBase,
            id=st.just(potion_id),
            name=st.just(potion_metadata.name),
            requires_target=st.just(potion_metadata.requires_target),
        )
    )


@given(create_potion_base())
def test_potion_base_serde_binary(potion: PotionBase):
    ser = potion.serialize()
    de = potion.deserialize(ser)

    assert potion == de


@given(create_potion_base())
def test_potion_base_serde_discrete(potion: PotionBase):
    ser = potion.serialize(discrete=True)
    de = potion.deserialize(ser)

    assert potion == de


def test_potion_base_serde_empty_binary():
    ser = PotionBase.serialize_empty()
    de = PotionBase.deserialize(ser)

    assert de.id == PotionCatalog.NONE.id


def test_potion_base_serde_empty_discrete():
    ser = PotionBase.serialize_empty(discrete=True)
    de = PotionBase.deserialize(ser)

    assert de.id == PotionCatalog.NONE.id


def create_potion_subclass(Model: Union[type[Potion], type[ShopPotion]]):
    @st.composite
    def create_subclass(draw, potion_bases=create_potion_base()):
        potion_base = draw(potion_bases)

        return draw(
            st.builds(
                Model,
                id=st.just(potion_base.id),
                name=st.just(potion_base.name),
                requires_target=st.just(potion_base.requires_target),
            )
        )

    return create_subclass()


@given(create_potion_subclass(Potion))
def test_potion_serde(potion: Potion):
    ser = potion.serialize()
    de = potion.deserialize(ser)

    assert potion == de


def test_potion_serde_empty():
    ser = Potion.serialize_empty()
    de = Potion.deserialize(ser)

    assert de.id == PotionCatalog.NONE.id


@given(create_potion_subclass(ShopPotion))
def test_shop_potion_serde(potion: ShopPotion):
    ser = potion.serialize()
    de = potion.deserialize(ser)

    assert potion == de


def test_shop_potion_serde_empty():
    ser = ShopPotion.serialize_empty()
    de = ShopPotion.deserialize(ser)

    assert de.id == PotionCatalog.NONE.id
    assert de.price == 0
