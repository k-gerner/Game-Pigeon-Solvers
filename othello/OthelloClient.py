# Kyle Gerner
# Started 7.15.22
# Othello AI, client facing
import os
import sys
import time
from importlib import import_module
from datetime import datetime
from util.terminaloutput.colors import NO_COLOR, YELLOW_COLOR, GREEN_COLOR, BLUE_COLOR, RED_COLOR, ORANGE_COLOR, \
    DARK_GREY_BACKGROUND as HIGHLIGHT
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL
from util.terminaloutput.erasing import erasePreviousLines

from othello.strategy import OthelloStrategy, copyOfBoard, BOARD_DIMENSION, getValidMoves, opponentOf, playMove, \
    currentScore, checkGameOver, numberOfPieceOnBoard, pieceAt, hasValidMoves, isMoveValid, isMoveInRange
from othello.Player import Player

BLACK = "0"
WHITE = "O"
EMPTY = "."

# Escape sequences for terminal color output

# Miscellaneous
COLUMN_LABELS = list(map(chr, range(65, 65 + BOARD_DIMENSION)))
BOARD_OUTLINE_HEIGHT = 4
ERASE_MODE_ON = True
SAVE_FILENAME = "saved_game.txt"
TIME_TAKEN_PER_PLAYER = {}

# Relevant to game state
BOARD = []
BOARD_HISTORY = []
USER_PIECE = BLACK      # may be changed in game setup
OPPONENT_PIECE = WHITE  # may be changed in game setup

# class for the Human player
class HumanPlayer(Player):

    def __init__(self, color):
        super().__init__(color, isAI=False)

    def getMove(self, board):
        """Takes in the user's input and returns the move"""
        coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
            COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
        erasePreviousLines(1)
        linesWrittenToConsole = BOARD_DIMENSION + 6
        while True:
            if coord == 'Q':
                endGame()
            elif coord == 'S':
                saveGame(board, self.color)
                coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
                erasePreviousLines(2)
            elif coord == 'QS' or coord == 'SQ':
                saveGame(board, self.color)
                endGame()
            elif coord == 'H':
                coord, linesWrittenToConsole = getBoardHistoryInputFromUser(board, self.color, False, linesWrittenToConsole)
            elif len(coord) in ([2] if BOARD_DIMENSION < 10 else [2, 3]) and coord[0] in COLUMN_LABELS and \
                    coord[1:].isdigit() and int(coord[1:]) in range(1, BOARD_DIMENSION + 1):
                row, col = int(coord[1]) - 1, COLUMN_LABELS.index(coord[0])
                if isMoveValid(self.color, row, col, board):
                    erasePreviousLines(linesWrittenToConsole)
                    printBoard()
                    print("\n")
                    return row, col
                elif isMoveInRange(row, col) and pieceAt(row, col, board) != EMPTY:
                    coord = input(
                        f"{ERROR_SYMBOL} That spot is already taken! Please choose a different spot:   ").strip().upper()
                    erasePreviousLines(1)
                else:
                    coord = input(f"{ERROR_SYMBOL} Please choose one of the highlighted spaces:   ").strip().upper()
                    erasePreviousLines(1)
            else:
                coord = input(f"{ERROR_SYMBOL} Please enter a valid move (A1 - %s%d):   " % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
                erasePreviousLines(1)


def printBoard(highlightedCoordinates=None, board=None):
    """Prints the gameBoard in a human-readable format"""
    if highlightedCoordinates is None:
        highlightedCoordinates = []
    if board is None:
        board = BOARD
    print("\n\t    %s" % " ".join(COLUMN_LABELS))
    for rowNum in range(BOARD_DIMENSION):
        print("\t%d%s| " % (rowNum + 1, "" if rowNum > 8 else " "), end='')
        for colNum in range(BOARD_DIMENSION):
            piece = pieceAt(rowNum, colNum, board)
            pieceColor = HIGHLIGHT if [rowNum, colNum] in highlightedCoordinates else ''
            pieceColor += textColorOf(piece)
            print(f"{pieceColor}%s{NO_COLOR} " % piece, end='')
        if rowNum == BOARD_DIMENSION // 2:
            movesRemaining = numberOfPieceOnBoard(EMPTY, board)
            if movesRemaining <= 5:
                movesRemainingColor = ORANGE_COLOR
            elif movesRemaining <= 10:
                movesRemainingColor = YELLOW_COLOR
            else:
                movesRemainingColor = NO_COLOR
            print(f"   {movesRemainingColor}{movesRemaining} turn{'' if movesRemaining == 1 else 's'} remain{'s' if movesRemaining == 1 else ''}.{NO_COLOR}", end='')
        print()
    userScore, aiScore = currentScore(USER_PIECE, board)
    additionalIndent = " " * ((2 + (2 * (BOARD_DIMENSION // 2 - 1))) - (1 if userScore >= 10 else 0))
    print(f"\t{additionalIndent}{GREEN_COLOR}{userScore}{NO_COLOR} to {RED_COLOR}{aiScore}{NO_COLOR}\n")


def printMoveHistory(numMovesPrevious):
    """Prints the move history of the current game"""
    while True:
        printBoard(BOARD_HISTORY[-(numMovesPrevious + 1)][0], BOARD_HISTORY[-(numMovesPrevious + 1)][1])
        if numMovesPrevious == 0:
            return
        print("(%d move%s before current board state)" % (numMovesPrevious, "s" if numMovesPrevious != 1 else ""))
        numMovesPrevious -= 1
        userInput = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
        if userInput == 'q':
            endGame()
        elif userInput == 'e':
            erasePreviousLines(2)
            return
        else:
            erasePreviousLines(BOARD_DIMENSION + BOARD_OUTLINE_HEIGHT + 2)


def getBoardHistoryInputFromUser(board, turn, isAi, linesWrittenToConsole):
    """
    Prompts the user for input for how far the board history function.
    Returns the user's input for the next move, and the new value for linesWrittenToConsole
    """
    nextMovePrompt = "Press enter to continue." if isAi else "Enter a valid move to play:"
    if len(BOARD_HISTORY) < 2:
        userInput = input(f"No previous moves to see. {nextMovePrompt}   ").strip().upper()
        erasePreviousLines(1)
    else:
        numMovesPrevious = input(f"How many moves ago do you want to see? (1 to {len(BOARD_HISTORY) - 1})  ").strip()
        if numMovesPrevious.isdigit() and 1 <= int(numMovesPrevious) <= len(BOARD_HISTORY) - 1:
            linesWrittenToConsole += 1
            erasePreviousLines(linesWrittenToConsole)
            printMoveHistory(int(numMovesPrevious))
            erasePreviousLines(BOARD_DIMENSION + BOARD_OUTLINE_HEIGHT)
            printBoard(getValidMoves(turn, board))
            userInput = input(f"{INFO_SYMBOL} You're back in play mode. {nextMovePrompt}   ").strip().upper()
            erasePreviousLines(1)
            linesWrittenToConsole = BOARD_DIMENSION + 4
        else:
            userInput = input(f"{ERROR_SYMBOL} Invalid input. {nextMovePrompt}   ").strip().upper()
            erasePreviousLines(2)
    return userInput, linesWrittenToConsole

def textColorOf(piece):
    """Gets the text color of the given piece, or an empty string if no piece given"""
    if piece == USER_PIECE:
        return GREEN_COLOR
    elif piece == OPPONENT_PIECE:
        return RED_COLOR
    else:
        return ""


def nameOfPieceColor(piece):
    """Gets the name of the color of the given piece"""
    if piece == BLACK:
        return "BLACK"
    elif piece == WHITE:
        return "WHITE"
    else:
        return "EMPTY"


def endGame(winner=None):
    """Ends the game"""
    if winner:
        textColor = textColorOf(winner)
        colorName = nameOfPieceColor(winner)
        print(f"\n{textColor}{colorName}{NO_COLOR} wins!\n")
    else:
        print("\nThe game ended in a draw!\n")
    userTimeTaken = round(TIME_TAKEN_PER_PLAYER[USER_PIECE][1]/max(1, TIME_TAKEN_PER_PLAYER[USER_PIECE][2]), 2)
    aiTimeTaken = round(TIME_TAKEN_PER_PLAYER[OPPONENT_PIECE][1]/max(1, TIME_TAKEN_PER_PLAYER[OPPONENT_PIECE][2]), 2)
    print("Average time taken per move:")
    print(f"{GREEN_COLOR}{TIME_TAKEN_PER_PLAYER[USER_PIECE][0]}{NO_COLOR}: {userTimeTaken}s")
    print(f"{RED_COLOR}{TIME_TAKEN_PER_PLAYER[OPPONENT_PIECE][0]}{NO_COLOR}: {aiTimeTaken}s")
    print("\nThanks for playing!")
    exit(0)


def saveGame(board, turn):
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
        saveFile.write(f"User piece: " + USER_PIECE  +"\n")
        saveFile.write("Opponent piece: " + OPPONENT_PIECE  +"\n")
        saveFile.write("Turn: " + turn)
    print(f"{INFO_SYMBOL} The game has been saved!")


def printGameRules():
    """Gives the user the option to view the rules of the game"""
    print("\nType 'q' at any move prompt to quit the game.")
    print("Type 's' save the game.")
    print("Type 'h' to see previous moves.")
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


def getOpposingAiModuleName():
    """Reads the command line arguments to determine the name of module for the opposing AI"""
    try:
        indexOfFlag = sys.argv.index("-d") if "-d" in sys.argv else sys.argv.index("-aiDuel")
        module = sys.argv[indexOfFlag + 1].split(".py")[0]
        return module
    except (IndexError, ValueError):
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
              f"{INFO_SYMBOL} Pass the name of your Python file as a command line argument.")
        exit(0)
    except AttributeError:
        print(f"{ERROR_SYMBOL} Please make sure your AI's class name is 'OthelloStrategy'")
        exit(0)


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
        except Exception:
            print(f"{ERROR_SYMBOL} There was an issue reading from the save file. Starting a new game...")
            return None, None, None


def validateLoadedSaveState(board, piece, turn):
    """Make sure the state loaded from the save file is valid. Returns a boolean"""
    if len(board) != BOARD_DIMENSION:
        print(f"{ERROR_SYMBOL} Board dimension does not match!")
        return False
    if piece not in [BLACK, WHITE]:
        print(f"{ERROR_SYMBOL} Invalid user piece!")
        return False
    if turn not in [BLACK, WHITE]:
        print(f"{ERROR_SYMBOL} Invalid player turn!")
        return False
    boardDimension = len(board)
    for row in board:
        if len(row) != boardDimension:
            print(f"{ERROR_SYMBOL} Board is not square!")
            return False
        if row.count(EMPTY) + row.count(BLACK) + row.count(WHITE) != boardDimension:
            print(f"{ERROR_SYMBOL} Board contains invalid pieces!")
            return False
    return True


def getUserPieceColorInput():
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


def createNewBoard():
    """Creates the initial game board state"""
    board = [[EMPTY for _ in range(BOARD_DIMENSION)] for __ in range(BOARD_DIMENSION)]
    board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2 - 1] = WHITE
    board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2] = WHITE
    board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2] = BLACK
    board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2 - 1] = BLACK
    return board


def main():
    global BOARD, USER_PIECE, OPPONENT_PIECE, TIME_TAKEN_PER_PLAYER
    os.system("") # allows colored terminal to work on Windows OS
    if "-e" in sys.argv or "-eraseModeOff" in sys.argv:
        global ERASE_MODE_ON
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

    useSavedGame = False
    if os.path.exists(SAVE_FILENAME):
        BOARD, USER_PIECE, turn = loadSavedGame()
        if turn is not None:
            useSavedGame = True
    if not useSavedGame:
        USER_PIECE = getUserPieceColorInput()
        BOARD = createNewBoard()
        turn = BLACK
    BOARD_HISTORY.append([[], copyOfBoard(BOARD)])
    OPPONENT_PIECE = opponentOf(USER_PIECE)
    userPlayerName = "Your AI" if AI_DUEL_MODE else "You"
    aiPlayerName = "My AI" if AI_DUEL_MODE else "AI"
    playerNames = {USER_PIECE: userPlayerName, OPPONENT_PIECE: aiPlayerName}
    players = {
        USER_PIECE: UserPlayerClass(USER_PIECE),
        OPPONENT_PIECE: OthelloStrategy(OPPONENT_PIECE)
    }
    TIME_TAKEN_PER_PLAYER = {
        USER_PIECE: [userPlayerName, 0, 0],    # [player name, total time, num moves]
        OPPONENT_PIECE: [aiPlayerName, 0, 0]
    }

    printBoard(getValidMoves(turn, BOARD))
    print("\n")

    numValidMovesInARow = 0
    gameOver, winner = False, None
    while not gameOver:
        linesWrittenToConsole = BOARD_DIMENSION + 6
        if hasValidMoves(turn, BOARD):
            numValidMovesInARow = 0
            nameOfCurrentPlayer = playerNames[turn]
            currentPlayer = players[turn]
            if currentPlayer.isAI:
                userInput = input(f"{nameOfCurrentPlayer}'s turn, press enter for it to play.\t").strip().upper()
                erasePreviousLines(1)
                while userInput in ['Q', 'S', 'QS', 'SQ', 'H']:
                    if userInput == 'Q':
                        endGame()
                    elif userInput == 'S':
                        saveGame(BOARD, turn)
                        userInput = input("Press enter to continue. ").strip().upper()
                        erasePreviousLines(2)
                    elif userInput == 'QS' or userInput == 'SQ':
                        saveGame(BOARD, turn)
                        endGame()
                    elif userInput == 'H':
                        userInput, linesWrittenToConsole = getBoardHistoryInputFromUser(BOARD, turn, True, linesWrittenToConsole)
            startTime = time.time()
            row, col = currentPlayer.getMove(BOARD)
            endTime = time.time()
            timeToPlayMove = (endTime - startTime)
            TIME_TAKEN_PER_PLAYER[turn][1] += timeToPlayMove
            TIME_TAKEN_PER_PLAYER[turn][2] += 1
            timeToPlayMove = round(timeToPlayMove, 2)
            playMove(turn, row, col, BOARD)
            BOARD_HISTORY.append([[[row, col]], copyOfBoard(BOARD)])
            erasePreviousLines(linesWrittenToConsole)
            printBoard([[row, col]] + getValidMoves(opponentOf(turn), BOARD))
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
                userScore, aiScore = currentScore(USER_PIECE, BOARD)
                if userScore > aiScore:
                    endGame(USER_PIECE)
                elif aiScore > userScore:
                    endGame(OPPONENT_PIECE)
                else:
                    endGame()
            noValidMovesColor = textColorOf(turn)
            playAgainColor = textColorOf(opponentOf(turn))
            erasePreviousLines(2)
            print(
                f"{INFO_SYMBOL} {noValidMovesColor}%s{NO_COLOR} has no valid moves this turn! {playAgainColor}%s{NO_COLOR} will play again.\n" % (
                    nameOfPieceColor(turn), nameOfPieceColor(opponentOf(turn))))
        gameOver, winner = checkGameOver(BOARD)
        turn = opponentOf(turn)
    endGame(winner)

if __name__ == '__main__':
    main()
