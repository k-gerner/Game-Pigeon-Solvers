# Kyle Gerner
# Started 7.15.22
# Contains AI strategy and board manipulation methods
import math
from othello.othello_player import OthelloPlayer
from functools import cmp_to_key
from collections import defaultdict

# String representations of the board pieces
BLACK = "0"
WHITE = "O"
EMPTY = "."

##### MODIFIABLE #####
BOARD_DIMENSION = 8                 # Range: 4 to 26
MAX_DEPTH = 7                       # Recommended: 5 to 8
MAX_VALID_MOVES_TO_EVALUATE = 20    # Recommended: 12 to 20
######################

WIN_SCORE = 1000000000
CORNER_COORDINATES = {(0, 0), (0, BOARD_DIMENSION - 1), (BOARD_DIMENSION - 1, 0),
                      (BOARD_DIMENSION - 1, BOARD_DIMENSION - 1)}
CORNER_ADJACENT_COORDINATES = {(0, 1), (1, 1), (1, 0),
                               (0, BOARD_DIMENSION - 2), (1, BOARD_DIMENSION - 2), (1, BOARD_DIMENSION - 1),
                               (BOARD_DIMENSION - 2, 0), (BOARD_DIMENSION - 2, 1), (BOARD_DIMENSION - 1, 1),
                               (BOARD_DIMENSION - 1, BOARD_DIMENSION - 2),
                               (BOARD_DIMENSION - 2, BOARD_DIMENSION - 2),
                               (BOARD_DIMENSION - 2, BOARD_DIMENSION - 1)}


class OthelloStrategy(OthelloPlayer):
    """Where all the calculations are performed to find the best move"""

    def __init__(self, color):
        super().__init__(color)
        self.aiColor = color
        self.enemyColor = opponentOf(color)
        self.movesPlayed = 0
        self.numBoardsEvaluated = 0
        self.positionsScores = {}
        self.buildPositionScoresDictionary()

    def buildPositionScoresDictionary(self):
        """Builds the dictionary that maps coordinate positions to scores"""
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                positionScore = evaluatePosition(row, col)
                self.positionsScores[(row, col)] = positionScore

    def getMove(self, board):
        """Gets the best move for the AI on the given board"""
        self.movesPlayed = BOARD_DIMENSION**2 - numberOfPieceOnBoard(EMPTY, board)
        self.numBoardsEvaluated = 0
        row, col = self.minimax(self.aiColor, -math.inf, math.inf, 0, board)[:2]
        return  row, col

    def minimax(self, turn, alpha, beta, depth, board, noMoveForOpponent=False):
        """Recursively searches the move tree to find the best move. Prunes when optimal."""
        if depth == MAX_DEPTH or depth + self.movesPlayed == BOARD_DIMENSION ** 2:
            self.numBoardsEvaluated += 1
            return -1, -1, self.evaluateBoard(board, depth)
        validMoves = getValidMoves(turn, board)
        validMoves.sort(key=validMoveSortKey)
        if len(validMoves) > MAX_VALID_MOVES_TO_EVALUATE:
            # check a maximum of MAX_VALID_MOVES_TO_EVALUATE moves per board state
            validMoves = validMoves[:MAX_VALID_MOVES_TO_EVALUATE]
        if len(validMoves) == 0:
            if noMoveForOpponent:
                self.numBoardsEvaluated += 1
                return -1, -1, self.evaluateBoard(board, BOARD_DIMENSION**2 - self.movesPlayed)
            return self.minimax(opponentOf(turn), alpha, beta, depth, board, noMoveForOpponent=True)
        if turn == self.aiColor:
            # maximize
            highScore = -math.inf
            bestRow, bestCol = validMoves[0]
            for row, col in validMoves:
                boardCopy = copyOfBoard(board)  # possible bottleneck
                playMove(turn, row, col, boardCopy)
                _, __, score = self.minimax(opponentOf(turn), alpha, beta, depth + 1, boardCopy)
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
                boardCopy = copyOfBoard(board)  # possible bottleneck
                playMove(turn, row, col, boardCopy)
                _, __, score = self.minimax(opponentOf(turn), alpha, beta, depth + 1, boardCopy)
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
        spotsRemaining = BOARD_DIMENSION**2 - (additionalPiecesPlayed + self.movesPlayed)
        if spotsRemaining == 0:
            aiScore, humanScore = currentScore(self.aiColor, board)
            if aiScore > humanScore:
                return WIN_SCORE
            elif aiScore < humanScore:
                return -WIN_SCORE
            else:
                return 0


        scores = defaultdict(int)
        numOccurrences = defaultdict(int)
        for rowIndex in range(BOARD_DIMENSION):
            for colIndex in range(BOARD_DIMENSION):
                piece = board[rowIndex][colIndex]
                score = self.positionsScores[(rowIndex, colIndex)]
                scores[piece] += score
                numOccurrences[piece] += 1

        scores[self.aiColor] += evaluateBoardByFilledRows(board, self.aiColor)
        scores[self.enemyColor] += evaluateBoardByFilledRows(board, self.enemyColor)
        if spotsRemaining <= 15:
            scores[self.aiColor] *= (1 + (numOccurrences[self.aiColor]/(spotsRemaining*25)))
            scores[self.enemyColor] *= (1 + (numOccurrences[self.enemyColor]/(spotsRemaining*25)))
        return scores[self.aiColor] - scores[self.enemyColor]


def copyOfBoard(board):
    """Returns a copy of the given board"""
    return list(map(list, board))  # use numpy if this becomes bottleneck


def evaluatePosition(row, col):
    """Gets the score of a position on the board"""
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


def evaluateBoardByFilledRows(board, color):
    """
    Evaluates all the stretches of length BOARD_DIMENSION (rows, columns, and the two longest diagonals), as
    it is very beneficial to have long stretches of friendly pieces in the same row/column/diagonal
    """
    score = 0
    # evaluate each row to see if any of them are completely filled or almost completely filled
    for row in board:
        nonFriendlyCount = BOARD_DIMENSION - row.count(color)
        if nonFriendlyCount == 0:
            score += 17
        elif nonFriendlyCount == 1:
            score += 8

    # evaluate each column
    for colNum in range(BOARD_DIMENSION):
        nonFriendlyCount = 0
        for rowNum in range(BOARD_DIMENSION):
            if board[rowNum][colNum] != color:
                nonFriendlyCount+=1
                if nonFriendlyCount >= 2:
                    break
        if nonFriendlyCount == 0:
            score += 17
        elif nonFriendlyCount == 1:
            score += 8

    # evaluate top left to bottom right diagonal
    nonFriendlyCount = 0
    for index in range(BOARD_DIMENSION):
        if board[index][index] != color:
            nonFriendlyCount+=1
            if nonFriendlyCount >= 2:
                break
    if nonFriendlyCount == 0:
        score += 25
    elif nonFriendlyCount == 1:
        score += 16

    # evaluate top right to bottom left diagonal
    nonFriendlyCount = 0
    for index in range(BOARD_DIMENSION):
        if board[index][BOARD_DIMENSION - index - 1] != color:
            nonFriendlyCount+=1
            if nonFriendlyCount >= 2:
                break
    if nonFriendlyCount == 0:
        score += 25
    elif nonFriendlyCount == 1:
        score += 16

    return score


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


def pieceAt(row, col, board):
    """Gets the piece at the given coordinate"""
    return board[row][col]


def opponentOf(piece):
    """Gets the string representation of the opposing piece"""
    if piece == BLACK:
        return WHITE
    elif piece == WHITE:
        return BLACK
    else:
        raise ValueError(f"Invalid value passed to opponentOf({piece})")


def numberOfPieceOnBoard(piece, board):
    """Gets the number of the given piece that are on the board"""
    count = 0
    for row in board:
        count += row.count(piece)
    return count


def currentScore(userPiece, board):
    """Gets the score of the game, returning {userPiece}'s score in [0] and opposing score in [1]"""
    enemy = opponentOf(userPiece)
    score, enemyScore = 0, 0
    for row in board:
        for spot in row:
            if spot == userPiece:
                score += 1
            elif spot == enemy:
                enemyScore += 1
    return score, enemyScore


def isMoveInRange(row, col):
    """Checks if the given coordinates are in range of the board"""
    return 0 <= row < BOARD_DIMENSION and 0 <= col < BOARD_DIMENSION


def isMoveValid(piece, row, col, board, confirmedInRange=False):
    """Determines if a move is valid for the given color"""
    if not confirmedInRange and not isMoveInRange(row, col) or board[row][col] != EMPTY:
        return False
    for rowIncrement in [-1, 0, 1]:
        for colIncrement in [-1, 0, 1]:
            if rowIncrement == colIncrement == 0: continue
            rowToCheck = row + rowIncrement
            colToCheck = col + colIncrement
            seenEnemyPiece = False
            while isMoveInRange(rowToCheck, colToCheck) \
                    and board[rowToCheck][colToCheck] == opponentOf(piece):
                seenEnemyPiece = True
                rowToCheck += rowIncrement
                colToCheck += colIncrement
            if seenEnemyPiece and isMoveInRange(rowToCheck, colToCheck) \
                    and board[rowToCheck][colToCheck] == piece:
                return True
    return False


def hasValidMoves(piece, board):
    """Checks if the given color has any available moves"""
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if isMoveValid(piece, row, col, board, confirmedInRange=True):
                return True
    return False


def getValidMoves(piece, board):
    """Gets a list of coordinates [row ,col] of valid moves for the given color"""
    validMoves = []
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if isMoveValid(piece, row, col, board, confirmedInRange=True):
                validMoves.append([row, col])
    return validMoves


def playMove(piece, row, col, board):
    """Adds a piece to the board and flips all the captured pieces"""
    if isMoveInRange(row, col) and board[row][col] == EMPTY:
        board[row][col] = piece
        convertCapturedPieces(piece, row, col, board)
    else:
        raise ValueError(f"{piece} tried to play in invalid spot ({row}, {col})!")


def convertCapturedPieces(piece, row, col, board):
    """Converts the captured opposing pieces to the given color"""
    for rowIncrement in [-1, 0, 1]:
        for colIncrement in [-1, 0, 1]:
            if rowIncrement == colIncrement == 0: continue
            rowToEval = row + rowIncrement
            colToEval = col + colIncrement
            enemyPieceCoordinates = []
            while True:
                if not isMoveInRange(rowToEval, colToEval) or board[rowToEval][colToEval] == EMPTY:
                    enemyPieceCoordinates.clear()
                    break
                elif board[rowToEval][colToEval] == piece:
                    break
                enemyPieceCoordinates.append([rowToEval, colToEval])
                rowToEval += rowIncrement
                colToEval += colIncrement
            for r, c in enemyPieceCoordinates:
                board[r][c] = piece


def checkGameOver(board):
    """Checks if all spaces on the board are filled"""
    blackCount, whiteCount = 0, 0
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            piece = pieceAt(row, col, board)
            if piece == EMPTY:
                return False, None
            elif piece == BLACK:
                blackCount += 1
            else:
                whiteCount += 1

    if blackCount > whiteCount:
        return True, BLACK
    elif whiteCount > blackCount:
        return True, WHITE
    else:
        return True, None


# sets the sorting key for valid move comparisons
validMoveSortKey = cmp_to_key(validMovesComparator)
