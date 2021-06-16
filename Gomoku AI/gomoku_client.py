# Kyle Gerner
# Started 3.22.2021
# Gomoku solver, client facing

import strategy
import time
import os

EMPTY, BLACK, WHITE = '.', 'X', 'O'
gameBoard = [] # created later
MY_COLOR, ENEMY_COLOR, NO_COLOR = '\033[92m', '\033[91m', '\033[0m' 		# green, red, white
MOST_RECENT_HIGHLIGHT_COLOR = '\u001b[48;5;238m' # dark grey; to make lighter, increase 238 to anything 255 or below

def createGameBoard(dimension):
	'''Creates the gameBoard with the specified number of rows and columns'''
	for i in range(dimension):
		row = []
		for j in range(dimension):
			row.append(EMPTY)
		gameBoard.append(row)

def printGameBoard(mostRecentMove):
	'''Prints the gameBoard in a human readable format'''
	columnLabels = list(map(chr, range(65, 65 + len(gameBoard))))
	print("\n\t    %s" % " ".join(columnLabels))
	for rowNum in range(len(gameBoard)):
		print("\t%d%s| " % (rowNum+1, "" if rowNum > 8 else " "), end = '')
		for colNum in range(len(gameBoard[rowNum])):
			# print("%s " % spot, end='')
			spot = gameBoard[rowNum][colNum]
			pieceColor = MOST_RECENT_HIGHLIGHT_COLOR if [rowNum, colNum] == mostRecentMove else ''
			pieceColor += MY_COLOR if spot == playerColor else ENEMY_COLOR
			if spot == EMPTY:
				print("%s " % spot, end='')
			else:
				print(f"{pieceColor}%s{NO_COLOR} " % spot, end = '')

		print("")
	print()

def givePythonCodeForBoardInput():
	'''
	Prints out the Python code needed to recreate the game board at this state
	For debugging purposes
	'''
	print("\n# Copy and paste this code into createGameBoard() and comment out the for loop:\n")
	for i in range(len(gameBoard)):
		strRepOfRow = ""
		for spot in gameBoard[i]:
			strRepOfRow += spot + " "
		print("row%d = \"%s\".split()" % (i + 1, strRepOfRow))
	for i in range(len(gameBoard)):
		print("gameBoard.append(row%d)" % (i + 1))
	print()

def printAsciiTitleArt():
	'''Prints the fancy text when you start the program'''
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
                                                       

def getPlayerMove():
	'''Takes in the user's input and performs that move on the board, returns the move'''
	columnLabels = list(map(chr, range(65, 65 + len(gameBoard))))
	spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (columnLabels[-1], len(gameBoard))).strip().upper()
	while True:
		if spot == 'Q':
			print("\nThanks for playing!\n")
			exit(0)
		elif spot == 'P':
			givePythonCodeForBoardInput()
			spot = input("Enter a coordinates for a move, or press 'q' to quit:\t").strip().upper()
		elif len(spot) >= 4 or len(spot) == 0 or spot[0] not in columnLabels or not spot[1:].isdigit() or int(spot[1:]) > len(gameBoard) or int(spot[1:]) < 1:
			spot = input("Invalid input. Please try again.\t").strip().upper()
		elif gameBoard[int(spot[1:]) - 1][columnLabels.index(spot[0])] != EMPTY:
			spot = input("That spot is already taken, please choose another:\t").strip().upper()
		else:
			break
	row = int(spot[1:]) - 1
	col = columnLabels.index(spot[0])
	ai.performMove(gameBoard, row, col, playerColor)
	ai.checkGameState(gameBoard)
	return [row, col]

def main():
	'''main method that prompts the user for input'''
	global ai
	global gameBoard
	global playerColor
	# print("\nWelcome to Kyle's Gomoku AI!")
	os.system("") # allows colored terminal to work on Windows OS
	printAsciiTitleArt()
	boardDimension = input("What is the dimension of the board? (Default is 13x13)\nEnter a single odd number:\t").strip()
	if boardDimension.isdigit() and int(boardDimension) % 2 == 1 and 6 < int(boardDimension) < 100:
		print("The board will be %sx%s!" % (boardDimension, boardDimension))
	else:
		boardDimension = 13
		print("Invalid input. The board will be 13x13!")
	createGameBoard(int(boardDimension))
	playerColorInput = input("Would you like to be BLACK ('b') or WHITE ('w')? (black goes first!):\t").strip().lower()
	if playerColorInput == 'b':
		playerColor = BLACK
		print("You will be black!")
	else:
		playerColor = WHITE
		if playerColorInput == 'w':
			print("You will be white!")
		else:
			print("Invalid input. You'll be white!")

	ai = strategy.Strategy(int(boardDimension), playerColor)
	print(f"\nYou: {MY_COLOR}%s{NO_COLOR}\tAI: {ENEMY_COLOR}%s{NO_COLOR}" % (playerColor, ai.opponentOf(playerColor)))
	print("Press 'q' at any prompt to quit.\nOr, press 'p' to end the game and receive Python code for recreating the gameBoard.")
	turn = BLACK
	columnLabels = list(map(chr, range(65, 65 + len(gameBoard))))
	mostRecentMove = None

	while not ai.GAME_OVER:
		printGameBoard(mostRecentMove)
		if turn == playerColor:
			mostRecentMove = getPlayerMove()
		else:
			userInput = input("It's the AI's turn, press enter for it to play.\t").strip().lower()
			while userInput == 'q' or userInput == 'p':
				if userInput == 'q':
					print("\nThanks for playing!\n")
					exit(0)
				else:
					givePythonCodeForBoardInput()
					userInput = input("Press enter for the AI to play, or press 'q' to quit:\t").strip().lower()
			startTime = time.time()
			ai_move_row, ai_move_col = ai.playBestMove(gameBoard)
			endTime = time.time()
			minutesTaken, secondsTaken = int(endTime - startTime) // 60, (endTime - startTime) % 60
			print("Time taken: %s %.2fs" % ('' if minutesTaken == 0 else '%dm' % minutesTaken, secondsTaken))
			ai_move_formatted = columnLabels[ai_move_col] + str(ai_move_row + 1)
			print("AI played in spot %s\n" % ai_move_formatted)
			mostRecentMove = [ai_move_row, ai_move_col]
		turn = ai.opponentOf(turn) # switch the turn

	printGameBoard(mostRecentMove)
	boardCompletelyFilled = True
	for row in gameBoard:
		for spot in row:
			if spot == EMPTY:
				boardCompletelyFilled = False
				break

	if boardCompletelyFilled:
		print("Nobody wins, it's a tie!")
	else:
		winner = "BLACK" if ai.opponentOf(turn) == BLACK else "WHITE"
		print("%s wins!\n" % winner)



if __name__ == "__main__":
    main()