import os, math, time, threading, random
import numpy as np
import gomokuCollection as boardlib

""" TODO
FOR boardlib
"""

# Constants - Variables that won't change
TEAM_NAME = "Large_Horse"
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
TIME_LIMIT = 10  # Seconds
BOARD_SIZE = 15
DEBUG = True # if DEBUG: print("")
DEBUG2 = False
WIN_SCORE_CUTOFF = 100000 #If heuristics weight is higher than this score, than it is a win

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
def interruptWriteToFile():
    print("Interrupt Called")
    writeToFile()
t = None

def init():
    global firstPlayer
    global bestValue
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
                if DEBUG: print("Wrote")
                f.close()
                addMoveToBoard(7, 7, True)

            elif move.split()[0] != TEAM_NAME:
                if(DEBUG): print("Init making a move")
                bestValue = float("-inf")

                # Player is not starting player in beginning of game
                # Because there will always be a move in other turns,
                # this statement will always be true after the first play
    
                firstPlayer = False # Plays after other enemy player
                #t.start()
                # Obtain row and column of enemy player move
                row = int(move.split()[2]) - 1
                col = COLUMNS.index(move.split()[1].upper())
                if DEBUG2: print("ROW: %i, COLUMN: %i" % (row,col))

                addMoveToBoard(row, col, False)  # add enemy move to board
                # Obtain the enemy player move, update move to internal board, and make a move and write to file
                makeMove()
                t.cancel()


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
            
        except Exception as e:
            #white.debugPrintDictionary()
            #print(white.history)
            #print(black.history)
            #print("Bhon lied its still going out of bounds " + str(i) + " " + str(j))
            print("Wooooooooooooo")
    else:
        try:
            board[i, j] = 1
            white.addMove((i,j))
            black.addEnemyMove((i,j))
            
        except Exception as e:
            #print("Bhon lied its still going out of bounds" + str(i) + " " + str(j))
            #print(e)
            #print(white.history)
            #print(black.history)
            print("Wooooooooooooo")
    #if not DEBUG: print(board)
    return

def removeMoveFromBoard(i, j, ourMove):
    global white
    global black
    global board
    #print("Cur move Min: " + COLUMNS[j] + " " + str(i+1))

    black.undoMove()
    white.undoMove()
    board[i, j] = 0
    return

def makeMove():
    iterativeDeepening()
    writeToFile()

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
opponent's move: d5 
valid moves: e5, c5, d4, d6, e4, e6, c4, c6
scans all of them, pick any move
"""

def iterativeDeepening():
    #depth = 3
    #for i in range(1,depth+1):
    #    bestMove = minimaxTry(i)
    #    print("depth achieved: " + str(i))
    minimaxTry(2)

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
            #print(maxScore)
            alpha = max(alpha, maxScore)
            removeMoveFromBoard(move[0], move[1], True)
            if(beta <= alpha):
                break;
        return maxScore
    else:
        minScore = 1 <<31
        #print(validMoves)

        for move in validMoves:
            addMoveToBoard(move[0], move[1], False)
            #print("Cur move Min: " + COLUMNS[move[1]] + " " + str(move[0]+1))
            minScore = min(minScore, alphaBeta(depth-1,alpha, beta, True))
            #print(minScore)
            beta = min(beta, minScore)
            removeMoveFromBoard(move[0], move[1], False)
            #print(minScore)
            if(beta <= alpha):
                break;
        return minScore
"""
   A B C D E F G H I J K L M N O
 1 - - - - - - - - - - - - - - -
 2 - - - - - - - - - - - - - - -
 3 - - - - - - - - - - - - - - -
 4 - - - - - - - - - - - - - - -
 5 - - - - - O - - O - - - - - -
 6 - - - - - - O O X X - - - - -
 7 - - - - - - - O X - - - - - -
 8 - - - - - - - X X - - - - - -
 9 - - - - - - - - - - - - - - -
10 - - - - - - - - - - - - - - -
11 - - - - - - - - - - - - - - -
12 - - - - - - - - - - - - - - -
13 - - - - - - - - - - - - - - -
14 - - - - - - - - - - - - - - -
15 - - - - - - - - - - - - - - -
Why was K5 not play at depth = 2? fter placing K5, creating a free 4, if the opponent plays G9
the evaluation drops since it now interprets the position as a close 4. Though 
"""
def minimaxTry(depth = 1):
    global white
    global black
    global bestMove
    global cutOff
    allValidMoves = getValidMoves()
    #x = []
    maxScore = -1<<31
    #print(allValidMoves)
    #print white.printBoard()
    for move in allValidMoves:
        addMoveToBoard(move[0], move[1], True)
        #curScore = white.getScore()-black.getScore()
        #print("Cur move MM: " + COLUMNS[move[1]] + " " + str(move[0]+1))
        # print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
        #   for row in white.board]))
        curScore = alphaBeta(depth,alpha = -1<<31, beta = 1<<31, isMaxPlayer = False)
        #print(curScore)

        if(curScore > maxScore):
            maxScore = curScore
            bestMove = move
            #print("Best Move Updated: " + COLUMNS[move[1]] + " " + str(move[0]+1))
        removeMoveFromBoard(move[0], move[1], True)
    return bestMove

def getMin(depth = 3, alpha = -1<<31, beta = 1<<31):
    global white
    global black
    levelScore = white.getScore()-black.getScore()
    if(abs(levelScore) > WIN_SCORE_CUTOFF):
        return levelScore
    elif(depth==1):
        return levelScore
    else:
        minScore = 1<<31
        validMoves = getValidMoves()
        #print(validMoves)
        for move in validMoves:
            #print("Cur move Min: " + COLUMNS[move[1]] + " " + str(move[0]+1))

            addMoveToBoard(move[0], move[1], False)
            curScore = getMax(depth-1, alpha, beta)
            #print(curScore)
            if(curScore < minScore): minScore = curScore
            beta = min(alpha, minScore)
            removeMoveFromBoard(move[0], move[1], False)
            if(beta <= alpha):
                break;
        return minScore
            
def getMax(depth, alpha, beta):
    global white
    global black
    levelScore = white.getScore()-black.getScore()
    if(abs(levelScore) > WIN_SCORE_CUTOFF):
        return levelScore
    elif(depth==1):
        return levelScore
    else:
        maxScore = -1<<31
        validMoves = getValidMoves()
        for move in validMoves:
            #print("Cur move max: " + COLUMNS[move[1]] + " " + str(move[0]+1))
            addMoveToBoard(move[0], move[1], True)
            #curScore = white.getScore()-black.getScore()
            curScore = getMin(depth-1, alpha, beta)
            #print(curScore)
            #print("Score: " + str(curScore))
            removeMoveFromBoard(move[0], move[1], True)
            if(curScore > maxScore): maxScore = curScore
            alpha = max(alpha, maxScore)
            if(beta <= alpha):
                break;
        return maxScore


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
        print("Score: " + str(curScore))
        if(curScore > maxScore):
            maxScore = curScore
            bestMove = move
            print("Cur best move: " + COLUMNS[bestMove[1]] + " " + str(bestMove[0]+1))
        removeMoveFromBoard(move[0], move[1], True)
    return

def minimax():
    global white
    global black
    global bestMove
    global cutOff
    validMoves = getValidMoves()
    maxScore = float("-inf")
    depthLimit = 1
    curScore = 0

    if(DEBUG):
        print("Printing Valid Moves Obtained: ")
        print(validMoves)
    for move in validMoves:
        stopTime = time.time() + (TIME_LIMIT-4)/len(validMoves)
        if (DEBUG):
            print("should go to next node at ", str(stopTime))
            print("given this many seconds ", str(stopTime-time.time()))
        addMoveToBoard(move[0], move[1], True)
        while (1):
            curTime = time.time()
            if (curTime >= stopTime):
                if (DEBUG): print("BREAK! ", curTime, stopTime)
                break
            if (DEBUG): print("depthLimit: ", str(depthLimit))
            if (DEBUG): print("time limit: ", str(stopTime-curTime))
            maxVal = getMaxValue(float("-inf"), float("inf"), depthLimit, curTime, stopTime-curTime)
            depthLimit += 1
            if (DEBUG): print("currentMax: ", str(maxVal))

            if (curScore >= WIN_SCORE_CUTOFF):
                maxScore = curScore
                bestMove = move
                removeMoveFromBoard(move[0], move[1], True)
                return

            if (not cutOff and maxVal>curScore):
                curScore = maxVal
                bestMove = move
                if (DEBUG): print("not cutoff")


        cutOff = False
        depthLimit = 1
        if(curScore >= WIN_SCORE_CUTOFF):
            maxScore = curScore
            bestMove = move
            removeMoveFromBoard(move[0], move[1], True)
            return

        if(maxScore < curScore):
            if(DEBUG): print("current move ", str(move))
            maxScore=curScore
            bestMove = move
            if DEBUG: print("Best Move so far: " + str(bestMove))

        removeMoveFromBoard(move[0], move[1], True)


def getValidMoves():
    global white
    #global black
    #whitePotentialMoves = white.getPotentialMoves()
    #blackPotentialMoves = black.getPotentialMoves()
    #return (whitePotentialMoves | blackPotentialMoves)
    return white.getPotentialMoves()
    

def getMaxValue(alpha, beta, depth, curTime, timeLimit):
    global cutOff
    if (DEBUG): print("Max")
    eval = white.getScore()-black.getScore()
    if (time.time()-curTime >= timeLimit):
        cutOff = True
    if (eval >= WIN_SCORE_CUTOFF or cutOff or depth == 1):
        # if DEBUG: print("Val: " + str(white.getScore() - black.getScore()))
        return eval
    else:
        value = float("-inf")
        for move in getValidMoves():
            addMoveToBoard(move[0], move[1], True)
            child = getMinValue(alpha, beta, depth - 1, curTime, timeLimit)
            value = max(value, child)
            removeMoveFromBoard(move[0], move[1], True)
            if (value >= beta):
                if DEBUG: print("Prune: "+str(value))
                return value
            alpha = max(alpha, value)
    return value

def getMinValue(alpha, beta, depth, curTime, timeLimit):
    if (DEBUG): print("Min")
    global cutOff
    eval = white.getScore() - black.getScore()
    if (time.time() - curTime >= timeLimit):
        cutOff = True
    if (eval >= WIN_SCORE_CUTOFF or cutOff or depth == 1):
        # if DEBUG: print("Val: " + str(white.getScore() - black.getScore()))
        return eval
    else:
        value = float("inf")
        
        for move in getValidMoves():
            addMoveToBoard(move[0], move[1], False)
            child = getMaxValue(alpha, beta, depth - 1, curTime, timeLimit)
            value = min(value, child)
            removeMoveFromBoard(move[0], move[1], False)
            if (value <= alpha):
                if DEBUG: print("Prune: "+str(value))
                return value
            beta = min(beta, value)
    return value

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
        raise Exception("Go to MacDonalds pls")
def algebraToMove(move):
    row = int(move.split()[1]) - 1
    col = COLUMNS.index(move.split()[0].upper())

returns = init()

