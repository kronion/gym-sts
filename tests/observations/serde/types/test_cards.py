from typing import Union

from hypothesis import given
from hypothesis import strategies as st

from gym_sts.spaces.constants.cards import CardCatalog, CardMetadata
from gym_sts.spaces.observations.types import Card, HandCard, ShopCard


@st.composite
def create_card(
    draw, card_ids=st.sampled_from(CardCatalog.ids), upgrades=st.booleans()
):
    card_id = draw(card_ids)
    upgraded = draw(upgrades)
    card_metadata: CardMetadata = getattr(CardCatalog, card_id)
    card_props = card_metadata.upgraded if upgraded else card_metadata.unupgraded

    return draw(
        st.builds(
            Card,
            id=st.just(card_id),
            name=st.just(card_metadata.name),
            cost=st.just(card_props.default_cost),
            exhausts=st.just(card_props.exhausts),
            ethereal=st.just(card_props.ethereal),
            has_target=st.just(card_props.has_target),
            upgrades=st.just(int(upgraded)),
        )
    )


@given(create_card())
def test_card_serde_binary(card: Card):
    ser = card.serialize()
    de = card.deserialize(ser)

    assert card == de


@given(create_card())
def test_card_serde_discrete(card: Card):
    ser = card.serialize(discrete=True)
    de = card.deserialize(ser)

    assert card == de


def test_card_serde_empty_binary():
    ser = Card.serialize_empty()
    de = Card.deserialize(ser)

    assert de.id == CardCatalog.NONE.id


def test_card_serde_empty_discrete():
    ser = Card.serialize_empty(discrete=True)
    de = Card.deserialize(ser)

    assert de.id == CardCatalog.NONE.id


def create_card_subclass(Model: Union[type[HandCard], type[ShopCard]]):
    @st.composite
    def create_subclass(draw, cards=create_card()):
        card = draw(cards)

        return draw(
            st.builds(
                Model,
                id=st.just(card.id),
                name=st.just(card.name),
                cost=st.just(card.cost),
                exhausts=st.just(card.exhausts),
                ethereal=st.just(card.ethereal),
                has_target=st.just(card.has_target),
                upgrades=st.just(card.upgrades),
            )
        )

    return create_subclass()


@given(create_card_subclass(HandCard))
def test_hand_card_serde(card: HandCard):
    ser = card.serialize()
    de = card.deserialize(ser)

    assert card == de


def test_hand_card_serde_empty():
    ser = HandCard.serialize_empty()
    de = HandCard.deserialize(ser)

    assert de.id == CardCatalog.NONE.id


@given(create_card_subclass(ShopCard))
def test_shop_card_serde(card: ShopCard):
    ser = card.serialize()
    de = card.deserialize(ser)

    assert card == de


def test_shop_potion_serde_empty():
    ser = ShopCard.serialize_empty()
    de = ShopCard.deserialize(ser)

    assert de.id == CardCatalog.NONE.id
    assert de.price == 0
