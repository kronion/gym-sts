from gym_sts.envs.base import SlayTheSpireGymEnv


def test_combat_serde(env: SlayTheSpireGymEnv):
    env.reset()

    # Enter combat
    env.communicator.basemod("fight 2_Orb_Walkers")

    obs = env.observe(add_to_cache=True)
    orig_state = obs.combat_state
    ser = orig_state.serialize()
    de = obs.combat_state.deserialize(ser)

    assert orig_state == de


def test_dead_minions_dont_overflow_serde_bounds(env: SlayTheSpireGymEnv):
    """
    Combats with large numbers of minions shouldn't cause exceptions during serde.

    There should only be up to 6 enemies on-screen at a time, but
    CommunicationMod continues to send data about dead enemies/minions.
    Confirm that we filter out the dead enemies/minions to guarantee we don't
    overflow the bounds of the serialization representation.
    """

    env.reset(seed=42)

    # Enter combat
    env.communicator.basemod("fight Reptomancer")

    # Add enough HP that we can just wait for tons of minions to spawn and kamikaze
    env.communicator.basemod("maxhp add 900")

    for _ in range(22):
        obs = env.observe(add_to_cache=True)
        orig_state = obs.combat_state
        ser = orig_state.serialize()
        de = obs.combat_state.deserialize(ser)

        assert orig_state.enemies == de.enemies

        # End turn
        env.step(0)

    # Confirm that attacking a specific enemy index works as expected.
    # We attack one of Reptomancer's daggers and confirm that its health decreases.
    env.step(75)
    obs = env.observe(add_to_cache=True)
    enemies = obs.combat_state.enemies
    assert enemies[1].current_hp == 16
