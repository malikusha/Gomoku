import os
import scipy.io

teamName = "knuckles"

def init():
    if teamName+".go" in os.listdir(".") and "end_game" not in os.listdir("."):
        move = open("move_file").read()                         # move is the opponent's move
        if (move):                                              # if the move_file is empty, you are playing with white (move = 0)
            open("move_file", 'w').write(minimax(move))
        else:
            open("move_file", 'w').write(minimax(0))
    return

def minimax(move):
    return teamName+" "+"E"+" "+"4"

init()






