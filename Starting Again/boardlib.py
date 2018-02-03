import copy


"""
If numRow = 1, a copy of the object needs to be created
TODO: removeMove((i,j)) - removes the move from the board
TODO: think a bit more about the terminal condition
TODO: open or closed?
TODO: remove stuff from dictionary? space will be pretty big, but i dont think it will
affect the speed
"""

"""
This class basically contains all of the InARow objects. Should be initialized for each player
"""
DEBUG = False

class GomokuCollection:
    # Initializes the GomokuCollection object. scoreN represents the weights
    # Given to n-in-a-rows
    def __init__(self, score2=2, score3=5, score4=10):
        # the dictionary basically links a coordinate with all InARow objects that can grow
        # (IE by placing a piece there the InARoW object evolves from an N in a row to an
        # N+1 in a row
        #Dictionary: move -> list of moves
        self.dictionary = {}
        # Created to save time.
        # Stores all InARow object of length greater than 1
        self.scorable = set()

        #Stores all the moves in order
        self.orderedMoves = []
        self.history = []
        # The weights of the 2,3,4 in a rows. should be experimented and changed
        self.score2 = score2
        self.score3 = score3
        self.score4 = score4
        # when a moved is played, this move should be called

    def getPotentialMoves(self):
        return set(self.dictionary.keys())


    def getMovesMade(self):
        return set(self.orderedMoves)

    #sdf
    def debugPrint(self, include1 = False, fulldebug = False):
        print("Init Debugging")
        if(include1 and fulldebug):
            for e in self.dictionary:
                curList = self.dictionary[e]
                print("Current Key: " + str(e))
                for e1 in curList:
                    e1.debugPrint()
        elif(include1):
            bigList = set()
            for e in self.dictionary:
                print("Current Key: " + str(e))
                curList = self.dictionary[e]
                for e1 in curList:
                    if(e1 not in bigList):
                        e1.debugPrint()
                        bigList.add(e1)
        elif(fulldebug):
            if(include1 and fulldebug):
                for e in self.dictionary:
                    curList = self.dictionary[e]
                    print("Current Key: " + str(e))
                    for e1 in curList:
                        if(e1.numRow>1): e1.debugPrint()
        else:
            for e in self.scorable:
                e.debugPrint()
            

    def addNewMove(self, move):
        self.history += ["Add Move: " + str(move)]
        if(DEBUG): print("Adding Move: " + str(move))
        #print("History: ")
       # print(self.history)
        """
        Adds a move and creates up to 4 InARow objects of length 1. 
        Then, it tries to join itself with existing InARow objects
        """
        aRow = InARow(move)
        coordinates = aRow.validCont
        if (move not in self.dictionary): self.dictionary[move] = set()
        rows = self.dictionary[move]
        taken = []
        self.orderedMoves += [move]
        # Tries to join the new move with previous InARow objects
        for row in rows:
            if (row.numRow == 1): self.scorable.add(row)


            row.addMove(move)
            self.tryAdd(row.head, row)
            # self.dictionary[row.head].add(row)
            self.tryAdd(row.tail, row)
            # self.dictionary[row.tail].add(row)
            taken += [row.head]
            taken += [row.tail]

        # Adds up to 4 copies of a new InARow object, with numRow value of 1
        for e in coordinates:
            if ((e[0] not in taken) and (e[1] not in taken)):
                aRow.setHeadTail(e)
                copyRow = copy.deepcopy(aRow)
                self.tryAdd(e[0], copyRow)
                # self.dictionary[e[0]].add(copyRow)
                self.tryAdd(e[1], copyRow)
                # self.dictionary[e[1]].add(copyRow)
        #del self.dictionary[move]  # if we remove this will it make the AI worse?

    # tries to add a move to the dictionary
    def tryAdd(self, key, move):
        if(not(key[0] > 14 or key[0] < 0 or key[1] > 14 or key[1] < 0)):
            #print("WOW its the key!: " + str(key))
            if (key not in self.dictionary): self.dictionary[key] = set()
            self.dictionary[key].add(move)

    def undoMove(self):
        curMove = self.orderedMoves.pop()
        self.history += ["Remove Move: " + str(curMove)]
        if (DEBUG):
            print("Removing move: " + str(curMove))
        x = curMove[0]
        y = curMove[1]
        boundaryList = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y - 1),
                          (x - 1, y + 1), (x + 1, y - 1)]
        #remove all InARow  objects of length 1
        if(DEBUG):
            print(self.dictionary)
        for e1 in boundaryList:
            if(e1 in self.dictionary.keys()):
                self.dictionary[e1] = set(s for s in self.dictionary[e1] if curMove not in s.pos)
                if(len(self.dictionary[e1])==0): del self.dictionary[e1]
                
        #For objects of length greater than 1
        #-> reduce count by 1
        #-> change head tail
        #-> remove from position
        if(curMove in self.dictionary.keys()):
            for move in self.dictionary[curMove]:
                move.removeMove(curMove)
                if(move.numRow <2):
                    self.scorable.remove(move)
                    
                

                
                

    def getAllValidMoves(self):
        return self.dictionary.keys()

    def getAllMoves(self):
        return self.dictionary.values()

    def getScore(self):
        score = 0
        for e in self.scorable:
            if (e.numRow == 2):
                score += self.score2
            elif (e.numRow == 3):
                score += self.score3
            elif (e.numRow == 4):
                score += self.score4
            else:
                score += 1000000
                return score
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
        if (not (move[0][0] > 14 or move[0][0] < 0 or move[0][1] > 14 or move[0][1] < 0)): self.head = move[0]
        if (not (move[1][0] > 14 or move[1][0] < 0 or move[1][1] > 14 or move[1][1] < 0)): self.tail = move[1]

    def initValidCont(self, move):
        x = move[0]
        y = move[1]
        self.validCont = [((x + 1, y), (x - 1, y)), ((x, y + 1), (x, y - 1)), ((x + 1, y + 1), (x - 1, y - 1)),
                          ((x - 1, y + 1), (x + 1, y - 1))]

    def addMove(self, move):
        isOne = self.numRow == 1
        self.updateLength()

        self.setValidVector(move, isOne)
        self.pos += [move]

    def setValidVector(self, move, isOne):
        if (isOne):
            self.dx = move[0] - self.pos[0][0]
            self.dy = move[1] - self.pos[0][1]
            if not((move[0] + self.dx > 14 or move[0] + self.dx < 0) or (move[1] + self.dy > 14 or move[1] + self.dy < 0)):
                self.head = (move[0] + self.dx, move[1] + self.dy)
            if not(self.pos[0][0] - self.dx > 14 or self.pos[0][0] - self.dx < 0):
                self.tail = (self.pos[0][0] - self.dx, self.pos[0][1] - self.dy)
        else:
            if (move == self.head): # and not(move[0] >= 14 or move[0] <= 0 or move[1] >= 14 or move[1] <= 0)):
                self.head = (self.head[0] + self.dx, self.head[1] + self.dy)
            elif (move == self.tail): # and not(move[0] >= 14 or move[0] <= 0 or move[1] >= 14 or move[1] <= 0)):
                self.tail = (self.tail[0] - self.dx, self.tail[1] - self.dy)
            else:
                pass
                #print("Error in the setValidvector")
                #print("Current Value: " + str(move))
                #print("Head: " + str(self.head))
                #print("Tail: " + str(self.tail))

                # self.validCont = [(newMove[0]+self.dx, newMove[0]+self.dy), (self.pos[0][0]-self.dx, self.pos[0][1]-self.dx)]

    def updateLength(self):
        self.numRow += 1
        # Update validContinuations

    def __init__(self, move):
        self.pos = []
        self.numRow = 1
        self.initValidCont(move)
        self.pos += [move]
        self.dx = 0
        self.dy = 0
        self.head = (-1, -1)
        self.tail = (-1, -1)

    def removeMove(self, move):
        self.numRow = self.numRow - 1
        headVal = self.head[0] - move[0] + self.head[1] - move[1]
        tailVal = self.tail[0] - move[0] + self.tail[1] - move[1]
        if(headVal>tailVal):
            self.head = move
        else:
            self.tail = move
        self.pos.remove(move)
        #TODO: change head/tail
    
    def debugPrint(self):
        print("Pos: " + str(self.pos) + " Num Rows: " + str(self.numRow)
              + " Head: " + str(self.head) + " Tail: " + str(self.tail))
        # print("X: " + str(self.dx))
        # print("Y: " + str(self.dy))


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

def testDelete():
    white = GomokuCollection()
    white.addNewMove((4, 4))
    white.addNewMove((5, 4))
    white.addNewMove((6, 4))
    white.addNewMove((4, 3))
    white.undoMove()
    printOutStuff(white)

def printOutStuff(aCollection):
    allMoves = aCollection.getAllValidMoves()
    count = 0
    for e1 in allMoves:
        e = aCollection.dictionary[e1]
        if (len(e) >= 1):
            print("Coordinate: " + str(e1))
            for eoe in e:
                count += 1
                if (eoe.numRow > 1):
                    # x= 3
                    print(eoe)
                    eoe.debugPrint()
            print("")
    print("Num: " + str(count))


def test():
    white = GomokuCollection()
    white.addNewMove((4, 4))
    white.addNewMove((5, 4))
    white.addNewMove((6, 4))
    white.addNewMove((4, 3))
    allMoves = white.getAllValidMoves()
    count = 0
    for e1 in allMoves:
        e = white.dictionary[e1]
        if (len(e) >= 1):
            print("Coordinate: " + str(e1))
            for eoe in e:
                count += 1
                if (eoe.numRow > 1):
                    # x= 3
                    print(eoe)
                    eoe.debugPrint()
            print("")
    print("Num: " + str(count))
    return white


def testDebugCapabilities():
    white = GomokuCollection()
    white.addNewMove((4,3))
    white.addNewMove((2,3))
    white.addNewMove((3,3))
    white.debugPrint(include1 = True)


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
