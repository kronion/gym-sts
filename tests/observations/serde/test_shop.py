from gym_sts.envs.base import SlayTheSpireGymEnv


def test_shop_serde(env: SlayTheSpireGymEnv):
    env.reset(seed=43)

    # Neow event
    env.step(3)
    env.step(4)
    env.step(3)

    # Skip a combat
    env.step(3)
    env.communicator.basemod("kill all")
    env.step(2)

    # Shop
    env.step(3)
    env.step(3)

    obs = env.observe(add_to_cache=True)
    orig_state = obs.shop_state
    ser = orig_state.serialize()
    de = obs.shop_state.deserialize(ser)

    assert orig_state == de

    # Add plenty of gold so we can buy one of everything
    env.communicator.basemod("gold add 3000")

    # Buy a few things
    env.step(6)  # A card
    env.step(15)  # A potion
    env.step(12)  # A relic

    # A card removal
    env.step(3)
    env.step(3)
    env.step(2)

    obs = env.observe(add_to_cache=True)
    orig_state = obs.shop_state
    ser = orig_state.serialize()
    de = obs.shop_state.deserialize(ser)

    assert orig_state == de
