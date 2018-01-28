import osimport numpy as np
import time



teamName = "knuckles"
board = np.zeros((15, 15))
validMoves = []
for x in range(0,15):
    for y in range(0,15):
        validMoves.append([x, y])
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
print(board)

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






