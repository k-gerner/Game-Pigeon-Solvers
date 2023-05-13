# Kyle Gerner    7.9.2020


# class that represents the Player (of which, there are 2)
class AvalanchePlayer(object):
    def __init__(self):
        self.score = 0
    def incrementScore(self):
        self.score += 1
    def copyPlayer(self):
        p = AvalanchePlayer()
        p.score = self.score
        return p

################################################################################################
################################################################################################
################################################################################################

BANK = 0
EMPTY_PIT = 1
PIT_WITH_PIECES = 2

# Class that represents the board object.
class AvalancheBoard(object):

    # constructor
    def __init__(self, pebblesInEach, player1, player2, playerOneTurn):
        self.pebblesList = pebblesInEach.copy()
        self.p1 = player1
        self.p2 = player2
        self.p1Turn = playerOneTurn

    # Performs the moves on the board by calling the performMove function for each move given
    def performMoveSet(self, moveList):
        continueMoves = True
        moveNumber = 1
        for boardSpot in moveList:
            if not continueMoves:
                print("Move #%d in the given move set was invalid (previous move did not end in player bank)" % moveNumber)
                print("The move set was:  " + str(moveList))
                break
            continueMoves = self.performMove(boardSpot)
            moveNumber += 1
        self.switchTurn()
        return self.p1.score, self.p2.score

    # Performs the move on the board
    def performMove(self, position):
        currBankIndex, enemyBankIndex = self.getBankIndexes()
        currPlayer = self.p1 if self.p1Turn else self.p2
        numPebbles = self.pebblesList[position]
        self.pebblesList[position] = 0
        turnEndedInPlayerBank = False
        while True:
            if numPebbles == 0:
                endOfMove = self.endOfCurrentMove(position, currBankIndex)
                # if (endOfMove[0]):
                if(endOfMove != PIT_WITH_PIECES):
                    # turnEndedInPlayerBank = endOfMove[1]
                    turnEndedInPlayerBank = True if endOfMove == BANK else False
                    break
                else:
                    numPebbles = self.pebblesList[position]
                    self.pebblesList[position] = 0
            position = (position + 1) % 14 if (position + 1) != enemyBankIndex else (position + 2) % 14
            self.addPebbleToLocation(position, currBankIndex, currPlayer)
            numPebbles -= 1
        return turnEndedInPlayerBank

    # checks which spot the last piece was placed
    def endOfCurrentMove(self, pos, currBankIndex):
        # note if this method is called, we already know numPebbles = 0
        if pos == currBankIndex:
            return BANK
        elif self.pebblesList[pos] == 1:
            return EMPTY_PIT
        else:
            return PIT_WITH_PIECES

    # places a piece in the specified spot, and increments score if applicable
    def addPebbleToLocation(self, index, currBankIndex, currPlayer):
        self.pebblesList[index] += 1
        if index == currBankIndex:
            currPlayer.incrementScore()

    # get the player and opponent bank indexes
    def getBankIndexes(self):
        if self.p1Turn:
            return 6,13
        else:
            return 13,6

    # prints the board in a horizontal fashion
    def printBoardHorizontal(self):
        # E  |12 |11 |10 | 9 | 8 | 7 |
        #13  -------------------------  6
        #    | 0 | 1 | 2 | 3 | 4 | 5 |  P
        #     Enemy winning 13 to 6
        if self.p2.score == self.p1.score:
            scoreStr = "\t  The score is tied at %d\n" % self.p2.score
        else:
            if self.p2.score > self.p1.score:
                scoreStr = "\t  Enemy winning %d to %d\n" % (self.p2.score, self.p1.score)
            else:
                scoreStr = "\t  You're winning %d to %d\n" % (self.p1.score, self.p2.score)
        print(str(self) + scoreStr)

    # string representation of the board
    def __str__(self):
        enemyRow = "E\t|" + self.scoreRowToStrHoriz(12, 6, -1) + "\n"
        bankRow = "%d\t-------------------------\t%d\n" % (self.p2.score, self.p1.score)
        playerRow = "\t|" + self.scoreRowToStrHoriz(0, 6, 1) + "\tP\n"
        return enemyRow + bankRow + playerRow

    # string representation of one side of the board
    def scoreRowToStrHoriz(self, start, end, direction):
        scoresStr = ""
        for i in range(start, end, direction): # loop thru indexes of side
            thisSpotStr = "%d |" % self.pebblesList[i]
            if self.pebblesList[i] < 10:
                thisSpotStr = " " + thisSpotStr
            scoresStr += thisSpotStr
        return scoresStr

    # switches whose turn it is
    def switchTurn(self):
        self.p1Turn = not self.p1Turn

################################################################################################
################################################################################################
################################################################################################

# Class that contains the methods that calculate the best moves for a given board
class AvalancheSolver(object):

    # constructor
    def __init__(self, board):
        self.board = board

    # Returns a copy of the game board
    def copyBoard(self, boardToCopy):
        return AvalancheBoard(boardToCopy.pebblesList, boardToCopy.p1.copyPlayer(), boardToCopy.p2.copyPlayer(), boardToCopy.p1Turn)

    # Performs the moves of a given moveset on the given board
    def makeMovesOnMoveset(self, moveList, board):
        prevScore = board.p1.score
        board.performMoveSet(moveList)
        return board.p1.score - prevScore

    # Perform a single move on a given board
    # returns the score for this turn, and whether or not the turn ended in the player's bank
    def makeMove(self, index, board):
        prevScore = board.p1.score
        endedInBank = board.performMove(index)
        return board.p1.score - prevScore, endedInBank

    # Recursive method that finds the best move for the player for a given board
    # returns the points gained from a moveset, and the moveset list
    def findBestMove(self, board, currVal):
        indexOptions = self.getListOfNonZeroIndexes(board)
        if len(indexOptions) == 0:
            # if no available moves
            return currVal, []
        bestIncrease = -1
        bestIndex = indexOptions[0]
        bestMoveList = [0]
        # loop through each available move
        for index in indexOptions:
            thisRunIncrease = 0
            thisMoveList = []
            boardCopy = self.copyBoard(board)
            makeMoveResults = self.makeMove(index, boardCopy)
            pointsGained, endedInBank = makeMoveResults[0], makeMoveResults[1]
            if endedInBank:
                thisRunIncrease, thisMoveList = self.findBestMove(boardCopy, pointsGained)
            else:
                thisRunIncrease = pointsGained
            if thisRunIncrease > bestIncrease:
                bestIncrease = thisRunIncrease
                bestIndex = index
                bestMoveList = thisMoveList.copy()
                bestMoveList.insert(0, bestIndex)
        return bestIncrease + currVal, bestMoveList

    # get a list of the indexes that have pieces in them (and therefore are available to be played)
    def getListOfNonZeroIndexes(self, board):
        nonZeros = []
        for i in range(0, 6, 1):
            if board.pebblesList[i] != 0:
                nonZeros.append(i)
        return nonZeros
