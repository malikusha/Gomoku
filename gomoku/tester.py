#!env python

import logging
import time
import os
import random

logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)
logging.info("loading %s" % (__file__))


board_height = 15
board_width = 15
length_to_win = 5

turn_length_in_seconds = 10

move_file_name = "move_file"



team_names = ["team1", "team2"]

class Move(object):
    def __init__(self, team_name, x_loc, y_loc):
        self.team_name = team_name
        self.x = x_loc
        self.y = y_loc

    def __str__(self):
        col_str = chr(self.x + ord('a'))
        return "%s %s %s" % (self.team_name, col_str, self.y)


def getLosingTraces():

    # Fails due to using the same move
    yield [
        Move("team1", 0, 0),
        Move("team2", 0, 0),
        Move("team1", 0, 0)
    ]

## Fails due to moving out of order (first turn)
#yield [
#Move("team1", 0, 0),
#Move("team1", 1, 0)
#]

    # Fails due to moving out of order (after first turn)
    yield [
        Move("team1", 0, 0),
        Move("team2", 1, 0),
        Move("team2", 2, 0)
    ]

    # fails due to playing below the board in the x direction
    yield [
        Move("team1", -1, 0)
    ]

    # fails due to playing below the board in the y direction
    yield [
        Move("team1", 0, -1)
    ]

    # Fails due to being above the board in the x direction
    yield [
        Move("team1", (board_width + 1), 0)
    ]

    # Fails due to being above the board in the y direction
    yield [
        Move("team1", 0, (board_height + 1))
    ]

def getWinningTraces():

    # Straight in x direction, top row
    trace = []
    for i in range(length_to_win):
        trace.append(Move("team1", i, 0))
        trace.append(Move("team2", i, 1))
    del trace[-1]
    yield trace

    # Straight in x direction, last row
    trace = []
    for i in range(length_to_win):
        trace.append(Move("team1", i, (board_height-1)))
        trace.append(Move("team2", i, (board_height-2)))
    del trace[-1]
    yield trace

    # Straight in y direction, left col
    trace = []
    for i in range(length_to_win):
        trace.append(Move("team1", 0, i))
        trace.append(Move("team2", 1, i))
    del trace[-1]
    yield trace

    # Straight in y direction, right col
    trace = []
    for i in range(length_to_win):
        trace.append(Move("team1", (board_width-1), i))
        trace.append(Move("team2", (board_width-2), i))
    del trace[-1]
    yield trace

    # diagonal from origin
    trace = []
    for i in range(length_to_win):
        trace.append(Move("team1", i, i))
        trace.append(Move("team2", 0, i+1))
    del trace[-1]
    yield trace

    # diagonal back from end of first row
    trace = []
    for i in range(length_to_win):
        trace.append(Move("team1", (board_width-1-i), i))
        trace.append(Move("team2", 0, i))
    del trace[-1]
    yield trace

    # diagonal from end
    trace = []
    for i in range(length_to_win):
        trace.append(Move("team1", (board_width-1-i), (board_height-1-i)))
        trace.append(Move("team2", 0, i+1))
    del trace[-1]
    yield trace

    # diagonal back from end of first col
    trace = []
    for i in range(length_to_win):
        trace.append(Move("team1", i, (board_height-1-i)))
        trace.append(Move("team2", 0, i))
    del trace[-1]
    yield trace

def getTieingTraces():
    trace = []
    for y in range(board_height):
        offset = random.randint(0,1) # not actually a guarantee but hopefully good enough...
        for x in range(board_width)[::2]:
            trace.append(Move("team1", (x + offset % board_width), y))
            trace.append(Move("team2", (x + offset + 1 % board_width), y))
    yield trace

def waitForTurn(team_name):
    team_file = team_name + ".go"
    while (not os.path.isfile(team_file)):
        time.sleep(0.5)
    return True


def writeMoveFile(move, move_file="move_file"):
    with open(move_file, 'w') as move_fid:
        move_text = str(move)
        logging.debug("Writing move text \"%s\" to %s" % (move_text, move_file))
        move_fid.write(move_text)
        move_fid.write("\n")
        move_fid.flush()
    return True

def swapTeamname(move):
    move.team_name = team_names[(team_names.index(move.team_name) + 1)%len(team_names)]

def playGame(trace):
    if os.path.isfile("team2.go"):
        swap_teamname = True
    else:
        swap_teamname = False
    for move in trace:
        if swap_teamname:
            swapTeamname(move)
        logging.debug("%s ready for turn...." % move.team_name)
        waitForTurn(move.team_name)
        time.sleep(0.5)
        writeMoveFile(move)
        time.sleep(0.5)


def getTeamFileName(team_name):
    return team_name + ".go"


def cleanGame():
    files_to_delete = ["move_file", "end_game"] + [getTeamFileName(s) for s in team_names]
    for file_name in files_to_delete:
        if os.path.isfile(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    pass
    _ = raw_input("Press Enter to start testing...")
    logging.info("Checking losing traces")
    for i, trace in enumerate(getLosingTraces()):
        logging.info("Running trace %s" % (i,))
        playGame(trace)
        _ = raw_input("Press Enter to clean directory...")
        cleanGame()
        _ = raw_input("Press Enter to run next trace....")
        print ""
    logging.info("Checking winning traces")
    for i, trace in enumerate(getWinningTraces()):
        logging.info("Running trace %s" % (i,))
        playGame(trace)
        _ = raw_input("Press Enter to clean directory...")
        cleanGame()
        _ = raw_input("Press Enter to run next trace....")
        print ""
    logging.info("Checking tying traces")
    for i, trace in enumerate(getTieingTraces()):
        logging.info("Running trace %s" % (i,))
        playGame(trace)
        _ = raw_input("Press Enter to clean directory...")
        cleanGame()
        _ = raw_input("Press Enter to run next trace....")
        print ""

