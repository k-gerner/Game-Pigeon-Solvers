# Kyle Gerner
# Started 3.22.2021
# Gomoku solver, client facing
from datetime import datetime
from util.terminaloutput.colors import GREEN_COLOR, RED_COLOR, NO_COLOR, \
	DARK_GREY_BACKGROUND as MOST_RECENT_HIGHLIGHT_COLOR
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL
from util.terminaloutput.erasing import erasePreviousLines
from util.save.saving import path_to_save_file, allow_save
from util.aiduel.dueling import get_dueling_ai_class

from gomoku.gomoku_strategy import GomokuStrategy, opponentOf, performMove, copyOfBoard
import time
import os
import sys
from gomoku.gomoku_player import GomokuPlayer

EMPTY, BLACK, WHITE = '.', 'X', 'O'
gameBoard = [] # created later
userPiece = None

BOARD_OUTPUT_HEIGHT = -1
BOARD_DIMENSION = 10
TIME_TAKEN_PER_PLAYER = {}
COLUMN_LABELS = "<Will be filled later>"
SAVE_FILENAME = path_to_save_file("gomoku_save.txt")
BOARD_HISTORY = [] # [highlightCoordinates, board]


# class for the Human player
class HumanPlayer(GomokuPlayer):

	def __init__(self, color):
		super().__init__(color, isAI=False)

	def getMove(self, board):
		"""Takes in the user's input and returns the move"""
		spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (COLUMN_LABELS[-1], len(board))).strip().upper()
		erasePreviousLines(1)
		while True:
			if spot == 'Q':
				printAverageTimeTakenByPlayers()
				print("\nThanks for playing!\n")
				exit(0)
			elif spot == 'S':
				saveGame(board, self.color)
				spot = input("Enter a coordinates for a move, or press 'q' to quit:\t").strip().upper()
				erasePreviousLines(2)
			elif spot == 'H':
				spot = getBoardHistoryInputFromUser(isAi=False)
			elif len(spot) >= 4 or len(spot) == 0 or spot[0] not in COLUMN_LABELS or not spot[1:].isdigit() or int(spot[1:]) > len(board) or int(spot[1:]) < 1:
				spot = input(f"{ERROR_SYMBOL} Invalid input. Please try again.\t").strip().upper()
				erasePreviousLines(1)
			elif board[int(spot[1:]) - 1][COLUMN_LABELS.index(spot[0])] != EMPTY:
				spot = input(f"{ERROR_SYMBOL} That spot is already taken, please choose another:\t").strip().upper()
				erasePreviousLines(1)
			else:
				break
		row = int(spot[1:]) - 1
		col = COLUMN_LABELS.index(spot[0])
		return row, col


def createEmptyGameBoard(dimension):
	"""Creates the gameBoard with the specified number of rows and columns"""
	for i in range(dimension):
		row = []
		for j in range(dimension):
			row.append(EMPTY)
		gameBoard.append(row)


def printGameBoard(highlightCoordinates=None, board=None):
	"""Prints the gameBoard in a human-readable format"""
	if highlightCoordinates is None:
		highlightCoordinates = []
	if board is None:
		board = gameBoard
	print("\n\t    %s" % " ".join(COLUMN_LABELS))
	for rowNum in range(len(board)):
		print("\t%d%s| " % (rowNum+1, "" if rowNum > 8 else " "), end = '')
		for colNum in range(len(board[rowNum])):
			spot = board[rowNum][colNum]
			pieceColor = MOST_RECENT_HIGHLIGHT_COLOR if [rowNum, colNum] in highlightCoordinates else ''
			pieceColor += GREEN_COLOR if spot == userPiece else RED_COLOR
			if spot == EMPTY:
				print(f"{spot} ", end='')
			else:
				print(f"{pieceColor}{spot}{NO_COLOR} ", end = '')
		print("")
	print()


def printMoveHistory(numMovesPrevious):
	"""Prints the move history of the current game"""
	while True:
		printGameBoard(BOARD_HISTORY[-(numMovesPrevious + 1)][0], BOARD_HISTORY[-(numMovesPrevious + 1)][1])
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
			erasePreviousLines(BOARD_DIMENSION + 3)
			printGameBoard(BOARD_HISTORY[-1][0])
			userInput = input(f"{INFO_SYMBOL} You're back in play mode. {nextMovePrompt}   ").strip().upper()
			erasePreviousLines(1)
			print("\n") # make this output the same height as the other options
		else:
			userInput = input(f"{ERROR_SYMBOL} Invalid input. {nextMovePrompt}   ").strip().upper()
			erasePreviousLines(1)
	return userInput


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


def printAverageTimeTakenByPlayers():
	"""Prints out the average time taken per move for each player"""
	opponentPiece = opponentOf(userPiece)
	userTimeTaken = round(TIME_TAKEN_PER_PLAYER[userPiece][1]/max(1, TIME_TAKEN_PER_PLAYER[userPiece][2]), 2)
	aiTimeTaken = round(TIME_TAKEN_PER_PLAYER[opponentPiece][1]/max(1, TIME_TAKEN_PER_PLAYER[opponentPiece][2]), 2)
	print("Average time taken per move:")
	print(f"{GREEN_COLOR}{TIME_TAKEN_PER_PLAYER[userPiece][0]}{NO_COLOR}: {userTimeTaken}s")
	print(f"{RED_COLOR}{TIME_TAKEN_PER_PLAYER[opponentPiece][0]}{NO_COLOR}: {aiTimeTaken}s")


def saveGame(board, turn):
	"""Saves the given board state to a save file"""
	if not allow_save(SAVE_FILENAME):
		return
	with open(SAVE_FILENAME, 'w') as saveFile:
		saveFile.write("This file contains the save state of a previously played game.\n")
		saveFile.write("Modifying this file may cause issues with loading the save state.\n\n")
		timeOfSave = datetime.now().strftime("%m/%d/%Y at %I:%M:%S %p")
		saveFile.write(timeOfSave + "\n\n")
		saveFile.write("SAVE STATE:\n")
		for row in board:
			saveFile.write(" ".join(row) + "\n")
		saveFile.write(f"User piece: " + str(userPiece)  +"\n")
		saveFile.write("Opponent piece: " + opponentOf(userPiece)  +"\n")
		saveFile.write("Turn: " + turn)
	print(f"{INFO_SYMBOL} The game has been saved!")


def validateLoadedSaveState(board, piece, turn):
	"""Make sure the state loaded from the save file is valid. Returns a boolean"""
	if piece not in [BLACK, WHITE]:
		print(f"{ERROR_SYMBOL} Invalid user piece!")
		return False
	if turn not in [BLACK, WHITE]:
		print(f"{ERROR_SYMBOL} Invalid player turn!")
		return False
	boardDimension = len(board)
	if not 6 < boardDimension < 100:
		print(f"{ERROR_SYMBOL} Invalid board dimension!")
		return False
	for row in board:
		if len(row) != boardDimension:
			print(f"{ERROR_SYMBOL} Board is not square!")
			return False
		if row.count(EMPTY) + row.count(BLACK) + row.count(WHITE) != boardDimension:
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
				print(f"{INFO_SYMBOL} Starting a new game...")
				return
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
			gameBoard = board
			deleteSaveFile = input(f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			fileDeletedText = ""
			if deleteSaveFile == 'y':
				os.remove(SAVE_FILENAME)
				fileDeletedText = "Save file deleted. "
			print(f"{INFO_SYMBOL} %sResuming saved game..." % fileDeletedText )
			return turn
		except:
			print(f"{ERROR_SYMBOL} There was an issue reading from the save file. Starting a new game...")
			return None


def run():
	"""main method that prompts the user for input"""
	global gameBoard, userPiece, BOARD_OUTPUT_HEIGHT, COLUMN_LABELS, TIME_TAKEN_PER_PLAYER, BOARD_DIMENSION
	if "-d" in sys.argv or "-aiDuel" in sys.argv:
		UserPlayerClass = get_dueling_ai_class(GomokuPlayer, "GomokuStrategy")
		print(f"\n{INFO_SYMBOL} You are in AI Duel Mode!")
		AI_DUEL_MODE = True
	else:
		UserPlayerClass = HumanPlayer
		AI_DUEL_MODE = False

	printAsciiTitleArt()

	turn = BLACK
	useSavedGame = False
	if os.path.exists(SAVE_FILENAME):
		turnFromSaveFile = loadSavedGame()
		if turnFromSaveFile is not None:
			turn = turnFromSaveFile
			useSavedGame = True
			BOARD_HISTORY.append([[], copyOfBoard(gameBoard)])

	userPlayerName = "Your AI" if AI_DUEL_MODE else "You"
	aiPlayerName = "My AI" if AI_DUEL_MODE else "AI"
	if useSavedGame:
		opponentPiece = opponentOf(userPiece)
		boardDimension = len(gameBoard)
	else:
		boardDimension = input("What is the dimension of the board? (Default is 13x13)\nEnter a single odd number:\t").strip()
		erasePreviousLines(2)
		if boardDimension.isdigit() and int(boardDimension) % 2 == 1 and 6 < int(boardDimension) < 100:
			boardDimension = int(boardDimension)
			print("The board will be %dx%d!" % (boardDimension, boardDimension))
		else:
			boardDimension = 13
			print(f"{ERROR_SYMBOL} Invalid input. The board will be 13x13!")
		createEmptyGameBoard(int(boardDimension))

		playerColorInput = input("Would you like to be BLACK ('b') or WHITE ('w')? (black goes first!):\t").strip().lower()
		erasePreviousLines(2)
		if playerColorInput == 'b':
			userPiece = BLACK
			opponentPiece = WHITE
			print(f"{userPlayerName} will be {GREEN_COLOR}BLACK{NO_COLOR}!")
		else:
			userPiece = WHITE
			opponentPiece = BLACK
			if playerColorInput == 'w':
				print(f"{userPlayerName} will be {GREEN_COLOR}WHITE{NO_COLOR}!")
			else:
				print(f"{ERROR_SYMBOL} Invalid input. {userPlayerName} will be {GREEN_COLOR}WHITE{NO_COLOR}!")

	TIME_TAKEN_PER_PLAYER = {
		userPiece: [userPlayerName, 0, 0],    # [player name, total time, num moves]
		opponentPiece: [aiPlayerName, 0, 0]
	}
	COLUMN_LABELS = list(map(chr, range(65, 65 + boardDimension)))
	BOARD_DIMENSION = boardDimension
	BOARD_OUTPUT_HEIGHT = boardDimension + 5
	playerNames = {userPiece: userPlayerName, opponentPiece: aiPlayerName}
	players = {opponentPiece: GomokuStrategy(opponentPiece, boardDimension), userPiece: UserPlayerClass(userPiece)}

	print(f"\n{userPlayerName}: {GREEN_COLOR}{userPiece}{NO_COLOR}\t{aiPlayerName}: {RED_COLOR}{opponentPiece}{NO_COLOR}")
	print("Type 'q' to quit.")
	print("Type 's' to save the game.")
	print("Type 'h' to see previous moves.")
	printGameBoard()
	print("\n")

	gameOver, winner = False, None

	while not gameOver:
		nameOfCurrentPlayer = playerNames[turn]
		currentPlayer = players[turn]
		if currentPlayer.isAI:
			userInput = input(f"{nameOfCurrentPlayer}'s turn, press enter for it to play.\t").strip().upper()
			erasePreviousLines(1)
			while userInput in ['Q', 'S', 'H']:
				if userInput == 'Q':
					printAverageTimeTakenByPlayers()
					print("\nThanks for playing!\n")
					exit(0)
				elif userInput == 'H':
					userInput = getBoardHistoryInputFromUser(isAi=True)
				else:
					saveGame(gameBoard, turn)
					userInput = input(f"Press enter for {nameOfCurrentPlayer} to play, or press 'q' to quit:\t").strip().upper()
					erasePreviousLines(2)
		startTime = time.time()
		rowPlayed, colPlayed = currentPlayer.getMove(gameBoard)
		endTime = time.time()
		totalTimeTakenForMove = endTime - startTime
		TIME_TAKEN_PER_PLAYER[turn][1] += totalTimeTakenForMove
		TIME_TAKEN_PER_PLAYER[turn][2] += 1
		minutesTaken = int(totalTimeTakenForMove) // 60
		secondsTaken = totalTimeTakenForMove % 60
		timeTakenOutputStr = ("  (%dm " % minutesTaken if minutesTaken > 0 else "  (") + ("%.2fs)" % secondsTaken) if currentPlayer.isAI else ""
		performMove(gameBoard, rowPlayed, colPlayed, turn)
		BOARD_HISTORY.append([[[rowPlayed, colPlayed]], copyOfBoard(gameBoard)])
		erasePreviousLines(BOARD_OUTPUT_HEIGHT)
		printGameBoard([[rowPlayed, colPlayed]])
		moveFormatted = COLUMN_LABELS[colPlayed] + str(rowPlayed + 1)
		print("%s played in spot %s%s\n" % (nameOfCurrentPlayer, moveFormatted, timeTakenOutputStr))
		turn = opponentOf(turn)
		gameOver, winner = players[opponentPiece].isTerminal(gameBoard)

	if winner is None:
		print("Nobody wins, it's a tie!")
	else:
		highlightColor = GREEN_COLOR if winner == userPiece else RED_COLOR
		winnerColorName = "BLACK" if winner == BLACK else "WHITE"
		print(f"{highlightColor}{winnerColorName}{NO_COLOR} wins!\n")
	printAverageTimeTakenByPlayers()
	print("\nThanks for playing!\n")
