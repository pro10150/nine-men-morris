import random
from config import *

# ตัวกระดานตำแหน่งพิกัดต่างๆ

DEBUGPRINT = True

# 3 คือช่องว่าง
# board = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3] # 24 member of 3 (aka null)
board = [3] * 24

# พิกัดที่ต่อกัน3ตำแหน่งแล้วจะลบตัวฝั่งตรงข้ามได้
# first list: vertical mill / second list: horizontal mill
mill = [
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

# เช็คว่าแต่ละฝั่งมีเบี้ยเหลือเท่าไหร่บ้าง
playerPawn = {
    1: 9,
    2: 9
}

pawnToPlace = {
    1: 9,
    2: 9
}

# เก็บจำนวนรอบ
round = 0
# เช็คว่าphase3เริ่มรึยัง
phase3StartFlag = False
# เช็คว่าphase3จบรึยัง
phase3EndFlag = False
# เช็คว่าเกมจบรึยัง
endGameFlag = False
# เช็คว่าผู้เล่นที่1เป็นคนเข้าphase3รึเปล่า
player1Phase3Flag = False

pawn = [0, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 20, 21, 22, 23]

# ตำแหน่งที่เบี้ยเดินไปได้
movablePawn = [

    [9, 1],
    [4, 0, 2],
    [14, 1],
    [10, 4],
    [7, 1, 3, 5],
    [4, 13],
    [11, 7],
    [4, 6, 8],
    [12, 7],
    [21, 0, 10],
    [18, 3, 9, 11],
    [15, 6, 10],
    [17, 8, 13],
    [20, 5, 12, 14],
    [23, 2, 13],
    [11, 16],
    [19, 15, 17],
    [12, 16],
    [10, 19],
    [22, 16, 18, 20],
    [13, 19],
    [9, 22],
    [19, 21, 23],
    [14, 22]
]


# ฟังก์ชั่นสำหรับอัพเดทตัวในบอร์ดว่ามีตำแหน่งไหนใช้ไปแล้วบ้าง
def updateMill():
    global mill
    mill = [

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


# เช็คว่าตำแหน่งที่เราลงไปเรียง3ตัวรึยัง
def checkMill(player, cdn):

    if mill[cdn][0].count(player) == 2 or mill[cdn][1].count(player) == 2:
        return True
    else:
        return False

# วางเบี้ย phase 1


def placePawn(player, cdn):
    board[cdn] = player
    pawnToPlace[player] -= 1
    # if DEBUGPRINT:
    #     print('Player ' + str(player) + ' placed a pawn on ' + str(cdn))
    updateMill()
    updateCurrentBoardPosition()


# เช็คการเดิน phase 2 ว่าถูกต้องมั้ย
def move(player, st, end):
    while (True):
        if end in movablePawn[st] and board[end] == 3 and board[st] == player:
            movePawn(player, st, end)
            break
        else:
            print(
                "Invalid movement please choose another set of starting and ending coordinate")
            st = input("starting point: ")
            end = input("ending point: ")


# เช็คการเดิน phase 3 ว่าถูกต้องมั้ย
def jump(player, st, end):
    while (True):
        if board[end] == 3:
            movePawn(player, st, end)
            break
        else:
            print(
                "Invalid movement please choose another set of starting and ending coordinate")
            st = input("starting point: ")
            end = input("ending point: ")


# ฟังก์ชันการเดิน
def movePawn(player, st, end):
    board[st] = 3
    board[end] = player
    # if DEBUGPRINT:
    #     print('Player ' + str(player) + ' moved a pawn on ' +
    #           str(st) + ' to ' + str(end))
    updateMill()
    updateCurrentBoardPosition()


# การลบตัว
def delete(i):
    print("You connected 3 straight point and can remove one of oppoents pawn!")
    while (True):
        cdn = input("Please input opponent's pawn cdn: ")
        if cdn in board and board[cdn] == i:
            deletePawn(i, cdn)
            break
        else:
            print("Invalid cdn. Please use another cdn")


# ฟังก์ชันการลบตัว
def deletePawn(player, cdn):
    global phase3StartFlag
    global endGameFlag
    if board[cdn] == player:
        board[cdn] = 3
        playerPawn[player] = playerPawn[player] - 1
        if playerPawn[player] == 3:
            phase3StartFlag = True
        elif playerPawn[player] <= 2:
            endGameFlag = True

        if DEBUGPRINT:
            print('Player ' + str(player) +
                  ' chose to remove a pawn on ' + str(cdn))
        print("Player pawn: ", playerPawn[player])
        return True
    else:
        return False


def autoDelete(player):
    print("You connected 3 straight point and can remove one of oppoents pawn!")
    while (True):
        cdn = randomPlace()
        if deletable(player, cdn):
            deletePawn(player, cdn)
            break


def targetedDelete(player, cdn):
    print("You connected 3 straight point and can remove one of oppoents pawn!")
    if deletable(player, cdn):
        if board[cdn] == 3:  # Failsafe
            autoDelete(player)
        else:
            deletePawn(player, cdn)


def randomPlace():
    c = random.randrange(0, 24)
    # print('landing on ' + str(c))

    return c


def randomMove(player):
    while (True):
        a = random.randrange(0, 24)
        if board[a] == player:
            b = random.choice(movablePawn[a])
            break
    return a, b


def randomJump(player):
    while (True):
        a = random.randrange(0, 24)
        if board[a] == player:
            b = random.randrange(0, 24)
            if board[b] == 3:
                break

    return a, b


# เช็คว่าสามารถวางเบี้ยได้มั้ยใน phase 1
def placeable(player, cdn):
    if board[cdn] == 3:
        return True
    else:
        return False


# เช็คว่าสามารถเดินได้มั้ยใน phase 2
def movable(player, st, end):
    if end in movablePawn[st] and board[st] == player and board[end] == 3:
        return True
    else:
        return False


# เช็คว่าลบได้มั้ย
def deletable(player, cdn):
    if board[cdn] == player:
        return True
    else:
        return False


# เช็คว่ากระโดดได้มั้ยใน phase 3
def jumpable(player, st, end):
    if board[st] == player and board[end] == 3:
        return True
    else:
        return False


def updateCurrentBoardPosition():
    i = 0
    for x in board:
        CURRENTBOARDPOSITION[POSITION[i][0]][POSITION[i][1]] = board[i]
        i += 1
