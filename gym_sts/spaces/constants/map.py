# You can read more about the structure of the map here:
# https://kosgames.com/slay-the-spire-map-generation-guide-26769/
ALL_MAP_LOCATIONS = [
    "NONE",  # Indicates the absence of node
    "M",  # Monster
    "?",  # Unknown
    "$",  # Shop
    "E",  # Elite
    "B",  # Burning Elite. Note that this symbol isn't actually used by the game.
    "T",  # Treasure
    "R",  # Rest site
]
NUM_MAP_LOCATIONS = len(ALL_MAP_LOCATIONS)
NUM_MAP_NODES_PER_ROW = 7
NUM_MAP_ROWS = 15
NUM_MAP_NODES = NUM_MAP_NODES_PER_ROW * NUM_MAP_ROWS
# Nodes can only have edges to endpoints in the same column, or one column to the
# left or right. Thus, we store three bits per node, representing the presence of an
# edge to the left, center, and right.
NUM_MAP_EDGES_PER_NODE = 3  # Max branching factor from one layer to the next
NUM_MAP_EDGES = NUM_MAP_NODES_PER_ROW * NUM_MAP_EDGES_PER_NODE * (NUM_MAP_ROWS - 1)

NORMAL_BOSSES = [
    "NONE",  # A placeholder for an "empty" observation
    "The Guardian",
    "Hexaghost",
    "Slime Boss",
    "Collector",
    "Automaton",
    "Champ",
    "Awakened One",
    "Time Eater",
    "Donu and Deca",
]
NUM_NORMAL_BOSSES = len(NORMAL_BOSSES)
