points = [3,4,5]

"""
If numRow = 1, a copy of the object needs to be created
TODO: open or closed?

"""

class InARow:
    moveToClass = {}
    """
        Assumes move is a size 2 list TODO: change to Tuple
    """
    """
    Existing Variables:
        validCont = coordinates that allow the rows to grow
        dx = x vector of valid coordinates
        dy = y vector of valid coordinates
        numRow = how many in a rows existing
        pos = list of all coordinates in the row
    """
    def initValidCont(self, move):
        x = move[0]
        y = move[1]
        #self.validCont = [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y+1)]
        
    def addMove(self, move):
        isOne = self.numRow == 1
        if(isOne):
            self.updateLength()
        self.setValidVector(move, isOne)
        self.pos += [move]
    """
    newMove = [3,3]
    Move = [2,2]
    dx = 1
    dy = 1
    """
    def setValidVector(self, move, isOne):
        if(isOne):
            self.dx = move[0] - self.pos[0][0]
            self.dy = move[1] - self.pos[0][1]
            self.head = (move[0]+self.dx, move[1]+self.dy)
            self.tail = (self.pos[0][0]-self.dx, self.pos[0][1]-self.dy)
        else:
            if(move==self.head):
                self.head = (self.head[0]+self.dx,self.head[1]+self.dy)
            elif(move==self.tail):
                self.tail = (self.tail[0]-self.dx,self.tail[1]-self.dy)
            else:
                print("BHON SCReWED UP KEKEKEKEKEKEKEKEKEKEKEKefjkjl")
        #self.validCont = [(newMove[0]+self.dx, newMove[0]+self.dy), (self.pos[0][0]-self.dx, self.pos[0][1]-self.dx)]
    def updateLength(self):
        self.numRow += 1
        #Update validContinuations
        
    def __init__(self, move):
        self.pos = []
        self.numRow = 1
        self.initValidCont(move)
        self.pos += [move]
def debugPrint(x):
    print("Pos: " + str(x.pos))
    print("Num Rows: " + str(x.numRow))
    print("X: " + str(x.dx))
    print("Y: " + str(x.dy))
    print("Head: " + str(x.head))
    print("Tail: " + str(x.tail))
    print("\n")

x = InARow((4,4))
x.addMove((5,4))
x.addMove((6,4))
debugPrint(x)
x.addMove((3,4))
debugPrint(x)

def utilityFunction():
    return calcPts(2) + calcPts(3) + calcPts(4)

"""
First Iteration
1. A move is made
2. Looks for Existing n-in-a-row, closed and free, around the move made
3. If exists, updates to n+1-in a row
4. 



Dictionary = {Position : List of InARows}


move = getMove()
listOfIAR = Dictioanry(move)
for IAR in listOFIAR:
    IAR.addMove(move)

"""
