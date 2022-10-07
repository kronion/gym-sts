"""Tests that an action leads to an error iff it is valid.

Best to run with ipdb to post-mortem debug errors:

python -m ipdb -c c gym_sts/test_valid_actions.py
"""

import argparse
import random
import time

from gym_sts.envs.action_validation import validate
from gym_sts.envs.base import SlayTheSpireGymEnv
from gym_sts.spaces.actions import ACTIONS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lib_dir")
    parser.add_argument("mods_dir")
    parser.add_argument("out_dir")
    parser.add_argument("--build_image", action="store_true")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--runtime", default=30, type=int)
    parser.add_argument("--allow_invalid", action="store_true")
    parser.add_argument("--screenshots", action="store_true")
    args = parser.parse_args()

    if args.build_image:
        SlayTheSpireGymEnv.build_image()
    env = SlayTheSpireGymEnv(
        args.lib_dir, args.mods_dir, args.out_dir, headless=args.headless
    )
    env.reset(seed=42)
    rng = random.Random(42)

    valid_choices = [True]
    if args.allow_invalid:
        valid_choices.append(False)

    num_steps = 0
    start_time = time.perf_counter()

    while True:
        if args.screenshots:
            env.screenshot(f"frame{num_steps:03d}.png")

        last_obs = env.observation_cache.get()
        assert last_obs is not None
        print(last_obs.screen_type)

        want_valid = rng.choice(valid_choices)

        actions = [
            action for action in ACTIONS if validate(action, last_obs) == want_valid
        ]

        if len(actions) == 0:
            raise ValueError("No %svalid actions!" % ("" if want_valid else "in"))

        action = rng.choice(actions)
        print(action)
        try:
            _, _, done, info = env.step(action._id)
        except TimeoutError as e:
            run_time = time.perf_counter() - start_time
            print(f"Error on step {num_steps} after {run_time} seconds.")
            print(e)
            if args.headless:
                env.screenshot("error.png")
            raise e

        assert info["had_error"] != want_valid

        if done:
            print("RESET")
            env.reset()

        num_steps += 1
        run_time = time.perf_counter() - start_time
        if run_time >= args.runtime:
            break

    fps = num_steps / run_time
    print(f"fps: {fps}")


if __name__ == "__main__":
    main()
