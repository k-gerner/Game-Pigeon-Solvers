# Tic Tac Toe AI client facing
# Kyle G 6.6.2021

from Player import Player
from strategy import Strategy, opponentOf, isTerminal, performMove, copyOfBoard
from importlib import import_module
from datetime import datetime
import os
import sys

EMPTY, X_PIECE, O_PIECE = ' ', 'X', 'O'
ROW_LABELS = "ABC"
gameBoard = [[EMPTY, EMPTY, EMPTY], 
			 [EMPTY, EMPTY, EMPTY],
			 [EMPTY, EMPTY, EMPTY]]
USER_PIECE = X_PIECE

GREEN_COLOR = '\033[92m'  	 # green
RED_COLOR = '\033[91m'	  	 # red
BLUE_COLOR = '\033[38;5;39m' # blue
NO_COLOR = '\033[0m' 	  	 # white

ERASE_MODE_ON = True
BOARD_OUTPUT_HEIGHT = 7

CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"
INFO_SYMBOL = f"{BLUE_COLOR}<!>{NO_COLOR}"
SAVE_FILENAME = "saved_game.txt"
BOARD_HISTORY = []

# class for the Human player
class HumanPlayer(Player):

	def __init__(self, color):
		super().__init__(color, isAI=False)


	def getMove(self, board):
		"""Takes in the user's input and returns the move"""
		spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (ROW_LABELS[-1], len(board))).strip().upper()
		erasePreviousLines(1)
		while True:
			if spot == 'Q':
				print("\nThanks for playing!\n")
				exit(0)
			elif spot == 'H':
				spot = getBoardHistoryInputFromUser(False)
			elif spot == 'S':
				saveGame(self.color)
				spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (ROW_LABELS[-1], len(board))).strip().upper()
				erasePreviousLines(2)
			elif len(spot) >= 3 or len(spot) == 0 or spot[0] not in ROW_LABELS or not spot[1:].isdigit() or int(spot[1:]) > len(board) or int(spot[1:]) < 1:
				spot = input(f"{ERROR_SYMBOL} Invalid input. Please try again.\t").strip().upper()
				erasePreviousLines(1)
			elif board[ROW_LABELS.index(spot[0])][int(spot[1:]) - 1] != EMPTY:
				spot = input(f"{ERROR_SYMBOL} That spot is already taken, please choose another:\t").strip().upper()
				erasePreviousLines(1)
			else:
				break
		row = ROW_LABELS.index(spot[0])
		col = int(spot[1:]) - 1
		return row, col


def printGameBoard(board=None):
	"""Prints the gameBoard in a human-readable format"""
	if board is None:
		board = gameBoard
	print()
	for rowNum in range(len(board)):
		row = board[rowNum]
		print("\t%s  " % ROW_LABELS[rowNum], end = '')
		for colNum in range(len(row)):
			piece = board[rowNum][colNum]
			if piece == EMPTY:
				pieceColor = NO_COLOR
			elif piece == USER_PIECE:
				pieceColor = GREEN_COLOR
			else:
				pieceColor = RED_COLOR
			print(f" {pieceColor}%s{NO_COLOR} %s" % (piece, '|' if colNum < 2 else '\n'), end = '')
		if rowNum < 2:
			print("\t   ---+---+---")
	print("\t    1   2   3\n")


def printMoveHistory(numMovesPrevious):
	"""Prints the move history of the current game"""
	while True:
		printGameBoard(BOARD_HISTORY[-(numMovesPrevious + 1)])
		if numMovesPrevious == 0:
			return
		print("(%d move%s before current board state)\n" % (numMovesPrevious, "s" if numMovesPrevious != 1 else ""))
		numMovesPrevious -= 1
		userInput = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
		erasePreviousLines(1)
		if userInput == 'q':
			erasePreviousLines(2)
			print("Thanks for playing!\n")
			exit(0)
		elif userInput == 'e':
			erasePreviousLines(2)
			return
		else:
			erasePreviousLines(BOARD_OUTPUT_HEIGHT + 3)


def getBoardHistoryInputFromUser(isAi):
	"""
    Prompts the user for input for how far the board history function.
    Returns the user's input for the next move
    """
	nextMovePrompt = "Press enter to continue." if isAi else "Enter a valid move to play:"
	if len(BOARD_HISTORY) < 2:
		userInput = input(f"{INFO_SYMBOL} No previous moves to see. {nextMovePrompt}   ").strip().upper()
		erasePreviousLines(1)
	else:
		numMovesPrevious = input(f"How many moves ago do you want to see? (1 to {len(BOARD_HISTORY) - 1})  ").strip()
		erasePreviousLines(1)
		if numMovesPrevious.isdigit() and 1 <= int(numMovesPrevious) <= len(BOARD_HISTORY) - 1:
			erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
			printMoveHistory(int(numMovesPrevious))
			erasePreviousLines(BOARD_OUTPUT_HEIGHT + 1)
			printGameBoard(BOARD_HISTORY[-1])
			userInput = input(f"{INFO_SYMBOL} You're back in play mode. {nextMovePrompt}   ").strip().upper()
			erasePreviousLines(2)
			print("\n") # make this output the same height as the other options
		else:
			userInput = input(f"{ERROR_SYMBOL} Invalid input. {nextMovePrompt}   ").strip().upper()
			erasePreviousLines(1)
	return userInput


def erasePreviousLines(numLines, overrideEraseMode=False):
	"""Erases the specified previous number of lines from the terminal"""
	eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
	if eraseMode:
		print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')


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
			rowWithDifferentEmptyCharacter = row.copy()
			for index, piece in enumerate(rowWithDifferentEmptyCharacter):
				if piece == EMPTY:
					# replace EMPTY character with '-' so it can be parsed correctly when loading save
					rowWithDifferentEmptyCharacter[index] = "-"
			saveFile.write(" ".join(rowWithDifferentEmptyCharacter) + "\n")
		saveFile.write("User piece: " + str(USER_PIECE)  +"\n")
		saveFile.write("Opponent piece: " + opponentOf(USER_PIECE)  +"\n")
		saveFile.write("Turn: " + turn)
	print(f"{INFO_SYMBOL} The game has been saved!")


def validateLoadedSaveState(board, piece, turn):
	"""Make sure the state loaded from the save file is valid. Returns a boolean"""
	if piece not in [X_PIECE, O_PIECE]:
		print(f"{ERROR_SYMBOL} Invalid user piece!")
		return False
	if turn not in [X_PIECE, O_PIECE]:
		print(f"{ERROR_SYMBOL} Invalid player turn!")
		return False
	for row in board:
		if len(row) != 3:
			print(f"{ERROR_SYMBOL} Invalid board!")
			return False
		if row.count(EMPTY) + row.count(X_PIECE) + row.count(O_PIECE) != 3:
			print(f"{ERROR_SYMBOL} Board contains invalid pieces!")
			return False
	return True


def loadSavedGame():
	"""Try to load the saved game data"""
	global gameBoard
	with open(SAVE_FILENAME, 'r') as saveFile:
		try:
			linesFromSaveFile = saveFile.readlines()
			timeOfPreviousSave = linesFromSaveFile[3].strip()
			useExistingSave = input(f"{INFO_SYMBOL} Would you like to load the saved game from {timeOfPreviousSave}? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			if useExistingSave != 'y':
				print(f"{INFO_SYMBOL} Starting a new game...\n")
				return None, None
			lineNum = 0
			currentLine = linesFromSaveFile[lineNum].strip()
			while currentLine != "SAVE STATE:":
				lineNum += 1
				currentLine = linesFromSaveFile[lineNum].strip()
			lineNum += 1
			currentLine = linesFromSaveFile[lineNum].strip()
			boardFromSaveFile = []
			while not currentLine.startswith("User piece"):
				piecesInRow = currentLine.split()
				for index, piece in enumerate(piecesInRow):
					if piece == "-":
						piecesInRow[index] = EMPTY
				boardFromSaveFile.append(piecesInRow)
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
			return turn, userPiece
		except Exception:
			print(f"{ERROR_SYMBOL} There was an issue reading from the save file. Starting a new game...\n")
			return None, None


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
			  f"{INFO_SYMBOL} Pass the name of your Python file as a command line argument.")
		exit(0)
	except AttributeError:
		print(f"{ERROR_SYMBOL} Please make sure your AI's class name is 'Strategy'")
		exit(0)


def main():
	"""main method that prompts the user for input"""
	global gameBoard, USER_PIECE
	players = {}
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
	os.system("") # allows colored terminal to work on Windows OS
	print("""
  _______ _        _______           _______                    _____ 
 |__   __(_)      |__   __|         |__   __|             /\\   |_   _|
    | |   _  ___     | | __ _  ___     | | ___   ___     /  \\    | |  
    | |  | |/ __|    | |/ _` |/ __|    | |/ _ \\ / _ \\   / /\\ \\   | |  
    | |  | | (__     | | (_| | (__     | | (_) |  __/  / ____ \\ _| |_ 
    |_|  |_|\\___|    |_|\\__,_|\\___|    |_|\\___/ \\___| /_/    \\_\\_____|
                                                                      
                                                                      
		""")
	print("Type 's' at any prompt to save the game.")
	print("Type 'h' to see previous moves.")
	print("Press 'q' at any point to quit.")

	turn = X_PIECE
	useSavedGame = False
	if os.path.exists(SAVE_FILENAME):
		turnFromSaveFile, USER_PIECE = loadSavedGame()
		if turnFromSaveFile is not None:
			turn = turnFromSaveFile
			opponentPiece = opponentOf(USER_PIECE)
			useSavedGame = True
			BOARD_HISTORY.append(copyOfBoard(gameBoard))
	if not useSavedGame:
		userPieceSelect = input("\nDo you want to be X or O? (X goes first)\t").strip().lower()
		erasePreviousLines(1)
		while userPieceSelect not in ['x', 'o']:
			if userPieceSelect == 'q':
				print("Thanks for playing!\n")
				exit(0)
			userPieceSelect = input(f"{ERROR_SYMBOL} Invalid input. Please choose either X or O:\t").strip().lower()
			erasePreviousLines(1)
		if userPieceSelect == 'x':
			USER_PIECE = X_PIECE
			opponentPiece = O_PIECE
		else:
			USER_PIECE = O_PIECE
			opponentPiece = X_PIECE
	print(f"{'Your AI' if AI_DUEL_MODE else 'Human'}: {GREEN_COLOR}{USER_PIECE}{NO_COLOR}")
	print(f"{'My AI' if AI_DUEL_MODE else 'AI'}: {RED_COLOR}{opponentPiece}{NO_COLOR}")

	players[opponentPiece] = Strategy(opponentPiece)
	players[USER_PIECE] = UserPlayerClass(USER_PIECE)

	printGameBoard()

	first_turn = True
	gameOver, winner = False, None
	while not gameOver:
		if AI_DUEL_MODE:
			nameOfPlayer = "My AI" if turn == opponentPiece else "Your AI"
		else:
			nameOfPlayer = "AI" if turn == opponentPiece else "You"
		currentPlayer = players[turn]
		if currentPlayer.isAI:
			userInput = input(f"{nameOfPlayer}'s turn, press enter for it to play.\t").strip().upper()
			erasePreviousLines(1)
			while userInput in ['Q', 'S', 'H']:
				if userInput == 'Q':
					print("\nThanks for playing!\n")
					exit(0)
				elif userInput == 'H':
					userInput = getBoardHistoryInputFromUser(True)
				else:
					saveGame(turn)
					userInput = input(f"{nameOfPlayer}'s turn, press enter for it to play.\t").strip().upper()
					erasePreviousLines(2)
		rowPlayed, colPlayed = currentPlayer.getMove(gameBoard)
		performMove(gameBoard, rowPlayed, colPlayed, turn)
		BOARD_HISTORY.append(copyOfBoard(gameBoard))
		erasePreviousLines(BOARD_OUTPUT_HEIGHT + (1 if first_turn else 2))
		first_turn = False
		printGameBoard()
		move_formatted = ROW_LABELS[rowPlayed] + str(colPlayed + 1)
		print(f"{nameOfPlayer} played in spot {move_formatted}")
		turn = opponentOf(turn)
		gameOver, winner = isTerminal(gameBoard)

	if winner is None:
		print("Nobody wins, it's a tie!\n")
	else:
		highlightColor = GREEN_COLOR if winner == USER_PIECE else RED_COLOR
		print(f"{highlightColor}{winner}{NO_COLOR} player wins!\n")


if __name__ == "__main__":
	main()


