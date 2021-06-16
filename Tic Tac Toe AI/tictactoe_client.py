# Tic Tac Toe AI client facing
# Kyle G 6.6.2021

import strategy
import os

EMPTY, X_PIECE, O_PIECE = ' ', 'X', 'O'
gameBoard = [[EMPTY, EMPTY, EMPTY], 
			 [EMPTY, EMPTY, EMPTY], 
			 [EMPTY, EMPTY, EMPTY]]

HUMAN_COLOR, AI_COLOR, NO_COLOR = '\033[92m', '\033[91m', '\033[0m' 		# green, red, white

def printGameBoard():
	'''Prints the gameBoard in a human readable format'''
	print()
	for rowNum in range(len(gameBoard)):
		row = gameBoard[rowNum]
		print("\t%s  " % "ABC"[rowNum], end = '')
		for colNum in range(len(row)):
			piece = gameBoard[rowNum][colNum]
			if piece == EMPTY:
				pieceColor = NO_COLOR
			elif piece == playerPiece:
				pieceColor = HUMAN_COLOR
			else:
				pieceColor = AI_COLOR
			print(f" {pieceColor}%s{NO_COLOR} %s" % (piece, '|' if colNum < 2 else '\n'), end = '')
		if rowNum < 2:
			print("\t   ---+---+---")
	print("\t    1   2   3\n")

def getPlayerMove():
	'''Takes in the user's input and performs that move on the board, returns the move'''
	rowLabels = "ABC"
	spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (rowLabels[-1], len(gameBoard))).strip().upper()
	while True:
		if spot == 'Q':
			print("\nThanks for playing!\n")
			exit(0)
		elif len(spot) >= 3 or len(spot) == 0 or spot[0] not in rowLabels or not spot[1:].isdigit() or int(spot[1:]) > len(gameBoard) or int(spot[1:]) < 1:
			spot = input("Invalid input. Please try again.\t").strip().upper()
		elif gameBoard[rowLabels.index(spot[0])][int(spot[1:]) - 1] != EMPTY:
			spot = input("That spot is already taken, please choose another:\t").strip().upper()
		else:
			break
	row = rowLabels.index(spot[0])
	col = int(spot[1:]) - 1
	return [row, col]

def main():
	'''main method that prompts the user for input'''
	global ai 
	global gameBoard
	global playerPiece
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
	while playerPieceSelect not in ['x', 'o']:
		playerPieceSelect = input("Invalid input. Try again:\t").strip().lower()
	if playerPieceSelect == 'x':
		playerPiece = X_PIECE
		aiPiece = O_PIECE
	else:
		playerPiece = O_PIECE
		aiPiece = X_PIECE

	printGameBoard()

	ai = strategy.Strategy(X_PIECE if playerPiece == O_PIECE else O_PIECE)
	turn = X_PIECE

	while not ai.GAME_OVER:
		if turn == playerPiece:
			recentMove = getPlayerMove()
			gameBoard[recentMove[0]][recentMove[1]] = playerPiece
			ai.checkGameState(gameBoard)
		else:
			# AI's turn
			userInput = input("It's the AI's turn, press enter for it to play.\t").strip().lower()
			if userInput == 'q':
				print("\nThanks for playing!\n")
				exit(0)
			recentMove = ai.findBestMove(gameBoard)
			ai_move_formatted = 'ABC'[recentMove[0]] + str(recentMove[1] + 1)
			print("AI played in spot %s\n" % ai_move_formatted)
		printGameBoard()
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
		print("%s player wins!\n" % winner)


if __name__ == "__main__":
    main()


