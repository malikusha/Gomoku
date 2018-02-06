import os, math, time, threading, random
import numpy as np
import gomokuCollection as boardlib

# Constants - Variables that won't change
TEAM_NAME = "minimax"
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
TIME_LIMIT = 10  # Seconds
BOARD_SIZE = 15

WIN_SCORE_CUTOFF = 1000000 #If heuristics weight is higher than this score, than it is a win

# Objects
white = boardlib.GomokuCollection()
black = boardlib.GomokuCollection()

# Variables that will change
firstPlayer = True
playerMoves = []
enemyMoves = []
firstMove = True

validMoves = []  # Holds a list of all valid moves in the vicinity
bestMove = None
bestValue = float("-inf")
cutOff = False

board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

def init():
    global firstPlayer
    global bestValue
    # The Player stops playing once the game has ended
    while "end_game" not in os.listdir("."):

        # The player moves only if "Large_Horse.go" file appears in directory
        if TEAM_NAME+".go" in os.listdir("."):
            time.sleep(0.1)
            # Check move_file to read the current moves
            move_file = open("move_file", 'r')
            move = move_file.read()
            move_file.close()
            time.sleep(.1)
            # On first turn, need to denote whether player is playing first in start of game or not
            if not move:
                # There are no previous moves, therefore player is playing first in the game

                firstPlayer = True  # Starting Player

                # Make a move and write to file
                f = open("move_file", 'w')
                f.write(TEAM_NAME + " " + "H" + " " + str(8)) # First play at H 8
                f.close()
                addMoveToBoard(7, 7, True)

            elif move.split()[0] != TEAM_NAME:
                bestValue = float("-inf")

                # Player is not starting player in beginning of game
                # Because there will always be a move in other turns,
                # this statement will always be true after the first play

                firstPlayer = False # Plays after other enemy player

                # Obtain row and column of enemy player move
                row = int(move.split()[2]) - 1
                col = COLUMNS.index(move.split()[1].upper())

                addMoveToBoard(row, col, False)  # add enemy move to board
                # Obtain the enemy player move, update move to internal board, and make a move and write to file
                makeMove()


    return

def addMoveToBoard(i, j, ourMove):
    global white
    global black
    global board
    if not ourMove:
        try:
            board[i, j] = -1
            black.addMove((i,j))
            white.addEnemyMove((i,j))
            black.addMove((i, j))
            
        except Exception as e:
            print("Move is not added")
    else:
        try:
            board[i, j] = 1
            white.addMove((i,j))
            black.addEnemyMove((i,j))
            
        except Exception as e:
            print("Move is not added")

    return

def removeMoveFromBoard(i, j, ourMove):
    global white
    global black
    global board

    black.undoMove()
    white.undoMove()
    board[i, j] = 0
    return

def makeMove():
    global bestMove
    global white
    minimax2()
    addMoveToBoard(bestMove[0], bestMove[1], True)
    f = open("move_file", 'w')
    f.write( TEAM_NAME + " " + COLUMNS[bestMove[1]] + " " + str(bestMove[0]+1))
    f.close()

def minimax2():
    global white
    global black
    global bestMove
    global cutOff
    validMoves = getValidMoves()
    maxScore = -1<<31
    for move in validMoves:
        addMoveToBoard(move[0], move[1], True)
        curScore = white.getScore()-black.getScore()
        if(curScore > maxScore):
            maxScore = curScore
            bestMove = move
        removeMoveFromBoard(move[0], move[1], True)
    return


def getValidMoves():
    global white
    global black
    whitePotentialMoves = white.getPotentialMoves()
    blackPotentialMoves = black.getPotentialMoves()
    return (whitePotentialMoves | blackPotentialMoves) 


returns = init()

