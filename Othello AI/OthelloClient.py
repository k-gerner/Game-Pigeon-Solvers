# Kyle Gerner
# Started 7.15.22
# Othello AI, client facing
import os
import sys
import time
from importlib import import_module
from datetime import datetime

from strategy import OthelloStrategy, copyOfBoard, BOARD_DIMENSION, getValidMoves, opponentOf, playMove, \
    currentScore, checkGameOver, numberOfPieceOnBoard, pieceAt, hasValidMoves, isMoveValid, isMoveInRange
from Player import Player

BLACK = "0"
WHITE = "O"
EMPTY = "."

# Escape sequences for terminal color output
GREEN_COLOR = '\033[92m'
RED_COLOR = '\033[91m'
BLUE_COLOR = '\033[38;5;39m'
ORANGE_COLOR = '\033[38;5;208m'
NO_COLOR = '\033[0m'
HIGHLIGHT = '\033[48;5;238m'

CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'

# Miscellaneous
COLUMN_LABELS = list(map(chr, range(65, 65 + BOARD_DIMENSION)))
AI_DUEL_MODE = False
BOARD_OUTLINE_HEIGHT = 4
SAVE_STATE_OUTPUT_HEIGHT = BOARD_DIMENSION + 6
ERASE_MODE_ON = True
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"
INFO_SYMBOL = f"{BLUE_COLOR}<!>{NO_COLOR}"
SAVE_FILENAME = "saved_game.txt"

# class for the Human player
class HumanPlayer(Player):

    def __init__(self, color):
        super().__init__(color, isAI=False)

    def getMove(self, board):
        """Takes in the user's input and returns the move"""
        # TODO: refactor logic so that user input is in this class instead of GameRunner
        pass

class GameRunner:
    """Handles overall gameplay"""

    def __init__(self, UserPlayerClass, OpponentPlayerClass):
        useSavedGame = False
        if os.path.exists(SAVE_FILENAME):
            self.board, self.userPiece, self.turn = loadSavedGame()
            if self.turn is not None:
                useSavedGame = True
        if not useSavedGame:
            self.userPiece = getPieceColorInput()
            self.board = [[EMPTY for _ in range(BOARD_DIMENSION)] for __ in range(BOARD_DIMENSION)]
            self.board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2 - 1] = WHITE
            self.board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2] = WHITE
            self.board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2] = BLACK
            self.board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2 - 1] = BLACK
            self.turn = BLACK
        self.opponentPiece = opponentOf(self.userPiece)
        userPlayerName = "Your AI" if AI_DUEL_MODE else "You"
        aiPlayerName = "My AI" if AI_DUEL_MODE else "AI"
        self.playerNames = {self.userPiece: userPlayerName, self.opponentPiece: aiPlayerName}
        self.players = {
            self.opponentPiece: OpponentPlayerClass(self.opponentPiece),
            self.userPiece: UserPlayerClass(self.userPiece)
        }
        self.boardHistory = [[[], copyOfBoard(self.board)]] # [0]: highlighted coordinates  [1]: game board
        self.linesWrittenToConsole = 0

    def endGame(self, winner=None):
        """Ends the game"""
        textColor = self.textColorOf(winner)
        colorName = nameOfPieceColor(winner)
        if winner:
            print(f"\n{textColor}{colorName}{NO_COLOR} wins!")
        else:
            print("\nThe game ended in a draw!")
        print("\nThanks for playing!")
        exit(0)


    def getNextMove(self, player):
        """Gets a move input from the user"""
        if player.isAI:
            return player.getMove(self.board)
        coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
            COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
        self.linesWrittenToConsole = BOARD_DIMENSION + 7
        while True:
            if coord == 'Q':
                self.endGame()
            elif coord == 'S':
                erasePreviousLines(self.linesWrittenToConsole)
                self.saveGame(self.board, self.userPiece)
                coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
                erasePreviousLines(2)
                self.linesWrittenToConsole = SAVE_STATE_OUTPUT_HEIGHT + 3
            elif coord == 'QS' or coord == 'SQ':
                self.saveGame(self.board, self.userPiece)
                self.endGame()
            elif coord == 'H':
                if len(self.boardHistory) < 2:
                    coord = input("No previous moves to see. Enter a valid move to play:   ").strip().upper()
                    self.linesWrittenToConsole += 1
                else:
                    numMovesPrevious = input(f"How many moves ago do you want to see? (1 to {len(self.boardHistory) - 1})  ").strip()
                    self.linesWrittenToConsole += 1
                    if numMovesPrevious.isdigit() and 1 <= int(numMovesPrevious) <= len(self.boardHistory):
                        erasePreviousLines(self.linesWrittenToConsole)
                        self.printMoveHistory(int(numMovesPrevious))
                        erasePreviousLines(BOARD_DIMENSION + BOARD_OUTLINE_HEIGHT)
                        self.printBoard(getValidMoves(self.userPiece, self.board))
                        coord = input(f"{INFO_SYMBOL} You're back in play mode. Which spot would you like to play?   ").strip().upper()
                        self.linesWrittenToConsole = BOARD_DIMENSION + BOARD_OUTLINE_HEIGHT + 1
                    else:
                        coord = input(f"{ERROR_SYMBOL} Invalid input. Enter a valid move to play:   ").strip().upper()
            elif len(coord) in ([2] if BOARD_DIMENSION < 10 else [2, 3]) and coord[0] in COLUMN_LABELS and \
                    coord[1:].isdigit() and int(coord[1:]) in range(1, BOARD_DIMENSION + 1):
                row, col = int(coord[1]) - 1, COLUMN_LABELS.index(coord[0])
                if isMoveValid(self.userPiece, row, col, self.board):
                    return row, col
                elif isMoveInRange(row, col) and pieceAt(row, col, self.board) != EMPTY:
                    erasePreviousLines(1)
                    coord = input(
                        f"{ERROR_SYMBOL} That spot is already taken! Please choose a different spot:   ").strip().upper()
                else:
                    erasePreviousLines(self.linesWrittenToConsole)
                    self.printBoard(getValidMoves(self.userPiece, self.board))
                    coord = input(f"{ERROR_SYMBOL} Please choose one of the highlighted spaces:   ").strip().upper()
                    self.linesWrittenToConsole = BOARD_DIMENSION + BOARD_OUTLINE_HEIGHT + 1
            else:
                erasePreviousLines(1)
                coord = input(f"{ERROR_SYMBOL} Please enter a valid move (A1 - %s%d):   " % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()


    def textColorOf(self, piece):
        """Gets the text color of the given piece, or an empty string if no piece given"""
        if piece == self.userPiece:
            return GREEN_COLOR
        elif piece == self.opponentPiece:
            return RED_COLOR
        else:
            return ""


    def start(self):
        """Starts the game and handles all basic gameplay functionality"""
        self.printBoard(getValidMoves(self.turn, self.board))
        print("\n")
        numValidMovesInARow = 0
        gameOver, winner = False, None
        while not gameOver:
            self.linesWrittenToConsole = BOARD_DIMENSION + 6
            if hasValidMoves(self.turn, self.board):
                numValidMovesInARow = 0
                nameOfCurrentPlayer = self.playerNames[self.turn]
                currentPlayer = self.players[self.turn]
                if currentPlayer.isAI:
                    userInput = input(f"{nameOfCurrentPlayer}'s turn, press enter for it to play.\t").strip().lower()
                    erasePreviousLines(1)
                    while userInput in ['q', 's', 'qs', 'sq']:
                        if userInput == 'q':
                            self.endGame()
                        elif userInput == 's':
                            self.saveGame(self.board, self.turn)
                            userInput = input("Press enter to continue. ").strip().lower()
                            erasePreviousLines(2)
                        elif userInput == 'qs' or userInput == 'sq':
                            self.saveGame(self.board, self.turn)
                            self.endGame()
                startTime = time.time()
                row, col = self.getNextMove(currentPlayer)
                endTime = time.time()
                timeToPlayMove = round(endTime - startTime, 2)
                playMove(self.turn, row, col, self.board)
                self.boardHistory.append([[row, col], copyOfBoard(self.board)])
                erasePreviousLines(self.linesWrittenToConsole)
                self.printBoard([[row, col]] + getValidMoves(opponentOf(self.turn), self.board))
                if currentPlayer.isAI:
                    additionalOutput = "  (%0.2f sec" % timeToPlayMove
                    if hasattr(currentPlayer, 'numBoardsEvaluated'):
                        additionalOutput += ", %d possible futures)" % currentPlayer.numBoardsEvaluated
                    else:
                        additionalOutput += ")"
                else:
                    additionalOutput = ""
                moveOutputFormatted = COLUMN_LABELS[col] + str(row + 1)
                print(f"{nameOfCurrentPlayer} played in spot {moveOutputFormatted}{additionalOutput}\n")

            else:
                numValidMovesInARow += 1
                if numValidMovesInARow == 2:
                    print("Neither player has any valid moves left!")
                    userScore, aiScore = currentScore(self.userPiece, self.board)
                    if userScore > aiScore:
                        self.endGame(self.userPiece)
                    elif aiScore > userScore:
                        self.endGame(self.opponentPiece)
                    else:
                        self.endGame()
                noValidMovesColor = self.textColorOf(self.turn)
                playAgainColor = self.textColorOf(opponentOf(self.turn))
                print(
                    f"{noValidMovesColor}%s{NO_COLOR} has no valid moves this turn! {playAgainColor}%s{NO_COLOR} will play again." % (
                        nameOfPieceColor(self.turn), nameOfPieceColor(opponentOf(self.turn))))
                self.linesWrittenToConsole += 3 + BOARD_DIMENSION
            gameOver, winner = checkGameOver(self.board)
            self.turn = opponentOf(self.turn)
        if gameOver:
            self.endGame(winner)


    def printBoard(self, highlightedCoordinates=None, board=None):
        """Prints the gameBoard in a human-readable format"""
        if highlightedCoordinates is None:
            highlightedCoordinates = []
        if board is None:
            board = self.board
        print("\n\t    %s" % " ".join(COLUMN_LABELS))
        for rowNum in range(BOARD_DIMENSION):
            print("\t%d%s| " % (rowNum + 1, "" if rowNum > 8 else " "), end='')
            for colNum in range(BOARD_DIMENSION):
                piece = pieceAt(rowNum, colNum, board)
                pieceColor = HIGHLIGHT if [rowNum, colNum] in highlightedCoordinates else ''
                pieceColor += self.textColorOf(piece)
                print(f"{pieceColor}%s{NO_COLOR} " % piece, end='')
            if rowNum == BOARD_DIMENSION // 2:
                print("   %d turns remain." % (numberOfPieceOnBoard(EMPTY, board)), end='')
            print()
        userScore, aiScore = currentScore(self.userPiece, board)
        additionalIndent = " " * ((2 + (2 * (BOARD_DIMENSION // 2 - 1))) - (1 if userScore >= 10 else 0))
        print(f"\t{additionalIndent}{GREEN_COLOR}{userScore}{NO_COLOR} to {RED_COLOR}{aiScore}{NO_COLOR}\n")


    def printMoveHistory(self, numMovesPrevious):
        """Prints the move history of the current game"""
        while True:
            self.printBoard(self.boardHistory[-(numMovesPrevious + 1)][0], self.boardHistory[-(numMovesPrevious + 1)][1])
            if numMovesPrevious == 0:
                return
            print("(%d move%s before current board state)" % (numMovesPrevious, "s" if numMovesPrevious != 1 else ""))
            numMovesPrevious -= 1
            userInput = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
            if userInput == 'q':
                self.endGame()
            elif userInput == 'e':
                erasePreviousLines(2)
                return
            else:
                erasePreviousLines(BOARD_DIMENSION + BOARD_OUTLINE_HEIGHT + 2)


    def saveGame(self, board, turn):
        """Saves the given board state to a save file"""
        if os.path.exists(SAVE_FILENAME):
            with open(SAVE_FILENAME, 'r') as saveFile:
                try:
                    timeOfPreviousSave = saveFile.readlines()[3].strip()
                    overwrite = input(f"{INFO_SYMBOL} A save state already exists from {timeOfPreviousSave}.\nIs it okay to overwrite it? (y/n)\t").strip().lower()
                    erasePreviousLines(1)
                    while overwrite not in ['y', 'n']:
                        erasePreviousLines(1)
                        overwrite = input(f"{ERROR_SYMBOL} Invalid input. Is it okay to overwrite the existing save state? (y/n)\t").strip().lower()
                    erasePreviousLines(1)
                    if overwrite == 'n':
                        print(f"{INFO_SYMBOL} The current game state will not be saved.")
                        return
                except IndexError:
                    pass
        with open(SAVE_FILENAME, 'w') as saveFile:
            saveFile.write("This file contains the save state of a previously played game.\n")
            saveFile.write("Modifying this file may cause issues with loading the save state.\n\n")
            timeOfSave = datetime.now().strftime("%m/%d/%Y at %I:%M:%S %p")
            saveFile.write(timeOfSave + "\n\n")
            saveFile.write("SAVE STATE:\n")
            for row in board:
                saveFile.write(" ".join(row) + "\n")
            saveFile.write(f"User piece: " + self.userPiece  +"\n")
            saveFile.write("Opponent piece: " + self.opponentPiece  +"\n")
            saveFile.write("Turn: " + turn)
        print(f"{INFO_SYMBOL} The game has been saved!")


def nameOfPieceColor(piece):
    """Gets the name of the color of the given piece"""
    if piece == BLACK:
        return "BLACK"
    elif piece == WHITE:
        return "WHITE"
    else:
        return "EMPTY"


def getPieceColorInput():
    """Gets input from the user to determine which color they will be"""
    color_input = input("Would you like to be BLACK ('b') or WHITE ('w')?   ").strip().lower()
    erasePreviousLines(1)
    color = BLACK if color_input == 'b' else WHITE
    if color == BLACK:
        print(f"You will be BLACK {GREEN_COLOR}{BLACK}{NO_COLOR}!")
    else:
        print(f"You will be WHITE {GREEN_COLOR}{WHITE}{NO_COLOR}!")
    print(f"Your pieces are shown in {GREEN_COLOR}%s{NO_COLOR}!" % (
        "blue" if GREEN_COLOR == BLUE_COLOR else "green"))
    print(f"Enemy pieces are shown in {RED_COLOR}%s{NO_COLOR}!" % (
        "orange" if RED_COLOR == ORANGE_COLOR else "red"))
    return color


def validateLoadedSaveState(board, piece, turn):
    """Make sure the state loaded from the save file is valid. Returns a boolean"""
    if piece not in [BLACK, WHITE]:
        return False
    if turn not in [BLACK, WHITE]:
        return False
    boardDimension = len(board)
    for row in board:
        if len(row) != boardDimension:
            return False
        if row.count(EMPTY) + row.count(BLACK) + row.count(WHITE) != boardDimension:
            return False
    return True


def loadSavedGame():
    """Try to load the saved game data"""
    with open(SAVE_FILENAME, 'r') as saveFile:
        try:
            linesFromSaveFile = saveFile.readlines()
            timeOfPreviousSave = linesFromSaveFile[3].strip()
            useExistingSave = input(f"{INFO_SYMBOL} Would you like to load the saved game from {timeOfPreviousSave}? (y/n)\t").strip().lower()
            erasePreviousLines(1)
            if useExistingSave != 'y':
                print(f"{INFO_SYMBOL} Starting a new game...")
                return None, None, None
            lineNum = 0
            currentLine = linesFromSaveFile[lineNum].strip()
            while currentLine != "SAVE STATE:":
                lineNum += 1
                currentLine = linesFromSaveFile[lineNum].strip()
            lineNum += 1
            currentLine = linesFromSaveFile[lineNum].strip()
            board = []
            while not currentLine.startswith("User piece"):
                board.append(currentLine.split())
                lineNum += 1
                currentLine = linesFromSaveFile[lineNum].strip()
            userPiece = currentLine.split(": ")[1].strip()
            lineNum += 2
            currentLine = linesFromSaveFile[lineNum].strip()
            turn = currentLine.split(": ")[1].strip()
            if not validateLoadedSaveState(board, userPiece, turn):
                raise ValueError
            deleteSaveFile = input(f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
            erasePreviousLines(1)
            fileDeletedText = ""
            if deleteSaveFile == 'y':
                os.remove(SAVE_FILENAME)
                fileDeletedText = "Save file deleted. "
            print(f"{INFO_SYMBOL} %sResuming saved game..." % fileDeletedText )
            return board, userPiece, turn
        except:
            print(f"{ERROR_SYMBOL} There was an issue reading from the save file. Starting a new game...")
            return None, None, None


def erasePreviousLines(numLines, overrideEraseMode=False):
    """Erases the specified previous number of lines from the terminal"""
    eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
    if eraseMode:
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')


def printGameRules():
    """Gives the user the option to view the rules of the game"""
    print("\nType 'q' at any move prompt to quit the game.")
    print("Type 's' save the game.")
    print("Type 'h' at your turn to see previous moves.")
    print("AI constants are modifiable in the strategy.py file.")
    showRules = input("Would you like to see the rules? (y/n)   ").strip().lower()
    erasePreviousLines(1)
    if showRules == 'q':
        print("\nThanks for playing!")
        exit(0)
    elif showRules == 'y':
        print("""
    - OBJECTIVE: Have more pieces on the board than the opponent when all spaces are full
    - TURNS: Black will go first. Each player will take turns placing one piece each turn
    - GAMEPLAY: Trap enemy pieces between two friendly pieces to convert them to friendly pieces
        """)


def getOpposingAiModuleName():
    """Reads the command line arguments to determine the name of module for the opposing AI"""
    remainingCommandLineArgs = sys.argv[2:]
    for arg in remainingCommandLineArgs:
        if "-" not in arg:
            return arg
    print(f"{ERROR_SYMBOL} You need to provide the name of your AI strategy module.")
    exit(0)


def getDuelingAi():
    """Returns the imported AI Strategy class if the import is valid"""
    duelAiModuleName = getOpposingAiModuleName()
    try:
        DuelingAi  = getattr(import_module(duelAiModuleName), 'OthelloStrategy')
        if not issubclass(DuelingAi, Player):
            print(f"{ERROR_SYMBOL} Please make sure your AI is a subclass of 'Player'")
            exit(0)
        return DuelingAi
    except ImportError:
        print(f"{ERROR_SYMBOL} Please provide a valid module to import.\n" +
              f"{INFO_SYMBOL} Pass the name of your Python file as a command line argument, WITHOUT the .py extension.")
        exit(0)
    except AttributeError:
        print(f"{ERROR_SYMBOL} Please make sure your AI's class name is 'OthelloStrategy'")
        exit(0)


def printAsciiTitleArt():
    """Prints the fancy text when you start the program"""
    print("""
             _  __     _      _
            | |/ /    | |    ( )
            | ' /_   _| | ___|/ ___
            |  <| | | | |/ _ \ / __|
            | . \ |_| | |  __/ \__ \\
            |_|\_\__, |_|\___| |___/
 _____  _   _     __/ |_ _                  _____
/  __ \\| | | |   |___/| | |           /\\   |_   _|
| |  | | |_| |__   ___| | | ___      /  \\    | |
| |  | | __| '_ \\ / _ \\ | |/ _ \\    / /\\ \\   | |
| |__| | |_| | | |  __/ | | (_) |  / ____ \\ _| |_
\\_____/ \\__|_| |_|\\___|_|_|\\___/  /_/    \\_\\_____|
    """)


def main():
    """Prompts user for input and creates a new GameRunner"""
    global AI_DUEL_MODE, ERASE_MODE_ON
    os.system("")  # allows output text coloring for Windows OS
    if "-e" in sys.argv or "-eraseModeOff" in sys.argv:
        ERASE_MODE_ON = False
    if "-cb" in sys.argv or "-colorblindMode" in sys.argv:
        global RED_COLOR, GREEN_COLOR
        RED_COLOR = ORANGE_COLOR
        GREEN_COLOR = BLUE_COLOR
    if "-d" in sys.argv or "-aiDuel" in sys.argv:
        UserPlayerClass = getDuelingAi()
        print(f"\n{INFO_SYMBOL} You are in AI Duel Mode!")
        AI_DUEL_MODE = True
    else:
        UserPlayerClass = HumanPlayer
        AI_DUEL_MODE = False
    printAsciiTitleArt()
    printGameRules()
    game = GameRunner(UserPlayerClass, OthelloStrategy)
    game.start()


if __name__ == '__main__':
    main()
