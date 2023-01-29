from gym_sts.envs.base import SlayTheSpireGymEnv


def test_combat_serde(env: SlayTheSpireGymEnv):
    env.reset(seed=46)

    # Neow event
    env.step(3)
    env.step(4)
    env.step(3)

    # Skip a bunch of combats (and one shop)
    env.step(3)
    env.communicator.basemod("kill all")
    env.step(2)
    env.step(3)
    env.communicator.basemod("kill all")
    env.step(2)
    env.step(3)
    env.communicator.basemod("kill all")
    env.step(2)
    env.step(3)
    env.step(2)
    env.step(3)
    env.communicator.basemod("kill all")
    env.step(2)
    env.step(4)
    env.communicator.basemod("kill all")
    env.step(2)

    # Event
    env.step(3)
    env.step(3)
    env.step(3)
    env.step(2)
    env.step(3)

    # Burning elite
    env.step(3)
    env.communicator.basemod("kill all")

    obs = env.observe(add_to_cache=True)
    orig_state = obs.combat_reward_state
    ser = orig_state.serialize()
    de = obs.combat_reward_state.deserialize(ser)

    assert orig_state == de
