# Gomoku
___
## Team Name: Large_Horse
#### Contributors: Bhon Bunnag, Malika Nurbekova, Yil Verdeja
___
## 1 Project Description and Goal
This project consists of developing and implementing a computer program that plays Gomoku. Also known as "five in-a-row", is a board game similar to tic-tac-toe but on a larger board. This project will exemplify the minimax algorithm and alpha-beta pruning.
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
The minimax implementation can be found within the *agent.py* class as a the function named *_______*. The following snippets on lines __ to __ shows the minimax implementation

```python

```



***
### 2.2 Alpha-Beta Pruning Implementation

```python

```

***
### 2.3 Heuristic Evaluation Function and Strategies

```python

```

***
### 2.4 Offensive and Defensive Behavior

***
### 2.5 Interaction with Referee


### 2.6 Program Testing
The *GomokuCollection* class is the class that controls the movement on the board and assigns evaluation scores to it. In order to proceed in using this class, it needed to be heavily tested. Using Test Driven Development (TDD), inside the *testCollection.py* class, the GomokuCollection was thouroughly examined to make sure that the code worked as expected.    

___
## 3 Problems Faced
In this section, all the bugs that have been encountered during the process of programming the Gomoku AI are listed below as well as how they were fixed.
***
### 3.1 Bugs

***
### 3.2 Fixes

___
