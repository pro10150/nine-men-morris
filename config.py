FPS = 45

T1 = {
    1: "RED",
    2: "BLUE"
}

T2 = {
    2: "RED",
    1: "BLUE"
}

PLAYER = [None, "RED", "BLUE"]

ROWS = 7
COLS = 7
SQUARESIZE = 93
SMALLSIZE = 50
RADIUS = 20
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
MEN = 2 * 9

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
BRIGHTRED = (255,   0,   0)
RED = (155,   0,   0)
BRIGHTGREEN = (0, 255,   0)
GREEN = (0, 155,   0)
BRIGHTBLUE = (0,   0, 255)
BLUE = (0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW = (155, 155,   0)
ORANGE = (255, 127,   0)
GRAY = (210, 210, 210)

BLANK = 0  # an unplayable spot on the board
PLAY1 = 1  # holds player 1 location in board list
PLAY2 = 2  # holds player 2 location in board list
VALID = 3  # this is a valid placement


LINES = [
    # plus sign pattern
    [3.5,  .5, 3.5, 2.5],  # N1 to N2
    [0.5, 3.5, 2.5, 3.5],  # E1 to E2
    [3.5, 4.5, 3.5, 6.5],  # S1 to S2
    [4.5, 3.5, 6.5, 3.5],  # W1 to W2
    # ourer square
    [.5,  .5, 6.5,  .5],
    [6.5,  .5, 6.5, 6.5],
    [6.5, 6.5,  .5, 6.5],
    [0.5, 6.5,  .5,  .5],
    # middle square
    [1.5, 1.5, 5.5, 1.5],
    [5.5,  1.5, 5.5, 5.5],
    [5.5, 5.5,  1.5, 5.5],
    [1.5, 5.5, 1.5, 1.5],
    # small square
    [2.5, 2.5, 4.5, 2.5],
    [4.5,  2.5, 4.5, 4.5],
    [4.5, 4.5,  2.5, 4.5],
    [2.5, 4.5, 2.5, 2.5],
]


BOARDPOSTION = [
    [3, 0, 0, 3, 0, 0, 3, 0],
    [0, 3, 0, 3, 0, 3, 0, 0],
    [0, 0, 3, 3, 3, 0, 0, 0],
    [3, 3, 3, 0, 3, 3, 3, 0],
    [0, 0, 3, 3, 3, 0, 0, 0],
    [0, 3, 0, 3, 0, 3, 0, 0],
    [3, 0, 0, 3, 0, 0, 3, 0],
    # needed for valid hover position if on the "help section"
    [0, 0, 0, 0, 0, 0, 0, 0],
]

CURRENTBOARDPOSITION = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

POSITION = {
    "00": (0, 0),
    "01": (0, 3),
    "02": (0, 6),
    "03": (1, 1),
    "04": (1, 3),
    "05": (1, 5),
    "06": (2, 2),
    "07": (2, 3),
    "08": (2, 4),
    "09": (3, 0),
    "10": (3, 1),
    "11": (3, 2),
    "12": (3, 4),
    "13": (3, 5),
    "14": (3, 6),
    "15": (4, 2),
    "16": (4, 3),
    "17": (4, 4),
    "18": (5, 1),
    "19": (5, 3),
    "20": (5, 4),
    "21": (6, 0),
    "22": (6, 3),
    "23": (6, 6)
}
