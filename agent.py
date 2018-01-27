import os
import scipy.io

teamName = "knuckles"

def init():
    if teamName+".go" in os.listdir(".") and "end_game" not in os.listdir("."):
        move_file = open("move_file")
        move = move_file.read()                                   # move is the opponent's move
        move_file.close()
        if not move: move = 0                                     # if the move_file is empty, you are playing with white (move = 0)
        f = open("move_file", 'w')
        f.write(minimax(move))
        f.close()

    return

def minimax(move):

    return teamName+" "+"E"+" "+"4"

init()






