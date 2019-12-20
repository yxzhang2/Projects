from time import sleep
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE

        if uttt.checkWinner() == 1 and isMax:
            score = self.winnerMaxUtility
        if uttt.checkWinner() == -1 and not isMax:
            score = self.winnerMinUtility

        searchnum = 0
        preventionnum = 0
        if uttt.checkWinner() == 0 and isMax:

            for x in range(0, 7, 3):
                for y in range(0, 7, 3):

                    for i in range(3):  # rows
                        xnum = 0
                        onum = 0
                        for j in range(3):
                            if self.board[x + i][y + j] == 'X':
                                xnum += 1
                            if self.board[x + i][y + j] == 'O':
                                onum += 1
                        if xnum == 2 and onum == 0:
                            searchnum += 1
                        if xnum == 1 and onum == 2:
                            preventionnum += 1

                    for i in range(3):  # column
                        xnum = 0
                        onum = 0
                        for j in range(3):
                            if self.board[x + j][y + i] == 'X':
                                xnum += 1
                            if self.board[x + j][y + i] == 'O':
                                onum += 1
                        if xnum == 2 and onum == 0:
                            searchnum += 1
                        if xnum == 1 and onum == 2:
                            preventionnum += 1
                    xnum = 0
                    onum = 0
                    for i in range(3):  # diagonal (left to right)
                        if self.board[x + i][y + i] == 'X':
                            xnum += 1
                        if self.board[x + i][y + i] == 'O':
                            onum += 1
                    if xnum == 2 and onum == 0:
                        searchnum += 1
                    if xnum == 1 and onum == 2:
                        preventionnum += 1
                    xnum = 0
                    onum = 0
                    for i in range(3):
                        if self.board[x + i][y + 2 - i] == 'X':
                            xnum += 1
                        if self.board[x + i][y + 2 - i] == 'O':
                            onum += 1
                    if xnum == 2 and onum == 0:
                        searchnum += 1
                    if xnum == 1 and onum == 2:
                        preventionnum += 1

            score = self.twoInARowMaxUtility * searchnum + self.preventThreeInARowMaxUtility * preventionnum

        cornernum = 0
        if searchnum + preventionnum == 0 and isMax:
            for x in range(0, 7, 3):
                for y in range(0, 7, 3):
                    if self.board[x][y] == "X":
                        cornernum += 1
                    if self.board[x + 2][y + 2] == "X":
                        cornernum += 1
                    if self.board[x][y + 2] == "X":
                        cornernum += 1
                    if self.board[x + 2][y] == "X":
                        cornernum += 1
            score = self.cornerMaxUtility * cornernum

        ############################################

        if uttt.checkWinner() == 0 and not isMax:

            for x in range(0, 7, 3):
                for y in range(0, 7, 3):

                    for i in range(3):  # rows
                        xnum = 0
                        onum = 0
                        for j in range(3):
                            if self.board[x + i][y + j] == 'X':
                                xnum += 1
                            if self.board[x + i][y + j] == 'O':
                                onum += 1
                        if xnum == 0 and onum == 2:
                            searchnum += 1
                        if xnum == 2 and onum == 1:
                            preventionnum += 1

                    for i in range(3):  # column
                        xnum = 0
                        onum = 0
                        for j in range(3):
                            if self.board[x + j][y + i] == 'X':
                                xnum += 1
                            if self.board[x + j][y + i] == 'O':
                                onum += 1
                        if xnum == 0 and onum == 2:
                            searchnum += 1
                        if xnum == 2 and onum == 1:
                            preventionnum += 1

                    xnum = 0
                    onum = 0
                    for i in range(3):  # diagonal (left to right)
                        if self.board[x + i][y + i] == 'X':
                            xnum += 1
                        if self.board[x + i][y + i] == 'O':
                            onum += 1
                    if xnum == 0 and onum == 2:
                        searchnum += 1
                    if xnum == 2 and onum == 1:
                        preventionnum += 1

                    xnum = 0
                    onum = 0
                    for i in range(3):
                        if self.board[x + i][y + 2 - i] == 'X':
                            xnum += 1
                        if self.board[x + i][y + 2 - i] == 'O':
                            onum += 1
                    if xnum == 0 and onum == 2:
                        searchnum += 1
                    if xnum == 2 and onum == 1:
                        preventionnum += 1

                    score = self.twoInARowMinUtility * searchnum + self.preventThreeInARowMinUtility * preventionnum

        cornernum = 0
        if searchnum + preventionnum == 0 and not isMax:
            for x in range(0, 7, 3):
                for y in range(0, 7, 3):
                    if self.board[x][y] == "O":
                        cornernum += 1
                    if self.board[x + 2][y + 2] == "O":
                        cornernum += 1
                    if self.board[x][y + 2] == "O":
                        cornernum += 1
                    if self.board[x + 2][y] == "O":
                        cornernum += 1
            score = self.cornerMinUtility * cornernum
        return score


    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for x in range(9):
            for y in range(9):
                if self.board[x][y] == "_":
                    return True

        movesLeft = False
        return movesLeft

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        winner=0
        for x in range(0, 7, 3):
            for y in range(0, 7, 3):
                for i in range(3):  # rows
                    xnum = 0
                    onum = 0
                    for j in range(3):
                        if self.board[x + i][y + j] == 'X':
                            xnum += 1
                        if self.board[x + i][y + j] == 'O':
                            onum += 1
                    if xnum == 3:
                        winner = 1
                    if onum == 3:
                        winner = -1
                for i in range(3):  # column
                    xnum = 0
                    onum = 0
                    for j in range(3):
                        if self.board[x + j][y + i] == 'X':
                            xnum += 1
                        if self.board[x + j][y + i] == 'O':
                            onum += 1
                    if xnum == 3:
                        winner = 1
                    if onum == 3:
                        winner = -1
                xnum = 0
                onum = 0
                for i in range(3):  # diagonal (left to right)
                    if self.board[x + i][y + i] == 'X':
                        xnum += 1
                    if self.board[x + i][y + i] == 'O':
                        onum += 1
                if xnum == 3:
                    winner = 1
                if onum == 3:
                    winner = -1

                xnum = 0
                onum = 0
                for i in range(3):
                    if self.board[x + i][y + 2 - i] == 'X':
                        xnum += 1
                    if self.board[x + i][y + 2 - i] == 'O':
                        onum += 1
                if xnum == 3:
                    winner = 1
                if onum == -3:
                    winner = -1
        return winner

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        bestValue=0.0
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE

        bestValue = 0
        for i in range(3):
            for j in range(3):
                x = self.globalIdx[currBoardIdx] + i
                y = self.globalIdx[currBoardIdx] + j
                if self.board[x][y] == "_":


                    childbest = minimax(self,depth+1,i*3+j, not isMax)
                    if isMAx:
                        bestValue < child

        bestValue=0.0
        return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE

        if isMinimaxOffensive and isMinimaxDefensive:
            # minmax vs minmax

        if not isMinimaxOffensive and isMinimaxDefensive:
            # ab  vs minmax

        if isMinimaxOffensive and not isMinimaxDefensive:
            # minmax vs ab

        if not isMinimaxOffensive and not isMinimaxDefensive:
            # ab vs ab





        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()

    # for x in range(0,9,2):
    #     for y in range(0,9,3):
    #         uttt.board[x][y] = "X"
    #         uttt.board[y][x] = "O"
    # uttt.board[1][4] = "X"
    # uttt.board[0][5] = "O"
    #
    # uttt.board[0][0] = "X"
    #
    # print(uttt.board)
    # score = uttt.evaluatePredifined(True)


    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
