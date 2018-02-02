import os, math, time, threading, random
import numpy as np
import boardlib as boardlib

""" TODO
FOR boardlib
make sure that all pieces have to be within the borders of the board of the game

"""

# Constants - Variables that won't change
TEAM_NAME = "Large_Horse"
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
TIME_LIMIT = 10  # Seconds
BOARD_SIZE = 15
DEBUG = False # if DEBUG: print("")
DEBUG2 = True
WIN_SCORE_CUTOFF = 1000000 #If heuristics weight is higher than this score, than it is a win

# Objects
white = boardlib.GomokuCollection()
black = boardlib.GomokuCollection()

# Variables that will change
firstPlayer = True
playerMoves = []
enemyMoves = []

validMoves = []  # Holds a list of all valid moves in the vicinity
bestMove = None
bestValue = float("-inf")
cutOff = False

board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

def init():
    global firstPlayer
    # The Player stops playing once the game has ended
    while "end_game" not in os.listdir("."):

        # The player moves only if "Large_Horse.go" file appears in directory
        if TEAM_NAME+".go" in os.listdir("."):
            time.sleep(0.5)
            # Check move_file to read the current moves
            move_file = open("move_file", 'r')
            move = move_file.read()
            move_file.close()
            # On first turn, need to denote whether player is playing first in start of game or not
            if not move:
                # There are no previous moves, therefore player is playing first in the game

                firstPlayer = True  # Starting Player

                # Make a move and write to file
                f = open("move_file", 'w')
                f.write(TEAM_NAME + " " + "H" + " " + str(8)) # First play at H 8
                if DEBUG: print("Wrote")
                f.close()
                addMoveToBoard(7, 7, True)

            elif move.split()[0] != TEAM_NAME:

                # Player is not starting player in beginning of game
                # Because there will always be a move in other turns,
                # this statement will always be true after the first play

                firstPlayer = False # Plays after other enemy player

                # Obtain row and column of enemy player move
                row = int(move.split()[2]) - 1
                col = COLUMNS.index(move.split()[1].upper())
                if DEBUG2: print("ROW: %i, COLUMN: %i" % (row,col))

                addMoveToBoard(row, col, False)  # add enemy move to board

                # Obtain the enemy player move, update move to internal board, and make a move and write to file
                f = open("move_file", 'w')
                f.write(makeMove())
                f.close()


    return

def addMoveToBoard(i, j, ourMove):
    global white
    global black
    global board
    if not ourMove:
        try:
            board[i, j] = -1
            black.addNewMove((i, j))
        except:
            print("Bhon lied its still going out of bounds " + str(i) + " " + str(j))
    else:
        try:
            board[i, j] = 1
            white.addNewMove((i, j))
        except:
            print("Bhon lied its still going out of bounds" + str(i) + " " + str(j))
    # Remove the move from the validMoves list
    # validMoves.remove((i,j))
    return

def removeMoveFromBoard(i, j, ourMove):
    global white
    global black
    global board

    if (not ourMove):
        black.undoMove()
    else:
        white.undoMove()
    board[i, j] = 0
    return

def makeMove():
    global bestMove
    minimax()
    addMoveToBoard(bestMove[0], bestMove[1], True)
    return TEAM_NAME + " " + COLUMNS[bestMove[1]] + " " + str(bestMove[0]+1)

"""
opponent's move: d5 
valid moves: e5, c5, d4, d6, e4, e6, c4, c6
scans all of them, pick any move
"""
def minimax():
    global white
    global black
    global bestMove
    validMoves = getValidMoves()
    maxScore = -10

    if(DEBUG):
        print("Printing Valid Moves Obtained: ")
        print(validMoves)
    for move in validMoves:
        addMoveToBoard(move[0], move[1], True)
        # curScore = white.getScore()-black.getScore()
        curScore = getMaxValue(float("-inf"), float("-inf"), 3)
        if(maxScore < curScore):
            if(DEBUG): print(move)
            maxScore=curScore
            bestMove = move
            if DEBUG: print("Best Move: " + str(bestMove))
        removeMoveFromBoard(move[0], move[1], True)
    if(DEBUG):
        print("Best Move: " + str(bestMove))
        print("Best Score: " + str(maxScore))
        print("White")
        white.debugPrint()
        print("Black")
        black.debugPrint()

def getValidMoves():
    global white
    global black
    whitePotentialMoves = white.getPotentialMoves()
    whiteMovesMade = white.getMovesMade()
    blackPotentialMoves = black.getPotentialMoves()
    blackMovesMade = black.getMovesMade()
    y = ((whitePotentialMoves | blackPotentialMoves) - (whiteMovesMade|blackMovesMade))
    return y

def getMaxValue(alpha, beta, depth):
    if (depth == 0):
        if DEBUG: print("Val: " + str(white.getScore() - black.getScore()))
        return white.getScore()-black.getScore()
    else:
        value = float("-inf")
        for move in getValidMoves():
            addMoveToBoard(move[0], move[1], True)
            child = getMinValue(alpha, beta, depth - 1)
            value = max(value, child)
            removeMoveFromBoard(move[0], move[1], True)
            if (value >= beta):
                if DEBUG: print("Prune: "+str(value))
                return value
            alpha = max(alpha, value)
    return value

def getMinValue(alpha, beta, depth):
    if (depth == 0):
        if DEBUG: print("Val: "+str(white.getScore()-black.getScore()))
        return white.getScore()-black.getScore()
    else:
        value = float("inf")
        for move in getValidMoves():
            addMoveToBoard(move[0], move[1], False)
            child = getMaxValue(alpha, beta, depth - 1)
            value = min(value, child)
            removeMoveFromBoard(move[0], move[1], False)
            if (value <= alpha):
                if DEBUG: print("Prune: "+str(value))
                return value
            beta = min(beta, value)
    return value

returns = init()

