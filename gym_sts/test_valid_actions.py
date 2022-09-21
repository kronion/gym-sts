"""Tests that an action leads to an error iff it is valid."""

import argparse
import random
import time

from gym_sts.envs.base import SlayTheSpireGymEnv
from gym_sts.envs.utils import ActionValidators
from gym_sts.spaces.actions import ACTIONS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lib_dir")
    parser.add_argument("mods_dir")
    parser.add_argument("--build_image", action="store_true")
    parser.add_argument("--runtime", default=30, type=int)
    args = parser.parse_args()

    if args.build_image:
        SlayTheSpireGymEnv.build_image()
    env = SlayTheSpireGymEnv(args.lib_dir, args.mods_dir, headless=True)
    env.reset(seed=42)
    rng = random.Random(42)

    num_steps = 0
    start_time = time.perf_counter()

    while True:
        last_obs = env.observation_cache.get()
        assert last_obs is not None

        want_valid = rng.choice([True, False])

        actions = [
            action
            for action in ACTIONS
            if ActionValidators.validate(action, last_obs) == want_valid
        ]

        action = rng.choice(actions)
        _, _, done, info = env.step(action._id)
        assert info["had_error"] != want_valid

        if done:
            env.reset()

        num_steps += 1
        run_time = time.perf_counter() - start_time
        if run_time >= args.runtime:
            break

    fps = num_steps / run_time
    print(f"fps: {fps}")


if __name__ == "__main__":
    main()
