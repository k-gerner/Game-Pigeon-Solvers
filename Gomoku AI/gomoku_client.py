# Kyle Gerner
# Started 3.22.2021
# Gomoku solver, client facing

import strategy

EMPTY, BLACK, WHITE = '.', 'X', 'O'
gameBoard = [] # created later

def createGameBoard(width):
	'''Creates the gameBoard with the specified number of columns'''
	for i in range(width):
		row = []
		for j in range(width):
			row.append(EMPTY)
		gameBoard.append(row)

def printGameBoard():
	'''Prints the gameBoard in a human readable format'''
	columnLabels = list(map(chr, range(65, 65 + len(gameBoard))))
	print("\n\t   ", end='')
	for letter in columnLabels:
		print(" %s" % letter, end='')
	print()
	for rowNum in range(len(gameBoard)):
		print("\t%d%s| " % (rowNum+1, "" if rowNum > 8 else " "), end = '')
		for spot in gameBoard[rowNum]:
			print("%s " % spot, end='')
		print("")
	print()

def getPlayerMove(playerColor):
	'''Takes in the user's input and performs that move on the board'''
	columnLabels = list(map(chr, range(65, 65 + len(gameBoard))))
	spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (columnLabels[-1], len(gameBoard))).strip().upper()
	while True:
		if len(spot) >= 4 or spot[0] not in columnLabels or not spot[1:].isdigit() or int(spot[1:]) > len(gameBoard) or int(spot[1:]) < 1:
			spot = input("Invalid input. Please try again.\t").strip().upper()
		elif not ai.isValidMove(gameBoard, int(spot[1:]) - 1, columnLabels.index(spot[0])):
			spot = input("That spot is already taken, please choose another:\t").strip().upper()
		else:
			break
	row = int(spot[1:]) - 1
	col = columnLabels.index(spot[0])
	ai.performMove(gameBoard, row, col, playerColor)
	ai.checkGameState(gameBoard)

def main():
	'''main method that prompts the user for input'''
	global ai
	global gameBoard
	print("\nWelcome to Kyle's Gomoku AI!")
	boardDimension = input("What is the dimension of the board? (Default is 13x13)\nEnter a single odd number:\t").strip()
	if boardDimension.isdigit() and int(boardDimension) % 2 == 1 and 4 < int(boardDimension) < 100:
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
	print("You: %s\tAI: %s" % (playerColor, ai.opponentOf(playerColor)))
	
	turn = BLACK
	columnLabels = list(map(chr, range(65, 65 + len(gameBoard))))
	while not ai.GAME_OVER:
		printGameBoard()
		if turn == playerColor:
			getPlayerMove(playerColor)
		else:
			ai_move_row, ai_move_col = ai.playBestMove(gameBoard)
			ai_move_formatted = columnLabels[ai_move_col] + str(ai_move_row + 1)
			print("AI played in spot %s\n" % ai_move_formatted)
		turn = ai.opponentOf(turn) # switch the turn

	winner = "BLACK" if ai.opponentOf(turn) == BLACK else "WHITE"
	printGameBoard()
	print("%s wins!\n" % winner)





if __name__ == "__main__":
    main()