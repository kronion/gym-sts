import time

import numpy as np

import gym_sts.spaces.constants.combat as combat_consts
from gym_sts.spaces import actions
from gym_sts.spaces.observations import utils


def test_enemy_attack_serialization(env):
    env.reset(seed=42)

    # First, demonstrate that damage is 0 when the enemy's intent isn't an attack
    env.communicator.basemod("fight Hexaghost")

    # Hexaghost's intent on turn 1 is always "unknown"
    obs = env.observe(add_to_cache=True)
    serialization = obs.combat_state.serialize()
    enemies = serialization["enemies"]
    assert len(enemies) > 0
    hexaghost = enemies[0]
    expected_damage = utils.to_binary_array(0, combat_consts.LOG_MAX_ATTACK)
    assert np.array_equal(hexaghost["attack"]["damage"], expected_damage)

    # Next, demonstrate that damage and number of hits are correct
    # Hexaghost's attack on turn 2 is ((player HP / 12) + 1) * 6
    hp = obs.persistent_state.hp
    env.communicator.basemod(f"hp lose {hp - 1}")
    action_id = actions.ACTIONS.index(actions.EndTurn())
    _, _, _, info = env.step(action_id)
    obs = info["observation"]
    serialization = obs.combat_state.serialize()
    enemies = serialization["enemies"]
    assert len(enemies) > 0
    hexaghost = enemies[0]
    expected_damage = utils.to_binary_array(1, combat_consts.LOG_MAX_ATTACK)
    expected_times = utils.to_binary_array(6, combat_consts.LOG_MAX_ATTACK_TIMES)
    assert np.array_equal(hexaghost["attack"]["damage"], expected_damage)
    assert np.array_equal(hexaghost["attack"]["times"], expected_times)

    # Next, demonstrate that damage may be adjusted from base values
    env.communicator.basemod("fight Gremlin_Nob")
    env.communicator.basemod("deck remove all")
    env.communicator.basemod("deck add Discovery")
    time.sleep(0.5)  # Wait briefly for card adding animation to complete
    obs = env.observe(add_to_cache=True)
    _, _, _, info = env.step(action_id)
    obs = info["observation"]
    serialization = obs.combat_state.serialize()
    enemies = serialization["enemies"]
    assert len(enemies) > 0
    gremlin_nob = enemies[0]
    damage = utils.from_binary_array(gremlin_nob["attack"]["damage"])

    # At this point the only card in hand is Discovery
    # TODO make action selection easier
    action_id = actions.ACTIONS.index(
        actions.PlayCard(card_position=1, target_index=None)
    )
    _, _, _, info = env.step(action_id)
    obs = info["observation"]
    serialization = obs.combat_state.serialize()
    enemies = serialization["enemies"]
    assert len(enemies) > 0
    gremlin_nob = enemies[0]
    new_damage = gremlin_nob["attack"]["damage"]
    expected_damage = utils.to_binary_array(damage + 2, combat_consts.LOG_MAX_ATTACK)
    assert np.array_equal(new_damage, expected_damage)

    # Runic Dome doesn't cause an error
    env.communicator.basemod("relic add Runic_Dome")
    env.communicator.basemod("fight Looter")
    obs = env.observe(add_to_cache=True)
    serialization = obs.combat_state.serialize()
    enemies = serialization["enemies"]
    assert len(enemies) > 0
    looter = enemies[0]
    damage = utils.from_binary_array(looter["attack"]["damage"])
    times = utils.from_binary_array(looter["attack"]["times"])
    assert damage == 0
    assert times == 0
