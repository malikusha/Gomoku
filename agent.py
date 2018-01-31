import os, math
import numpy as np
import boardlib as boardlib

teamName = "Large_Horse"
white = boardlib.GomokuCollection()
black = boardlib.GomokuCollection()
validMoves = []
for x in range(0,15):
    for y in range(0,15):
        validMoves.append((x, y))
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def init():
    while("end_game" not in os.listdir(".")):
        print("hi")
        if (teamName+".go" in os.listdir(".")):
            move_file = open("move_file", 'r')
            move = move_file.read()
            move_file.close()
            if (move):
                if (move.split()[0] != "Large_Horse"):
                    j = columns.index(move.split()[1])
                    i = int(move.split()[2])
                    f = open("move_file", 'w')
                    f.write(makeMove("min", i, j))
                    f.close()
            elif (not move):
                f = open("move_file", 'w')
                f.write(makeMove("max", -1, -1))
                f.close()
    return

def makeMove(team, i, j):
    # add the opponent's move to the board
    if (team == "min"):
        addMove(team, i, j)
        team = "max"
    move = minimax(team)
    return teamName + " " + str(move[1]) + " " + str(move[0])

def minimax(team):
    bestMoveSoFar = validMoves[0]
    bestValueSoFar = getMaxValue(3)
    # choose a move
    for move in validMoves:
        # add each move to the board and get the value
        addMove(team, move[0], move[1])
        currentMaxVal = getMaxValue(3)
        if (bestValueSoFar < currentMaxVal):
            bestValueSoFar = currentMaxVal
            bestMoveSoFar = move
        else:
            deleteMove(team, move[0], move[1])
    return [bestMoveSoFar[0], columns[bestMoveSoFar[1]]]

def getMaxValue(depth):
    if (depth == 0):
        return white.getScore()-black.getScore()
    else:
        result = None
        max = float("-inf")
        for move in validMoves:
            addMove("max", move[0], move[1])
            child = getMinValue(depth-1)
            result = max(child, max)
    return result

def getMinValue(depth):
    if (depth == 0):
        return white.getScore()-black.getScore()
    else:
        result = None
        min = float("inf")
        for move in validMoves:
            addMove("min", move[0], move[1])
            child = getMaxValue(depth-1)
            result = min(child, min)
    return result

# check first diagonal, color is the the color of a player black or white, -1 for black and +1 for white
# def winFDiagonal(color):
#     n = 0
#     for j in range(0, 11):
#         lower = j
#         upper = j
#         sum = 0
#         while (upper < 224-n) and (lower < 224-n):
#             if (sum != 5):
#                 if (board[lower] != color):
#                     sum = 0
#                     lower = upper + 16
#                     upper = lower
#                 elif (board[upper] == color):
#                     upper += 16
#                     sum = sum + 1
#                 elif (board[upper] != color):
#                     lower = upper
#             else:
#                 return True
#         n += 15
#     i = 15
#     while (i < 167):
#         lower = i
#         upper = i
#         sum = 0
#         while (upper < 223-n) and (lower < 223-n):
#             if (sum != 5):
#                 if(board[lower] != color):
#                     sum = 0
#                     lower = upper + 16
#                     upper = lower
#                 elif(board[upper] == color):
#                     upper += 16
#                     sum = sum + 1
#                 elif(board[upper] != color):
#                     lower = upper
#             else:
#                 return True
#         n += 1
#         i += 16
#     return False

# and then bottom part of the board, excluding the last three rows/columns


def addMove(team, i, j):
    if (team == "min"):
        black.addNewMove(i,j)
    else:
        white.addNewMove(i, j)
    # Remove the move from the validMoves list
    validMoves.remove((i,j))
    return

def deleteMove(team, i, j):
    if (team == "min"):
        black.removeMove(i,j)
    else:
        white.removeMove(i,j)
    # Add the move to the validMoves list
    (i, j)+validMoves
    return

returns = init()



white = boardlib.GomokuCollection()
black = boardlib.GomokuCollection()
white.addNewMove((3,3))
black.addNewMove((2,3))
white.addNewMove((4,3))
black.addNewMove((1,3))
utility = white.getScore() - black.getScore()
print(utility)