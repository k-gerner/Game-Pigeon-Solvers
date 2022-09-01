# Tic Tac Toe AI client facing
# Kyle G 6.6.2021

from Player import Player
import strategy
import os
import sys

EMPTY, X_PIECE, O_PIECE = ' ', 'X', 'O'
ROW_LABELS = "ABC"
gameBoard = [[EMPTY, EMPTY, EMPTY], 
			 [EMPTY, EMPTY, EMPTY],
			 [EMPTY, EMPTY, EMPTY]]

GREEN_COLOR = '\033[92m'  # green
RED_COLOR = '\033[91m'	  # red
NO_COLOR = '\033[0m' 	  # white

ERASE_MODE_ON = True
BOARD_OUTPUT_HEIGHT = 7

CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"

# class for the Human player
class HumanPlayer(Player):

	def __init__(self, color):
		super().__init__(color)

	def getMove(self, board):
		"""Takes in the user's input and performs that move on the board, returns the move"""
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
		return [row, col]

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

def main():
	"""main method that prompts the user for input"""
	global gameBoard
	global playerPiece
	if len(sys.argv) == 2 and sys.argv[1] in ["-e", "-eraseModeOff"]:
		global ERASE_MODE_ON
		ERASE_MODE_ON = False
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
	playerPieceSelect = input("\nDo you want to be X or O? (X goes first)\t").strip().lower()
	erasePreviousLines(1)
	while playerPieceSelect not in ['x', 'o']:
		playerPieceSelect = input(f"{ERROR_SYMBOL} Invalid input. Please choose either 'x' or 'o':\t").strip().lower()
		erasePreviousLines(1)
	if playerPieceSelect == 'x':
		playerPiece = X_PIECE
		aiPiece = O_PIECE
	else:
		playerPiece = O_PIECE
		aiPiece = X_PIECE
	print(f"Human: {GREEN_COLOR}{playerPiece}{NO_COLOR}")
	print(f"AI: {RED_COLOR}{aiPiece}{NO_COLOR}")

	greenColorPiece = playerPiece
	printGameBoard(greenColorPiece)

	ai = strategy.Strategy(X_PIECE if playerPiece == O_PIECE else O_PIECE)
	turn = X_PIECE

	humanPlayer = HumanPlayer(playerPiece)

	first_turn = True
	while not ai.GAME_OVER:
		if turn == playerPiece:
			recentMove = humanPlayer.getMove(gameBoard)
			gameBoard[recentMove[0]][recentMove[1]] = playerPiece
			ai.checkGameState(gameBoard)
		else:
			# AI's turn
			userInput = input("It's the AI's turn, press enter for it to play.\t").strip().lower()
			erasePreviousLines(2)
			if userInput == 'q':
				print("\nThanks for playing!\n")
				exit(0)
			recentMove = ai.findBestMove(gameBoard)
		erasePreviousLines(BOARD_OUTPUT_HEIGHT + (0 if first_turn else 1))
		first_turn = False
		printGameBoard(greenColorPiece)
		move_formatted = ROW_LABELS[recentMove[0]] + str(recentMove[1] + 1)
		print("%s played in spot %s" % ("You" if turn == playerPiece else "AI", move_formatted))
		turn = ai.opponentOf(turn)

	boardCompletelyFilled = True
	for row in gameBoard:
		for spot in row:
			if spot == EMPTY:
				boardCompletelyFilled = False
				break

	if boardCompletelyFilled:
		print("Nobody wins, it's a tie!\n")
	else:
		winner = "X" if ai.opponentOf(turn) == X_PIECE else "O"
		highlightColor = GREEN_COLOR if winner == playerPiece else RED_COLOR
		print(f"{highlightColor}{winner}{NO_COLOR} player wins!\n")


if __name__ == "__main__":
	main()


