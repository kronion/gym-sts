"""Measures steps per second of the StS env.

Currently I get about ~1 sps.

TODO: try with and without the superfast mod.
"""

import argparse
import random
import time

from gym_sts.envs.base import SlayTheSpireGymEnv


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
        action = rng.choice(env.valid_actions())
        _, _, done, _ = env.step(action._id)
        if done:
            env.reset()

        num_steps += 1
        run_time = time.perf_counter() - start_time
        if run_time >= args.runtime:
            break

    sps = num_steps / run_time
    print(f"sps: {sps}")


if __name__ == "__main__":
    main()
