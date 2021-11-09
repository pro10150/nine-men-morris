# Based on the code from https://github.com/S7uXN37/NineMensMorrisBoard
import numpy as np
from ai_copy import opposite_player
import logic

WIN_REWARD = 2.0
CAPTURE_REWARD = 0.3

new_board = np.zeros(24)


def ai_step(board, side, my_piece, their_piece):
    depth = 2  # depth 3 is too much for my computer
    best_score = -999999

    move = -1
    place = -1
    remove = -1
    # print('The current board is...')
    # print(board)
    # the best board must iterate backwards

    best_board, _, reward, end_state = minimaxAB(
        board, side, depth, my_piece, their_piece)

    # print('The best board is...')
    # print(best_board)

    # compares current board and the best board then extracts move indices
    for i in range(24):
        print(board[i], best_board[i])
        # move (leaving the starting spot empty)
        if board[i] == side and best_board[i] == 3:
            move = i
        # placing in an empty space
        if board[i] == 3 and best_board[i] == side:
            place = i
        # remove the opponent
        if board[i] == swap(side) and best_board[i] == 3:
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            remove = i

    print('Move: ' + str(move))
    print('Place: ' + str(place))
    print('Delete: ' + str(remove))

    return move, place, remove


def minimaxAB(board, side, depth, my_piece, their_piece):

    if depth <= 0:
        # and evaluate boards
        return board, eval_board(board, side=side) - eval_board(board, side=-side), 0, False
    else:

        if type(board) == list:
            board = np.asarray(board)

        worst_their_score = 999999  # want to get this as low as possible
        best_board = board  # initialize the board

        reward = -WIN_REWARD  # base reward if no possible moves
        end_state = True

        for board_f in moves(board, side, my_piece):

            # minimizes the opponent, and swap role
            _, their_score, _, _ = minimaxAB(
                board_f, swap(side), depth-1, their_piece, my_piece-1)

            temp_reward = 0
            temp_end_state = False

            # not to be confused with my_piece, their_piece
            # these variables belowcount how much pieces left for each side
            pieces_mine = len(board_f[board_f == side])
            pieces_theirs = len(board_f[board_f == swap(side)])
            if pieces_mine < 3 and my_piece <= 0:
                temp_reward = -WIN_REWARD  # Don't lose...
                temp_end_state = True
            elif pieces_theirs < 3 and their_piece <= 0:
                temp_reward = WIN_REWARD  # I win.
                temp_end_state = True
            elif pieces_theirs < len(board[board == swap(side)]):
                temp_reward = CAPTURE_REWARD  # Let's capture.
            elif pieces_mine < len(board[board == side]):
                temp_reward = -CAPTURE_REWARD  # Avoid being captured again.

            # outputs these variables with best board for ai
            # also gets the value advantage as well
            if (their_score < worst_their_score) or temp_reward == WIN_REWARD:
                best_board = board_f
                worst_their_score = their_score
                reward = temp_reward
                end_state = temp_end_state
            if temp_reward == WIN_REWARD:  # I found the winning board so PRUNE it
                break

        return best_board, -worst_their_score, reward, end_state


def moves(board, side, my_piece):

    global new_board

    board_list = np.array([], dtype=np.int16)  # stores all the legal boards

    if my_piece > 0:  # I am in PHASE 1

        for i, value in enumerate(board):
            if value == 3:  # is placeable
                new_board = [va for va in board]  # copy a current board...
                new_board[i] = side  # ... with my placed piece

            # find capturable pieces if it forms a mill
            if checkMillWithBoard(new_board, side, i):
                board_list = np.append(
                    board_list, capturables(new_board, side))
            # Or just simply add the board to the list
            else:
                board_list = np.append(board_list, new_board)

    elif len(board[board == side]) > 3:  # I am in PHASE 2

        # get own pieces then find possible moves
        for i, value in enumerate(board):
            if value == side:
                for space in logic.movablePawn[i]:
                    if board[space] == 3:  # empty?

                        new_board = [va for va in board]
                        new_board[i] = 3
                        new_board[space] = side

                        # find capturable pieces if it forms a mill
                        if checkMillWithBoard(new_board, side, i):
                            board_list = np.append(
                                board_list, capturables(new_board, side))
                        # Or just simply add the board to the list
                        else:
                            board_list = np.append(board_list, new_board)

    else:  # I am in PHASE 3 darn it

        # get own pieces then find empty nodes
        for i, value in enumerate(board):
            if value == side:
                for j, space in enumerate(board):
                    if space == 3:  # empty?

                        new_board = [va for va in board]
                        new_board[i] = 3
                        new_board[space] = side

                        # find capturable pieces if it forms a mill
                        if checkMillWithBoard(new_board, side, i):
                            board_list = np.append(
                                board_list, capturables(new_board, side))
                        else:
                            board_list = np.append(board_list, new_board)

    num_moves = int(len(board_list)/24)
    #print('calculated %d possible moves:' % num_moves)
    # print(board_list)
    # print(type(board_list))
    # print(board_list.reshape(num_moves, 24))
    return board_list.reshape(num_moves, 24)


def capturables(board, side):
    legal = np.array([], dtype=np.int16)  # array of enemy nodes outside mill
    # enemy nodes inside mill, uncapturable
    illegal = np.array([], dtype=np.int16)
    for i, value in enumerate(board):
        if value == swap(side):
            new_board = [va for va in board]
            new_board[i] = 3
            # add em to the list
            if checkMillWithBoard(board, swap(side), i):
                illegal = np.append(illegal, new_board)
            else:
                legal = np.append(legal, new_board)
    if len(legal) <= 0:  # No legal piece? just use the illegal list
        return illegal
    else:
        return legal


def eval_board(board, side=1):
    value = 0
    mills = 0

    for i in range(len(board)):
        if board[i] == side:
            # count number of a player's piece left
            # higher = better
            value += 3

            # count available moves per piece
            for space in logic.movablePawn[i]:
                if board[space] == 3:  # empty?
                    value += 0.3

            # count number of pieces mills then
            # divide by 3 rounded up
            if checkMillWithBoard(board, side, i):
                mills += 1

    if mills % 3 != 0:
        mills += 3 - (mills % 3)
    mills = mills / 3
    value += (1 * mills)

    return value


def swap(side):
    if side == 1:
        return 2
    elif side == 2:
        return 1
    else:
        print('SWAP ERROR')
        return 0

# check mill with given board


def checkMillWithBoard(board, player, cdn):

    new_mill = [
        [[board[9], board[21]], [board[1], board[2]]],
        [[board[4], board[7]], [board[0], board[2]]],
        [[board[14], board[23]], [board[0], board[1]]],
        [[board[10], board[18]], [board[4], board[5]]],
        [[board[1], board[7]], [board[3], board[5]]],
        [[board[13], board[20]], [board[3], board[4]]],
        [[board[11], board[15]], [board[7], board[8]]],
        [[board[1], board[4]], [board[6], board[8]]],
        [[board[12], board[17]], [board[6], board[7]]],
        [[board[0], board[21]], [board[10], board[11]]],
        [[board[3], board[18]], [board[9], board[11]]],
        [[board[6], board[15]], [board[9], board[10]]],
        [[board[8], board[17]], [board[13], board[14]]],
        [[board[5], board[20]], [board[12], board[14]]],
        [[board[2], board[23]], [board[12], board[13]]],
        [[board[6], board[11]], [board[16], board[17]]],
        [[board[19], board[22]], [board[15], board[17]]],
        [[board[8], board[12]], [board[15], board[16]]],
        [[board[3], board[10]], [board[19], board[20]]],
        [[board[16], board[22]], [board[18], board[20]]],
        [[board[5], board[13]], [board[18], board[19]]],
        [[board[0], board[9]], [board[22], board[23]]],
        [[board[16], board[19]], [board[21], board[23]]],
        [[board[2], board[14]], [board[21], board[22]]]
    ]

    if new_mill[cdn][0].count(player) == 2 or new_mill[cdn][1].count(player) == 2:
        return True
    else:
        return False
