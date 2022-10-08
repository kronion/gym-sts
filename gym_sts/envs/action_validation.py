from gym_sts.spaces import actions
from gym_sts.spaces.observations import Observation


def validate_end_turn(action: actions.EndTurn, observation: Observation) -> bool:
    return "end" in observation._available_commands


def validate_return(action: actions.Return, observation: Observation) -> bool:
    for word in ["cancel", "leave", "return", "skip"]:
        if word in observation._available_commands:
            return True

    return False


def validate_proceed(action: actions.Proceed, observation: Observation) -> bool:
    for word in ["confirm", "proceed"]:
        if word in observation._available_commands:
            return True

    return False


def _validate_choice(action: actions.Choose, observation: Observation) -> bool:
    return action.choice_index < len(observation.choice_list)


def validate_choose(action: actions.Choose, observation: Observation) -> bool:
    if "choose" not in observation._available_commands:
        return False

    if observation.in_combat:
        if observation.screen_type in ["CARD_REWARD", "GRID", "HAND_SELECT"]:
            return _validate_choice(action, observation)
        else:
            # TODO determine if there are any other choices that could
            # be made mid-combat, such as picking from deck/discard/exhaust,
            # or scrying.
            print("NOT IMPLEMENTED")
            return False
    elif observation.screen_type in [
        "CARD_REWARD",
        "CHEST",
        "COMBAT_REWARD",
        "EVENT",
        "GRID",
        "MAP",
        "REST",
        "SHOP_ROOM",
        "SHOP_SCREEN",
    ]:
        return _validate_choice(action, observation)
    else:
        # TODO handle choices outside of combat, like events
        print("NOT IMPLEMENTED")
        return True


def validate_play(action: actions.PlayCard, observation: Observation) -> bool:
    if "play" not in observation._available_commands:
        return False

    if not observation.in_combat or observation.screen_type != "NONE":
        return False

    # Choices correspond to playing cards
    hand = observation.combat_state.hand
    index = action.card_position
    # Adjust to account for CommunicationMod's odd indexing scheme.
    index -= 1
    if index < 0:
        index += 10

    if index >= len(hand):
        return False

    card = hand[index]

    target_index = action.target_index

    # Technically it should be invalid to specify a target if the card
    # doesn't take a target (and this would cut down on the number of valid
    # actions), but the game simply ignores the target choice, so it's not an
    # error. Because we only want actions to be invalid if the game truly won't
    # accept them, we've commented this validation check out for now.
    # if target_index is not None and not card.has_target:
    #     return False

    if target_index is None and card.has_target:
        return False

    enemies = observation.combat_state.enemies
    if target_index is not None:
        # Even if the card doesn't take a target, STS still requires the stated
        # target index to be in bounds.
        if target_index >= len(enemies):
            return False

        # We confirm the card actually takes a target. If it doesn't, the target
        # selection is ignored anyway.
        if card.has_target:
            enemy = enemies[target_index]
            if enemy["is_gone"]:
                return False

    return card.is_playable


def _validate_potion(
    action: actions.PotionAction, observation: Observation, prop: str
) -> bool:
    if "potion" not in observation._available_commands:
        return False

    index = action.potion_index
    potions = observation.persistent_state.potions
    if index >= len(potions):
        return False

    potion = potions[index]
    return getattr(potion, prop)


def validate_use_potion(action: actions.UsePotion, observation: Observation) -> bool:
    if not _validate_potion(action, observation, "can_use"):
        return False

    index = action.potion_index
    potions = observation.persistent_state.potions
    potion = potions[index]

    target_index = action.target_index

    # Technically it should be invalid to specify a target if the card
    # doesn't take a target (and this would cut down on the number of valid
    # actions), but the game simply ignores the target choice, so it's not an
    # error. Because we only want actions to be invalid if the game truly won't
    # accept them, we've commented this validation check out for now.
    # if target_index is not None and not potion.requires_target:
    #     return False

    if potion.requires_target:
        # Explosive Potion is basically incorrectly defined within STS.
        # It doesn't actually require a target.
        if potion.id == "Explosive Potion":
            return True

        if target_index is None:
            return False

        # Unlike when playing cards, STS disregards out-of-range target indices
        # when using potions that don't take a target.
        enemies = observation.combat_state.enemies
        if target_index >= len(enemies):
            return False

    return True


def validate_discard_potion(
    action: actions.DiscardPotion, observation: Observation
) -> bool:
    return _validate_potion(action, observation, "can_discard")


def validate(action: actions.Action, observation: Observation) -> bool:
    if isinstance(action, actions.EndTurn):
        return validate_end_turn(action, observation)

    elif isinstance(action, actions.Return):
        return validate_return(action, observation)

    elif isinstance(action, actions.Proceed):
        return validate_proceed(action, observation)

    elif isinstance(action, actions.Choose):
        return validate_choose(action, observation)

    elif isinstance(action, actions.UsePotion):
        return validate_use_potion(action, observation)

    elif isinstance(action, actions.DiscardPotion):
        return validate_discard_potion(action, observation)

    elif isinstance(action, actions.PlayCard):
        return validate_play(action, observation)

    raise ValueError("Unrecognized action type")


def get_valid(observation: Observation):
    # Note: this method is rather inefficient. We could instead generate the
    # valid actions from the observation.
    return [a for a in actions.ACTIONS if validate(a, observation)]
