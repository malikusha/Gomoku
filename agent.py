import os, math
import numpy as np
import boardlib as boardlib

"""
TODO: Set the timer to return bestMoveSoFar when 9 seconds pass
TODO: Alpha-beta pruning with iterative deepening
"""


teamName = "Large_Horse"
bestMoveSoFar = None
bestValueSoFar = 0
white = boardlib.GomokuCollection()
black = boardlib.GomokuCollection()
validMoves = []
board = np.zeros((15,15), dtype=int)
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
    global bestValueSoFar
    global bestMoveSoFar
    # choose a move
    for move in validMoves:
        # add each move to the board and get the value
        addMove(team, move[0], move[1])
        currentMaxVal = getMaxValue(3)
        if (bestValueSoFar < currentMaxVal or bestValueSoFar == None):
            bestValueSoFar = currentMaxVal
            bestMoveSoFar = move
        else:
            deleteMove(team, move[0], move[1])
    return (bestMoveSoFar[0], columns[bestMoveSoFar[1]])

def getMaxValue(depth):
    utility = white.getScore()-black.getScore()
    if (depth == 0 or not validMoves or utility >= 10000000000000000000000000000):
        return utility
    else:
        max_val = float("-inf")
        for move in validMoves:
            addMove("max", move[0], move[1])
            child = getMinValue(depth-1)
            result = max(child, max_val)
    return result

def getMinValue(depth):
    utility = white.getScore() - black.getScore()
    if (depth == 0 or not validMoves or utility >= 10000000000000000000000000000):
        return utility
    else:
        min_val = float("inf")
        for move in validMoves:
            addMove("min", move[0], move[1])
            child = getMaxValue(depth-1)
            result = min(child, min_val)
    return result

def addMove(team, i, j):
    global white
    global black
    if (team == "min"):
        black.addNewMove((i, j))
        board[i, j] = -1
    else:
        white.addNewMove((i, j))
        board[i, j] = 1
    # Remove the move from the validMoves list
    validMoves.remove((i,j))
    return

def deleteMove(team, i, j):
    if (team == "min"):
        black.removeMove((i, j))
    else:
        white.removeMove((i, j))
    board[i, j] = 0
    # Add the move to the validMoves list
    (i, j)+validMoves
    return

returns = init()


# Tests for adding the move to the board
print(board)
print((2,3) in validMoves)
addMove("min", 2, 3)
print(board)
print((2,3) in validMoves)
# getMaxValue(4)



# white = boardlib.GomokuCollection()
# black = boardlib.GomokuCollection()
# white.addNewMove((3,3))
# black.addNewMove((2,3))
# white.addNewMove((4,3))
# black.addNewMove((1,3))
# utility = white.getScore() - black.getScore()
# print(utility)