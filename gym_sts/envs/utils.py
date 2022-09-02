from gym_sts.spaces import actions
from gym_sts.spaces.observations import Observation


class ActionValidators:
    @staticmethod
    def validate_end_turn(action: actions.EndTurn, observation: Observation) -> bool:
        return "end" in observation._available_commands

    @staticmethod
    def validate_return(action: actions.Return, observation: Observation) -> bool:
        for word in ["cancel", "leave", "return", "skip"]:
            if word in observation._available_commands:
                return True

        return False

    @staticmethod
    def validate_proceed(action: actions.Proceed, observation: Observation) -> bool:
        for word in ["confirm", "proceed"]:
            if word in observation._available_commands:
                return True

        return False

    @staticmethod
    def _validate_hand_select(action: actions.Choose, observation: Observation) -> bool:
        # If the maximum number of selection has been hit, no more choices are allowed.
        selects = observation.combat_state.hand_selects
        max_selects = observation.combat_state.max_selects
        if len(selects) == max_selects:
            return False

        # Choices correspond to selecting cards
        hand = observation.combat_state.hand
        index = action.choice_index
        return index < len(hand)

    @staticmethod
    def _validate_campfire(action: actions.Choose, observation: Observation) -> bool:
        campfire_state = observation.campfire_state
        index = action.choice_index
        return index < campfire_state.num_options

    @staticmethod
    def _validate_shop(action: actions.Choose, observation: Observation) -> bool:
        index = action.choice_index
        shop_state = observation.shop_state
        gold = observation.persistent_state.gold

        prices = []
        if shop_state.purge_available:
            prices.append(shop_state.purge_price)

        for card in shop_state.cards:
            prices.append(card.price)

        for relic in shop_state.relics:
            prices.append(relic.price)

        for potion in shop_state.potions:
            prices.append(potion.price)

        if index >= len(prices):
            return False

        price = prices[index]
        return price <= gold

    @classmethod
    def validate_choose(cls, action: actions.Choose, observation: Observation) -> bool:
        if "choose" not in observation._available_commands:
            return False

        if observation.in_combat:
            if observation.screen_type == "HAND_SELECT":
                return cls._validate_hand_select(action, observation)
            else:
                # TODO determine if there are any other choices that could
                # be made mid-combat, such as picking from deck/discard/exhaust,
                # or scrying.
                print("NOT IMPLEMENTED")
                return False
        elif observation.screen_type == "REST":
            return cls._validate_campfire(action, observation)
        elif observation.screen_type == "COMBAT_REWARD":
            print("NOT IMPLEMENTED")
            return True
        elif observation.screen_type == "CARD_REWARD":
            print("NOT IMPLEMENTED")
            return True
        elif observation.screen_type == "SHOP_SCREEN":
            return cls._validate_shop(action, observation)
        else:
            # TODO handle choices outside of combat, like events, map
            print("NOT IMPLEMENTED")
            return True

    @staticmethod
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
        if target_index is not None and not card.has_target:
            return False
        if target_index is None and card.has_target:
            return False

        enemies = observation.combat_state.enemies
        if target_index is not None and target_index >= len(enemies):
            return False

        return card.is_playable

    @staticmethod
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

    @classmethod
    def validate_use_potion(
        cls, action: actions.UsePotion, observation: Observation
    ) -> bool:
        if not cls._validate_potion(action, observation, "can_use"):
            return False

        index = action.potion_index
        potions = observation.persistent_state.potions
        potion = potions[index]

        target_index = action.target_index
        if target_index is not None and not potion.requires_target:
            return False
        if target_index is None and potion.requires_target:
            return False

        enemies = observation.combat_state.enemies
        if target_index is not None and target_index >= len(enemies):
            return False

        return True

    @classmethod
    def validate_discard_potion(
        cls, action: actions.DiscardPotion, observation: Observation
    ) -> bool:
        return cls._validate_potion(action, observation, "can_discard")

    @classmethod
    def validate(cls, action: actions.Action, observation: Observation) -> bool:
        if isinstance(action, actions.EndTurn):
            return cls.validate_end_turn(action, observation)

        elif isinstance(action, actions.Return):
            return cls.validate_return(action, observation)

        elif isinstance(action, actions.Proceed):
            return cls.validate_proceed(action, observation)

        elif isinstance(action, actions.Choose):
            return cls.validate_choose(action, observation)

        elif isinstance(action, actions.UsePotion):
            return cls.validate_use_potion(action, observation)

        elif isinstance(action, actions.DiscardPotion):
            return cls.validate_discard_potion(action, observation)

        elif isinstance(action, actions.PlayCard):
            return cls.validate_play(action, observation)

        raise ValueError("Unrecognized action type")
