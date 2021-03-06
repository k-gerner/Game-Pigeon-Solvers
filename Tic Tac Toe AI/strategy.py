# Contains AI strategy and board manipulation methods
# Kyle G 6.6.2021

import math # for infinities
import random # for randomizing valid moves list in minimax

EMPTY, X_PIECE, O_PIECE = ' ', 'X', 'O'
MAX, MIN = True, False # to be used in minimax
WIN_SCORE = 1000000000 # large enough to always be the preferred outcome

# class for the A.I.
class Strategy(object):

	def __init__(self, aiColor):
		'''Initializes the board attributes'''
		self.AI_COLOR = aiColor
		self.HUMAN_COLOR = self.opponentOf(aiColor)
		self.GAME_OVER = False

	def opponentOf(self, piece):
		'''Get the opposing piece'''
		return X_PIECE if piece == O_PIECE else O_PIECE

	def checkGameState(self, board):
		'''Sets the GAME_OVER var to True if there is a winner'''
		if self.isTerminal(board)[0]: 
		 	self.GAME_OVER = True

	def isTerminal(self, board):
		'''
		Checks if the current board state is Game Over
		Returns a tuple, with [0] being the True or False value
		[1] being the winning color (None if neither color wins)
		'''
		winner = self.findWinner(board)
		if winner != None:
			return True, winner
		
		for row in board:
			for spot in row:
				if spot == EMPTY:
					return False, None

		return True, None

	def findWinner(self, board):
		'''
		Checks if there is a winner
		returns the color of the winner if there is one, otherwise None
		'''
		# Check horizontal
		for row in board:
			if row[0] == row[1] == row[2] != EMPTY:
				return row[0]

		# Check vertical
		for col in range(3):
			if board[0][col] == board[1][col] == board[2][col] != EMPTY:
				return board[0][col]

		# Check diagonal from top left to bottom right
		if board[0][0] == board[1][1] == board[2][2] != EMPTY:
			return board[0][0]

		# Check diagonal from top right to bottom left
		if board[0][2] == board[1][1] == board[2][0] != EMPTY:
			return board[0][2]

		return None

	def performMove(self, board, row, col, piece):
		'''Performs a given move on the board'''
		board[row][col] = piece

	def findBestMove(self, board):
		'''Calculates and performs the best move for the AI for the given board'''
		moveRow, moveCol, _ = self.minimax(board, MAX, -math.inf, math.inf)
		self.performMove(board, moveRow, moveCol, self.AI_COLOR)
		self.checkGameState(board)
		return [moveRow, moveCol]

	def getValidMoves(self, board):
		'''Returns a list of valid moves (moves in the center area or near other pieces)'''
		validLocations = []
		for rowNum in range(3):
			for colNum in range(3):
				if board[rowNum][colNum] == EMPTY:
					validLocations.append([rowNum, colNum])
		return validLocations

	def minimax(self, board, maxOrMin, alpha, beta):
		'''
		Recursively finds the best move for a given board
		Returns the row in [0], column in [1], and score of the board in [2]
		'''
		gameOver, winner = self.isTerminal(board)
		if gameOver:
			if winner == AI_COLOR:
				return WIN_SCORE
			elif winner == HUMAN_COLOR:
				return -1 * WIN_SCORE
			else:
				return 0

		validMoves = self.getValidMoves(board)
		if len(validMoves) == 0:
			return -1, -1, 0
		elif len(validMoves) == 9:
			# if start of the game, always go in the middle
			return 1, 1, 0 
		random.shuffle(validMoves)
		if maxOrMin == MAX:
			# want to maximize this move
			score = -math.inf
			bestMove = validMoves[0] # default best move
			for move in validMoves:
				boardCopy = list(map(list, board)) # copies board
				self.performMove(boardCopy, move[0], move[1], self.AI_COLOR)
				gameOver, winner = self.isTerminal(boardCopy)
				if winner == self.AI_COLOR:
					updatedScore = WIN_SCORE
				elif winner == self.HUMAN_COLOR:
					updatedScore = -1 * WIN_SCORE
				else:
					# no winner
					if gameOver:
						# if board filled
						updatedScore = 0
					else:
						_, __, updatedScore = self.minimax(boardCopy, MIN, alpha, beta)
				if updatedScore > score:
					score = updatedScore
					bestMove = move
				alpha = max(alpha, score)
				if alpha >= beta:
					break # pruning
			return bestMove[0], bestMove[1], score

		else: 
			# maxOrMin == MIN
			# want to minimize this move
			score = math.inf
			bestMoveForHuman = validMoves[0]
			for move in validMoves:
				boardCopy = list(map(list, board)) # copies board
				self.performMove(boardCopy, move[0], move[1], self.HUMAN_COLOR)
				gameOver, winner = self.isTerminal(boardCopy)
				if winner == self.AI_COLOR:
					updatedScore = WIN_SCORE
				elif winner == self.HUMAN_COLOR:
					updatedScore = -1 * WIN_SCORE
				else:
					# no winner
					if gameOver:
						# if board filled
						updatedScore = 0
					else:
						_, __, updatedScore = self.minimax(boardCopy, MAX, alpha, beta)
				if updatedScore < score:
					score = updatedScore
					bestMoveForHuman = move
				beta = min(beta, score)
				if beta <= alpha:
					break # pruning
			return bestMoveForHuman[0], bestMoveForHuman[1], score




