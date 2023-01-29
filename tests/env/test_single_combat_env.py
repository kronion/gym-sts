import time

from gym_sts.spaces.actions import PlayCard


def test_single_combat_spawns_into_gremlin_nob(single_combat_env):
    single_combat_env.reset()

    obs = single_combat_env.observe()

    assert obs.in_combat
    assert obs.screen_type == "NONE"
    enemies = obs.combat_state.enemies

    assert len(enemies) == 1
    assert enemies[0].id == "GremlinNob"


def test_single_combat_resets_after_defeating_enemy(single_combat_env):
    single_combat_env.reset(seed=42)

    single_combat_env.communicator.basemod("relic add NeowsBlessing")
    single_combat_env.communicator.basemod("fight Gremlin_Nob")
    time.sleep(0.1)
    single_combat_env.communicator.basemod("hand discard all")
    time.sleep(0.1)
    obs = single_combat_env.communicator.basemod("hand add Strike_B")
    time.sleep(0.1)

    # Current state should have exactly 1 Strike card in player's hand
    assert obs.combat_state.enemies[0].current_hp == 1
    assert len(obs.valid_actions) == 2
    assert isinstance(obs.valid_actions[1], PlayCard)

    # Playing a card doesn't immediately reduce the enemy's HP, it simply queues the
    # card to be played by the action manager
    _, _, should_reset, _ = single_combat_env.step(1)
    # End turn
    _, _, should_reset, info = single_combat_env.step(0)

    # End of combat, we should reset
    assert not info["observation"].in_combat
    assert should_reset
