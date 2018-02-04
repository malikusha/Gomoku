import theNewBoardLib as board
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def convertToAlgebraicCoord(coord):
    return (COLUMNS[coord[1]], coord[0]+1)

def testExpect(check, expect):
    print("Actual Value: " + str(check) + " Expected Value: " + str(expect))
    if(check==expect):
        return True
    else:
        raise Exception('testExpect Failed!')

def testSameInARows(iars, expected):
    print(expected)
    for iar in iars:
        curSet = iar.moveList
        print(curSet)
        if(curSet not in expected):
            raise Exception('testSameInARows Failed!')
    return True

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

        gmk.debugPrintDictionary()
    print("Movelist: ")
    x = []
    for e in gmk.orderedMoves:
        x+= [convertToAlgebraicCoord(e)]
    print(x)
    x=[]
    print("keys: ")
    for e in gmk.dictionary.keys():
        x += [convertToAlgebraicCoord(e)]
    print(x)
    print("Dictionary")
   
    
##Testing Init of GOmoku Collection
print("TESTING INIT \n")
white= board.GomokuCollection()
testExpect(white.dictionary, {})
testExpect(white.score2, 2)
testExpect(white.score3, 5)
testExpect(white.score4, 10)

##

##Testing InARow
iar = board.InARow((3,4), (2,4), (4,4))
testExpect(iar.lengthOfRow, 1)
testExpect(iar.moveList, set([(3,4)]))

##

##Testing add move to Gomoku Collection
white.addMove((3,4))
white.addMove((3,3))
"""
Two IAR at following key:
(4,4),(2,4), (2,3), (4,3)
"""
x = set([(4,4),(2,4), (2,3), (4,3)])
print("Testing 2 IAR")
testExpect(white.getAllNKeys(2), x)

"""
IAR of length 2 at following key:
(3,2), (3,5)
Keys that should not exist:
(3,3),(3,4)
"""
white.addMove((3,5))
testExpect(white.getScore(), 10)

white.addMove((2,3))
""" Added from the top
 123456
1######
2##X###
3##XXX#
4######
TWO IAR:
(4,3), (4,5), (2,5)
Three IAR
(4,4)
Four IAR
(2,4)
Two in a row IAR:
(1,2),(4,5), (4,3), (1,3)
THree in a row IAR:
(3,2), (3,5)
"""

white.addMove((0,0))
#white.debugPrintDictionary(False)
white.addMove((0,1))
a = set([(0,1),(0,0)])
b = set([(2,3),(3,4)])
c = set([(2,3),(3,3)])
testSameInARows(white.getAllInARow(2), [a, b, c])
##print("\n all 2 in a rows: ")
##for e in white.getAllInARow(2):
##    e.debugPrint()
##print("\n all 3 in a rows: ")
##for e in white.getAllInARow(3):
##    e.debugPrint()
##white.getAllDictKeys()

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
testExpect(white.getScore(), 1000000)

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
testExpect(black.getScore(), 1000000)


blue = board.GomokuCollection()
blue.addMove((3,3))
blue.addMove((5,1))
blue.addMove((1,5))
testExpect(blue.getScore(), 0)
blue.addMove((4,2))
testExpect(blue.getScore(),10)
blue.addEnemyMove((6,0))
testExpect(blue.getScore(),5)
blue.undoEnemyMove()
testExpect(blue.getScore(),10)

#blue.addEnemyMove((0,6)) figure this shit out later
#testExpect(blue.getScore(),5)

blue.addMove((2,4))
testExpect(blue.getScore(),1000000)


green = board.GomokuCollection()
green.addMove((4,4))
green.addMove((5,4))
green.addMove((6,4))
testExpect(green.getScore(),10)
green.removeMove()
testExpect(green.getScore(),4)
green.addMove((6,4))
green.addMove((5,5))
testExpect(green.getScore(),22)
green.removeMove()
testExpect(green.getScore(),10)
green.addMove((5,5))
green.addEnemyMove((7,4))
testExpect(green.getScore(),17)
green.undoEnemyMove()
testExpect(green.getScore(),22)

pink = board.GomokuCollection()
pink.addMove((1,1))
pink.addMove((3,3))
pink.addMove((2,2))
testExpect(pink.getScore(),10)
pink.removeMove()
pink.debugPrintDictionary()

cyan = board.GomokuCollection()
cyan.addEnemyMove((3,4))
cyan.undoMove()
cyan.addMove((3,4))
cyan.addMove((4,3))
cyan.debugPrintDictionary()
testExpect(cyan.getScore(),4)

truq = board.GomokuCollection()
truq.addEnemyMove((1,2))
truq.addMove((1,3))
aSet = set([(0,2),(0,3),(0,4),(2,2),(2,3),(2,4),(1,4)])
testExpect(truq.getPotentialMoves(), aSet)
#print(black.deleteDictionary)
#
"""
actionTable = [('a', (2, 6)), ('r', (2, 6)), ('a', (1, 4)), ('r', (1, 4)),
               ('a', (0, 6)), ('r', (0, 6)), ('a', (1, 6)), ('r', (1, 6)),
               ('a', (0, 4)), ('r', (0, 4)), ('a', (0, 5)), ('r', (0, 5)),
               ('a', (2, 5)), ('r', (2, 5)), ('a', (2, 4)), ('r', (2, 4)),
               ('a', (2, 6))]

printSomeActionTables(actionTable)
actionTable2 = [('a', (10, 11)), ('r', (10, 11)), ('a', (11, 11)), ('r', (11, 11)),
                ('a', (12, 13)), ('r', (12, 13)), ('a', (10, 13)), ('r', (10, 13)),
                ('a', (12, 12)), ('r', (12, 12)), ('a', (10, 12)), ('r', (10, 12)),
                ('a', (12, 11)), ('r', (12, 11)), ('a', (11, 13)), ('r', (11, 13)),
                ('a', (10, 11)), ('a', (11, 11)), ('r', (11, 11)), ('a', (0, 14)),
                ('r', (0, 14)) , ('a', (10, 13)), ('r', (10, 13)), ('a', (12, 12)),
                ('r', (12, 12)), ('a', (9, 10)) , ('r', (9, 10)) , ('a', (12, 11)),
                ('r', (12, 11)), ('a', (2, 14)) , ('r', (2, 14)) , ('a', (11, 10)),
                ('r', (11, 10)), ('a', (10, 10)), ('r', (10, 10)), ('a', (12, 13)),
                ('r', (12, 13)), ('a', (0, 13)) , ('r', (0, 13)) , ('a', (10, 12)),
                ('r', (10, 12)), ('a', (2, 13)) , ('r', (2, 13)) , ('a', (9, 11)),
                ('r', (9, 11)) , ('a', (1, 13)) , ('r', (1, 13)) , ('a', (9, 12)),
                ('r', (9, 12)) , ('a', (11, 13)), ('r', (11, 13)), ('a', (11, 11))]

('a', (10, 11)), ('r', (10, 11)), ('a', (0, 14)) , ('r', (0, 14)),
                ('a', (12, 12)), ('r', (12, 12)), ('a', (3, 11)) , ('r', (3, 11)),
                ('a', (1, 11)) , ('r', (1, 11)) , ('a', (11, 10)), ('r', (11, 10)),
                ('a', (2, 9))  , ('r', (2, 9))  , ('a', (12, 13)), ('r', (12, 13)),
                ('a', (3, 10)) , ('r', (3, 10)) , ('a', (10, 12)), ('r', (10, 12)),
                ('a', (0, 13)) , ('r', (0, 13)) , ('a', (2, 13)) , ('r', (2, 13)),
                ('a', (9, 11)) , ('r', (9, 11)) , ('a', (1, 10)) , ('r', (1, 10)),
                ('a', (12, 10)), ('r', (12, 10)), ('a', (1, 13)) , ('r', (1, 13)),
                ('a', (10, 13)), ('r', (10, 13)), ('a', (9, 10)) , ('r', (9, 10)),
                ('a', (3, 9))  , ('r', (3, 9))  , ('a', (1, 9))  , ('r', (1, 9)),
                ('a', (12, 11)), ('r', (12, 11)), ('a', (2, 14)) , ('r', (2, 14)),
                ('a', (10, 10)), ('r', (10, 10)), ('a', (2, 11)) , ('r', (2, 11)),
                ('a', (9, 12)) , ('r', (9, 12))]

printSomeActionTables(actionTable2)



actionTable = [('a', (7, 7)), ('ae', (6, 8)), ('a', (5, 9)), ('r', (5, 9)),
               ('a', (6, 9)), ('r', (6, 9)), ('a', (6, 7)), ('r', (6, 7)),
               ('a', (6, 6)), ('r', (6, 6)), ('a', (7, 6)), ('r', (7, 6)),
               ('a', (5, 7)), ('r', (5, 7)), ('a', (8, 8)), ('r', (8, 8)),
               ('a', (8, 7)), ('r', (8, 7)), ('a', (8, 6)), ('r', (8, 6)),
               ('a', (7, 8)), ('r', (7, 8)), ('a', (5, 8)), ('r', (5, 8)),
               ('a', (7, 9)), ('r', (7, 9)), ('a', (5, 9)), ('ae', (11, 8)),
               ('a', (6, 9)), ('r', (6, 9)), ('a', (6, 6)), ('r', (6, 6)),
               ('a', (7, 7)), ('r', (7, 7)), ('a', (12, 9)), ('r', (12, 9)),
               ('a', (5, 8)), ('r', (5, 8)), ('a', (10, 8)), ('r', (10, 8)),
               ('a', (6, 7)), ('r', (6, 7)), ('a', (10, 7)), ('r', (10, 7)),
               ('a', (7, 6)), ('r', (7, 6)), ('a', (6, 10)), ('r', (6, 10)),
               ('a', (4, 8)), ('r', (4, 8)), ('a', (8, 6)), ('r', (8, 6)),
               ('a', (10, 9)), ('r', (10, 9)), ('a', (4, 10)), ('r', (4, 10)),
               ('a', (12, 7)), ('r', (12, 7)), ('a', (11, 9)), ('r', (11, 9)),
               ('a', (8, 7)), ('r', (8, 7)), ('a', (4, 9)), ('r', (4, 9)),
               ('a', (11, 7)), ('r', (11, 7)), ('a', (5, 10)), ('r', (5, 10)),
               ('a', (5, 7)), ('r', (5, 7)), ('a', (8, 8)), ('r', (8, 8)),
               ('a', (7, 8)), ('r', (7, 8)), ('a', (12, 8)), ('r', (12, 8)),
               ('a', (6, 9)), ('ae', (2, 12)), ('a', (5, 9)), ('r', (5, 9)),
               ('a', (4, 8)), ('r', (4, 8)), ('a', (7, 7)), ('r', (7, 7)),
               ('a', (1, 11)), ('r', (1, 11)), ('a', (12, 9)), ('r', (12, 9)),
               ('a', (5, 8)), ('r', (5, 8)), ('a', (10, 8)), ('r', (10, 8)),
               ('a', (4, 9)), ('r', (4, 9)), ('a', (10, 7)), ('r', (10, 7)),
               ('a', (7, 6)), ('r', (7, 6)), ('a', (6, 10)), ('r', (6, 10)),
               ('a', (3, 12)), ('r', (3, 12)), ('a', (2, 13)), ('r', (2, 13)),
               ('a', (7, 10)), ('r', (7, 10)), ('a', (8, 6)), ('r', (8, 6)),
               ('a', (10, 9)), ('r', (10, 9)), ('a', (4, 10)), ('r', (4, 10)),
               ('a', (6, 6)), ('r', (6, 6)), ('a', (3, 13)), ('r', (3, 13)),
               ('a', (1, 13)), ('r', (1, 13)), ('a', (12, 7)), ('r', (12, 7)),
               ('a', (11, 9)), ('r', (11, 9)), ('a', (3, 11)), ('r', (3, 11)),
               ('a', (8, 7)), ('r', (8, 7)), ('a', (6, 7)), ('r', (6, 7)),
               ('a', (7, 9)), ('r', (7, 9)), ('a', (11, 7)), ('r', (11, 7)),
               ('a', (5, 10)), ('r', (5, 10)), ('a', (1, 12)), ('r', (1, 12)),
               ('a', (5, 7)), ('r', (5, 7)), ('a', (2, 11)), ('r', (2, 11)),
               ('a', (8, 8)), ('r', (8, 8)), ('a', (7, 8)), ('r', (7, 8)),
               ('a', (5, 9))]
"""
actionTable = [('a', (7, 7)), ('ae', (14, 10)), ('a', (6, 7)), ('ae', (0, 1)),
             ('a', (6, 6)), ('ae', (4, 3))  , ('a', (5, 6)), ('ae', (4, 8)),
             ('a', (4, 7)), ('ae', (8, 10)) , ('a', (5, 9)), ('ae', (2, 9)),
             ('a', (6, 9)), ('ae', (14, 7)) , ('a', (5, 8)), ('ae', (1, 14))]
printSomeActionTables(actionTable)

actionTable2 = [('ae', (9, 6)), ('a', (10, 5)), ('r', (10, 5)), ('a', (10, 7)), ('r', (10, 7)), ('a', (10, 6)), ('r', (10, 6)), ('a', (8, 7)), ('r', (8, 7)), ('a', (9, 5)), ('r', (9, 5)), ('a', (8, 6)), ('r', (8, 6)), ('a', (8, 5)), ('r', (8, 5)), ('a', (9, 7)), ('r', (9, 7)), ('a', (10, 5)), ('ae', (4, 14)), ('a', (11, 4)), ('r', (11, 4)), ('a', (10, 4)), ('r', (10, 4)), ('a', (3, 13)), ('r', (3, 13)), ('a', (10, 6)), ('r', (10, 6)), ('a', (5, 13)), ('r', (5, 13)), ('a', (9, 4)), ('r', (9, 4)), ('a', (8, 6)), ('r', (8, 6)), ('a', (8, 5)), ('r', (8, 5)), ('a', (3, 14)), ('r', (3, 14)), ('a', (4, 13)), ('r', (4, 13)), ('a', (8, 7)), ('r', (8, 7)), ('a', (11, 5)), ('r', (11, 5)), ('a', (10, 7)), ('r', (10, 7)), ('a', (5, 14)), ('r', (5, 14)), ('a', (9, 5)), ('r', (9, 5)), ('a', (11, 6)), ('r', (11, 6)), ('a', (9, 7)), ('r', (9, 7)), ('a', (10, 4)), ('ae', (2, 5)), ('a', (10, 6)), ('r', (10, 6)), ('a', (5, 13)), ('r', (5, 13)), ('a', (1, 6)), ('r', (1, 6)), ('a', (9, 4)), ('r', (9, 4)), ('a', (10, 3)), ('r', (10, 3)), ('a', (3, 14)), ('r', (3, 14)), ('a', (11, 5)), ('r', (11, 5)), ('a', (10, 7)), ('r', (10, 7)), ('a', (8, 5)), ('r', (8, 5)), ('a', (4, 13)), ('r', (4, 13)), ('a', (1, 5)), ('r', (1, 5)), ('a', (3, 6)), ('r', (3, 6)), ('a', (8, 6)), ('r', (8, 6)), ('a', (9, 7)), ('r', (9, 7)), ('a', (2, 6)), ('r', (2, 6)), ('a', (11, 4)), ('r', (11, 4)), ('a', (3, 13)), ('r', (3, 13)), ('a', (9, 3)), ('r', (9, 3)), ('a', (1, 4)), ('r', (1, 4)), ('a', (8, 7)), ('r', (8, 7)), ('a', (3, 5)), ('r', (3, 5)), ('a', (10, 5)), ('r', (10, 5)), ('a', (11, 3)), ('r', (11, 3)), ('a', (5, 14)), ('r', (5, 14)), ('a', (9, 5)), ('r', (9, 5)), ('a', (3, 4)), ('r', (3, 4)), ('a', (2, 4)), ('r', (2, 4)), ('a', (11, 6)), ('r', (11, 6)), ('a', (9, 4)), ('ae', (2, 4)), ('a', (1, 3)), ('r', (1, 3)), ('a', (10, 6)), ('r', (10, 6)), ('a', (5, 13)), ('r', (5, 13)), ('a', (1, 6)), ('r', (1, 6)), ('a', (2, 5)), ('r', (2, 5)), ('a', (8, 5)), ('r', (8, 5)), ('a', (3, 14)), ('r', (3, 14)), ('a', (3, 3)), ('r', (3, 3)), ('a', (11, 5)), ('r', (11, 5)), ('a', (10, 7)), ('r', (10, 7)), ('a', (10, 3)), ('r', (10, 3)), ('a', (4, 13)), ('r', (4, 13)), ('a', (1, 5)), ('r', (1, 5)), ('a', (3, 6)), ('r', (3, 6)), ('a', (8, 6)), ('r', (8, 6)), ('a', (9, 7)), ('r', (9, 7)), ('a', (2, 6)), ('r', (2, 6)), ('a', (11, 4)), ('r', (11, 4)), ('a', (10, 4)), ('r', (10, 4)), ('a', (3, 13)), ('r', (3, 13)), ('a', (9, 3)), ('r', (9, 3)), ('a', (8, 3)), ('r', (8, 3)), ('a', (1, 4)), ('r', (1, 4)), ('a', (2, 3)), ('r', (2, 3)), ('a', (8, 7)), ('r', (8, 7)), ('a', (3, 5)), ('r', (3, 5)), ('a', (10, 5)), ('r', (10, 5)), ('a', (11, 3)), ('r', (11, 3)), ('a', (5, 14)), ('r', (5, 14)), ('a', (9, 5)), ('r', (9, 5)), ('a', (3, 4)), ('r', (3, 4)), ('a', (8, 4)), ('r', (8, 4)), ('a', (10, 3)), ('ae', (1, 0)), ('a', (1, 3)), ('r', (1, 3)), ('a', (11, 2)), ('r', (11, 2)), ('a', (10, 6)), ('r', (10, 6)), ('a', (5, 13)), ('r', (5, 13)), ('a', (2, 1)), ('r', (2, 1)), ('a', (2, 6)), ('r', (2, 6)), ('a', (1, 6)), ('r', (1, 6)), ('a', (9, 4)), ('r', (9, 4)), ('a', (2, 5)), ('r', (2, 5)), ('a', (8, 5)), ('r', (8, 5)), ('a', (3, 14)), ('r', (3, 14)), ('a', (3, 3)), ('r', (3, 3)), ('a', (11, 5)), ('r', (11, 5)), ('a', (10, 7)), ('r', (10, 7)), ('a', (4, 13)), ('r', (4, 13)), ('a', (1, 5)), ('r', (1, 5)), ('a', (3, 6)), ('r', (3, 6)), ('a', (8, 6)), ('r', (8, 6)), ('a', (1, 1)), ('r', (1, 1)), ('a', (9, 7)), ('r', (9, 7)), ('a', (0, 0)), ('r', (0, 0)), ('a', (11, 4)), ('r', (11, 4)), ('a', (10, 4)), ('r', (10, 4)), ('a', (3, 13)), ('r', (3, 13)), ('a', (9, 3)), ('r', (9, 3)), ('a', (8, 3)), ('r', (8, 3)), ('a', (1, 4)), ('r', (1, 4)), ('a', (2, 3)), ('r', (2, 3)), ('a', (8, 7)), ('r', (8, 7)), ('a', (3, 5)), ('r', (3, 5)), ('a', (0, 1)), ('r', (0, 1)), ('a', (10, 5)), ('r', (10, 5)), ('a', (9, 2)), ('r', (9, 2)), ('a', (11, 3)), ('r', (11, 3)), ('a', (5, 14)), ('r', (5, 14)), ('a', (2, 0)), ('r', (2, 0)), ('a', (9, 5)), ('r', (9, 5)), ('a', (8, 4)), ('r', (8, 4)), ('a', (2, 4)), ('r', (2, 4)), ('a', (11, 6)), ('r', (11, 6)), ('a', (10, 2)), ('r', (10, 2)), ('a', (11, 2)), ('ae', (0, 12)), ('a', (1, 3)), ('r', (1, 3)), ('a', (12, 1)), ('r', (12, 1)), ('a', (8, 7)), ('r', (8, 7)), ('a', (10, 6)), ('r', (10, 6)), ('a', (5, 13)), ('r', (5, 13)), ('a', (2, 1)), ('r', (2, 1)), ('a', (0, 0)), ('r', (0, 0)), ('a', (1, 6)), ('r', (1, 6)), ('a', (9, 4)), ('r', (9, 4)), ('a', (2, 5)), ('r', (2, 5)), ('a', (1, 11)), ('r', (1, 11)), ('a', (8, 5)), ('r', (8, 5)), ('a', (3, 14)), ('r', (3, 14)), ('a', (12, 2)), ('r', (12, 2)), ('a', (3, 3)), ('r', (3, 3)), ('a', (11, 5)), ('r', (11, 5)), ('a', (10, 7)), ('r', (10, 7)), ('a', (10, 3)), ('r', (10, 3)), ('a', (4, 13)), ('r', (4, 13)), ('a', (1, 5)), ('r', (1, 5)), ('a', (0, 11)), ('r', (0, 11)), ('a', (11, 1)), ('r', (11, 1)), ('a', (3, 6)), ('r', (3, 6)), ('a', (8, 6)), ('r', (8, 6)), ('a', (1, 1)), ('r', (1, 1)), ('a', (12, 3)), ('r', (12, 3)), ('a', (9, 7)), ('r', (9, 7)), ('a', (2, 6)), ('r', (2, 6)), ('a', (11, 4)), ('r', (11, 4)), ('a', (10, 4)), ('r', (10, 4)), ('a', (3, 13)), ('r', (3, 13)), ('a', (1, 13)), ('r', (1, 13)), ('a', (9, 3)), ('r', (9, 3)), ('a', (10, 5)), ('r', (10, 5)), ('a', (1, 4)), ('r', (1, 4)), ('a', (2, 3)), ('r', (2, 3)), ('a', (10, 1)), ('r', (10, 1)), ('a', (0, 1)), ('r', (0, 1)), ('a', (8, 3)), ('r', (8, 3)), ('a', (1, 12)), ('r', (1, 12)), ('a', (9, 2)), ('r', (9, 2)), ('a', (0, 13)), ('r', (0, 13)), ('a', (11, 3)), ('r', (11, 3)), ('a', (5, 14)), ('r', (5, 14)), ('a', (2, 0)), ('r', (2, 0)), ('a', (9, 5)), ('r', (9, 5)), ('a', (8, 4)), ('r', (8, 4)), ('a', (3, 4)), ('r', (3, 4)), ('a', (10, 2)), ('r', (10, 2)), ('a', (12, 1)), ('ae', (0, 3)), ('a', (1, 3)), ('r', (1, 3)), ('a', (12, 1))]
printSomeActionTables(actionTable2)

"""
CURRENT BOARD

 0123456
0XX#X###
1###X###
2###X###
3###XXX#
4###X###
5#######
6#######
Score = 2 + 10 + 4 + 4 + 10
"""

"""
No negative key

########
########
###XXX##
########
"""
