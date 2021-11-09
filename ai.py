# Based on the code from https://github.com/S7uXN37/NineMensMorrisBoard
import numpy as np
import logic

WIN_REWARD = 2.0
CAPTURE_REWARD = 0.3


def ai_step(board, side, my_piece, their_piece):

    best_score = -999999

    best_move = {
        'move': 0,
        'place': 0,
        'delete': 0
    }

    bestBoard, _, reward, terminal = minimax(
        board, side, my_piece, their_piece)

    return best_move['move'], best_move['place'], best_move['delete']


def minimax(board, side, my_piece, their_piece):
    return 1
