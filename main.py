import pygame
import sys
from PIL.ImageChops import screen
from pygame.locals import *
from config import *
from logic import *
from ai import *

from pygame.surface import *

import time
import pygame.freetype
import re
import random

waittime = 0.1


def draw_board():
    pygame.init()

    # Initializing surface
    surface = pygame.display.set_mode((650, 650))
    pygame.display.set_caption("Nine men's morris")

    # Initialing Color
    color = (255, 0, 0)

    for x in range(len(LINES)):
        pygame.draw.line(surface, WHITE,
                         (LINES[x][0] * SQUARESIZE, SQUARESIZE * LINES[x][1]),
                         (LINES[x][2] * SQUARESIZE, LINES[x][3] * SQUARESIZE), 5)

    for r in range(ROWS):
        for c in range(COLS):
            radius = RADIUS
            color2 = WHITE
            if (int(CURRENTBOARDPOSITION[r][c]) == PLAY1):  # p1 is red
                (color2, radius) = (RED, radius)
            elif (int(CURRENTBOARDPOSITION[r][c]) == PLAY2):  # p2 is blue
                (color2, radius) = (BLUE, radius)
            elif (int(BOARDPOSTION[r][c] == VALID)):
                radius = int(RADIUS / 2)
            else:
                radius = 0

            pygame.draw.circle(surface, color2,
                               (int(c * SQUARESIZE + SQUARESIZE / 2),
                                int(r * SQUARESIZE + SQUARESIZE / 2)), radius)

# phase 1


def mainAutoPhase1():
    global round
    for round in range(9):
        time.sleep(waittime)
        # print("round ", round + 1)
        for i in range(2):  # i = 0 is player 1, i = 1 is player 2
            # print("Player " + str(i+1) + " round")
            draw_board()
            pygame.display.update()
            while (True):

                if i == 0:
                    cdn = randomPlace()  # using random ai
                else:
                    # using algorithm
                    _, cdn, remov = ai_step(
                        board, i + 1, pawnToPlace[2], pawnToPlace[1])

                if placeable(i, cdn):  # only check if placeable
                    break

            placePawn(i + 1, cdn)

            if checkMill(i + 1, cdn):  # after placing, check if a mill is formed
                if i == 0:
                    autoDelete(2)  # using random ai
                else:
                    targetedDelete(1, remov)  # using algorithm

    print("This is the end of phase 1")

# phase 2


def mainAutoPhase2():
    global round, phase3EndFlag, phase3StartFlag, player1Phase3Flag
    istie = False
    round += 1
    print("Welcome to Phase 2 of the game!")
    print("You can now move the pawn in the board next to their starting point.")
    print("Same rule applies.")

    while (True):
        round += 1
        # print("round " + str(round))

        time.sleep(waittime)
        draw_board()
        pygame.display.update()

        for i in range(2):
            # print("Player " + str(i+1) + " round")
            if player1Phase3Flag:
                player1Phase3Flag = False
                continue
            time.sleep(waittime)
            draw_board()
            pygame.display.update()
            # Move
            while (True):
                if i == 0:
                    st, end = randomMove(i + 1)  # using random ai
                else:
                    # using algorithm
                    st, end, remov = ai_step(
                        board, i + 1, pawnToPlace[2], pawnToPlace[1])

                    if end == -1 or st == -1:
                        print('FAILSAFE ACTIVE')
                        # FAILSAFE WHEN EITHER IS INVALID
                        st, end = randomMove(i + 1)

                if movable(i + 1, st, end):
                    break

            move(i + 1, st, end)

            if checkMill(i + 1, end):
                if i == 0:
                    autoDelete(2)  # using random ai
                else:
                    targetedDelete(1, remov)  # using algorithm

            if phase3StartFlag and phase3EndFlag == False:
                if i == 0:
                    mainAutoPhase3(2)
                    phase3EndFlag = True
                    break
                else:
                    mainAutoPhase3(1)
                    phase3EndFlag = True
                    player1Phase3Flag = True
            elif playerPawn[1] == 2 or playerPawn[2] == 2:
                break

        if round > 99:  # END THE GAME WITH TIE
            istie = True
            break
        if playerPawn[1] == 2 or playerPawn[2] == 2:  # END THE GAME
            break
    print("YEET")
    time.sleep(waittime)
    updateCurrentBoardPosition()
    draw_board()
    pygame.display.update()
    print("This game has ended!")
    if istie:
        print("It's a tie")
    else:
        print("Congrats to player ", i + 1)
    print("Round : ", round)


def mainAutoPhase3(player):
    global round
    round += 1
    print("Welcome to Phase 3 of the game!")
    print("You can now move the pawn in the board in any coordinate that's still an empty spot for one move.")
    print("Same rule applies.")
    print("Player " + str(player) + "round")
    time.sleep(waittime)
    draw_board()
    pygame.display.update()
    while (True):
        if player == 1:
            st, end = randomJump(player)  # using randomness
        else:
            # using algorithm
            st, end, remov = ai_step(
                board, player, pawnToPlace[2], pawnToPlace[1])

            if end == -1:
                print('FAILSAFE ACTIVE')
                st, end = randomMove(player)  # FAILSAFE
        if st in board and end in board and board[st] == player and board[end] == 3:
            break
    jump(player, st, end)
    if checkMill(player, end):
        if player == 1:
            autoDelete(2)  # using randomness
        else:
            targetedDelete(1, remov)  # using algorithm


def main():
    mainAutoPhase1()
    mainAutoPhase2()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


main()
