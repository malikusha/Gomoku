import copy

"""
If numRow = 1, a copy of the object needs to be created
TODO: open or closed?
TODO: remove stuff from dictionary? space will be pretty big, but i dont think it will
affect the speed
"""
class GomokuCollection:
    #Initializes the GomokuCollection object. scoreN represents the weights
    #Given to n-in-a-rows
    def __init__(self, score2 = 2, score3 = 3, score4 = 4):
        self.dictionary = {}
        self.scorable = set()
        self.score2 = score2
        self.score3 = score3
        self.score4 = score4
    def addNewMove(self, move):
        aRow = InARow(move)
        coordinates = aRow.validCont
        if(move not in self.dictionary): self.dictionary[move] = set()
        rows = self.dictionary[move]
        taken = []

        #Tries to join the new move with previous InARow objects
        for row in rows:
            if(row.numRow==1): self.scorable.add(row)
            row.addMove(move)
            self.tryAdd(row.head, row)
            #self.dictionary[row.head].add(row)
            self.tryAdd(row.tail, row)
            #self.dictionary[row.tail].add(row)
            taken += [row.head]
            taken += [row.tail]
            
        #Adds up to 4 copies of a new InARow object, with numRow value of 1
        for e in coordinates:
            if((e[0] not in taken) and (e[1] not in taken)):
                aRow.setHeadTail(e)
                copyRow = copy.deepcopy(aRow)
                self.tryAdd(e[0], copyRow)
                #self.dictionary[e[0]].add(copyRow)
                self.tryAdd(e[1], copyRow)
                #self.dictionary[e[1]].add(copyRow)
        del self.dictionary[move] #if we remove this will it make the AI worse?
    def tryAdd(self, key, move):
        if(key not in self.dictionary): self.dictionary[key] = set()
        self.dictionary[key].add(move)
        
    def getAllValidMoves(self):
        return self.dictionary.keys()
    def getAllMoves(self):
        return self.dictionary.values()
    def getScore(self):
        score = 0
        for e in self.scorable:
            if(e.numRow == 2):
                score += self.score2
            elif(e.numRow == 3):
                score += self.score3
            elif(e.numRow == 4):
                score += self.score4
            else:
                print("Hfjsfdafdklj error detected")
        return score
                
class InARow:
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
    def setHeadTail(self, move):
        self.head = move[0]
        self.tail = move[1]
    def initValidCont(self, move):
        x = move[0]
        y = move[1]
        self.validCont = [((x+1,y),(x-1,y)),((x,y+1),(x,y-1)),((x+1,y+1),(x-1,y-1)),((x-1,y+1),(x+1,y-1))]
        
    def addMove(self, move):
        isOne = self.numRow == 1
        self.updateLength()
        self.setValidVector(move, isOne)
        self.pos += [move]

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
        self.dx = 0
        self.dy = 0
        self.head = (-1,-1)
        self.tail = (-1,-1)
    def debugPrint(self):
        print("Pos: " + str(self.pos) + " Num Rows: " + str(self.numRow)
              + " Head: " + str(self.head) + " Tail: " + str(self.tail))
        #print("X: " + str(self.dx))
        #print("Y: " + str(self.dy))



"""
x = InARow((4,4))
x.addMove((5,4))
x.addMove((6,4))
debugPrint(x)
x.addMove((3,4))
debugPrint(x)
"""

"""
Call this function to test
"""
def test():
    white = GomokuCollection()
    white.addNewMove((4,4))
    white.addNewMove((5,4))
    white.addNewMove((6,4))
    white.addNewMove((4,3))
    allMoves = white.getAllValidMoves()
    count = 0
    for e1 in allMoves:
        e = white.dictionary[e1]
        if(len(e) >= 1):
            print("Coordinate: " + str(e1))
            for eoe in e:
                count += 1
                if(eoe.numRow > 1):
                    #x= 3
                    print(eoe)
                    eoe.debugPrint()
            print("")
    print("Num: " + str(count))
    return white


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
