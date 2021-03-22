# Kyle Gerner 
# Started 3.18.21
# Connect 4 Solver, client facing 
import strategy

EMPTY, RED, YELLOW = '.', 'o', '@'
gameBoard = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY], # bottom row
			[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]] # top row
playerColor = YELLOW
ai = strategy.Strategy()

def printBoard(board):
	'''Prints the given game board'''
	print("\n  1 2 3 4 5 6 7")
	for rowNum in range(len(board)-1, -1, -1):
		print("| ", end = '')
		for spot in board[rowNum]:
			print("%s " % spot, end='')
		print("|")
	print("-"*17)

def getPlayerMove():
	'''Takes in the user's input and performs that move on the board'''
	col = input("It's your turn, which column would you like to play? (1-7):\t")
	while True:
		if not col.isdigit() or int(col.strip()) not in [1,2,3,4,5,6,7]:
			col = input("Invalid input. Please enter a number 1 through 7:\t")
		elif not ai.isValidMove(gameBoard, int(col) - 1):
			col = input("That column is full, please choose another:\t")
		else:
			break
	ai.performMove(gameBoard, int(col) - 1, playerColor)
	ai.checkGameState(gameBoard)


def main():
	'''main method that prompts the user for input'''
	global playerColor 
	print("\nWelcome to Kyle's Connect 4 AI!")
	playerColorInput = input("Would you like to be RED ('r') or YELLOW ('y')? (red goes first!):\t").strip().lower()
	if playerColorInput == 'r':
		playerColor = RED
		print("You will be red!")
	elif playerColorInput == 'y':
		print("You will be yellow!")
	else:
		print("Invalid input. You'll be yellow!")
	ai.setPlayerColor(playerColor)
	turn = RED
	while not ai.GAME_OVER:
		printBoard(gameBoard)
		if turn == playerColor:
			getPlayerMove()
		else:
			ai_move = ai.playBestMove(gameBoard)
			print("AI played in spot %d" % (ai_move + 1))
		turn = ai.opponentOf(turn) # switch the turn

	winner = "RED" if ai.opponentOf(turn) == RED else "YELLOW"
	printBoard(gameBoard)
	print("%s wins!" % winner)

if __name__ == "__main__":
    main()