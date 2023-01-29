from gym_sts.envs.base import SlayTheSpireGymEnv


def test_card_reward_serde(env: SlayTheSpireGymEnv):
    env.reset(seed=42)

    env.communicator.basemod("relic add Singing_Bowl")
    env.communicator.basemod("fight 2_Orb_Walkers")
    env.communicator.basemod("kill all")

    # Open the card reward
    env.step(5)

    obs = env.observe(add_to_cache=True)
    orig_state = obs.card_reward_state
    ser = orig_state.serialize()
    de = obs.card_reward_state.deserialize(ser)

    assert orig_state == de
