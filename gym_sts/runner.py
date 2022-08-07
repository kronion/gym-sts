from game.game_state import LegacyGameState, DockerGameState
from settings import *

import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_docker", type=bool, action="store_true")
    args = parser.parse_args()

    # Init game

    if args.no_docker:
        game_state = LegacyGameState()
    else:
        game_state = DockerGameState(f"{os.getcwd()}/out")

    observation = game_state.begin(42)

    while True:
        action = input()
        if not action:
            print("No action given. Defaulting to STATE.")
            action = "STATE"
        observation = game_state.do_action(action)
        print(observation)
        if "error" in observation:
            print("ERROR")
            print(observation["error"])
        else:
            print("AVAILABLE COMMANDS:")
            print(observation["available_commands"])

if __name__ == "__main__":
    main()
