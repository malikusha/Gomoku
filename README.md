# Gomoku
___
## Team Name: Large_Horse
#### Contributors: Bhon Bunnag, Malika Nurbekova, Yil Verdeja
___
## Program Instructions on compiling and running the program
Initially to test the program, two different agents needed to be executed with the referee. As that became a slow and painstaking effort, the *gameTest.py* class was created in order to quicken this process. This was possible by changing the attributes of the team names and the agent files. An example is the snippet below which uses two example agents with their corresponding team names.

```python
def callReferee(teamName1 = 'Large_Horse', teamName2 = 'notKnuckles'):
    subprocess.call(['python.exe', 'referee.py', teamName1, teamName2])
def callAgent():
    subprocess.call(['python.exe', 'agent.py'])
def callAgent2():
    subprocess.call(['python.exe', 'agent2.py'])
def removeFiles(teamName1 = 'Large_Horse', teamName2 = 'notKnuckles'):
    listOfFiles = [teamName1 + ".go", teamName2 + ".go", "move_file",
                   "history_file", "end_game"]
    for e in listOfFiles:
        try:
            os.remove(os.path.join('./', e))
        except:
            print("No file named " + e)
```
If you don't have python installed, click on this [link](https://www.python.org/).
Depending on the version of python, use this command to initiate the game:
```
$ python gameTest.py
```
However if *python gameTest.py* command does not run on your computer, run:
```
$ python referee.py Large_Horse enemy_team
```
Instead of *enemy_team*, use the TEAM_NAME of the agent that is being run. At the same time while running the *agent.py* and one of the testing agents files(e.g. *testingAgent2.py*):
```
$ python agent.py
```
If it doesn't run, make sure that these files are not inside the system: *move_file*, *end_file*, and any files ending in *.go*.
___
## 1 Project Description and Goal
This project consists of developing and implementing a computer program that plays Gomoku. Also known as "five in-a-row", is a board game similar to tic-tac-toe but on a larger board.
***
### 1.1 Game Description
Gomoku is a two player game. The two players take turns putting markers on the board. One of the player uses **white** markers and the other uses **black** markers. 

The size of the board is a 15 x 15 cell board. Columns are marked with letters *A* to *O* from left to right and rows are numbered 1 to 15 from top to bottom.

A move is specified by the column letter and row number pair (e.g., F8, G3, etc)
The player who gets 5 markers in a row wins. If the board fills up before anyone can win, the game ends in a tie.
***
### 1.2 Game Rules
A game will consist of a sequence of the following actions:
1. A random selection method is used to determine which player will use the white markers and which player will use the black markers. In what follows, the player who gets to use the white markers is called *player1* and the player who gets to use the black markers is called *player2*
2. *Player1* gets to play first.
3. After *Player1* has made its first move, *player2* is given the chance to change the color of the stone on the board to black. This is done to limit the advantages of playing first.
4. After that, *player1* and *player2* take turns making moves until the game ends with one player winning or a tie. There is a **10 second time limit** for a player to make its move.
___
## 2 Program Implementation
The following subsections will go through and describe the different algorithms, heuristics and strategies that were implemented to run the Gomoku AI. This section will also step through the AI's offensive and defensive behavior, as well as its interaction with the referee.

***
### 2.1 Minimax Implementation
The minimax implementation can be found within the *agent.py* class as a the function named *minimax*. The following snippets on lines __ to __ shows the minimax implementation

```python
def minimax(depth = 1):
    global white
    global black
    global bestMove
    global cutOff
    allValidMoves = getValidMoves()
    maxScore = -1<<31
    for move in allValidMoves:
        addMoveToBoard(move[0], move[1], True)
        curScore = alphaBeta(depth,alpha = -1<<31, beta = 1<<31, isMaxPlayer = False)
        if(curScore > maxScore):
            maxScore = curScore
            bestMove = move
        removeMoveFromBoard(move[0], move[1], True)
    return bestMove
```
According to *geeksforgeeks.org*
> Minimax is a kind of backtracking algorithm that is used in decision making and game theory to find the optimal move for a player, assuming that your opponent also plays optimally.

That being said, the following algorithm obtains all the valid moves on the board (which are all the open positions adjacent to the placed pieces on the board), and running the *alphaBeta* algorithm given a certain depth it obtains the most optimal move to play.
***
### 2.2 Alpha-Beta Pruning Implementation
The alpha-beta pruning implementation can be found within the *agent.py* class as a the function named *alphaBeta*. The following snippets on lines __ to __ shows the minimax implementation

```python
def alphaBeta(depth = 3, alpha = -1<<31, beta = 1<<31, isMaxPlayer = False):
    global white
    global black
    validMoves = getValidMoves()
    levelScore = white.getScore()-black.getScore()
    if(depth == 1 or (abs(levelScore)>WIN_SCORE_CUTOFF)):
        return levelScore
    if(isMaxPlayer):
        maxScore = -1<<31
        for move in validMoves:
            addMoveToBoard(move[0], move[1], True)
            maxScore = max(maxScore, alphaBeta(depth-1,alpha, beta, False))
            alpha = max(alpha, maxScore)
            removeMoveFromBoard(move[0], move[1], True)
            if(beta <= alpha):
                break;
        return maxScore
    else:
        minScore = 1 <<31
        for move in validMoves:
            addMoveToBoard(move[0], move[1], False)
            minScore = min(minScore, alphaBeta(depth-1,alpha, beta, True))
            beta = min(beta, minScore)
            removeMoveFromBoard(move[0], move[1], False)
            if(beta <= alpha):
                break;
        return minScore
```
The alpha-beta pruning function incorporates the minimax algorithm as it recursively calls the *alphaBeta* (i.e. itself) function changing between players (max and min) to obtain the most optimal move. It obtains an optimal move more efficiently using alpha-beta pruning by pruning branches that need not to be expanded further.
#### Utility Function
The variable *levelScore* obtains the score for the current state of the board by using a heuristic evaluation function in order to assign a number to any intermediate board configuration.
***
### 2.3 Heuristic Evaluation Function and Strategies
#### Heuristic Evaluation Function

```python
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
                    ...
                    # Expands the Tail node and Head node until it reaches a different marker or an empty cell
                    ...
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
```
#### Depth Limited Search vs Iterative Deepening
Depth-limited search with a depth of 2 was used as a heuristic strategy to avoid expanding the whole minimax tree so that a move is produced withim the time limit. The reason why we preferred using depth-limited search over iterative deepening was due to the performance. We implemented Iterative Deepening and while testing it, we realized that on average it goes as deep as 2-3 depths down when timed. However, it is performing the move much slower due to it's recalculating when going to each depth. So, using depth-limited search with a limit of 2 gives the same result, but with faster performance.

```python
def depthLimited():
    minimax(2)
```

### 2.5 Program Testing
#### Test Driven Development
The *GomokuCollection* class is the class that controls the movement on the board and assigns evaluation scores to it. In order to proceed in using this class, it needed to be heavily tested. Using Test Driven Development (TDD), inside the *testCollection.py* class, the GomokuCollection was thouroughly examined to make sure that the code worked as expected.

#### Testing Agent vs Agent
The first agent was tested against an agent that made random moves on the board (filename: testingAgent1.py, team name: random-move). Once the AI could beat a testAgent1, then we moved on to it playing with smarter agents. As the program progressed, different agents were created with slight tweaks in their search algorithm or heuristics evaluation function. These agents played against each other in order to obtain the most optimal agent (Performance measure: Winning to Losing ratio). Without any time constraints, agents would play against human users. Almost all the time, the AI would beat the human. (This human is **Bhon Bunnag** who is an excellent Chess Player (President of Chess Club) and Gomoku Player).

In case if you would like to test *agent.py* (our final agent that uses minimax with alpha-beta pruning and depth-limited search as its heuristic strategy) against all the previous versions we had, we included those versions into the submission folder since we tested *agent.py* against them:

- *testingAgent1.py* (random-move) - Makes random moves on the board
- *testingAgent2.py* (minimax) - minimax algorithm with no alpha-beta pruning or heuristic strategy
- *testingAgent3.py* (minimax-alpha-beta) - minimax algorithm with alpha-beta pruning and no heuristic strategy
- *testingAgent4.py* (ID) - Iterative Deepening heuristic strategy

#### Strengths and Weaknesses
Weakness: Since depth limiting search is used (to a depth of 2) rather than iterative deepening, this becomes a weakness for the program since it can  only look 2 moves ahead rather than five or ten.

Strenghts: The strength of our AI lies in the fact that the utility score takes into account both the players move and the opponent move, thus performing both offensively and defensively.

***
### 2.6 Discussion
GENERAL IDEA

The utility function attempts to assign points depending on the existence of interests
structures. The most relevant ones are the existance of N-in-a-row objects.
 -------   -------    ----X_-    -X-----   -------
 -------   ----_X-    ---X---    --X----   -------
 ---X---   -----X-    --X----    ---X---   XXXXXX-
 -------   -------    -------    ----X--   -------
1-in-a-row 2-in-a-row 3-in-a-row 4-in-a-row 5-in-a-row

Each of these structures are assigned to be either open, closed, or dead
-------   -------   -------
----X--   -------   ----O--
---X---   --OXX--   -----X-
--X----   -------   ------X 
-------   -------   -------
Open	  Closed	Dead

The first example is an open structure because it can grow into a four in a row by 
placing a piece on either end of the structure. The second one is a closed structure
because an oponent piece is blocking one side of the sturcture, but can still grow
into a four in a row on the other side. The last one is dead because on one side an
oponent's piece is blocking and on the other side it is facing a boundary.

For each of these existing structures, a weight is given depending on how many pieces 
in a row (For example, 2 points are awarded for each existing 2 in a row structure, 3
points are awarded for eaach existing 3 in a row structure, etc;). Then, it is given 
a multiplier bonus depending on whether it is open, closed, or dead. An open structure
gets a 2x bonus multiplier, a closed structure gets a 1x multiplier, and a dead structure
gets 0x multiplier. 

The scores are summed up for each team, and the final score is calculated by subtracting
the points of the player team by the points of the enemy team. This allows the AI to 
take into account both offensive and defensive moves.

TERMINAL CONDITION
The terminal condition is determined when a 5-in-a-row structure is detected. A score of 
1000000 will be assigned, which will allow the minimax algorithm to identify as the terminal
condition (and thus, proceed accordingly).

SPECIAL CASES
The strength of the program lies in the ability to detect positions that are 'forced wins', 
positions that are not terminal conditions but will put us in a state that will by forced
lead us to one. For example, an Open-4-in-a-row state, where the opponent is not able to make
any instant win, is a forced win state. 

DISCUSSION

DEPTH OF 2
Though we intended to use iterative deepening, it turns out that there were too many problems,
and we ended up using a minimax algorithm with depth of 2 in order to stay under the tine limit.
Unfortunately, this limits the strength of our program

FURTHER HEURISTICS FOR CUTTING DOWN
By identifying the positions that will lead to forced wins, we can use this information to further
prune the minimax tree, which allows us to search faster.
 

***
___
