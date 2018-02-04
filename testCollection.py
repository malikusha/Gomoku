import gomokuCollection as board

def testExpect(check, expect):
    print("Actual Value: " + str(check) + " Expected Value: " + str(expect))
    if(check==expect):
        return True
    else:
        raise Exception('testExpect Failed!')


lenso = board.GomokuCollection()
lenso.addMove((1,1))
lenso.addMove((2,2))
testExpect(lenso.getScore(),4)
##
leno = board.GomokuCollection()
leno.addMove((1,1))
leno.addMove((3,3))
leno.addMove((1,3))
leno.addMove((3,1))
leno.addMove((2,2))
testExpect(leno.getScore(),20)

white= board.GomokuCollection()

##

##Testing InARow

##

##Testing add move to Gomoku Collection
white.addMove((3,4))
white.addMove((3,3))
white.addMove((3,5))
testExpect(white.getScore(), 10)

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
testExpect(white.getScore(), 20)

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
testExpect(white.getScore(), 30)
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
testExpect(white.getScore(), 32)


white.addMove((1,3))
testExpect(white.getScore(), 42)

white.addMove((14,14))
white.addMove((13,14))
testExpect(white.getScore(), 44)

white.addMove((10,10))
white.addMove((9,9))
testExpect(white.getScore(), 48)

white.addMove((8,8))
testExpect(white.getScore(), 54)

white.addEnemyMove((11,11))
testExpect(white.getScore(), 49)
white.addEnemyMove((7,7))
testExpect(white.getScore(), 44)

white.addMove((0,3))
testExpect(white.getScore(), 10000000)

black = board.GomokuCollection()
black.addMove((5,5))
black.addMove((7,5))
black.addMove((6,5))
testExpect(black.getScore(), 10)

black.addMove((6,7))
black.addMove((6,6))
testExpect(black.getScore(), 28)

black.addMove((3,5))
black.addEnemyMove((8,5))
testExpect(black.getScore(), 23)
black.addMove((4,5))
testExpect(black.getScore(), 10000000)


blue = board.GomokuCollection()
blue.addMove((3,3))
blue.addMove((5,1))
blue.addMove((1,5))
testExpect(blue.getScore(), 0)
blue.addMove((4,2))
testExpect(blue.getScore(),10)
blue.addEnemyMove((6,0))
testExpect(blue.getScore(),5)
blue.undoMove()
testExpect(blue.getScore(),10)

#blue.addEnemyMove((0,6)) figure this shit out later
#testExpect(blue.getScore(),5)

blue.addMove((2,4))
testExpect(blue.getScore(),10000000)


green = board.GomokuCollection()
green.addMove((4,4))
green.addMove((5,4))
green.addMove((6,4))
testExpect(green.getScore(),10)
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
