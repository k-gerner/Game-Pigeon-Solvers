# Kyle Gerner
# Started 11.19.2022
# Mancala Capture, client facing
import os
import sys
import time
from datetime import datetime
from importlib import import_module
from constants import *
from Player import Player
from board_functions import *
from strategy import *

ERASE_MODE_ON = True
USE_REVERSED_PRINT_LAYOUT = False
BOARD = [4] * 6 + [0] + [4] * 6 + [0]
PLAYER1_ID = 1
PLAYER2_ID = 2
SAVE_FILENAME = "saved_game.txt"
BOARD_HISTORY = []  # [highlightPocketIndex, playerId, board]


# class for the Human player
class HumanPlayer(Player):

	def __init__(self, bankIndex=6):
		super().__init__(bankIndex, isAI=False)

	def getMove(self, board):
		"""Takes in the user's input and returns the index on the board for the selected move"""
		spot = input(f"It's your turn, which spot would you like to play? (1 - {POCKETS_PER_SIDE}):\t").strip().upper()
		erasePreviousLines(1)
		while True:
			if spot == 'Q':
				print("\nThanks for playing!\n")
				exit(0)
			elif spot == 'F':
				global USE_REVERSED_PRINT_LAYOUT
				USE_REVERSED_PRINT_LAYOUT = not USE_REVERSED_PRINT_LAYOUT
				erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
				printBoard(board)
				print("\n")
				spot = input(
					f"Board print layout changed. Which spot would you like to play? (1 - {POCKETS_PER_SIDE}):\t").strip().upper()
				erasePreviousLines(1)
			elif spot == 'S':
				saveGame(board, PLAYER1_ID)
				spot = input("Enter a coordinates for a move, or press 'q' to quit:\t").strip().upper()
				erasePreviousLines(2)
			elif spot == 'H':
				spot = getBoardHistoryInputFromUser(isAi=False)
			elif not spot.isdigit() or int(spot) < 1 or int(spot) > 6:
				spot = input(f"{ERROR_SYMBOL} Please enter a number 1 - {POCKETS_PER_SIDE}:\t").strip().upper()
				erasePreviousLines(1)
			elif board[int(spot) - 1] == 0:
				spot = input(f"{ERROR_SYMBOL} That pocket is empty! Please try again:\t").strip().upper()
				erasePreviousLines(1)
			else:
				break

		return int(spot) - 1


def printBoard(board, playerId=None, move=None):
	"""Prints the game board"""
	# orientation
	arrowIndex = -1
	if USE_REVERSED_PRINT_LAYOUT:
		topBankIndex = PLAYER1_BANK_INDEX
		bottomBankIndex = PLAYER2_BANK_INDEX
		leftSidePlayerId = PLAYER2_ID
		topLeftPocketIndex = POCKETS_PER_SIDE + 1  # which index is printed in the top left corner of the printed board
		leftSideColor = RED_COLOR
		rightSideColor = GREEN_COLOR
		if move is not None:
			arrowIndex = move if move > POCKETS_PER_SIDE else getIndexOfOppositeHole(move)
	else:
		topBankIndex = PLAYER2_BANK_INDEX
		bottomBankIndex = PLAYER1_BANK_INDEX
		leftSidePlayerId = PLAYER1_ID
		topLeftPocketIndex = 0
		leftSideColor = GREEN_COLOR
		rightSideColor = RED_COLOR
		if move is not None:
			arrowIndex = move if move < POCKETS_PER_SIDE else getIndexOfOppositeHole(move)

	print()
	print(SIDE_INDENT_STR + " " * 5 + f"{rightSideColor}{board[topBankIndex]}{NO_COLOR}")  # top bank
	print(SIDE_INDENT_STR + "___________")
	for index in range(topLeftPocketIndex, topLeftPocketIndex + POCKETS_PER_SIDE):
		leftSideStrPrefix = SIDE_INDENT_STR  # may change to arrow
		rightSideStrSuffix = ""  # may change to arrow
		if index == arrowIndex:
			if playerId == leftSidePlayerId:
				leftSideStrPrefix = LEFT_SIDE_ARROW
			else:
				rightSideStrSuffix = RIGHT_SIDE_ARROW

		leftSideStr = leftSideStrPrefix + " " * 2 \
					  + f"{leftSideColor}{board[index]}{NO_COLOR}" \
					  + (" " if board[index] >= 10 else "  ")
		rightSideStr = (" " if board[getIndexOfOppositeHole(index)] >= 10 else "  ") \
					   + f"{rightSideColor}{board[getIndexOfOppositeHole(index)]}{NO_COLOR}" \
					   + rightSideStrSuffix
		print(SIDE_INDENT_STR + "     |     ")
		print(leftSideStr + str(min(index, getIndexOfOppositeHole(index)) + 1) + rightSideStr)
		print(SIDE_INDENT_STR + "_____|_____")
	print("\n" + SIDE_INDENT_STR + " " * 5 + f"{leftSideColor}{board[bottomBankIndex]}{NO_COLOR}\n")  # bottom bank


def opponentOf(playerId):
	"""Gets the id opponent of the given id"""
	return PLAYER1_ID if playerId == PLAYER2_ID else PLAYER2_ID


def printAverageTimeTakenByPlayers(timeTakenPerPlayer):
	"""Prints out the average time taken per move for each player"""
	userTimeTaken = round(timeTakenPerPlayer[PLAYER1_ID][1] / max(1, timeTakenPerPlayer[PLAYER1_ID][2]), 2)
	aiTimeTaken = round(timeTakenPerPlayer[PLAYER2_ID][1] / max(1, timeTakenPerPlayer[PLAYER2_ID][2]), 2)
	print("Average time taken per move:")
	print(f"{GREEN_COLOR}{timeTakenPerPlayer[PLAYER1_ID][0]}{NO_COLOR}: {userTimeTaken}s")
	print(f"{RED_COLOR}{timeTakenPerPlayer[PLAYER2_ID][0]}{NO_COLOR}: {aiTimeTaken}s")


def printAsciiArt():
	"""Prints the Mancala Capture Ascii Art"""
	print("""
  __  __                       _       
 |  \/  |                     | |      
 | \  / | __ _ _ __   ___ __ _| | __ _ 
 | |\/| |/ _` | '_ \ / __/ _` | |/ _` |
 | |  | | (_| | | | | (_| (_| | | (_| |
 |_|__|_|\__,_|_| |_|\___\__,_|_|\__,_|
  / ____|          | |                 
 | |     __ _ _ __ | |_ _   _ _ __ ___ 
 | |    / _` | '_ \| __| | | | '__/ _ \ 
 | |___| (_| | |_) | |_| |_| | | |  __/
  \_____\__,_| .__/ \__|\__,_|_|  \___|
             | |                       
             |_|  
    """)


def erasePreviousLines(numLines, overrideEraseMode=False):
	"""Erases the specified previous number of lines from the terminal"""
	eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
	if eraseMode:
		print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(int(numLines), 0), end='')


def saveGame(board, turn):
	"""Saves the given board state to a save file"""
	if os.path.exists(SAVE_FILENAME):
		with open(SAVE_FILENAME, 'r') as saveFile:
			try:
				timeOfPreviousSave = saveFile.readlines()[3].strip()
				overwrite = input(
					f"{INFO_SYMBOL} A save state already exists from {timeOfPreviousSave}.\nIs it okay to overwrite it? (y/n)\t").strip().lower()
				erasePreviousLines(1)
				while overwrite not in ['y', 'n']:
					erasePreviousLines(1)
					overwrite = input(
						f"{ERROR_SYMBOL} Invalid input. Is it okay to overwrite the existing save state? (y/n)\t").strip().lower()
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
		saveFile.write(f"   {board[PLAYER2_BANK_INDEX]}\n")  # opponent bank
		for row in range(len(board) // 2 - 1):  # playable caves; default 1 - 6
			saveFile.write(
				str(board[row]) + (" | " if board[row] >= 10 else "  | ") + str(board[-1 * (row + 2)]) + "\n")
		saveFile.write(f"   {str(board[PLAYER1_BANK_INDEX])}\n")  # player bank
		saveFile.write(f"Turn: {turn}")
	print(f"{INFO_SYMBOL} The game has been saved!")


def validateLoadedSaveState(board, turn):
	"""Make sure the state loaded from the save file is valid. Returns a boolean"""
	if turn not in [PLAYER1_ID, PLAYER2_ID]:
		print(f"{ERROR_SYMBOL} Invalid player turn!")
		return False
	if len(board) % 2 != 0:
		print(f"{ERROR_SYMBOL} Please ensure each player has a bank and the same number of pockets!")
		return False
	num_rows = len(board) // 2 - 1
	if num_rows != POCKETS_PER_SIDE:
		print(f"{ERROR_SYMBOL} # Rows must be {POCKETS_PER_SIDE}! Was {num_rows}")
		return False
	for spot in board:
		if spot < 0:
			print(f"{ERROR_SYMBOL} Pockets cannot have a negative amount of pebbles!")
			return False
	return True


def loadSavedGame():
	"""Try to load the saved game data"""
	global BOARD
	with open(SAVE_FILENAME, 'r') as saveFile:
		try:
			linesFromSaveFile = saveFile.readlines()
			timeOfPreviousSave = linesFromSaveFile[3].strip()
			useExistingSave = input(
				f"{INFO_SYMBOL} Would you like to load the saved game from {timeOfPreviousSave}? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			if useExistingSave != 'y':
				print(f"{INFO_SYMBOL} Starting a new game...")
				return
			lineNum = 0
			currentLine = linesFromSaveFile[lineNum].strip()
			while currentLine != "SAVE STATE:":
				lineNum += 1
				currentLine = linesFromSaveFile[lineNum].strip()
			lineNum += 1
			currentLine = linesFromSaveFile[lineNum].strip()

			opponent_bank = [int(currentLine.strip())]
			lineNum += 1
			currentLine = linesFromSaveFile[lineNum].strip()

			user_pockets = []
			opponent_pockets = []
			while "|" in currentLine:
				user_pockets.append(int(currentLine.split("|")[0].strip()))
				opponent_pockets.append(int(currentLine.split("|")[1].strip()))
				lineNum += 1
				currentLine = linesFromSaveFile[lineNum].strip()
			user_bank = [int(currentLine.strip())]
			board = user_pockets + user_bank + opponent_pockets + opponent_bank

			while not currentLine.startswith("Turn:"):
				lineNum += 1
				currentLine = linesFromSaveFile[lineNum].strip()
			turn = int(currentLine.split()[1])

			if not validateLoadedSaveState(board, turn):
				raise ValueError
			BOARD = board
			deleteSaveFile = input(
				f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			fileDeletedText = ""
			if deleteSaveFile == 'y':
				os.remove(SAVE_FILENAME)
				fileDeletedText = "Save file deleted."
			print(f"{INFO_SYMBOL} {fileDeletedText} Resuming saved game...")
			return turn
		except:
			print(f"{ERROR_SYMBOL} There was an issue reading from the save file. Starting a new game...")
			return None


def printMoveHistory(numMovesPrevious):
	"""Prints the move history of the current game"""
	while True:
		erasePreviousLines(2)
		printBoard(BOARD_HISTORY[-(numMovesPrevious + 1)][2], BOARD_HISTORY[-(numMovesPrevious + 1)][1],
				   BOARD_HISTORY[-(numMovesPrevious + 1)][0])
		if numMovesPrevious == 0:
			return
		print("(%d move%s before current board state)\n" % (numMovesPrevious, "s" if numMovesPrevious != 1 else ""))
		numMovesPrevious -= 1
		userInput = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
		erasePreviousLines(1)
		if userInput == 'q':
			erasePreviousLines(2)
			printAverageTimeTakenByPlayers()
			print("\nThanks for playing!\n")
			exit(0)
		elif userInput == 'e':
			erasePreviousLines(2)
			return
		else:
			erasePreviousLines(BOARD_OUTPUT_HEIGHT)


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
			erasePreviousLines(BOARD_OUTPUT_HEIGHT)
			printMoveHistory(int(numMovesPrevious))
			erasePreviousLines(BOARD_OUTPUT_HEIGHT)
			printBoard(BOARD_HISTORY[-1][2], BOARD_HISTORY[-1][1], BOARD_HISTORY[-1][0])
			userInput = input(f"{INFO_SYMBOL} You're back in play mode. {nextMovePrompt}   ").strip().upper()
			erasePreviousLines(1)
			print("\n")  # make this output the same height as the other options
		else:
			userInput = input(f"{ERROR_SYMBOL} Invalid input. {nextMovePrompt}   ").strip().upper()
			erasePreviousLines(1)
	return userInput


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
	os.system("")  # allows colored terminal to work on Windows OS
	printAsciiArt()

	players = {  # remove hardcode values later
		PLAYER1_ID: UserPlayerClass(PLAYER1_BANK_INDEX),
		PLAYER2_ID: Strategy(PLAYER2_BANK_INDEX)
	}
	nameOfPlayer1 = "Your AI" if AI_DUEL_MODE else "Human"
	nameOfPlayer2 = "My AI" if AI_DUEL_MODE else "AI"
	playerNames = {
		PLAYER1_ID: nameOfPlayer1,
		PLAYER2_ID: nameOfPlayer2
	}
	timeTakenPerPlayer = {
		PLAYER1_ID: [nameOfPlayer1, 0, 0],  # [player name, total time, num moves]
		PLAYER2_ID: [nameOfPlayer2, 0, 0]
	}

	turn = PLAYER1_ID
	useSavedGame = False
	if os.path.exists(SAVE_FILENAME):
		turnFromSaveFile = loadSavedGame()
		if turnFromSaveFile is not None:
			turn = turnFromSaveFile
			useSavedGame = True
			BOARD_HISTORY.append([-1, turn, BOARD.copy()])

	if not useSavedGame:
		userGoFirst = input("Would you like to go first? (y/n):\t").strip().upper()
		erasePreviousLines(1)
		if userGoFirst == "Y":
			turn = PLAYER1_ID
			print("%s will go first!" % playerNames[turn])
		else:
			turn = PLAYER2_ID
			print("%s will go first!" % playerNames[turn])

	print("Type 'q' to quit.")
	print("Type 'f' to flip the board orientation 180 degrees.")
	print("Type 's' to save the game.")
	print("Type 'h' to see previous moves.")

	gameOver = False
	printBoard(BOARD)
	print("\n")
	extraLinesPrinted = 2
	while not gameOver:
		nameOfCurrentPlayer = playerNames[turn]
		currentPlayer = players[turn]
		if currentPlayer.isAI:
			userInput = input(f"{nameOfCurrentPlayer}'s turn, press enter for it to play.\t").strip().upper()
			erasePreviousLines(1)
			while userInput in ['Q', 'H', 'F', 'S']:
				if userInput == 'Q':
					printAverageTimeTakenByPlayers(timeTakenPerPlayer)
					print("\nThanks for playing!\n")
					exit(0)
				elif userInput == 'H':
					userInput = getBoardHistoryInputFromUser(isAi=True)
				elif userInput == 'F':
					global USE_REVERSED_PRINT_LAYOUT
					USE_REVERSED_PRINT_LAYOUT = not USE_REVERSED_PRINT_LAYOUT
					erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
					printBoard(BOARD)
					print("\n")
					userInput = input(f"Board print layout changed. Press enter to continue:\t").strip().upper()
					erasePreviousLines(1)
				else:
					saveGame(BOARD, turn)
					userInput = input(
						f"Press enter for {nameOfCurrentPlayer} to play, or press 'q' to quit:\t").strip().upper()
					erasePreviousLines(2)

		startTime = time.time()
		chosenMove = currentPlayer.getMove(BOARD)
		endTime = time.time()
		totalTimeTakenForMove = endTime - startTime
		timeTakenPerPlayer[turn][1] += totalTimeTakenForMove
		timeTakenPerPlayer[turn][2] += 1
		minutesTaken = int(totalTimeTakenForMove) // 60
		secondsTaken = totalTimeTakenForMove % 60
		timeTakenOutputStr = ("  (%dm " if minutesTaken > 0 else "  (") + (
				"%.2fs)" % secondsTaken) if currentPlayer.isAI else ""
		finalPebbleLocation = performMove(BOARD, chosenMove, currentPlayer.bankIndex)
		BOARD_HISTORY.append([chosenMove, turn, BOARD.copy()])
		erasePreviousLines(BOARD_OUTPUT_HEIGHT + extraLinesPrinted)
		printBoard(BOARD, turn, chosenMove)
		moveFormatted = str(min(BOARD_SIZE - 2 - chosenMove, chosenMove) + 1)
		print("%s played in spot %s%s. " % (nameOfCurrentPlayer, moveFormatted, timeTakenOutputStr), end='')
		if finalPebbleLocation != currentPlayer.bankIndex:
			print("\n")
			turn = opponentOf(turn)
		else:
			print("%s's move ended in their bank, so they get another turn.\n" % nameOfCurrentPlayer)
		extraLinesPrinted = 2
		gameOver = isBoardTerminal(BOARD)

	pushAllPebblesToBank(BOARD)
	erasePreviousLines(BOARD_OUTPUT_HEIGHT + extraLinesPrinted)
	printBoard(BOARD)
	winnerId = PLAYER1_ID if winningPlayerBankIndex(BOARD) == PLAYER1_BANK_INDEX else PLAYER2_ID
	if winnerId is None:
		print("It's a tie!\n")
	else:
		print("%s wins!\n" % playerNames[winnerId])
	printAverageTimeTakenByPlayers(timeTakenPerPlayer)


if __name__ == '__main__':
	main()
