# Tic Tac Toe AI client facing
# Kyle G 6.6.2021

from Player import Player
from strategy import Strategy, opponentOf, isTerminal, performMove
from importlib import import_module
import os
import sys

EMPTY, X_PIECE, O_PIECE = ' ', 'X', 'O'
ROW_LABELS = "ABC"
gameBoard = [[EMPTY, EMPTY, EMPTY], 
			 [EMPTY, EMPTY, EMPTY],
			 [EMPTY, EMPTY, EMPTY]]

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

# class for the Human player
class HumanPlayer(Player):

	def __init__(self, color):
		super().__init__(color, isAI=False)

	def getMove(self, board):
		"""Takes in the user's input and returns the move"""
		spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (ROW_LABELS[-1], len(board))).strip().upper()
		while True:
			erasePreviousLines(1)
			if spot == 'Q':
				print("\nThanks for playing!\n")
				exit(0)
			elif len(spot) >= 3 or len(spot) == 0 or spot[0] not in ROW_LABELS or not spot[1:].isdigit() or int(spot[1:]) > len(board) or int(spot[1:]) < 1:
				spot = input(f"{ERROR_SYMBOL} Invalid input. Please try again.\t").strip().upper()
			elif board[ROW_LABELS.index(spot[0])][int(spot[1:]) - 1] != EMPTY:
				spot = input(f"{ERROR_SYMBOL} That spot is already taken, please choose another:\t").strip().upper()
			else:
				break
		erasePreviousLines(1)
		row = ROW_LABELS.index(spot[0])
		col = int(spot[1:]) - 1
		return row, col

def printGameBoard(pieceToHighlightGreen):
	"""Prints the gameBoard in a human-readable format"""
	print()
	for rowNum in range(len(gameBoard)):
		row = gameBoard[rowNum]
		print("\t%s  " % ROW_LABELS[rowNum], end = '')
		for colNum in range(len(row)):
			piece = gameBoard[rowNum][colNum]
			if piece == EMPTY:
				pieceColor = NO_COLOR
			elif piece == pieceToHighlightGreen:
				pieceColor = GREEN_COLOR
			else:
				pieceColor = RED_COLOR
			print(f" {pieceColor}%s{NO_COLOR} %s" % (piece, '|' if colNum < 2 else '\n'), end = '')
		if rowNum < 2:
			print("\t   ---+---+---")
	print("\t    1   2   3\n")

def erasePreviousLines(numLines, overrideEraseMode=False):
	"""Erases the specified previous number of lines from the terminal"""
	eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
	if eraseMode:
		print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')

def getOpposingAiModuleName():
	"""Reads the command line arguments to determine the name of module for the opposing AI"""
	remainingCommandLineArgs = sys.argv[2:]
	for arg in remainingCommandLineArgs:
		if "-" not in arg:
			return arg
	print(f"{ERROR_SYMBOL} You need to provide the name of your AI strategy module.")
	exit(0)

def getDuelingAi():
	"""Returns the imported AI Strategy class if it the import valid"""
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
	global gameBoard
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
	print("Press 'q' at any point to quit.")
	userPieceSelect = input("\nDo you want to be X or O? (X goes first)\t").strip().lower()
	erasePreviousLines(1)
	while userPieceSelect not in ['x', 'o']:
		if userPieceSelect == 'q':
			print("Thanks for playing!\n")
			exit(0)
		userPieceSelect = input(f"{ERROR_SYMBOL} Invalid input. Please choose either 'x' or 'o':\t").strip().lower()
		erasePreviousLines(1)
	if userPieceSelect == 'x':
		userPiece = X_PIECE
		aiPiece = O_PIECE
	else:
		userPiece = O_PIECE
		aiPiece = X_PIECE
	print(f"{'Your AI' if AI_DUEL_MODE else 'Human'}: {GREEN_COLOR}{userPiece}{NO_COLOR}")
	print(f"{'My AI' if AI_DUEL_MODE else 'AI'}: {RED_COLOR}{aiPiece}{NO_COLOR}")

	players[aiPiece] = Strategy(aiPiece)
	players[userPiece] = UserPlayerClass(userPiece)

	greenColorPiece = userPiece
	printGameBoard(greenColorPiece)

	turn = X_PIECE
	first_turn = True
	gameOver, winner = False, None
	while not gameOver:
		if AI_DUEL_MODE:
			nameOfPlayer = "My AI" if turn == aiPiece else "Your AI"
		else:
			nameOfPlayer = "AI" if turn == aiPiece else "You"
		currentPlayer = players[turn]
		if currentPlayer.isAI:
			userInput = input(f"{nameOfPlayer}'s turn, press enter for it to play.\t").strip().lower()
			if userInput == 'q':
				print("\nThanks for playing!\n")
				exit(0)
			erasePreviousLines(2)
		rowPlayed, colPlayed = currentPlayer.getMove(gameBoard)
		performMove(gameBoard, rowPlayed, colPlayed, turn)
		erasePreviousLines(BOARD_OUTPUT_HEIGHT + (0 if first_turn else 1))
		first_turn = False
		printGameBoard(greenColorPiece)
		move_formatted = ROW_LABELS[rowPlayed] + str(colPlayed + 1)
		print(f"{nameOfPlayer} played in spot {move_formatted}")
		turn = opponentOf(turn)
		gameOver, winner = isTerminal(gameBoard)

	if winner is None:
		print("Nobody wins, it's a tie!\n")
	else:
		highlightColor = GREEN_COLOR if winner == greenColorPiece else RED_COLOR
		print(f"{highlightColor}{winner}{NO_COLOR} player wins!\n")


if __name__ == "__main__":
	main()


