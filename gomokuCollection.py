class GomokuCollection:

    def __init__(self, length = 15, width = 15, score2=2, score3=5, score4=10, score5 = 10000000):
        self.board = [[0 for x in range(length)] for y in range(width)] 
        self.orderedMoves = []
        self.score = [0,0,score2,score3,score4,score5]
    def addMove(self, move):
        self.orderedMoves += [move]
        self.board[move[0]][move[1]] = 1
        
    def addEnemyMove(self, move):
        self.orderedMoves += [move]
        self.board[move[0]][move[1]] = -1
    def undoMove(self):
        move = self.orderedMoves.pop()
        self.board[move[0]][move[1]] = 0
        

    def outOfRange(self, move):
        return (move[0] < 0) or (move[0] > 14) or (move[1] <0) or (move[1] > 14)


    def getPotentialMoves(self):
        retSet = set()
        for move in self.orderedMoves:
            if(self.board[move[0]][move[1]]==1):
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
##                    print("The head tail: " + str(headTail))
##                    print("Score: " + str(self.score[curLen]))
                    headTail = (head,tail)
                    if(headTail not in alreadyExistingHeadTails):
                        alreadyExistingHeadTails.add(headTail)
                        if((headBlock and not tailBlock) or (not headBlock and tailBlock)):
                            totalScore += self.score[curLen]
                        if(not (headBlock or tailBlock)):
                            totalScore += 2*self.score[curLen]
        if(totalScore > 900000): return self.score[5]
        return totalScore

