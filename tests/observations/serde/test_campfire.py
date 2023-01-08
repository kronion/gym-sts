import time

from gym_sts.envs.base import SlayTheSpireGymEnv
from gym_sts.spaces.observations.components import CampfireObs
from gym_sts.spaces.observations.types import CampfireChoice


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


def test_rest_option_order_matters():
    dig_then_toke = [
        CampfireChoice.REST,
        CampfireChoice.SMITH,
        CampfireChoice.DIG,
        CampfireChoice.TOKE,
        CampfireChoice.RECALL,
    ]

    toke_then_dig = [
        CampfireChoice.REST,
        CampfireChoice.SMITH,
        CampfireChoice.TOKE,
        CampfireChoice.DIG,
        CampfireChoice.RECALL,
    ]

    obs1 = CampfireObs(has_rested=False, rest_options=dig_then_toke)
    obs2 = CampfireObs(has_rested=False, rest_options=toke_then_dig)

    assert obs1 != obs2

    ser1 = obs1.serialize()
    ser2 = obs2.serialize()
    de1 = CampfireObs.deserialize(ser1)
    de2 = CampfireObs.deserialize(ser2)

    assert obs1 == de1
    assert obs2 == de2
    assert de1 != de2
