# Contains AI strategy
import math # for infinities
import random # for randomizing valid moves list in minimax
from constants import *
from board_functions import *
from Player import Player # super class

MAX_DEPTH = 10 # max number of moves ahead to calculate
MAX, MIN = True, False # to be used in minimax

# class for the A.I.
class Strategy(Player):

    def __init__(self, bankIndex=13):
        super().__init__(bankIndex)
        self.opponentBankIndex = (bankIndex + POCKETS_PER_SIDE + 1) % BOARD_SIZE
        self.totalPebbles = -1


    def getMove(self, board):
        """Calculates the best move for the AI for the given board"""
        self.totalPebbles = sum(board)
        move, score = -123, -123 # placeholders
        for i in range(1, MAX_DEPTH + 1): # iterative deepening
            # this will prioritize game winning move sequences that finish in less moves
            move, score = self.minimax(board, 0, MAX, -math.inf, math.inf, i)
            if score > 900:
                break
        return move


    def scoreBoard(self, board):
        """Scores the board"""
        playerBankScore = board[self.bankIndex]
        opponentBankScore = board[self.opponentBankIndex]
        if playerBankScore > TOTAL_PEBBLES / 2:
            playerBankScore += 1000
        elif opponentBankScore > TOTAL_PEBBLES / 2:
            opponentBankScore += 1000
        playerPockets = board[self.bankIndex - POCKETS_PER_SIDE : self.bankIndex]
        opponentPockets = board[self.opponentBankIndex - POCKETS_PER_SIDE : self.opponentBankIndex]
        playerScore = playerBankScore + scorePockets(playerPockets)
        opponentScore = opponentBankScore + scorePockets(opponentPockets)
        return playerScore - opponentScore
        # pebblesInPlay = sum(board[bankIndex - 6 : bankIndex])


    def minimax(self, board, depth, maxOrMin, alpha, beta, localMaxDepth):
        """
        Recursively finds the best move for a given board
        Returns the move index in [0] and score of the board in [1]
        """
        # random.shuffle(validMoves)
        if isBoardTerminal(board):
            pushAllPebblesToBank(board)
            winningBankIndex = winningPlayerBankIndex(board)
            if winningBankIndex == self.bankIndex:
                return None, 2000
            elif winningBankIndex is None:
                return None, 0
            else:
                return None, -2000
        if depth == localMaxDepth:
            return None, self.scoreBoard(board)
        if maxOrMin == MAX:
            # want to maximize this move
            validMoves = getValidMoves(board, self.bankIndex)
            score = -math.inf
            bestMove = validMoves[0] # default best move
            for move in validMoves:
                boardCopy = board.copy()
                performMove(boardCopy, move, self.bankIndex)
                _, updatedScore = self.minimax(boardCopy, depth + 1, MIN, alpha, beta, localMaxDepth)
                if updatedScore > score:
                    score = updatedScore
                    bestMove = move
                alpha = max(alpha, score)
                if alpha >= beta:
                    break # pruning
            return bestMove, score
        else:
            # want to minimize this move
            validMoves = getValidMoves(board, self.opponentBankIndex)
            score = math.inf
            bestMoveForOpponent = validMoves[0]
            for move in validMoves:
                boardCopy = board.copy()
                performMove(boardCopy, move, self.opponentBankIndex)
                _, updatedScore = self.minimax(boardCopy, depth + 1, MAX, alpha, beta, localMaxDepth)
                if updatedScore < score:
                    score = updatedScore
                    bestMoveForOpponent = move
                beta = min(beta, score)
                if beta <= alpha:
                    break # pruning
            return bestMoveForOpponent, score


def scorePockets(pockets):
    """Assigns a score for the given pocket layout. Favors pebbles further away from player bank"""
    score = 0
    multiplier = 0.3
    stepDown = (multiplier - 0.1) / POCKETS_PER_SIDE
    for pebbles in pockets:
        score += pebbles * multiplier
        multiplier -= stepDown
    return score




