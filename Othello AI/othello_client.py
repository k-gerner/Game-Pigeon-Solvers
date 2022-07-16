# Kyle Gerner
# Started 3.18.21
# Othello AI, client facing
import os
from enum import Enum
from strategy import OthelloStrategy

# String representations of the board pieces
BLACK = "0"
WHITE = "O"
EMPTY = "."

# Escape sequences for terminal color output
GREEN_COLOR = '\033[92m'
RED_COLOR = '\033[91m'
NO_COLOR = '\033[0m'
HIGHLIGHT = '\u001b[48;5;238m'

# Miscellaneous
BOARD_DIMENSION = 8
COLUMN_LABELS = list(map(chr, range(65, 65 + BOARD_DIMENSION)))


class GameRunner():
    """Handles overall gameplay"""

    def __init__(self, playerPiece):
        self.playerPiece = playerPiece
        self.enemyPiece = self.opponentOf(playerPiece)
        self.board = [[EMPTY for col in range(BOARD_DIMENSION)] for row in range(BOARD_DIMENSION)]
        self.board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2 - 1] = BLACK
        self.board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2] = BLACK
        self.board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2] = WHITE
        self.board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2 - 1] = WHITE
        self.gameOver = False
        self.ai = OthelloStrategy()

    def endGame(self, winner=None):
        """Ends the game"""
        textColor = GREEN_COLOR if winner == self.playerPiece else RED_COLOR
        colorName = self.nameOfColor(winner)
        if winner:
            print(f"\n{textColor}{colorName}{NO_COLOR} wins!")
        else:
            print("\nThe game ended in a draw!")
        print("\nThanks for playing!")
        exit(0)

    def hasValidMoves(self, piece):
        """Checks if the given color has any available moves"""
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                if self.isMoveValid(piece, row, col):
                    return True
        return False

    def getValidMoves(self, piece):
        """Gets a list of coordinates [row ,col] of valid moves for the given color"""
        validMoves = []
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                if self.isMoveValid(piece, row, col):
                    validMoves.append([row, col])
        return validMoves

    def isMoveInRange(self, row, col):
        """Checks if the given coordinates are in range of the board"""
        return row in range(0, BOARD_DIMENSION) and col in range(0, BOARD_DIMENSION)

    def isMoveValid(self, piece, row, col):
        """Determines if a move is valid for the given color"""
        if not self.isMoveInRange(row, col) or self.pieceAt(row, col) != EMPTY:
            return False
        for rowIncrement in [-1, 0, 1]:
            for colIncrement in [-1, 0, 1]:
                if rowIncrement == colIncrement == 0: continue
                rowToCheck = row + rowIncrement
                colToCheck = col + colIncrement
                seenEnemyPiece = False
                while self.isMoveInRange(rowToCheck, colToCheck) \
                        and self.pieceAt(rowToCheck, colToCheck) == self.opponentOf(piece):
                    seenEnemyPiece = True
                    rowToCheck += rowIncrement
                    colToCheck += colIncrement
                if seenEnemyPiece and self.isMoveInRange(rowToCheck, colToCheck) \
                        and self.pieceAt(rowToCheck, colToCheck) == piece:
                    return True
        return False

    def userInputLocation(self):
        """Gets a move input from the user"""
        coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
            COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
        while True:
            if coord == 'Q':
                self.endGame()
            elif coord == 'P':
                self.printBoard(self.getValidMoves(self.playerPiece))
                print("Your available moves have been highlighted.")
                coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
            elif len(coord) == (2 if BOARD_DIMENSION < 10 else 3) and coord[0] in COLUMN_LABELS and \
                    int(coord[1]) in range(1, BOARD_DIMENSION + 1):
                row, col = int(coord[1]) - 1, COLUMN_LABELS.index(coord[0])
                if self.isMoveValid(self.playerPiece, row, col):
                    return int(coord[1]) - 1, COLUMN_LABELS.index(coord[0].upper())
                elif self.isMoveInRange(row, col) and self.pieceAt(row, col) != EMPTY:
                    coord = input(
                        "That spot is already taken! Please choose a different spot:   ").strip().upper()
                else:
                    self.printBoard(self.getValidMoves(self.playerPiece))
                    coord = input("Please choose one of the highlighted spaces:   ").strip().upper()
            else:
                coord = input("Please enter a valid move (A1 - %s%d):   " % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()

    def nameOfColor(self, piece):
        """Gets the name of the color of the given piece"""
        if piece == BLACK:
            return "BLACK"
        elif piece == WHITE:
            return "WHITE"
        else:
            return "EMPTY"

    def textColorOf(self, piece):
        """Gets the text color of the given piece, or an empty string if no piece given"""
        if piece == self.playerPiece:
            return GREEN_COLOR
        elif piece == self.enemyPiece:
            return RED_COLOR
        else:
            return ""

    def pieceAt(self, row, col):
        """Gets the piece at the given coordinate"""
        return self.board[row][col]

    def checkGameOver(self):
        """Ends the game if all spaces are filled"""
        # do stuff to evaluate board
        # if no winner then just return out
        blackCount, whiteCount = 0, 0
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                piece = self.pieceAt(row, col)
                if piece == EMPTY:
                    return
                elif piece == BLACK:
                    blackCount += 1
                else:
                    whiteCount += 1
        if blackCount > whiteCount:
            self.endGame(BLACK)
        elif whiteCount > blackCount:
            self.endGame(WHITE)
        else:
            self.endGame()

    def start(self):
        """Starts the game and handles all basic gameplay functionality"""
        turn = BLACK
        self.printBoard()
        while not self.gameOver:
            if self.hasValidMoves(turn):
                if turn == self.playerPiece:
                    row, col = self.userInputLocation()
                    self.playMove(turn, row, col)
                    self.printBoard([row, col])
                else:
                    if input("Press enter for the AI to play.   ").strip().lower() == 'q':
                        self.endGame()
                    # row, col = self.ai.findBestMove(self.board)
                    row, col = self.userInputLocation()
                    self.playMove(turn, row, col)
                    self.printBoard([row, col])
                    print("The AI played in spot %s%d" % (COLUMN_LABELS[col], row + 1))
            else:
                print("%s has no valid moves this turn! %s will play again." % (
                    self.nameOfColor(turn), self.nameOfColor(self.opponentOf(turn))))
            self.checkGameOver()
            turn = self.opponentOf(turn)

    def printBoard(self, highlightedCoordinates=None):
        """Prints the gameBoard in a human-readable format"""
        if highlightedCoordinates is None:
            highlightedCoordinates = []
        print("\n\t    %s" % " ".join(COLUMN_LABELS))
        for rowNum in range(BOARD_DIMENSION):
            print("\t%d%s| " % (rowNum + 1, "" if rowNum > 8 else " "), end='')
            for colNum in range(BOARD_DIMENSION):
                piece = self.pieceAt(rowNum, colNum)
                pieceColor = HIGHLIGHT if [rowNum, colNum] in highlightedCoordinates else ''
                pieceColor += self.textColorOf(piece)
                print(f"{pieceColor}%s{NO_COLOR} " % piece, end='')
            print()
        print()

    def playMove(self, piece, row, col):
        """Adds a piece to the board and flips all the captured pieces"""
        if self.board[row][col] == EMPTY:
            self.board[row][col] = piece
            self.convertCapturedPieces(piece, row, col)
        else:
            raise ValueError(
                f"{self.nameOfColor(piece)} tried to play in spot ({row + 1}, {col + 1}), but it's already full!")

    def convertCapturedPieces(self, piece, row, col):
        """Converts the captured opposing pieces to the given color"""
        for rowIncrement in [-1, 0, 1]:
            for colIncrement in [-1, 0, 1]:
                if rowIncrement == colIncrement == 0: continue
                rowToEval = row + rowIncrement
                colToEval = col + colIncrement
                enemyPieceCoordinates = []
                while True:
                    if not self.isMoveInRange(rowToEval, colToEval) \
                            or self.pieceAt(rowToEval, colToEval) == EMPTY:
                        enemyPieceCoordinates.clear()
                        break
                    elif self.pieceAt(rowToEval, colToEval) == piece:
                        break
                    enemyPieceCoordinates.append([rowToEval, colToEval])
                    rowToEval += rowIncrement
                    colToEval += colIncrement
                for r, c in enemyPieceCoordinates:
                    self.board[r][c] = piece

    def opponentOf(self, piece):
        """Gets the string representation of the opposing piece"""
        if piece == BLACK:
            return WHITE
        elif piece == WHITE:
            return BLACK
        else:
            raise ValueError("Invalid value passed to opponentOf(piece)")


def getPieceColorInput():
    """Gets input from the user to determine which color they will be"""
    color_input = input("Would you like to be BLACK ('b') or WHITE ('w')?   ").strip().lower()
    color = BLACK if color_input == 'b' else WHITE
    if color == BLACK:
        print(f"You will be BLACK {GREEN_COLOR}{BLACK}{NO_COLOR}!")
    else:
        print(f"You will be WHITE {GREEN_COLOR}{WHITE}{NO_COLOR}!")
    print(f"Your pieces are shown in {GREEN_COLOR}green{NO_COLOR}!")
    print(f"Enemy pieces are shown in {RED_COLOR}red{NO_COLOR}!")
    return color


def printGameRules():
    """Gives the user the option to view the rules of the game"""
    print("\nType 'q' at any move prompt to quit the game.")
    print("Type 'p' when it is your turn to show your available moves")
    showRules = input("Would you like to see the rules? (y/n)   ").strip().lower()
    if showRules == 'q':
        print("\nThanks for playing!")
        exit(0)
    elif showRules == 'y':
        print("""\n
        - OBJECTIVE: Have more pieces on the board than the opponent when all spaces are full
        - TURNS: Black will go first. Each player will take turns placing one piece each turn
        - GAMEPLAY: Trap enemy pieces between two friendly pieces to convert them to friendly pieces
        """)


def main():
    """Prompts user for input and creates a new GameRunner"""
    os.system("")  # allows output coloring for Windows OS
    print("Welcome to Kyle's Othello AI!")
    printGameRules()
    playerPiece = getPieceColorInput()
    game = GameRunner(playerPiece)
    game.start()


if __name__ == '__main__':
    main()
