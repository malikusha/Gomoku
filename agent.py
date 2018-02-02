import os, math, time
import numpy as np
import boardlib as boardlib
import time
import threading
"""
TODO: Set the timer to return bestMoveSoFar when 9 seconds pass - iterarive deepening (aka cutoff)
TODO: Sort the validMoves by their desirability
"""


teamName = "Large_Horse"
timeLimit = 10
bestMove = (14, 14)
bestValue = float("-inf")
white = boardlib.GomokuCollection()
black = boardlib.GomokuCollection()
validMoves = []
board = np.zeros((15,15), dtype=int)
for x in range(0,15):
    for y in range(0,15):
        validMoves.append((x, y))
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
winScoreCutOff = 1000000
cutOff = False
DEBUG = True

def init():
    if(DEBUG):
        print("Starting init")
    t = threading.Timer(3.0, writeToFile)
    t.start()
    while("end_game" not in os.listdir(".")):
        if (teamName+".go" in os.listdir(".")):
            move_file = open("move_file", 'r')
            move = move_file.read()
            move_file.close()
           
            if (move):
                if (move.split()[0] != "Large_Horse"):
                    j = columns.index(move.split()[1])
                    i = int(move.split()[2])-1
                    f = open("move_file", 'w')
                    f.write(makeMove("min", i, j))
                    f.close()
            elif (not move):
                f = open("move_file", 'w')
                f.write(makeMove("max", -1, -1))
                f.close()

    return
#Writes the current best move to the move_file
def writeToFile():
    global bestMove
    f = open("move_file", 'w')
    #f.write(teamName + " " + columns[bestMove[1]] + " " + str(bestMove[0]+1))
    print("wrote: " + str(bestMove) + " to move_file")
    

def makeMove(team, i, j):
    # add the opponent's move to the board
    if (team == "min"):
        addMove(team, i, j)
        team = "max"
    move = minimax(team)
    #addMove(team, move[0], columns.index(move[1]))
    return teamName + " " + str(move[1]).upper() + " " + str(move[0]+1)

def minimax(team):
    global bestValue
    global bestMove
    # choose a move
    for move in validMoves:
        if(DEBUG):
            #print("Best Move: " +  str(bestMove))
            pass
        # add each move to the board and get the value
        addMove(team, move[0], move[1])
        timeLimitForMove = 1000/len(validMoves)
        currentMaxVal = ID(timeLimitForMove)
        if(DEBUG):
            #print("current max val: " + str(currentMaxVal))
            pass
        if (currentMaxVal >= winScoreCutOff):
            return (move[0], columns[move[1]])
        if (bestValue < currentMaxVal):
            bestValue = currentMaxVal
            bestMove = move
        deleteMove(team, move[0], move[1])
    return (bestMove[0], columns[bestMove[1]])

def ID(timeLimitForMove):
    global cutOff
    depthLimit = 1
    stopTime = time.time() + timeLimitForMove
    maxVal = 0
    while(1):
        if(DEBUG):
            print(maxVal)
            pass
        if (time.time() >= stopTime):
            print("BREAK!")
            break
        currentMaxVal = getMaxValue(stopTime, float("-inf"), float("inf"), depthLimit)
        
        if (currentMaxVal >= winScoreCutOff):
            return currentMaxVal
        if (not cutOff):
            maxVal = currentMaxVal
        depthLimit += 1
    cutOff = False
    return maxVal

def getMaxValue(stopTime, alpha, beta, depth):
    global cutOff
    eval = white.getScore()-black.getScore()
    if DEBUG:
        print("eval"+str(eval))
    if (time.time() >= stopTime):
        cutOff = True
    if (not validMoves or eval >= winScoreCutOff or cutOff or depth == 0):
        return eval
    else:
        value = float("-inf")
        for move in validMoves:
            addMove("max", move[0], move[1])
            child = getMinValue(stopTime, alpha, beta, depth - 1)
            value = max(value, child)
            deleteMove("max", move[0], move[1])
            if (value >= beta):
                return value
            alpha = max(alpha, value)
    return value

def getMinValue(stopTime, alpha, beta, depth):
    global cutOff
    eval = white.getScore() - black.getScore()

    if (time.time() >= stopTime):
        cutOff = True
    if (not validMoves or eval <= -winScoreCutOff or cutOff or depth == 0):
        return eval
    else:
        value = float("inf")
        for move in validMoves:
            addMove("min", move[0], move[1])
            child = getMaxValue(stopTime, alpha, beta, depth - 1)
            value = min(value, child)
            deleteMove("min", move[0], move[1])
            if (value <= alpha):
                return value
            beta = min(beta, value)
    return value

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
        black.undoMove()
    else:
        white.undoMove()
    board[i, j] = 0
    # Add the move to the validMoves list
    validMoves.append((i,j))
    return

returns = init()



# Tests for adding the move to the board
# print(board)
# print((2,3) in validMoves)
# addMove("min", 2, 3)
# print(board)
# print((2,3) in validMoves)
# getMaxValue(4)

# white = boardlib.GomokuCollection()
# black = boardlib.GomokuCollection()
# white.addNewMove((3,3))
# black.addNewMove((2,3))
# white.addNewMove((4,3))
# black.addNewMove((1,3))
# utility = white.getScore() - black.getScore()
# print(utility)
