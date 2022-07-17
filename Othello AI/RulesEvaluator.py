# Kyle Gerner
# Started 7.15.22

# String representations of the board pieces
BLACK = "0"
WHITE = "O"
EMPTY = "."

# Width / height of the board
BOARD_DIMENSION = 8


# Contains functions that return data about the state of a board

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
    return row in range(0, BOARD_DIMENSION) and col in range(0, BOARD_DIMENSION)


def isMoveValid(piece, row, col, board):
    """Determines if a move is valid for the given color"""
    if not isMoveInRange(row, col) or board[row][col] != EMPTY:
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
            if isMoveValid(piece, row, col, board):
                return True
    return False

def getValidMoves(piece, board):
    """Gets a list of coordinates [row ,col] of valid moves for the given color"""
    validMoves = []
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if isMoveValid(piece, row, col, board):
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
