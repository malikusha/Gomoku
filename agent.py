import os
import time
#import scipy.io

teamName = "knuckles"

def init():
    move = open("move_file").read()                         # move is the opponent's move
    if (move):                                              # if the move_file is empty, you are playing with white (move = 0)
        open("move_file", 'w').write(minimax(move))
    else:
        open("move_file", 'w').write(minimax(0))
    return

def minimax(move):
    return teamName+" "+"E"+" "+"4"
print("Agent py called")

while(1==1):
  while((teamName+".go" not in os.listdir(".")) and ("end_game" not in os.listdir("."))):
    pass
  init()
  time.sleep(4)





