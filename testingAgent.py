import agentNew as agent


def testExpect(check, expect):
    print("Actual Value: " + str(check) + " Expected Value: " + str(expect))
    if(check==expect):
        return True
    else:
        raise Exception('testExpect Failed!')

TEAM_NAME = "Large_Horse"
"""
agent.addMoveToBoard(1, 2, True)
agent.addMoveToBoard(1, 3, False)
aSet = set([(0, 1), (0, 4), (2, 1), (0, 2), (2, 3),
                (1, 4), (2, 2), (2, 4),(0, 3), (1, 1)])
testExpect(agent.getValidMoves(), aSet)

actionTable =   [('a', (10, 11)), ('r', (10, 11)), ('a', (11, 11)), ('r', (11, 11)),
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
isItmyMove = False
for e in actionTable:
    print(e)
    if(e[0] == 'r'):
        agent.removeMoveFromBoard(e[1][0],e[1][1], isItmyMove)
        isItmyMove = not isItmyMove
    elif(e[0] == 'a'):
        agent.addMoveToBoard(e[1][0],e[1][1], isItmyMove)
        isItmyMove = not isItmyMove
    else:
        raise Exception("wow go work at mcdonalds you cant code for shit")
    print(agent.getValidMoves())
"""

def lookAtTheHistoryFile():
    f = open("history_file", 'r')
    x = []
    for e in f.read().split('\n')[:-1]:
    
        y = e.split(' ')
        print(y)
        row = int(y[2]) - 1
        col = agent.COLUMNS.index(y[1].upper())
        if(y[0] == TEAM_NAME):
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
x = lookAtTheHistoryFile()
"""
 01234567
0########
1##XO####
2########
3########
4########
"""
