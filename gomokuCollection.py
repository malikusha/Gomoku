BOARD_SIZE = 15
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
class GomokuCollection:

    def __init__(self, length = BOARD_SIZE, width = BOARD_SIZE, score2=2, score3=9, score4=15, score5 = 10000000):
        self.board = [[0 for x in range(length)] for y in range(width)] 
        self.orderedMoves = []
        self.hashableMoves = []
        self.score = [0,0,score2,score3,score4,score5]
        self.ourMove = True
    def __hash__(self):
      return hash(tuple(set(self.hashableMoves)))
    def addMove(self, move):
        self.orderedMoves += [move]
        self.board[move[0]][move[1]] = 1
        self.hashableMoves += [(move,1)]
        self.ourMove = False
        
    def addEnemyMove(self, move):
        self.orderedMoves += [move]
        self.board[move[0]][move[1]] = -1
        self.hashableMoves += [(move,-1)]
        self.ourMove = True
    def undoMove(self):
        move = self.orderedMoves.pop()
        self.hashableMoves.pop()
        if(self.board[move[0]][move[1]] == 1):
            self.ourMove = True
        elif(self.board[move[0]][move[1]] == -1):
            self.ourMove = False
        else:
            raise Exception("gg broskeys")
        self.board[move[0]][move[1]] = 0
        

    def outOfRange(self, move):
        return (move[0] < 0) or (move[0] > BOARD_SIZE-1) or (move[1] <0) or (move[1] > BOARD_SIZE-1)


    def getPotentialMoves(self):
        retSet = set()
        for move in self.orderedMoves:
            boundaryList = [(1, 0),(0, 1),(1, 1),(-1, 1)]
            for vector in boundaryList:            
                head = (move[0] + vector[0], move[1] + vector[1])
                tail = (move[0] - vector[0], move[1] - vector[1])
                if(not self.outOfRange(head)):
                    if(self.board[head[0]][head[1]]==0):
                        retSet.add(head)
                if(not self.outOfRange(tail)):
                    if(self.board[tail[0]][tail[1]]==0):
                        retSet.add(tail)
        return retSet

    def printBoard(self):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in self.board]))
    
    def getScore(self):
        #Purely offensive strategy
        totalScore = 0
        alreadyExistingHeadTails = set()
        for move in self.orderedMoves:
            if(self.board[move[0]][move[1]]==1):
                boundaryList = [(1, 0),(0, 1),(1, 1),(-1, 1)]
                for vector in boundaryList:
                    head = (move[0] + vector[0], move[1] + vector[1])
                    tail = (move[0] - vector[0], move[1] - vector[1])
                    curLen = 1
                    headBlock = False
                    tailBlock = False
                    #Extending heads
                    if(not self.outOfRange(head)):
                        while(self.board[head[0]][head[1]]==1):
                            curLen+=1
                            head = (head[0] + vector[0], head[1] + vector[1])
                            if(self.outOfRange(head)):
                                break
                    if(self.outOfRange(head)):
                        headBlock = True
                    elif(self.board[head[0]][head[1]]==-1):
                        headBlock = True
                    #Extending tails
                    if(not self.outOfRange(tail)):
                        while(self.board[tail[0]][tail[1]]==1):
                            curLen+=1
                            tail = (tail[0] - vector[0], tail[1] - vector[1])
                            if(self.outOfRange(tail)):
                                break
                    if(self.outOfRange(tail)):
                        tailBlock = True
                    elif(self.board[tail[0]][tail[1]]==-1):
                        tailBlock = True
                    headTail = (head,tail)
                    if(headTail not in alreadyExistingHeadTails):
                        alreadyExistingHeadTails.add(headTail)
                        if(curLen >= 5): return self.score[5]
                        if((headBlock and not tailBlock) or (not headBlock and tailBlock)):
                            if(self.ourMove and curLen == 4): #A forced win
                                totalScore += 10000
                            else:
                                totalScore += self.score[curLen]
                        if(not (headBlock or tailBlock)):
                            if(curLen == 4): totalScore += 1000
                            totalScore += 2*self.score[curLen]
        return totalScore

