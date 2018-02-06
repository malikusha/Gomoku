import gomokuCollection as board
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
def algebraToMove(move):
    row = int(move.split()[1]) - 1
    col = COLUMNS.index(move.split()[0].upper())
    return (row, col)
def moveToAlgebra(coord):
    return (COLUMNS[coord[1]], coord[0]+1)

def testExpect(check, expect):
    print("Actual Value: " + str(check) + " Expected Value: " + str(expect))
    if(check==expect):
        return True
    else:
        raise Exception('testExpect Failed!')

score2 = 2
score3 = 9
score4 = 15
open4 = 1000
lenso = board.GomokuCollection()
lenso.addMove((1,1))
lenso.addMove((2,2))
testExpect(lenso.getScore(),2*score2)

leno = board.GomokuCollection()
leno.addMove((1,1))
leno.addMove((3,3))
leno.addMove((1,3))
leno.addMove((3,1))
leno.addMove((2,2))
testExpect(leno.getScore(),score3*4)

white= board.GomokuCollection()

##

##Testing InARow

##

##Testing add move to Gomoku Collection
white.addMove((3,4))
white.addMove((3,3))
white.addMove((3,5))
testExpect(white.getScore(), score3*2)

white.addMove((2,3))
white.addMove((0,0))
white.addMove((0,1))

"""
CURRENT BOARD

 0123456
0XX#####
1#######
2###X###
3###XXX#
4#######
5#######
6#######
Score = 2 + 4 + 4 + 10
"""
testExpect(white.getScore(), 5*score2+2*score3)

white.addMove((4,3))
"""
CURRENT BOARD

 0123456
0XX#####
1#######
2###X###
3###XXX#
4###X###
5#######
6#######
Score = 2 + 10 + 4 + 4 + 10
"""
testExpect(white.getScore(), 5*score2+4*score3)
white.addMove((1,0))
"""
CURRENT BOARD

 0123456
0XX#####
1X######
2###X###
3###XXX#
4###X###
5#######
6#######
Score = 2 + 2 + 10 + 4 + 4 + 10
"""
testExpect(white.getScore(), 6*score2+4*score3)


white.addMove((1,3))
testExpect(white.getScore(), open4 + 60)

white.addMove((14,14))
white.addMove((13,14))
testExpect(white.getScore(), 1062)

white.addMove((10,10))
white.addMove((9,9))
testExpect(white.getScore(), 1066)

white.addMove((8,8))
testExpect(white.getScore(), 1080)

white.addEnemyMove((11,11))
testExpect(white.getScore(), 1071)
white.addEnemyMove((7,7))
testExpect(white.getScore(), 1062)

white.addMove((0,3))
testExpect(white.getScore(), 10000000)

black = board.GomokuCollection()
black.addMove((5,5))
black.addMove((7,5))
black.addMove((6,5))
testExpect(black.getScore(), 2*score3)

black.addMove((6,7))
black.addMove((6,6))
testExpect(black.getScore(), 44)

black.addMove((3,5))
black.addEnemyMove((8,5))
testExpect(black.getScore(), 35)
black.addMove((4,5))
testExpect(black.getScore(), 10000000)

blue = board.GomokuCollection()
blue.addMove((3,3))
blue.addMove((5,1))
blue.addMove((1,5))
testExpect(blue.getScore(), 0)
blue.addMove((4,2))
testExpect(blue.getScore(),2*score3)
blue.addEnemyMove((6,0))
testExpect(blue.getScore(),score3)
blue.undoMove()
testExpect(blue.getScore(),2*score3)
"""
#blue.addEnemyMove((0,6)) figure this shit out later
#testExpect(blue.getScore(),5)

blue.addMove((2,4))
testExpect(blue.getScore(),10000000)

green = board.GomokuCollection()
green.addMove((4,4))
green.addMove((5,4))
green.addMove((6,4))
testExpect(green.getScore(),2*score3)
green.undoMove()
testExpect(green.getScore(),4)
green.addMove((6,4))
green.addMove((5,5))
testExpect(green.getScore(),22)
green.undoMove()
testExpect(green.getScore(),10)
green.addMove((5,5))
green.addEnemyMove((7,4))
testExpect(green.getScore(),17)
green.undoMove()
testExpect(green.getScore(),22)

pink = board.GomokuCollection()
pink.addMove((1,1))
pink.addMove((3,3))
pink.addMove((2,2))
testExpect(pink.getScore(),10)
pink.undoMove()

cyan = board.GomokuCollection()
cyan.addEnemyMove((3,4))
cyan.undoMove()
cyan.addMove((3,4))
cyan.addMove((4,3))
testExpect(cyan.getScore(),4)
"""

""""

0ABCDEFGHIJKLMN
1 # # # # # # #
2# # # # # # #
3 # # # # # # #
4# # # # # # #
5 # # O # # # #
6# # # O #X# #
7 # # # OX# # #
8# # # #X# # #
9 # # # # # # #
0# # # # # # #
"""
cyan = board.GomokuCollection()
pink = board.GomokuCollection()
cyan.addMove(algebraToMove("H 8"))
cyan.addEnemyMove(algebraToMove("H 7"))
cyan.addMove(algebraToMove("I 7"))
cyan.addEnemyMove(algebraToMove("G 6"))
cyan.addMove(algebraToMove("G 9"))
cyan.addEnemyMove(algebraToMove("F 5"))

pink.addEnemyMove(algebraToMove("H 8"))
pink.addMove(algebraToMove("H 7"))
pink.addEnemyMove(algebraToMove("I 7"))
pink.addMove(algebraToMove("G 6"))
pink.addEnemyMove(algebraToMove("G 9"))
pink.addMove(algebraToMove("F 5"))

print(cyan.getScore() - pink.getScore())
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in cyan.board]))

cyan.addMove(algebraToMove("G 8"))
pink.addEnemyMove(algebraToMove("G 8"))
x = (pink.getPotentialMoves() | cyan.getPotentialMoves())
print(x)
print(len(x))


asdf = board.GomokuCollection()
asdf.addMove(algebraToMove("H 8"))
asdf.addEnemyMove(algebraToMove("H 7"))
asdf.addMove(algebraToMove("G 9"))
asdf.addEnemyMove(algebraToMove("I 7"))
asdf.addMove(algebraToMove("J 7"))
asdf.addEnemyMove(algebraToMove("I 6"))
#asdf.addMove(algebraToMove("E 8"))
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in asdf.board]))
print(asdf.getPotentialMoves())


print(cyan.getScore() - pink.getScore())
def lookAtTheHistoryFile():
    f = open("history_file", 'r')
    x = []
    for e in f.read().split('\n')[:-1]:
    
        y = e.split(' ')
        print(y)
        row = int(y[2]) - 1
        col = COLUMNS.index(y[1].upper())
        if(y[0] == 'Large_Horse'):
            x +=[('a', (row,col))]
        else:
            x +=[('ae', (row,col))]
    print("national history day :")
    print(x)
    for e in x:
        print("Cur Val: " + str(e))
        if(e[0] == 'a'):
            agent.addMoveToBoard(e[1][0], e[1][0], True)
        else:
            agent.addMoveToBoard(e[1][0], e[1][0], False)
    agent.getHistory('w')
    return(x)
def printSomeActionTables(actionTable):
    gmk = board.GomokuCollection()
    for e in actionTable:
        print(e)
        if(e[0] == 'r'):
            gmk.undoMove()
        elif(e[0] == 'a'):
            gmk.addMove(e[1])
        elif(e[0] == 'ae'):
            gmk.addEnemyMove(e[1])
        elif(e[0] == 're'):
            gmk.addEnemyMove(e[1])
        else:
            raise Exception("wow go work at mcdonalds you cant code for shit")
    print("Movelist: ")
    x = []
    for e in gmk.orderedMoves:
        x+= [convertToAlgebraicCoord(e)]
    return gmko


#x = lookAtTheHistoryFile()
#printSomeActionTables(x)
