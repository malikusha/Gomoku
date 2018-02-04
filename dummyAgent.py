import os
import random
import time
#import scipy.io

teamName = "notKnuckles"

"""
Dummy AI
This AI is designed to make random moves so we have something to test our AI with 
"""

columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O']

"""
gets move from the move_file text and parses it
"""
def parseMove(move):
    if(move):
        splitMove = move.split()
        j = columns.index(splitMove[1].upper())
        i = int(splitMove[2])
    return [i,j]
"""
makes a random move based on the valid moves
"""
def randomMove(validMoves):
    move = random.choice(validMoves)
    return teamName + " " + columns[move[1]] + " " + str(move[0])

def remMove(move, validMoves):
    validMoves.remove(move)

def init(validMoves):
    print("init has been called on thread3")
    move = open("move_file").read()                         # move is the opponent's move
    if (move):
        oppMove = parseMove(move)
        remMove(oppMove, validMoves)
        # if the move_file is empty, you are playing with white (move = 0)
    open("move_file", 'w').write(randomMove(validMoves))
    return


print("Dummy AI Initiated")
validMoves = []
for x in range(0,15):
    for y in range(0,15):
        validMoves.append([x+1, y])
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O']

while(1):
  while((teamName+".go" not in os.listdir("."))):
    time.sleep(1)
  print("Dummy Activated")
  init(validMoves)
  time.sleep(1)
