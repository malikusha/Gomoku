import os, math
import numpy as np

teamName = "knuckles"
board = np.zeros((225,), dtype=np.int)
validMoves = []
for x in range(0,15):
    for y in range(0,15):
        validMoves.append([x, y])
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
print(board)

def init():
    while(teamName+".go" in os.listdir(".") and "end_game" not in os.listdir(".")):
        move_file = open("move_file", 'r')
        move = move_file.read()                            # move is the opponent's move
        i=-1; j=-1
        if not move:
            team = "max"
        else:
            team = "min"
            j = columns.index(move.split()[1])
            i = int(move.split()[2])
        move_file.close()                                  # if the move_file is empty, you are playing with white (move = 0)
        f = open("move_file", 'w')
        f.write(makeMove(team, i, j))
        f.close()
    return

def makeMove(team, i, j):
    # add the opponent's move to the board
    if (team == "min"):
        addMove(team, i, j)
        team = "max"
    move = minimax(team)
    return teamName + " " + move[1] + " " + move[0]

def minimax(team):
    bestMoveSoFar = validMoves[0]
    bestValueSoFar = getMaxValue()
    # choose a move
    for move in validMoves:
        # add each move to the board and get the value
        addMove(team, move[0], move[1])
        currentMaxVal = getMaxValue(move)
        if (bestValueSoFar < currentMaxVal):
            bestValueSoFar = currentMaxVal
            bestMoveSoFar = move
        else:
            deleteMove(team, move[0], move[1])
    return [bestMoveSoFar[0], columns[bestMoveSoFar[1]]]

def getMaxValue():
    state = terminalState()
    if (state != -2):
        return state
    else:
        result = None
        max = float("-inf")
        for move in validMoves:
            addMove("max", move[0], move[1])
            child = getMinValue()
            result = max(child, max)
    return result

def getMinValue():
    state = terminalState()
    if (state != -2):
        return state
    else:
        result = None
        min = float("inf")
        for move in validMoves:
            addMove("min", move[0], move[1])
            child = getMaxValue()
            result = min(child, min)
    return result

# returns 1 if max won, -1 if min won, 0 if a tie and -2 if not a terminal state yet
def terminalState():

    return

def addMove(team, i, j):
    x = IJToX(i, j)
    if (team == "min"):
        # -1 represents black piece on the board
        board[x] = -1
    else:
        # 1 represents white piece on the board
        board[x] = 1
    # Remove the move from the validMoves list
    validMoves.remove([i,j])
    return

def deleteMove(team, i, j):
    x = IJToX(i, j)
    board[x] = 0
    # Add the move to the validMoves list
    [i, j]+validMoves
    return

def IJToX(i, j):
    x = i*15+j
    return x

def xToIJ(x):
    i = math.floor(x/15)
    j = x%15
    return [i, j]

returns = init()






