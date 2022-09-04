# strategy.py sort of working
# Kyle Gerner 3.18.21
# Contains AI strategy and board manipulation methods

import math # for infinities
import random # for randomizing valid moves list in minimax
from Player import Player # super class

EMPTY, RED, YELLOW = '.', 'o', '@'
NUM_ROWS, NUM_COLS = 6, 7
MAX_DEPTH = 6 # max number of moves ahead to calculate
MAX, MIN = True, False # to be used in minimax
WIN_SCORE = 1000000 # large enough to always be the preferred outcome

# class for the A.I.
class Strategy(Player):

	def __init__(self, color):
		super().__init__(color)
		self.AI_COLOR = color
		self.HUMAN_COLOR = opponentOf(color)

	def getMove(self, board):
		"""Calculates the best move for the AI for the given board"""
		move, score = -123, -123 # placeholders
		for i in range(1, MAX_DEPTH + 1): # iterative deepening
			# this will prioritize game winning move sequences that finish in less moves
			move, score = self.minimax(board, 0, MAX, -math.inf, math.inf, i)
			if score == WIN_SCORE:
				break
		return move

	def minimax(self, board, depth, maxOrMin, alpha, beta, localMaxDepth):
		"""
		Recursively finds the best move for a given board
		Returns the column in [0] and score of the board in [1]
		"""
		validMoves = getValidMoves(board)
		random.shuffle(validMoves)
		gameOver, winner = checkIfGameOver(board)
		if gameOver:
			if winner == self.AI_COLOR:
				return None, WIN_SCORE
			elif winner == self.HUMAN_COLOR:
				return None, -1 * WIN_SCORE
			else:
				# no winner
				return None, 0
		if depth == localMaxDepth:
			return None, scoreBoard(board, self.AI_COLOR)
		if maxOrMin == MAX:
			# want to maximize this move
			score = -math.inf
			bestMove = validMoves[0] # default best move
			for move in validMoves:
				boardCopy = list(map(list, board)) # copies board
				performMove(boardCopy, move, self.AI_COLOR)
				_, updatedScore = self.minimax(boardCopy, depth + 1, MIN, alpha, beta, localMaxDepth)
				if updatedScore > score:
					score = updatedScore
					bestMove = move
				alpha = max(alpha, score)
				# if depth == 0:
				# 	print("Score for slot %d = %d. Max depth = %d" % (move, updatedScore, localMaxDepth))
				if alpha >= beta:
					break # pruning
			return bestMove, score
		else:
			# want to minimize this move
			score = math.inf
			bestMoveForHuman = validMoves[0]
			for move in validMoves:
				boardCopy = list(map(list, board)) # copies board
				performMove(boardCopy, move, self.HUMAN_COLOR)
				_, updatedScore = self.minimax(boardCopy, depth + 1, MAX, alpha, beta, localMaxDepth)
				if updatedScore < score:
					score = updatedScore
					bestMoveForHuman = move
				beta = min(beta, score)
				if beta <= alpha:
					break # pruning
			return bestMoveForHuman, score


def scoreBoard(board, color):
	"""Scores the entire board"""
	score = 0

	# Give a slight bonus to pieces in the center column
	for r in range(NUM_ROWS):
		if board[r][NUM_COLS//2] == color:
			score += 2

	# Check horizontal
	for c in range(NUM_COLS-3):
		for r in range(NUM_ROWS):
			score += scoreSection(board[r][c:c + 4], color)


	# Check vertical
	for c in range(NUM_COLS):
		for r in range(NUM_ROWS-3):
			section = []
			for i in range(4):
				section.append(board[r + i][c])
			score += scoreSection(section, color)

	# Check diagonal from bottom left to top right
	for c in range(NUM_COLS-3):
		for r in range(NUM_ROWS-3):
			section = []
			for i in range(4):
				section.append(board[r + i][c + i])
			score += scoreSection(section, color)

	# Check diagonal from bottom right to top left
	for c in range(NUM_COLS-3):
		for r in range(3, NUM_ROWS):
			section = []
			for i in range(4):
				section.append(board[r - i][c + i])
			score += scoreSection(section, color)

	return score

def scoreSection(section, color):
	"""Looks at the given length 4 section and scores it"""
	opponentColor = opponentOf(color)
	numMyColor = section.count(color)
	numOppColor = section.count(opponentColor)
	numEmpty = section.count(EMPTY)

	if numMyColor == 4:
		return WIN_SCORE
	elif numMyColor == 3 and numEmpty == 1:
		return 10
	elif numMyColor == 2 and numEmpty == 2:
		return 5
	elif numOppColor == 3 and numEmpty == 1:
		return -8
	elif numOppColor == 2 and numEmpty == 2:
		return -3
	else:
		return 0

def findWinner(board):
	"""
    Checks if there is a winner
    returns the color of the winner if there is one, otherwise None
    """
	# Check horizontal
	for c in range(NUM_COLS-3):
		for r in range(NUM_ROWS):
			if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] != EMPTY:
				return board[r][c]

	# Check vertical
	for c in range(NUM_COLS):
		for r in range(NUM_ROWS-3):
			if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] != EMPTY:
				return board[r][c]

	# Check diagonal from bottom left to top right
	for c in range(NUM_COLS-3):
		for r in range(NUM_ROWS-3):
			if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] != EMPTY:
				return board[r][c]

	# Check diagonal from bottom right to top left
	for c in range(NUM_COLS-3):
		for r in range(3, NUM_ROWS):
			if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] != EMPTY:
				return board[r][c]

	return None

def isValidMove(board, col):
	"""Checks if the column is full"""
	return board[NUM_ROWS - 1][col] == EMPTY

def getValidMoves(board):
	"""Returns a list of valid moves"""
	validCols = []
	for c in range(NUM_COLS):
		if isValidMove(board, c):
			validCols.append(c)
	return validCols

def checkIfGameOver(board):
	"""
    Checks if the current board state is Game Over
    Returns a tuple, with [0] being the True or False value
    [1] being the winning color (None if neither color wins)
    """
	winner = findWinner(board)
	if winner is not None:
		return True, winner
	elif len(getValidMoves(board)) == 0:
		return True, None
	else:
		return False, None

def opponentOf(color):
	"""Get the opposing color"""
	return RED if color == YELLOW else YELLOW

def performMove(board, col, color):
	"""Performs a given move on the board"""
	rowOfPlacement = 0
	for row in board:
		if row[col] == EMPTY:
			break
		rowOfPlacement += 1
	board[rowOfPlacement][col] = color