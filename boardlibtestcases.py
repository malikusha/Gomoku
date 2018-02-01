import boardlib as board


def test1():
    white = board.GomokuCollection()
    white.addNewMove((3,4))
    white.addNewMove((4,5))
    white.addNewMove((5,7))
    white.addNewMove((5,8))
    white.debugPrint()
    
    white.undoMove()
    white.debugPrint()
    #white.undoMove()
    #white.debugPrint()

test1()
