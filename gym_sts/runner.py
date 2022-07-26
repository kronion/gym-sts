import argparse

from gym_sts.envs.base import SlayTheSpireGymEnv
from gym_sts.spaces.observations import ObservationError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lib_dir")
    parser.add_argument("mods_dir")
    parser.add_argument("out_dir")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--build_image", action="store_true")
    args = parser.parse_args()

    if args.build_image:
        SlayTheSpireGymEnv.build_image()
    env = SlayTheSpireGymEnv(
        args.lib_dir, args.mods_dir, args.out_dir, headless=args.headless
    )
    observation = env.reset()
    print(observation.state)

    while True:
        action = input("Enter an action: ")
        if not action:
            print("No action given. Defaulting to STATE.")
            action = "STATE"
        observation = env._do_action(action)
        print(observation.state)
        try:
            commands = observation._available_commands
            print("AVAILABLE COMMANDS:")
            print(commands)
        except ObservationError as e:
            print("ERROR")
            print(e)


if __name__ == "__main__":
    main()
