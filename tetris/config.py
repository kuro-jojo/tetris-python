SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

GAMEZONE_WIDTH = 250
GAMEZONE_HEIGHT = SCREEN_HEIGHT

WHITE = (255,255,255)
BLACK = (0,0,0)

BACKGROUND_COLOR = BLACK
GRID_LINE_COLOR = WHITE

GAME_SPEED = TETRO_SIZE = 25
DOWN_SPEED = 50

# Define tetromino shapes
TETROMINO_SHAPES = {
    "I": [
        [[True, True, True, True]],  # Horizontal
        [[True], [True], [True], [True]],  # Vertical
    ],
    "L": [
        [[True, False], [True, False], [True, True]],  # Up
        [[True, True, True], [True, False, False]],  # Right
        [[True, True], [False, True], [False, True]],  # Down
        [[False, False, True], [True, True, True]],  # Left
    ],
    "J": [
        [[False, True], [False, True], [True, True]],  # Up
        [[True, False, False], [True, True, True]],  # Right
        [[True, True], [True, False], [True, False]],  # Down
        [[True, True, True], [False, False, True]],  # Left
    ],
    "T": [
        [[True, True, True], [False, True, False]],  # Up
        [[True, False], [True, True], [True, False]],  # Right
        [[False, True, False], [True, True, True]],  # Down
        [[False, True], [True, True], [False, True]],  # Left
    ],
    "S": [
        [[False, True, True], [True, True, False]],  # Horizontal
        [[True, False], [True, True], [False, True]],  # Vertical
    ],
    "Z": [
        [[True, True, False], [False, True, True]],  # Horizontal
        [[False, True], [True, True], [True, False]],  # Vertical
    ],
    "O": [[[True, True], [True, True]]],  # Only one rotation
}

# Accessing a specific tetromino and its rotations
I = TETROMINO_SHAPES["I"]
L = TETROMINO_SHAPES["L"]
J = TETROMINO_SHAPES["J"]
T = TETROMINO_SHAPES["T"]
S = TETROMINO_SHAPES["S"]
Z = TETROMINO_SHAPES["Z"]
O = TETROMINO_SHAPES["O"]

# Define the colors of the tetrominos
TETROMINO_COLORS = {
    "I": (0, 255, 255),
    "L": (255, 165, 0),
    "J": (0, 0, 255),
    "T": (128, 0, 128),
    "S": (0, 255, 0),
    "Z": (255, 0, 0),
    "O": (255, 255, 0),
}
