from communication import init_fifos
from game.game_state import GameState
from settings import *

def main():
    init_fifos([INPUT_FILE, OUTPUT_FILE])

    # Init game
    game_state = GameState()

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
