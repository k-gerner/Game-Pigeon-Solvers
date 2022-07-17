# Kyle Gerner
# Started 7.15.22
# Contains AI strategy and board manipulation methods
import math
import RulesEvaluator as eval
from RulesEvaluator import EMPTY, BOARD_DIMENSION
from functools import cmp_to_key
from collections import defaultdict

MAX_DEPTH = 5
WIN_SCORE = 1000000000

CORNER_COORDINATES = {(0, 0), (0, BOARD_DIMENSION - 1), (BOARD_DIMENSION - 1, 0),
                      (BOARD_DIMENSION - 1, BOARD_DIMENSION - 1)}
CORNER_ADJACENT_COORDINATES = {(0, 1), (1, 1), (1, 0),
                               (0, BOARD_DIMENSION - 2), (1, BOARD_DIMENSION - 2), (1, BOARD_DIMENSION - 1),
                               (BOARD_DIMENSION - 2, 0), (BOARD_DIMENSION - 2, 1), (BOARD_DIMENSION - 1, 1),
                               (BOARD_DIMENSION - 1, BOARD_DIMENSION - 2),
                               (BOARD_DIMENSION - 2, BOARD_DIMENSION - 2),
                               (BOARD_DIMENSION - 2, BOARD_DIMENSION - 1)}


class OthelloStrategy:
    """Where all the calculations are performed to find the best move"""

    def __init__(self, aiColor, aiGoesFirst):
        self.aiColor = aiColor
        self.humanColor = eval.opponentOf(aiColor)
        self.movesPlayed = 0 if aiGoesFirst else 1

    def findBestMove(self, board):
        """Gets the best move for the AI on the given board"""
        self.movesPlayed = BOARD_DIMENSION**2 - eval.numberOfPieceOnBoard(EMPTY, board)
        return self.minimax(self.aiColor, -math.inf, math.inf, 0, board)[:2]

    def minimax(self, turn, alpha, beta, depth, board):
        if depth == MAX_DEPTH or depth + self.movesPlayed == BOARD_DIMENSION ** 2:
            return -1, -1, self.evaluateBoard(board, depth)
        validMoves = eval.getValidMoves(turn, board)
        validMoves.sort(key=validMoveSortKey)
        if len(validMoves) == 0:
            return self.minimax(eval.opponentOf(turn), alpha, beta, depth, board)
        if turn == self.aiColor:
            # maximize
            highScore = -math.inf
            bestRow, bestCol = validMoves[0]
            for row, col in validMoves:
                boardCopy = self.copyOfBoard(board)  # possible bottleneck
                eval.playMove(turn, row, col, boardCopy)
                _, __, score = self.minimax(eval.opponentOf(turn), alpha, beta, depth + 1, boardCopy)
                if score > highScore:
                    highScore = score
                    bestRow = row
                    bestCol = col
                alpha = max(alpha, highScore)
                if alpha >= beta:
                    break
            return bestRow, bestCol, highScore
        else:
            # minimize
            lowScore = math.inf
            bestRow, bestCol = validMoves[0]
            for row, col in validMoves:
                boardCopy = self.copyOfBoard(board)  # possible bottleneck
                eval.playMove(turn, row, col, boardCopy)
                _, __, score = self.minimax(eval.opponentOf(turn), alpha, beta, depth + 1, boardCopy)
                if score < lowScore:
                    lowScore = score
                    bestRow = row
                    bestCol = col
                beta = min(beta, lowScore)
                if beta <= alpha:
                    break
            return bestRow, bestCol, lowScore

    def evaluateBoard(self, board, additionalPiecesPlayed):
        """Assigns a value to the board state based on how good it is for the AI"""
        if additionalPiecesPlayed + self.movesPlayed == BOARD_DIMENSION ** 2:
            aiScore, humanScore = eval.currentScore(self.aiColor, board)
            if aiScore > humanScore:
                return WIN_SCORE
            elif aiScore < humanScore:
                return -WIN_SCORE
            else:
                return 0

        scores = defaultdict(int)
        for rowIndex in range(BOARD_DIMENSION):
            for colIndex in range(BOARD_DIMENSION):
                piece = board[rowIndex][colIndex]
                score = evaluatePosition(rowIndex, colIndex)
                scores[piece] += score

        return scores[self.aiColor] - scores[self.humanColor]


    def copyOfBoard(self, board):
        """Returns a copy of the given board"""
        return list(map(list, board))  # use numpy if this becomes bottleneck


def evaluatePosition(row, col):
    move = row, col
    if move in CORNER_COORDINATES:
        return 10
    elif move in CORNER_ADJACENT_COORDINATES:
        return -8
    elif row in [0, BOARD_DIMENSION - 1] or col in [0, BOARD_DIMENSION - 1]:
        # on outer border
        return 6
    elif row in [1, BOARD_DIMENSION - 2] or col in [1, BOARD_DIMENSION - 2]:
        # one space inside of outer border
        return -7
    else:
        return 0

def validMovesComparator(move1, move2):
    """
    Defines a way to sort two possible moves.
    Penalizes corner-adjacent moves
    Prioritizes corners first, then edge pieces (unless corner adjacent)
    """
    move1Score = evaluatePosition(move1[0], move1[1])
    move2Score = evaluatePosition(move2[0], move2[1])
    if move1Score > move2Score:
        return -1
    elif move1Score < move2Score:
        return 1
    else:
        return 0

validMoveSortKey = cmp_to_key(validMovesComparator)