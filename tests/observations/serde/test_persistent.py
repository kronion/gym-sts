from gym_sts.envs.base import SlayTheSpireGymEnv


def test_persistent_serde(env: SlayTheSpireGymEnv):
    env.reset(seed=43)

    obs = env.observe(add_to_cache=True)
    orig_state = obs.persistent_state
    ser = orig_state.serialize()
    de = obs.persistent_state.deserialize(ser)

    assert orig_state == de

    # Edit health, max health, potions, relics, deck, and keys
    env.communicator.basemod("gold add 100")
    env.communicator.basemod("maxhp lose 7")
    env.communicator.basemod("hp lose 7")
    env.communicator.basemod("potions 0 Ambrosia")
    env.communicator.basemod("relic add Anchor")
    env.communicator.basemod("deck remove all")
    env.communicator.basemod("deck add Accuracy")
    env.communicator.basemod("key add ruby")

    obs = env.observe(add_to_cache=True)
    orig_state = obs.persistent_state
    ser = orig_state.serialize()
    de = obs.persistent_state.deserialize(ser)

    assert orig_state == de

    # Go to a different screen type (Neow is an event)
    env.step(3)
    env.step(4)
    env.step(3)
    env.step(3)

    obs = env.observe(add_to_cache=True)
    orig_state = obs.persistent_state
    ser = orig_state.serialize()
    de = obs.persistent_state.deserialize(ser)

    assert orig_state == de
