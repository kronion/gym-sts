"""Tests that an action leads to an error iff it is valid.

Best to run with ipdb to post-mortem debug errors:

python -m ipdb -c c gym_sts/test_valid_actions.py
"""

import argparse
import pickle

from gym_sts.envs.action_validation import validate
from gym_sts.envs.base import SlayTheSpireGymEnv
from gym_sts.spaces.actions import ACTIONS
from gym_sts.history import History

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
    parser.add_argument("--history", type=str, required=True)
    args = parser.parse_args()

    with open(args.history, 'rb') as f:
        history: History = pickle.load(f)

    assert len(history.states) == len(history.actions) + 1

    if args.build_image:
        SlayTheSpireGymEnv.build_image()
    env = SlayTheSpireGymEnv(
        args.lib_dir, args.mods_dir, args.out_dir, headless=args.headless
    )
    seed = history.seed
    env.reset(seed=seed)

    num_steps = 0

    for state, action in zip(history.states, history.actions):
        if args.screenshots:
            env.screenshot(f"frame{num_steps:03d}.png")

        obs = env.observation_cache.get()
        assert obs == state
        assert validate(action, obs)

        print(action)
        try:
            _, _, done, info = env.step(action._id)
        except TimeoutError as e:
            print(e)
            if args.headless:
                env.screenshot("error.png")
            raise e

        if done:
            print("RESET")
            env.reset()

        num_steps += 1

    obs = env.observation_cache.get()
    assert history.states[-1] == obs


if __name__ == "__main__":
    main()
