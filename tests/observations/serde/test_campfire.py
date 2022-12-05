import time

from gym_sts.envs.base import SlayTheSpireGymEnv


def test_campfire_serde(env: SlayTheSpireGymEnv):
    env.reset(seed=42)

    # Neow event
    env.step(3)
    env.step(4)
    env.step(3)

    # First combat
    env.step(6)
    time.sleep(0.5)  # Wait briefly for card adding animation to complete
    env.communicator.basemod("kill all")
    env.step(2)

    # Event
    env.step(3)
    env.step(4)
    env.step(3)

    # Event
    env.step(3)
    env.step(3)
    env.step(3)

    # Event
    env.step(3)
    env.step(4)
    env.step(3)
    env.step(2)
    env.step(3)

    # Combat
    env.step(3)
    time.sleep(0.5)  # Wait briefly for card adding animation to complete
    env.communicator.basemod("kill all")
    env.step(2)

    # Finally, a campfire
    env.step(3)

    obs = env.observe(add_to_cache=True)
    orig_state = obs.campfire_state
    ser = orig_state.serialize()
    de = obs.campfire_state.deserialize(ser)

    assert orig_state == de
