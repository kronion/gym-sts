"""
Tests that an action leads to an error iff it is valid.

Best to run with ipdb to post-mortem debug errors:

python -m ipdb -c c gym_sts/test_valid_actions.py
"""

import time

from gym_sts.envs.utils import ActionValidators
from gym_sts.spaces import actions


def test_card_reward_valid_in_combat(env):
    env.reset(seed=42)

    env.communicator.basemod("deck remove all")
    env.communicator.basemod("deck add Discovery")
    time.sleep(0.5)  # Wait briefly for card adding animation to complete
    env.communicator.basemod("fight Jaw_Worm")

    # At this point the only card in hand is Discovery
    # TODO make action selection easier
    _, _, _, info = env.step(58)
    obs = info["observation"]
    assert not obs.has_error
    expected_valid_actions = set(
        [
            actions.Choose(choice_index=0),
            actions.Choose(choice_index=1),
            actions.Choose(choice_index=2),
        ]
    )
    assert set(ActionValidators.valid_actions(obs)) == expected_valid_actions
