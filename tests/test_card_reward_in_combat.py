import time

from gym_sts.envs.action_validation import get_valid
from gym_sts.spaces import actions


def test_card_reward_valid_in_combat(env):
    env.reset(seed=42)

    env.communicator.basemod("deck remove all")
    env.communicator.basemod("deck add Discovery")
    time.sleep(0.5)  # Wait briefly for card adding animation to complete
    env.communicator.basemod("fight Jaw_Worm")

    # At this point the only card in hand is Discovery
    # TODO make action selection easier
    action_id = actions.ACTIONS.index(
        actions.PlayCard(card_position=1, target_index=None)
    )
    _, _, _, info = env.step(action_id)
    obs = info["observation"]
    assert not obs.has_error
    expected_valid_actions = set(
        [
            actions.Choose(choice_index=0),
            actions.Choose(choice_index=1),
            actions.Choose(choice_index=2),
        ]
    )
    assert set(get_valid(obs)) == expected_valid_actions
