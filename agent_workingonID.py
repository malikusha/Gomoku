import os, math, time, threading, random
import numpy as np
import gomokuCollection as boardlib

# Constants - Variables that won't change
TEAM_NAME = "Large_Horse"
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
TIME_LIMIT = 10  # Seconds
BOARD_SIZE = 15
WIN_SCORE_CUTOFF = 100000  # If heuristics weight is higher than this score, than it is a win

# Objects
white = boardlib.GomokuCollection()
black = boardlib.GomokuCollection()

# Variables that will change
firstPlayer = True
firstMove = True
playerMoves = []
enemyMoves = []
bestMove = None
bestValue = float("-inf")

board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

def interruptWriteToFile():
    print("Interrupt Called")
    writeToFile()
t = None

def init():
    global firstPlayer
    global bestValue
    global firstMove
    global t
    # The Player stops playing once the game has ended
    while "end_game" not in os.listdir("."):
        # The player moves only if "Large_Horse.go" file appears in directory
        if TEAM_NAME+".go" in os.listdir("."):
            t = threading.Timer(90.0, interruptWriteToFile)
            
            time.sleep(0.1)
            # Check move_file to read the current moves
            move_file = open("move_file", 'r')
            move = move_file.read()
            move_file.close()
            time.sleep(0.1)
            # On first turn, need to denote whether player is playing first in start of game or not
            if not move:
                # There are no previous moves, therefore player is playing first in the game

                firstPlayer = True  # Starting Player

                # Make a move and write to file
                f = open("move_file", 'w')
                f.write(TEAM_NAME + " " + "H" + " " + str(8)) # First play at H 8
                f.close()
                addMoveToBoard(7, 7, True)
                firstMove = False

            elif move.split()[0] != TEAM_NAME:
                bestValue = float("-inf")

                # Player is not starting player in beginning of game
                # Because there will always be a move in other turns,
                # this statement will always be true after the first play

                #t.start()
                # Obtain row and column of enemy player move
                row = int(move.split()[2]) - 1
                col = COLUMNS.index(move.split()[1].upper())
                if (firstPlayer and board[row, col] == 1 and not firstMove):
                    removeMoveFromBoard(row, col, True)
                if (firstMove and col != 'A' and col != 'O' and row != 0 and row != 14):
                    f = open("move_file", 'w')
                    f.write(TEAM_NAME + " " + str(COLUMNS[col]) + " " + str(row+1))
                    f.close()
                    addMoveToBoard(row, col, True)
                    firstPlayer = False  # Plays after other enemy player
                    firstMove = False
                else:
                    addMoveToBoard(row, col, False)  # add enemy move to board
                    firstPlayer = False  # Plays after other enemy player
                    firstMove = False
                    # Obtain the enemy player move, update move to internal board, and make a move and write to file
                    makeMove()
                    t.cancel()



    return
"""
adds a move on to the board model
"""
def addMoveToBoard(i, j, ourMove):
    global white
    global black
    global board
    """ case where it is the opponents move"""
    if not ourMove:
        try:
            board[i, j] = -1
            black.addMove((i,j))
            white.addEnemyMove((i,j))
            
        except Exception as e:
            print("Move not added" + str(i) + " " + str(j))
    else:
        try:
            board[i, j] = 1
            white.addMove((i,j))
            black.addEnemyMove((i,j))
            
        except Exception as e:
            print("Move not added" + str(i) + " " + str(j))
    return
"""
Remove Opponent's Move from our board
"""
def removeMoveFromBoard(i, j, ourMove):
    global white
    global black
    global board

    black.undoMove()
    white.undoMove()
    board[i, j] = 0
    return
"""
Intermediate function that calls the minimax
and writes the bestValue set to the move_file
"""
def makeMove():
    depthLimited()
    writeToFile()
"""
Writes the bestMove to the move_file
"""
def writeToFile():
    global bestMove
    global t
    t.cancel()
    addMoveToBoard(bestMove[0], bestMove[1], True)
    f = open("move_file", 'w')
    f.write( TEAM_NAME + " " + COLUMNS[bestMove[1]] + " " + str(bestMove[0]+1))
    f.close()
    init()
"""
To be implemented: depthLimited search
"""
def depthLimited():
    minimax(2)

"""
The minimax with alpha beta pruning algorithm
"""
def alphaBeta(depth = 3, alpha = -1<<31, beta = 1<<31, isMaxPlayer = False):
    global white
    global black
    validMoves = getValidMoves()
    levelScore = white.getScore()-black.getScore()
    if(depth == 1 or (abs(levelScore)>WIN_SCORE_CUTOFF)):
        return levelScore
    if(isMaxPlayer):
        maxScore = -1<<31
        for move in validMoves:
            addMoveToBoard(move[0], move[1], True)
            maxScore = max(maxScore, alphaBeta(depth-1,alpha, beta, False))
            alpha = max(alpha, maxScore)
            removeMoveFromBoard(move[0], move[1], True)
            if(maxScore >  WIN_SCORE_CUTOFF):
                break
            if(beta <= alpha):
                break;
        return maxScore
    else:
        minScore = 1 <<31
        for move in validMoves:
            addMoveToBoard(move[0], move[1], False)
            minScore = min(minScore, alphaBeta(depth-1,alpha, beta, True))
            beta = min(beta, minScore)
            removeMoveFromBoard(move[0], move[1], False)
            if(minScore < -WIN_SCORE_CUTOFF):
                break
            if(beta <= alpha):
                break;
        return minScore
"""
The initiator of the minimax algorithm
"""
def minimax(depth = 1):
    global white
    global black
    global bestMove
    global cutOff
    allValidMoves = getValidMoves()
    maxScore = -1<<31
    for move in allValidMoves:
        addMoveToBoard(move[0], move[1], True)
        curScore = alphaBeta(depth,alpha = -1<<31, beta = 1<<31, isMaxPlayer = False)
        if(curScore > maxScore):
            maxScore = curScore
            bestMove = move
        removeMoveFromBoard(move[0], move[1], True)
    return bestMove

"""
Get potential candidate moves
"""
def getValidMoves():
    global white
    return white.getPotentialMoves()



#### FUNCTIONS FOR DEBUGGING PURPOSES #####
def getBestMove():
    global bestMove
    print("Best Move: " + bestMove)
def getHistory(team):
    if(team == 'w'):
        global white
        return white.history
    elif(team == 'b'):
        global black
        return black.history
    else:
        raise Exception("Not a valid team")
def algebraToMove(move):
    row = int(move.split()[1]) - 1
    col = COLUMNS.index(move.split()[0].upper())

returns = init()

