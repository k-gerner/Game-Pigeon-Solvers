# Kyle Gerner 
# Started 3.18.21
# Connect 4 Solver, client facing
import os
import sys
import time
from importlib import import_module
from datetime import datetime
from Player import Player
from strategy import Strategy, opponentOf, performMove, checkIfGameOver, isValidMove, copyOfBoard

YELLOW_COLOR = "\u001b[38;5;226m"  # yellow
RED_COLOR = '\033[91m'             # red
BLUE_COLOR = "\u001b[38;5;39m"     # blue
GREEN_COLOR = "\x1B[38;5;47m"      # green
GREY_COLOR = "\x1B[38;5;247m"      # grey
NO_COLOR = '\033[0m'               # white

ERASE_MODE_ON = True
BOARD_OUTPUT_HEIGHT = 9

CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"
INFO_SYMBOL = f"{BLUE_COLOR}<!>{NO_COLOR}"
SAVE_FILENAME = "saved_game.txt"
BOARD_HISTORY = [] # [board, highlightCoordinates]

EMPTY, RED, YELLOW = '.', 'o', '@'
gameBoard = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],  # bottom row
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]]  # top row
userPiece = YELLOW
TIME_TAKEN_PER_PLAYER = {}

# class for the Human player
class HumanPlayer(Player):

    def __init__(self, color):
        super().__init__(color, isAI=False)

    def getMove(self, board):
        """Takes in the user's input and returns the move"""
        col = input("It's your turn, which column would you like to play? (1-7):\t").strip().lower()
        erasePreviousLines(1)
        while True:
            if col == 'q':
                endGame()
            elif col == 'h':
                col = getBoardHistoryInputFromUser(isAi=False)
            elif col == 's':
                saveGame(self.color)
                col = input("Which column would you like to play? (1-7):\t").strip().lower()
                erasePreviousLines(2)
            elif not col.isdigit() or int(col) not in range(1, 8):
                col = input(f"{ERROR_SYMBOL} Invalid input. Please enter a number 1 through 7:\t")
                erasePreviousLines(1)
            elif not isValidMove(gameBoard, int(col) - 1):
                col = input(f"{ERROR_SYMBOL} That column is full, please choose another:\t")
                erasePreviousLines(1)
            else:
                break
        erasePreviousLines(1)
        return int(col) - 1


def getHighlightColorForPiece(piece):
    """Gets the color highlight color for a given piece"""
    if piece == RED:
        return RED_COLOR
    elif piece == YELLOW:
        return YELLOW_COLOR
    else:
        return NO_COLOR


def printBoard(board, recentMove=None):
    """Prints the given game board"""
    columnColor = NO_COLOR
    print("\n   ", end='')
    for i in range(7):
        if i == recentMove:
            columnColor = GREEN_COLOR
        elif not isValidMove(board, i):
            columnColor = GREY_COLOR
        print(f"{columnColor}{i+1}{NO_COLOR} ", end='')
        columnColor = NO_COLOR
    print()
    for rowNum in range(len(board) - 1, -1, -1):
        print(f" {BLUE_COLOR}|{NO_COLOR} ", end='')
        for spot in board[rowNum]:
            pieceColor = getHighlightColorForPiece(spot)
            print(f"{pieceColor}%s{NO_COLOR} " % spot, end='')
        print(f"{BLUE_COLOR}|{NO_COLOR}")
    print(" " + f"{BLUE_COLOR}%s{NO_COLOR}" % "-" * 17)


def printMoveHistory(numMovesPrevious):
    """Prints the move history of the current game"""
    while True:
        printBoard(BOARD_HISTORY[-(numMovesPrevious + 1)][0], BOARD_HISTORY[-(numMovesPrevious + 1)][1])
        if numMovesPrevious == 0:
            return
        print("(%d move%s before current board state)\n" % (numMovesPrevious, "s" if numMovesPrevious != 1 else ""))
        numMovesPrevious -= 1
        userInput = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
        erasePreviousLines(1)
        if userInput == 'q':
            erasePreviousLines(2)
            endGame()
        elif userInput == 'e':
            erasePreviousLines(2)
            return
        else:
            erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)


def getBoardHistoryInputFromUser(isAi):
    """
    Prompts the user for input for how far the board history function.
    Returns the user's input for the next move
    """
    nextMovePrompt = "Press enter to continue." if isAi else "Enter a valid move to play:"
    if len(BOARD_HISTORY) < 2:
        userInput = input(f"{INFO_SYMBOL} No previous moves to see. {nextMovePrompt}   ").strip().lower()
        erasePreviousLines(1)
    else:
        numMovesPrevious = input(f"How many moves ago do you want to see? (1 to {len(BOARD_HISTORY) - 1})  ").strip()
        erasePreviousLines(1)
        if numMovesPrevious.isdigit() and 1 <= int(numMovesPrevious) <= len(BOARD_HISTORY) - 1:
            erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
            printMoveHistory(int(numMovesPrevious))
            erasePreviousLines(BOARD_OUTPUT_HEIGHT)
            printBoard(BOARD_HISTORY[-1][0], BOARD_HISTORY[-1][1])
            userInput = input(f"{INFO_SYMBOL} You're back in play mode. {nextMovePrompt}   ").strip().lower()
            erasePreviousLines(1)
            print("\n") # make this output the same height as the other options
        else:
            userInput = input(f"{ERROR_SYMBOL} Invalid input. {nextMovePrompt}   ").strip().lower()
            erasePreviousLines(1)
    return userInput


def endGame():
    """Ends the game"""
    opponentPiece = opponentOf(userPiece)
    userTimeTaken = round(TIME_TAKEN_PER_PLAYER[userPiece][1]/max(1, TIME_TAKEN_PER_PLAYER[userPiece][2]), 2)
    aiTimeTaken = round(TIME_TAKEN_PER_PLAYER[opponentPiece][1]/max(1, TIME_TAKEN_PER_PLAYER[opponentPiece][2]), 2)
    print("Average time taken per move:")
    print(f"{GREEN_COLOR}{TIME_TAKEN_PER_PLAYER[userPiece][0]}{NO_COLOR}: {userTimeTaken}s")
    print(f"{RED_COLOR}{TIME_TAKEN_PER_PLAYER[opponentPiece][0]}{NO_COLOR}: {aiTimeTaken}s")
    print("\nThanks for playing!\n")
    exit(0)


def saveGame(turn):
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
        for row in gameBoard:
            saveFile.write(" ".join(row) + "\n")
        saveFile.write("User piece: " + str(userPiece)  +"\n")
        saveFile.write("Opponent piece: " + opponentOf(userPiece)  +"\n")
        saveFile.write("Turn: " + turn)
    print(f"{INFO_SYMBOL} The game has been saved!")


def validateLoadedSaveState(board, piece, turn):
    """Make sure the state loaded from the save file is valid. Returns a boolean"""
    if piece not in [RED, YELLOW]:
        print(f"{ERROR_SYMBOL} Invalid user piece!")
        return False
    if turn not in [RED, YELLOW]:
        print(f"{ERROR_SYMBOL} Invalid player turn!")
        return False
    for row in board:
        if len(row) != 7:
            print(f"{ERROR_SYMBOL} Invalid board!")
            return False
        if row.count(EMPTY) + row.count(RED) + row.count(YELLOW) != 7:
            print(f"{ERROR_SYMBOL} Board contains invalid pieces!")
            return False
    return True


def loadSavedGame():
    """Try to load the saved game data"""
    global userPiece, gameBoard
    with open(SAVE_FILENAME, 'r') as saveFile:
        try:
            linesFromSaveFile = saveFile.readlines()
            timeOfPreviousSave = linesFromSaveFile[3].strip()
            useExistingSave = input(f"{INFO_SYMBOL} Would you like to load the saved game from {timeOfPreviousSave}? (y/n)\t").strip().lower()
            erasePreviousLines(1)
            if useExistingSave != 'y':
                print(f"{INFO_SYMBOL} Starting a new game...\n")
                return
            lineNum = 0
            currentLine = linesFromSaveFile[lineNum].strip()
            while currentLine != "SAVE STATE:":
                lineNum += 1
                currentLine = linesFromSaveFile[lineNum].strip()
            lineNum += 1
            currentLine = linesFromSaveFile[lineNum].strip()
            boardFromSaveFile = []
            while not currentLine.startswith("User piece"):
                boardFromSaveFile.append(currentLine.split())
                lineNum += 1
                currentLine = linesFromSaveFile[lineNum].strip()
            userPiece = currentLine.split(": ")[1].strip()
            lineNum += 2
            currentLine = linesFromSaveFile[lineNum].strip()
            turn = currentLine.split(": ")[1].strip()
            if not validateLoadedSaveState(boardFromSaveFile, userPiece, turn):
                raise ValueError
            gameBoard = boardFromSaveFile
            deleteSaveFile = input(f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
            erasePreviousLines(1)
            fileDeletedText = ""
            if deleteSaveFile == 'y':
                os.remove(SAVE_FILENAME)
                fileDeletedText = "Save file deleted. "
            print(f"{INFO_SYMBOL} {fileDeletedText}Resuming saved game...\n")
            return turn
        except Exception:
            print(f"{ERROR_SYMBOL} There was an issue reading from the save file. Starting a new game...\n")
            return None


def printAsciiTitleArt():
    """Prints the fancy text when you start the program"""
    print("""
   _____                            _     _  _   
  / ____|                          | |   | || |  
 | |     ___  _ __  _ __   ___  ___| |_  | || |_ 
 | |    / _ \| '_ \| '_ \ / _ \/ __| __| |__   _|
 | |___| (_) | | | | | | |  __/ (__| |_     | |  
  \_____\___/|_| |_|_| |_|\___|\___|\__|    |_|      
    """)


def erasePreviousLines(numLines, overrideEraseMode=False):
    """Erases the specified previous number of lines from the terminal"""
    eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
    if eraseMode:
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')


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
        DuelingAi  = getattr(import_module(duelAiModuleName), 'Strategy')
        if not issubclass(DuelingAi, Player):
            print(f"{ERROR_SYMBOL} Please make sure your AI is a subclass of 'Player'")
            exit(0)
        return DuelingAi
    except ImportError:
        print(f"{ERROR_SYMBOL} Please provide a valid module to import.\n" +
              f"{INFO_SYMBOL} Pass the name of your Python file as a command line argument, WITHOUT the .py extension.")
        exit(0)
    except AttributeError:
        print(f"{ERROR_SYMBOL} Please make sure your AI's class name is 'Strategy'")
        exit(0)


def main():
    """main method that prompts the user for input"""
    global userPiece, TIME_TAKEN_PER_PLAYER
    os.system("")  # allows colored terminal to work on Windows OS
    if "-e" in sys.argv or "-eraseModeOff" in sys.argv:
        global ERASE_MODE_ON
        ERASE_MODE_ON = False
    if "-d" in sys.argv or "-aiDuel" in sys.argv:
        UserPlayerClass = getDuelingAi()
        print(f"\n{INFO_SYMBOL} You are in AI Duel Mode!")
        AI_DUEL_MODE = True
    else:
        UserPlayerClass = HumanPlayer
        AI_DUEL_MODE = False
    print("\nWelcome to Kyle's Connect 4 AI!")
    printAsciiTitleArt()
    userPlayerName = "Your AI" if AI_DUEL_MODE else "You"
    aiPlayerName = "My AI" if AI_DUEL_MODE else "AI"

    turn = YELLOW
    useSavedGame = False
    if os.path.exists(SAVE_FILENAME):
        turnFromSaveFile = loadSavedGame()
        if turnFromSaveFile is not None:
            turn = turnFromSaveFile
            opponentPiece = opponentOf(userPiece)
            useSavedGame = True
            BOARD_HISTORY.append([copyOfBoard(gameBoard), None])
    if not useSavedGame:
        userPieceInput = input(
            "Would you like to be RED ('r') or YELLOW ('y')? (yellow goes first!):\t").strip().lower()
        erasePreviousLines(1)
        if userPieceInput == 'r':
            userPiece = RED
            opponentPiece = YELLOW
            print(f"{userPlayerName} will be {RED_COLOR}RED{NO_COLOR}!")
        elif userPieceInput == 'y':
            userPiece = YELLOW
            opponentPiece = RED
            print(f"{userPlayerName} will be {YELLOW_COLOR}YELLOW{NO_COLOR}!")
        else:
            userPiece = RED
            opponentPiece = YELLOW
            print(f"{ERROR_SYMBOL} Invalid input. {userPlayerName} will be {RED_COLOR}RED{NO_COLOR}!")

    TIME_TAKEN_PER_PLAYER = {
        userPiece: [userPlayerName, 0, 0],    # [player name, total time, num moves]
        opponentPiece: [aiPlayerName, 0, 0]
    }
    userHighlightColor = getHighlightColorForPiece(userPiece)
    opponentHighlightColor = getHighlightColorForPiece(opponentPiece)
    print(f"{userPlayerName}: {userHighlightColor}{userPiece}{NO_COLOR}\t{aiPlayerName}: {opponentHighlightColor}{opponentPiece}{NO_COLOR}")
    playerNames = {opponentPiece: aiPlayerName, userPiece: userPlayerName}
    players = {opponentPiece: Strategy(opponentPiece), userPiece: UserPlayerClass(userPiece)}
    gameOver = False
    winningPiece = None
    print("Type 's' at any prompt to save the game.")
    print("Type 'h' to see previous moves.")
    print("Type 'q' at any prompt to quit.")
    printBoard(gameBoard)
    print()
    firstTurn = True
    while not gameOver:
        nameOfCurrentPlayer = playerNames[turn]
        currentPlayer = players[turn]
        if currentPlayer.isAI:
            userInput = input(f"{nameOfCurrentPlayer}'s turn, press enter for it to play.\t").strip().lower()
            erasePreviousLines(1)
            while userInput in ['q', 's', 'h']:
                if userInput == 'q':
                    endGame()
                elif userInput == 'h':
                    userInput = getBoardHistoryInputFromUser(isAi=True)
                else:
                    saveGame(currentPlayer.color)
                    userInput = input(f"{nameOfCurrentPlayer}'s turn, press enter for it to play.\t").strip().lower()
                    erasePreviousLines(2)

            erasePreviousLines(1)
        startTime = time.time()
        column = currentPlayer.getMove(gameBoard)
        endTime = time.time()
        totalTimeTakenForMove = endTime - startTime
        TIME_TAKEN_PER_PLAYER[turn][1] += totalTimeTakenForMove
        TIME_TAKEN_PER_PLAYER[turn][2] += 1
        performMove(gameBoard, column, turn)
        BOARD_HISTORY.append([copyOfBoard(gameBoard), column])
        erasePreviousLines(BOARD_OUTPUT_HEIGHT + (0 if firstTurn else 1))
        printBoard(gameBoard, column)
        print(f"{nameOfCurrentPlayer} played in spot {column + 1}\n")
        turn = opponentOf(turn)  # switch the turn
        firstTurn = False
        gameOver, winningPiece = checkIfGameOver(gameBoard)

    if winningPiece is None:
        print("The game ended in a tie!\n")
    elif winningPiece == RED:
        print(f"{RED_COLOR}RED{NO_COLOR} wins!\n")
    else:
        print(f"{YELLOW_COLOR}YELLOW{NO_COLOR} wins!\n")
    endGame()


if __name__ == "__main__":
    main()
