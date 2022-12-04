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
