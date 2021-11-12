# Based on the code from https://github.com/S7uXN37/NineMensMorrisBoard
import numpy as np
import logic

AI_WON = 1

new_board = np.zeros(24)


def ai_step(board, side, my_piece, their_piece):
    depth = 2  # depth 3 is too much for my computer

    move = -1
    place = -1
    remove = -1

    best_board, worst_score, end_state = minimaxAB(
        board, side, depth, my_piece, their_piece)

    print('final worst score :', worst_score)

    for i in range(24):
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

    print(board)
    print(best_board)

    print('Move: ' + str(move))
    print('Place: ' + str(place))
    print('Delete: ' + str(remove))

    return move, place, remove


def minimaxAB(board, side, depth, my_piece, their_piece):

    if depth <= 0:
        # and evaluate boards
        advantage = eval_board(board, side=side) - \
            eval_board(board, side=swap(side))

        print(advantage)

        return board, advantage, False
    else:

        worst_their_score = 999999
        best_board = board.copy()

        end_state = True

        for board_f in moves(board, side, my_piece):

            # minimizes the opponent, and swap role
            _, their_score, _ = minimaxAB(
                board_f, swap(side), depth-1, their_piece, my_piece-1)

            temp_reward = 0
            temp_end_state = False
            # not to be confused with my_piece, their_piece
            # these variables below count how much pieces left for each side

            pieces_mine = board_f.count(side)
            pieces_theirs = board_f.count(swap(side))
            if pieces_mine < 3 and my_piece <= 0:
                temp_reward = -AI_WON  # Don't lose...
            elif pieces_theirs < 3 and their_piece <= 0:
                temp_reward = AI_WON  # I win.
                temp_end_state = True

            # outputs these variables with best board for ai
            # also gets the value advantage as well
            # beta < alpha
            if (their_score < worst_their_score) or temp_reward == AI_WON:  # good target

                best_board = board_f
                worst_their_score = their_score
                end_state = temp_end_state
            if temp_reward == AI_WON:  # I found the good board so PRUNE it
                break

        # print(board)
        print(best_board)
        print('final score: ', -worst_their_score)

        return best_board, -worst_their_score, end_state


def moves(board, side, my_piece):

    global new_board

    board_list = []
    step_actions = {
        'move': -1,
        'place': -1,
        'delete': -1,
    }

    if my_piece > 0:  # I am in PHASE 1

        for i, value in enumerate(board):
            if value == 3:  # is placeable
                new_board = [va for va in board]  # copy a current board...
                new_board[i] = side  # ... with my placed piece
                step_actions['place'] = i

                # find capturable pieces if it forms a mill
                if checkMillWithBoard(new_board, side, i):
                    for x in capturables(new_board, side):
                        # step_actions['delete'] = i
                        board_list.append(x)
                # Or just simply add the board to the list
                else:
                    board_list.append(new_board)

    elif board.count(side) > 3:  # I am in PHASE 2

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
                            for x in capturables(new_board, side):
                                board_list.append(x)
                        # Or just simply add the board to the list
                        else:
                            board_list.append(new_board)

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
                            for x in capturables(new_board, side):
                                board_list.append(x)
                        # Or just simply add the board to the list
                        else:
                            board_list.append(new_board)

    return board_list


def capturables(board, side):
    legal = []  # array of enemy nodes outside mill
    # enemy nodes inside mill, uncapturable
    illegal = []
    for i, value in enumerate(board):
        if value == swap(side):
            new_board = [va for va in board]
            new_board[i] = 3
            # add em to the list
            if checkMillWithBoard(board, swap(side), i):  # if correct.
                legal.append(new_board)
            else:
                illegal.append(new_board)
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

                    # extra value for potential mill
                    if checkMillWithBoard(board, side, space):
                        print('POTENTIAL MILL FOUND FROM', i, 'TO', space)
                        value += 10

            # count number of pieces mills then
            # divide by 3 rounded up
            if checkMillWithBoard(board, side, i):
                mills += 1

    if mills % 3 != 0:
        mills += 3 - (mills % 3)
    mills = mills / 3
    value += (15 * mills)

    print('player', side, 'has', value, 'with \t\t\t', mills, 'mills')

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
