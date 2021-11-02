# Based on the code from https://github.com/S7uXN37/NineMensMorrisBoard
import numpy as np
import logic

WIN_REWARD = 2.0
CAPTURE_REWARD = 0.3

# p1_pieces [your piece left to place, opponent piece left to place]


def ai_step(board, maxxing_player, maxxing_side, p1_pieces_ai, p1_pieces_oppo):
    depth = 3
    # best_board, _, my_score, endstate = minimax(
    #     board, depth, maxxing_player, maxxing_color)

    # print(p1_pieces_ai, p1_pieces_oppo)
    best_board, _, my_score, endstate = alphaBeta(
        board, False, depth, p1_pieces_ai, p1_pieces_oppo)

    # print(logic.boardOutput(board))
    # print('-------------VS--------------')
    # print(logic.boardOutput(best_board))

    # We need to either
    # 1. return cdn and dest somehow
    # 2. do not return but make move right on this function?

    # return cdn, dest


def alphaBeta(board, player, depth, p1_pieces_ai, p1_pieces_oppo):
    if depth <= 0:
        # reward and endstate won't be used
        return board, value(board, color=str(player)) - value(board, color=str(opposite_player(player))), 0, False
    else:
        worst_oppo_score = float("inf")
        bestBoard = board
        reward = -WIN_REWARD  # Loses
        endstate = True
        for board_after in moves(board, player, p1_pieces_ai):
            # trying to minimize reward of opponent
            _, oppo_score, _, _ = alphaBeta(
                board_after, -player, depth-1, p1_pieces_oppo, p1_pieces_ai-1)

            r = 0
            t = False
            num_pieces_self = len(board_after[board_after == str(player)])
            num_pieces_opponent = len(
                board_after[board_after == str(opposite_player(player))])
            if num_pieces_self < 3 and p1_pieces_ai <= 0:
                r = -WIN_REWARD
                t = True
            elif num_pieces_opponent < 3 and p1_pieces_oppo <= 0:
                r = WIN_REWARD
                t = True
            elif num_pieces_opponent < len(board[board == str(opposite_player(player))]):
                r = CAPTURE_REWARD
            elif num_pieces_self < len(board[board == str(player)]):
                r = -CAPTURE_REWARD

            if oppo_score < worst_oppo_score or r == WIN_REWARD:
                bestBoard = board_after
                worst_oppo_score = oppo_score
                reward = r
                endstate = t
            if r == WIN_REWARD:
                break

        return bestBoard, -worst_oppo_score, reward, endstate


def moves(board, player, p1_pieces_ai):
    boardlist = np.array([])

    if p1_pieces_ai > 0:  # if the bot is still in phase 1

        for i, key in enumerate(board):

            value = board[key]

            # board_node = locate_board(i)
            # print(board_node)

            if value == 3:  # is an empty space
                new_board = [x for x in board]
                new_board[i] = str(player)

                # if mill closed, also list all possibilities for taking pieces

                print(value)
                print(type(value))
                print(key)
                print(type(key))

                if logic.checkMill(player, key):  # STUCK HERE, WILL CONTINUE ON
                    boardlist = np.append(
                        boardlist, moves_on_mill_closed(new_board, player))
                else:
                    boardlist = np.append(boardlist, new_board)

    elif len(board[board == str(player)]) > 3:  # phase 2

        for i, val in enumerate(board):
            if val == str(player):  # own piece
                for f in logic.movablePawn[i]:
                    if f != 3:  # unneeded?
                        continue
                    if board[f] == 0:
                        new_board = [x for x in board]
                        new_board[i] = 0
                        new_board[f] = player

                        if logic.checkMill(player, f):
                            boardlist = np.append(
                                boardlist, moves_on_mill_closed(new_board, player))
                        else:
                            boardlist = np.append(boardlist, new_board)
    else:  # phase 3

        for i, val in enumerate(board):
            if val == str(player):  # own piece
                for j, val2 in enumerate(board):
                    if val2 == 3:  # also catches i==j because color!=0
                        new_board = [x for x in board]
                        new_board[i] = 0
                        new_board[j] = player

                        if logic.checkMill(player, j):
                            boardlist = np.append(
                                boardlist, moves_on_mill_closed(new_board, player))
                        else:
                            boardlist = np.append(boardlist, new_board)

    num_moves = int(len(boardlist)/24)

    return boardlist.reshape(num_moves, 24)


def moves_on_mill_closed(board, player):
    allowed = np.array([], dtype=np.int16)
    disallowed = np.array([], dtype=np.int16)
    for k, val3 in enumerate(board):
        if val3 == str(opposite_player(player)):
            new_board = [x for x in board]
            new_board[k] = 3  # moves away
            # save taking stones out of mills separately
            if logic.checkMill(opposite_player(player), k):
                disallowed = np.append(disallowed, new_board)
            else:
                allowed = np.append(allowed, new_board)
    if len(allowed) <= 0:  # no allowed moves -> all moves allowed
        return disallowed
    else:
        return allowed


def opposite_player(player):
    if player == 2:
        return 1
    else:
        return 2


def value(board, player=1):
    value = 0

    mills = 0
    for i in range(len(board)):
        if board[i] == str(player):
            # count pieces
            value += 3
            # count moves
            for f in logic.movablePawn[i]:
                index = f
                if index != 2:
                    if board[index] == 0:
                        value += 0.1
            # count pieces in mills
            if logic.checkMill(board, i):
                mills += 1

    # count mills
    if mills % 3 != 0:  # round up to next multiple of 3
        mills += 3 - (mills % 3)

    mills /= 3
    value += 1 * mills

    return value


def locate_board(i):
    if i < 10:
        node = '0' + str(i)
    else:
        node = str(i)

    return node
