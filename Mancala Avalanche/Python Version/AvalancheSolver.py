from AvalancheBoard import AvalancheBoard
from Player import Player

class AvalancheSolver(object):

    def __init__(self, board):
        self.board = board

    def copyBoard(self, boardToCopy):
        return AvalancheBoard(boardToCopy.pebblesList, boardToCopy.p1.copyPlayer(), boardToCopy.p2.copyPlayer(), boardToCopy.p1Turn)

    def makeMovesOnMoveset(self, moveList, board):
        prevScore = board.p1.score
        board.performMoveSet(moveList)
        return board.p1.score - prevScore

    def makeMove(self, index, board):
        prevScore = board.p1.score
        endedInBank = board.performMove(index)
        return board.p1.score - prevScore, endedInBank

    def findBestMove(self, board, currVal):
        indexOptions = self.getListOfNonZeroIndexes(board)
        if len(indexOptions) == 0:
            return currVal, []
        bestIncrease = -1
        bestIndex = indexOptions[0]
        bestMoveList = [0]
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


    def getListOfNonZeroIndexes(self, board):
        nonZeros = []
        for i in range(0, 6, 1):
            if board.pebblesList[i] != 0:
                nonZeros.append(i)
        return nonZeros

    def printBestMoveStatus(self, pointsGained, bestMoves):
        print("The max # of points you can score on this turn is %d in %d moves." % (pointsGained, len(bestMoves)))
        print("The move set is: " + str(self.increaseAllValuesInListByOne(bestMoves)))
        print("^ Notice: 1 corresponds to the first spot on your side, 6 corresponds to the last spot")

    def printBestMovesOneByOne(self, pointsGained, bestMoves):
        print("The max # of points you can score on this turn is %d in %d moves." % (pointsGained, len(bestMoves)))
        print("Notice: 1 corresponds to the first spot on your side, 6 corresponds to the last spot")
        print("Press enter each time to receive the next move. Press q to quit at any time.")
        l = self.increaseAllValuesInListByOne(bestMoves)
        count = 0
        for e in l:
            count += 1
            if input() == 'q':
                exit(0)
            print("#%d:  %d" % (count, e))


    def increaseAllValuesInListByOne(self, l):
        returnList = l.copy()
        for i in range(0, len(l), 1):
            returnList[i] += 1
        return returnList

