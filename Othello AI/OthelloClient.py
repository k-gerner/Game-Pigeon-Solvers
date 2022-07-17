# Kyle Gerner
# Started 7.15.22
# Othello AI, client facing
import os
from strategy import OthelloStrategy
import RulesEvaluator as eval
from RulesEvaluator import BLACK, WHITE, EMPTY, BOARD_DIMENSION

import random

# Escape sequences for terminal color output
GREEN_COLOR = '\033[92m'
RED_COLOR = '\033[91m'
NO_COLOR = '\033[0m'
HIGHLIGHT = '\u001b[48;5;238m'

# Miscellaneous
COLUMN_LABELS = list(map(chr, range(65, 65 + BOARD_DIMENSION)))


class GameRunner:
    """Handles overall gameplay"""

    def __init__(self):
        self.playerPiece = self.getPieceColorInput()
        self.enemyPiece = eval.opponentOf(self.playerPiece)
        self.board = [[EMPTY for _ in range(BOARD_DIMENSION)] for __ in range(BOARD_DIMENSION)]
        self.board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2 - 1] = BLACK
        self.board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2] = BLACK
        self.board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2] = WHITE
        self.board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2 - 1] = WHITE
        self.ai = OthelloStrategy(self.enemyPiece, self.enemyPiece == BLACK)

    def endGame(self, winner=None):
        """Ends the game"""
        textColor = GREEN_COLOR if winner == self.playerPiece else RED_COLOR
        colorName = self.nameOfPieceColor(winner)
        if winner:
            print(f"\n{textColor}{colorName}{NO_COLOR} wins!")
        else:
            print("\nThe game ended in a draw!")
        print("\nThanks for playing!")
        exit(0)

    def getUserCoordinateInput(self):
        """Gets a move input from the user"""
        coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
            COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
        while True:
            if coord == 'Q':
                self.endGame()
            elif coord == 'P':
                self.printBoard(eval.getValidMoves(self.playerPiece, self.board))
                print("Your available moves have been highlighted.")
                coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
            elif len(coord) == (2 if BOARD_DIMENSION < 10 else 3) and coord[0] in COLUMN_LABELS and \
                    int(coord[1]) in range(1, BOARD_DIMENSION + 1):
                row, col = int(coord[1]) - 1, COLUMN_LABELS.index(coord[0])
                if eval.isMoveValid(self.playerPiece, row, col, self.board):
                    return row, col
                elif eval.isMoveInRange(row, col) and eval.pieceAt(row, col, self.board) != EMPTY:
                    coord = input(
                        "That spot is already taken! Please choose a different spot:   ").strip().upper()
                else:
                    self.printBoard(eval.getValidMoves(self.playerPiece, self.board))
                    coord = input("Please choose one of the highlighted spaces:   ").strip().upper()
            else:
                coord = input("Please enter a valid move (A1 - %s%d):   " % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()

    def nameOfPieceColor(self, piece):
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

    def start(self):
        """Starts the game and handles all basic gameplay functionality"""
        turn = BLACK
        self.printBoard()
        while True:
            if eval.hasValidMoves(turn, self.board):
                if turn == self.playerPiece:
                    row, col = self.getUserCoordinateInput()
                    eval.playMove(turn, row, col, self.board)
                    self.printBoard([[row, col]])
                else:
                    userInput = input("Press enter for the AI to play.   ").strip().lower()
                    if userInput == 'q':
                        self.endGame()
                    elif userInput == 'p':
                        self.printBoard(eval.getValidMoves(turn, self.board))
                        input("AI's available moves have been highlighted. Press enter to continue.")
                    row, col = self.ai.findBestMove(self.board)
                    eval.playMove(turn, row, col, self.board)
                    self.printBoard([[row, col]])
                    print("The AI played in spot %s%d" % (COLUMN_LABELS[col], row + 1))
            else:
                print("%s has no valid moves this turn! %s will play again." % (
                    self.nameOfPieceColor(turn), self.nameOfPieceColor(eval.opponentOf(turn))))
            isOver, winner = eval.checkGameOver(self.board)
            if isOver:
                self.endGame(winner)
            turn = eval.opponentOf(turn)

    def printBoard(self, highlightedCoordinates=None):
        """Prints the gameBoard in a human-readable format"""
        if highlightedCoordinates is None:
            highlightedCoordinates = []
        print("\n\t    %s" % " ".join(COLUMN_LABELS))
        for rowNum in range(BOARD_DIMENSION):
            print("\t%d%s| " % (rowNum + 1, "" if rowNum > 8 else " "), end='')
            for colNum in range(BOARD_DIMENSION):
                piece = eval.pieceAt(rowNum, colNum, self.board)
                pieceColor = HIGHLIGHT if [rowNum, colNum] in highlightedCoordinates else ''
                pieceColor += self.textColorOf(piece)
                print(f"{pieceColor}%s{NO_COLOR} " % piece, end='')
            if rowNum == BOARD_DIMENSION // 2:
                print("   %d turns remain." % (eval.numberOfPieceOnBoard(EMPTY, self.board)), end='')
            print()
        userScore, aiScore = eval.currentScore(self.playerPiece, self.board)
        additionalIndent = " " * ((2 + (2 * (BOARD_DIMENSION // 2 - 1))) - (1 if userScore >= 10 else 0))
        print(f"\t{additionalIndent}{GREEN_COLOR}{userScore}{NO_COLOR} to {RED_COLOR}{aiScore}{NO_COLOR}\n")

    def getPieceColorInput(self):
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
    print("Type 'p' to show the available moves")
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
    game = GameRunner()
    game.start()


if __name__ == '__main__':
    main()
