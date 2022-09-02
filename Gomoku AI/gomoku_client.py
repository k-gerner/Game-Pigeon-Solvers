# Kyle Gerner
# Started 3.22.2021
# Gomoku solver, client facing

import strategy
import time
import os
import sys
from Player import Player

EMPTY, BLACK, WHITE = '.', 'X', 'O'
gameBoard = [] # created later
playerColor = None
GREEN_COLOR, RED_COLOR, NO_COLOR = '\033[92m', '\033[91m', '\033[0m' 		# green, red, white
MOST_RECENT_HIGHLIGHT_COLOR = '\u001b[48;5;238m' # dark grey; to make lighter, increase 238 to anything 255 or below

ERASE_MODE_ON = True
BOARD_OUTPUT_HEIGHT = -1
SAVE_STATE_OUTPUT_HEIGHT = -1
COLUMN_LABELS = "<Will be filled later>"

CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"
# class for the Human player
class HumanPlayer(Player):

	def __init__(self, color):
		super().__init__(color, isAI=False)

	def getMove(self, board):
		"""Takes in the user's input and returns the move"""
		spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (COLUMN_LABELS[-1], len(board))).strip().upper()
		erasePreviousLines(1)
		displayingSave = False
		linesToEraseOnSave = BOARD_OUTPUT_HEIGHT + 1
		while True:
			if spot.lower() == 'q':
				if displayingSave:
					printGameBoard()
				print("\nThanks for playing!\n")
				exit(0)
			elif spot.lower() == 's':
				displayingSave = True
				erasePreviousLines(linesToEraseOnSave)
				linesToEraseOnSave = 0
				givePythonCodeForBoardInput()
				spot = input("Enter a coordinates for a move, or press 'q' to quit:\t").strip().upper()
				erasePreviousLines(SAVE_STATE_OUTPUT_HEIGHT + 1)
			elif len(spot) >= 4 or len(spot) == 0 or spot[0] not in COLUMN_LABELS or not spot[1:].isdigit() or int(spot[1:]) > len(board) or int(spot[1:]) < 1:
				if displayingSave:
					printGameBoard()
					print("\n")
				spot = input(f"{ERROR_SYMBOL} Invalid input. Please try again.\t").strip().upper()
				erasePreviousLines(1)
				displayingSave = False
				linesToEraseOnSave = BOARD_OUTPUT_HEIGHT + 1
			elif board[int(spot[1:]) - 1][COLUMN_LABELS.index(spot[0])] != EMPTY:
				if displayingSave:
					printGameBoard()
					print("\n")
				spot = input(f"{ERROR_SYMBOL} That spot is already taken, please choose another:\t").strip().upper()
				erasePreviousLines(1)
				displayingSave = False
				linesToEraseOnSave = BOARD_OUTPUT_HEIGHT + 1
			else:
				break
		if displayingSave:
			printGameBoard()
			print("\n")
		row = int(spot[1:]) - 1
		col = COLUMN_LABELS.index(spot[0])
		ai.performMove(board, row, col, playerColor)
		ai.checkGameState(board)
		return [row, col]


def createGameBoard(dimension):
	"""Creates the gameBoard with the specified number of rows and columns"""
	for i in range(dimension):
		row = []
		for j in range(dimension):
			row.append(EMPTY)
		gameBoard.append(row)
	# paste board save state here if applicable

def printGameBoard(mostRecentMove=None):
	"""Prints the gameBoard in a human readable format"""
	columnLabels = list(map(chr, range(65, 65 + len(gameBoard))))
	print("\n\t    %s" % " ".join(columnLabels))
	for rowNum in range(len(gameBoard)):
		print("\t%d%s| " % (rowNum+1, "" if rowNum > 8 else " "), end = '')
		for colNum in range(len(gameBoard[rowNum])):
			spot = gameBoard[rowNum][colNum]
			pieceColor = MOST_RECENT_HIGHLIGHT_COLOR if [rowNum, colNum] == mostRecentMove else ''
			pieceColor += GREEN_COLOR if spot == playerColor else RED_COLOR
			if spot == EMPTY:
				print("%s " % spot, end='')
			else:
				print(f"{pieceColor}%s{NO_COLOR} " % spot, end = '')

		print("")
	print()

def givePythonCodeForBoardInput():
	"""
	Prints out the Python code needed to recreate the game board at this state
	For debugging purposes
	"""
	print("\n# Copy and paste this code into createGameBoard():\n")
	print("gameBoard = []")
	for i in range(len(gameBoard)):
		strRepOfRow = ""
		for spot in gameBoard[i]:
			strRepOfRow += spot + " "
		print("gameBoard.append(\"%s\".split())" % (strRepOfRow))
	print()

def printAsciiTitleArt():
	"""Prints the fancy text when you start the program"""
	print('\n\t    _  __     _      _')
	print('\t   | |/ /   _| | ___( )___')
	print('\t   | \' / | | | |/ _ \\// __|')
	print('\t   | . \\ |_| | |  __/ \\__ \\')
	print('\t   |_|\\_\\__, |_|\\___| |___/')
	print('   ___\t        |___/        _               _    ___')
	print(' / ___| ___  _ __ ___   ___ | | ___   _     / \\  |_ _|')
	print('| |  _ / _ \\| \'_ ` _ \\ / _ \\| |/ / | | |   / _ \\  | |')
	print('| |_| | (_) | | | | | | (_) |   <| |_| |  / ___ \\ | |')
	print(' \\____|\\___/|_| |_| |_|\\___/|_|\\\\_\\__,_| /_/   \\_\\___|\n')


def erasePreviousLines(numLines, overrideEraseMode=False):
	"""Erases the specified previous number of lines from the terminal"""
	eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
	if eraseMode:
		print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')


def main():
	"""main method that prompts the user for input"""
	global ai, gameBoard, playerColor, BOARD_OUTPUT_HEIGHT, SAVE_STATE_OUTPUT_HEIGHT, COLUMN_LABELS
	os.system("") # allows colored terminal to work on Windows OS
	if len(sys.argv) == 2 and sys.argv[1] in ["-e", "-eraseModeOff"]:
		global ERASE_MODE_ON
		ERASE_MODE_ON = False
	printAsciiTitleArt()
	boardDimension = input("What is the dimension of the board? (Default is 13x13)\nEnter a single odd number:\t").strip()
	erasePreviousLines(2)
	if boardDimension.isdigit() and int(boardDimension) % 2 == 1 and 6 < int(boardDimension) < 100:
		boardDimension = int(boardDimension)
		print("The board will be %dx%d!" % (boardDimension, boardDimension))
	else:
		boardDimension = 13
		print("Invalid input. The board will be 13x13!")
	COLUMN_LABELS = list(map(chr, range(65, 65 + boardDimension)))
	BOARD_OUTPUT_HEIGHT = boardDimension + 4
	SAVE_STATE_OUTPUT_HEIGHT = boardDimension + 5
	playerColorInput = input("Would you like to be BLACK ('b') or WHITE ('w')? (black goes first!):\t").strip().lower()
	erasePreviousLines(2)
	if playerColorInput == 'b':
		playerColor = BLACK
		print(f"You will be {GREEN_COLOR}BLACK{NO_COLOR}!")
	else:
		playerColor = WHITE
		if playerColorInput == 'w':
			print(f"You will be {GREEN_COLOR}WHITE{NO_COLOR}!")
		else:
			print(f"Invalid input. You'll be {GREEN_COLOR}WHITE{NO_COLOR}!")

	ai = strategy.Strategy(boardDimension, playerColor)
	print(f"\nYou: {GREEN_COLOR}%s{NO_COLOR}\tAI: {RED_COLOR}%s{NO_COLOR}" % (playerColor, ai.opponentOf(playerColor)))
	print("Press 'q' at any prompt to quit.\nType 's' to print out the board's save state.")
	turn = BLACK
	createGameBoard(int(boardDimension))
	columnLabels = list(map(chr, range(65, 65 + len(gameBoard))))
	printGameBoard()
	print("\n")

	human = HumanPlayer(playerColor)

	while not ai.GAME_OVER:
		if turn == playerColor:
			additionalOutput = ""
			rowPlayed, colPlayed = human.getMove(gameBoard)
		else:
			userInput = input("It's the AI's turn, press enter for it to play.\t").strip().lower()
			displayingSave = False
			while userInput == 'q' or userInput == 's':
				if userInput == 'q':
					if displayingSave:
						printGameBoard()
					print("\nThanks for playing!\n")
					exit(0)
				else:
					if not displayingSave:
						erasePreviousLines(BOARD_OUTPUT_HEIGHT + 1)
					displayingSave = True
					givePythonCodeForBoardInput()
					userInput = input("Press enter for the AI to play, or press 'q' to quit:\t").strip().lower()
					erasePreviousLines(SAVE_STATE_OUTPUT_HEIGHT + 1)
			if displayingSave and ERASE_MODE_ON:
				erasePreviousLines(1)
				printGameBoard()
				print("\n\n")
			startTime = time.time()
			rowPlayed, colPlayed = ai.playBestMove(gameBoard)
			endTime = time.time()
			minutesTaken, secondsTaken = int(endTime - startTime) // 60, (endTime - startTime) % 60
			additionalOutput = ("  (%dm " if minutesTaken > 0 else "  (") + ("%.2fs)" % secondsTaken)

		erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2 + (-1 if turn == playerColor else 0))
		printGameBoard([rowPlayed, colPlayed])
		moveFormatted = columnLabels[colPlayed] + str(rowPlayed + 1)
		print("%s played in spot %s%s\n" % ("You" if turn == playerColor else "AI", moveFormatted, additionalOutput))
		turn = ai.opponentOf(turn) # switch the turn

	boardCompletelyFilled = True
	for row in gameBoard:
		for spot in row:
			if spot == EMPTY:
				boardCompletelyFilled = False
				break

	if boardCompletelyFilled:
		print("Nobody wins, it's a tie!")
	else:
		highlightColor = GREEN_COLOR if turn == ai.opponentOf(playerColor) else RED_COLOR
		winner = "BLACK" if ai.opponentOf(turn) == BLACK else "WHITE"
		print(f"{highlightColor}{winner}{NO_COLOR} wins!\n")



if __name__ == "__main__":
	main()