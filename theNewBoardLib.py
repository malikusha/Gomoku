import copy

DEBUG = True
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
"""
Contains a collection of in a row objects, and basically maintains a model for the
board.


 ABCDEFGHIJKL
1############
2#####X######
3#####XO#####
4######O#####
5#####X######

X dictionary
F1: (ID1: 3 in a row object)
F5: (ID1: 3 in a row object)
G2: (ID2: 1 in a row object, ID3: 1 in a row object)
G1: ...
E4:
E3:
E2:
E1:
G3:
G4:

x = GomokuCollection()
x = GomokuCollection(score2 = 10, score3 = 69, score4 = 100, score5 = 1000)



TODO set(dictionary.values())
TODO when opponents makes a move delete the move from the dictionary key

#######
#OXXXO#
#######

TODO open 3 vs closed 3 might be simulatable maybe by how many times it appears
in the dictionary

TODO
adding hash functions
"""
class GomokuCollection:
    # Initializes the GomokuCollection object. scoreN represents the weights
    # Given to n-in-a-rows
    """
    dictionary: Move -> set(InARow): maps potential valid moves to a set of in a Row objects
    history: a String List: a history of all moves added and removed
    scoreN: integer:  score weight for an N in a row object, (N = 2,3,4,5)
    """
    def __init__(self, score2=2, score3=5, score4=10, score5 = 1000000):
        """
         the dictionary basically links a coordinate with all InARow objects that can grow
        (IE by placing a piece there the InARoW object evolves from an N in a row to an
         N+1 in a row
        Hashmap: move -> set of inARow objects
        """
        self.dictionary = {}
        """
        Store deleted dictionary values
        """
        self.deleteDictionary = {}
        self.deleteEnemyDictionary = {}
        """
        adds a "Move" + move made into the list when a move is made
        adds a "Remove" + move made into the list when a move is undo'ed
        """
        self.history = []
        self.orderedMoves = []

        self.enemyMoves = set()
        self.score2 = score2
        self.score3 = score3
        self.score4 = score4
        self.score5 = score5

        self.ourMove = True

    def removeMove(self):
        move = self.orderedMoves.pop()
        self.history += [("r", move)]
        x = move[0]
        y=  move[1]
        boundaryList = [(x + 1, y)    , (x - 1, y),
                        (x, y + 1)    , (x, y - 1),
                        (x + 1, y + 1), (x - 1, y - 1),
                        (x - 1, y + 1), (x + 1, y - 1)]
        
        """removes 1 in row IAR objects"""
        for e1 in boundaryList:
            if(e1 in self.dictionary):
                self.dictionary[e1] = set(s for s in self.dictionary[e1] if move not in s.moveList)
                if(len(self.dictionary[e1])==0): del self.dictionary[e1]
        
        #For objects of length greater than 1
        #-> reduce count by 1
        #-> change head tail
        #-> remove from position
        for curMove in self.deleteDictionary[move]:
            curMove.removeMove(move)
            if(curMove.head == move):
                if(curMove.tail in self.deleteDictionary):
                    self.dictionary[curMove.tail] = self.deleteDictionary[curMove.tail]
            elif(curMove.tail == move):
                if(curMove.head in self.deleteDictionary):
                    self.dictionary[curMove.head] = self.deleteDictionary[curMove.head]
            else:
                raise Exception("I screwed up")
        if(len(self.deleteDictionary[move])>0):
           self.dictionary[move] = self.deleteDictionary[move]
        del self.deleteDictionary[move]
        self.ourMove = True
        #delete any merged creations
        
    def getPotentialMoves(self):
        x = []
        for e in self.dictionary.keys():
            x += [COLUMNS[e[1]] + " " + str(e[0]+1)]
        print("All potential moves: " + str(x))
        return set(self.dictionary.keys())
    
        
    def addMove(self, move):
        """
         123456789
        1#########
        2#########
        3###X#####
        4#########

        Dictionary:
        (3,3): (1 in a row object, ...)
        (3,5): 1 in a row object
        (2,3): 1 in a row object
        ..
        .
        .
        I play move 3,3
        """
        self.history += [("a",move)]
        self.orderedMoves += [move]
        x = move[0]
        y=  move[1]
        allPossiblePotentialCoordinates = (((x-1,y),(x+1,y)),
                                           ((x,y-1),(x,y+1)),
                                           ((x-1,y-1),(x+1,y+1)),
                                           ((x+1,y-1),(x-1,y+1)))
        if(move not in self.deleteDictionary):
            self.deleteDictionary[move] = set()
        taken = []
        """adds the move to existing IAR objects"""
        if(move in self.dictionary):
            mergeIssues = []
            for iar in self.dictionary[move]:
                updateKey = iar.addMove(move) #to be fixed
                """
                check if the update key corresponds to ay
                """

              #  print("Another dictionary")
                if(updateKey in self.deleteDictionary):
                    for iar2 in self.dictionary[move]:
                        if(updateKey in iar2.moveList):
                            newIAR = iar2.merge(iar)

                    
                    if(newIAR.head in self.dictionary):
                        if(iar not in mergeIssues):
                            self.deleteDictionary[newIAR.head] = self.dictionary[newIAR.head].copy()
                        if(iar2 in self.dictionary[newIAR.head]):
                            self.dictionary[newIAR.head].remove(iar2)
                        if(iar in self.dictionary[newIAR.head]):
                            self.dictionary[newIAR.head].remove(iar)
                        if(iar2 in mergeIssues):
                            self.tryAdd(newIAR.head,newIAR)
                    if(newIAR.tail in self.dictionary):
                        if(iar not in mergeIssues):
                            self.deleteDictionary[newIAR.tail] = self.dictionary[newIAR.tail].copy()
                        if(iar2 in self.dictionary[newIAR.tail]):
                            self.dictionary[newIAR.tail].remove(iar2)
                        if(iar in self.dictionary[newIAR.tail]):
                            self.dictionary[newIAR.tail].remove(iar)
                        if(iar2 in mergeIssues):
                            self.tryAdd(newIAR.tail,newIAR)

                    mergeIssues +=[iar, iar2]
                else:           
                    self.tryAdd(updateKey,iar)
                taken += [updateKey]
            self.deleteDictionary[move] = self.dictionary[move]
            del self.dictionary[move] #instead of deleteing, move to different dict for easy restore

        """creates new 1 in row IAR objects
        TODO: dont add 1 in a row objects in which overlaps with a parallel
        N in a row object for N>1"""
        for coordTuple in allPossiblePotentialCoordinates:
            if(not ((coordTuple[0] in taken) or (coordTuple[1] in taken))):
                iarObject = InARow(move, coordTuple[0], coordTuple[1])
                self.tryAdd(coordTuple[0], iarObject)
                self.tryAdd(coordTuple[1], iarObject)
        self.ourMove = False
        
    def undoMove(self):
        #means we have to undo the opponents move
        if(self.ourMove): 
            self.undoEnemyMove()
        else:
            self.removeMove()
            
    def undoEnemyMove(self):
        move = self.enemyMoves.pop()
        self.history += [('re', move)]
        self.dictionary[move] = self.deleteEnemyDictionary[move]
        del self.deleteEnemyDictionary[move]
        self.ourMove = False

    def addEnemyMove(self,move):
        self.history += [('ae', move)]
        self.enemyMoves.add(move)
        if(move in self.dictionary):
            self.deleteEnemyDictionary[move] = self.dictionary[move]
            del self.dictionary[move]
        else:
            self.deleteEnemyDictionary[move] = set()
        self.ourMove = True
        
            
    """tries to add a move to the dictionary"""
    def tryAdd(self, key, move):
        if(move in self.enemyMoves or key in self.enemyMoves):
            return
        if(not(key[0] > 14 or key[0] < 0 or key[1] > 14 or key[1] < 0)):
            if (key not in self.dictionary): self.dictionary[key] = set()
            self.dictionary[key].add(move)

    """Get all InARow objects that have 'num' objects inside"""
    def getAllInARow(self, num):
        #TODO: improve functionality, cause there is a lot of repetition and its
        #slow
        retSet = set()
        for sets in self.dictionary.values():
            for e in sets:
                if(e.lengthOfRow == num):
                    retSet.add(e)
        return retSet
    """Get all keys with 'num' objects inside the set in the value"""
    def getAllNKeys(self, num):
        #TODO: same as on top, right now very repetitive
        retSet = set()
        for e in self.dictionary:
            if(len(self.dictionary[e])==num):
                retSet.add(e)
        return retSet
    
    def getScore(self):
        score = 0
        for key in self.dictionary:
            for move in self.dictionary[key]:
                if(move.lengthOfRow == 2):
                    score += self.score2
                if(move.lengthOfRow == 3):
                    score += self.score3
                if(move.lengthOfRow == 4):
                    score += self.score4
                if(move.lengthOfRow == 5):
                    return self.score5
        return score
    def debugPrintDictionary(self, printLengthOne = False):
        for e in self.dictionary:
            if(printLengthOne):
                if(len(self.dictionary[e])==1):
                    continue
            print("                                                     Current Key: " + str(e))
            curSet = self.dictionary[e]
            for iar in curSet:
                iar.debugPrint()
    def getAllDictKeys(self):
        print("All dictionary keys: ")
        for e in self.dictionary:
            print(e)



"""
A representation of moves that form N-in a row, as way of detecting potentially
good moves

"""
class InARow:
    """
        moveList: set(moves) -> contains all the moves inside the InARow object
        moves: tuple: (x,y) -> coordinates of the position of the tuple
        length: number of items in a row IE number of moves in the InARow object
    """
    def __init__(self, move, head, tail):
        self.moveList = set()
        self.moveList.add(move)
        self.lengthOfRow = 1
        self.head = head
        self.dx = head[0] - move[0]
        self.dy = head[1] - move[1]
        self.tail = tail
    
    def addMove(self,move):
        self.lengthOfRow +=1
        self.moveList.add(move)
        return self.updateHeadTail(move)

    def removeMove(self, move):
        self.lengthOfRow = self.lengthOfRow - 1
        headVal = abs(self.head[0] - move[0]) + abs(self.head[1] - move[1])
        tailVal = abs(self.tail[0] - move[0]) + abs(self.tail[1] - move[1])
##        print("headVal: " + str(headVal))
##        print("tailVal: " + str(tailVal))
##        print("move: " + str(move))
##        print("head: " + str(self.head))
##        print("tail: " + str(self.tail))
        if(headVal>tailVal):
            self.tail = move
        else:
            self.head = move
        self.moveList.remove(move)
        #TODO: change head/tail
        
    def merge(self, iar):
        retIAR = copy.deepcopy(self)
        retIAR.moveList.update(iar.moveList)
        head1 = retIAR.head
        head2 = iar.head
        tail1 = retIAR.tail
        tail2 = iar.tail
        if(head1 in retIAR.moveList):
            retIAR.head = head2
        elif(head2 in retIAR.moveList):
            retIAR.tail = tail2
        else:
            print("error in merging")
            print("To merge: " + str(iar.moveList))
            print("Head:" + str(head2))
            print("Tail:" + str(tail2))
            print("Being merge: " + str(self.moveList))
            print("Head:" + str(head1))
            print("Tail:" + str(tail1))
            raise Exception("Erroor in merge")
            
            
        
        #retIAR.updateHeadTail(front)
        #retIAR.updateHeadTail(back)
        retIAR.lengthOfRow = len(retIAR.moveList)
        return retIAR

    def updateHeadTail(self,move):
        if(move == self.head):
            self.head = (self.head[0]+self.dx,self.head[1]+self.dy)
            return self.head
        elif(move == self.tail):
            self.tail = (self.tail[0]-self.dx,self.tail[1]-self.dy)
            return self.tail
        else:
            print("Update Head Tail : ")
            print("Input Move: " + str(move))
            print("Head: " + str(self.head))
            print("Tail: " + str(self.tail))
            return -1
        
    def debugPrint(self):
        print(self)
        print("Length: " + str(self.lengthOfRow)
              +" Move List: "  + str(self.moveList)
              + " Head: " + str(self.head)
              + " Tail: " + str(self.tail))
    
