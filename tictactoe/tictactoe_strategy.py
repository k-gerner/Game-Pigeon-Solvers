# Contains AI strategy and board manipulation methods
# Kyle G 6.6.2021

from tictactoe.tictactoe_player import TicTacToePlayer
import math  # for infinities
import random  # for randomizing valid moves list in minimax

EMPTY, X_PIECE, O_PIECE = ' ', 'X', 'O'
MAX, MIN = True, False  # to be used in minimax
WIN_SCORE = 1000000000  # large enough to always be the preferred outcome


# class for the A.I.
class TicTacToeStrategy(TicTacToePlayer):

	def __init__(self, ai_color):
		"""Initializes the board attributes"""
		super().__init__(ai_color)
		self.AI_COLOR = ai_color
		self.HUMAN_COLOR = opponent_of(ai_color)

	def get_move(self, board):
		"""Calculates the best move for the AI for the given board"""
		move_row, move_col = -1, -1
		for depth_to_search in range(1, 10):  # iterative deepening
			# this will prioritize game winning movesets that occur with less total moves
			move_row, move_col, score = self.minimax(board, 0, MAX, -math.inf, math.inf, depth_to_search)
			if score == WIN_SCORE:
				break
		return move_row, move_col

	def minimax(self, board, depth, max_or_min, alpha, beta, local_max_depth):
		"""
		Recursively finds the best move for a given board
		Returns the row in [0], column in [1], and score of the board in [2]
		"""
		game_over, winner = is_terminal(board)
		if game_over or depth == local_max_depth:
			if winner == self.AI_COLOR:
				return None, None, WIN_SCORE
			elif winner == self.HUMAN_COLOR:
				return None, None, -1 * WIN_SCORE
			else:
				return None, None, 0

		valid_moves = get_valid_moves(board)
		if len(valid_moves) == 0:
			return -1, -1, 0
		elif len(valid_moves) == 9:
			# if start of the game, always go in the middle
			return 1, 1, 0 
		random.shuffle(valid_moves)
		if max_or_min == MAX:
			# want to maximize this move
			score = -math.inf
			best_move = valid_moves[0]  # default best move
			for move in valid_moves:
				board_copy = copy_of_board(board)
				perform_move(board_copy, move[0], move[1], self.AI_COLOR)
				game_over, winner = is_terminal(board_copy)
				if winner == self.AI_COLOR:
					updated_score = WIN_SCORE
				elif winner == self.HUMAN_COLOR:
					updated_score = -1 * WIN_SCORE
				else:
					# no winner
					if game_over:
						# if board filled
						updated_score = 0
					else:
						_, __, updated_score = self.minimax(board_copy, depth + 1, MIN, alpha, beta, local_max_depth)
				if updated_score > score:
					score = updated_score
					best_move = move
				alpha = max(alpha, score)
				if alpha >= beta:
					break  # pruning
			return best_move[0], best_move[1], score

		else: 
			# maxOrMin == MIN
			# want to minimize this move
			score = math.inf
			best_move_for_human = valid_moves[0]
			for move in valid_moves:
				board_copy = copy_of_board(board)
				perform_move(board_copy, move[0], move[1], self.HUMAN_COLOR)
				game_over, winner = is_terminal(board_copy)
				if winner == self.AI_COLOR:
					updated_score = WIN_SCORE
				elif winner == self.HUMAN_COLOR:
					updated_score = -1 * WIN_SCORE
				else:
					# no winner
					if game_over:
						# if board filled
						updated_score = 0
					else:
						_, __, updated_score = self.minimax(board_copy, depth + 1, MAX, alpha, beta, local_max_depth)
				if updated_score < score:
					score = updated_score
					best_move_for_human = move
				beta = min(beta, score)
				if beta <= alpha:
					break  # pruning
			return best_move_for_human[0], best_move_for_human[1], score


def opponent_of(piece):
	"""Get the opposing piece"""
	return X_PIECE if piece == O_PIECE else O_PIECE


def perform_move(board, row, col, piece):
	"""Performs a given move on the board"""
	board[row][col] = piece


def find_winner(board):
	"""
    Checks if there is a winner
    returns the color of the winner if there is one, otherwise None
    """
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


def is_terminal(board):
	"""
    Checks if the current board state is Game Over
    Returns a tuple, with [0] being the True or False value
    [1] being the winning color (None if neither color wins)
    """
	winner = find_winner(board)
	if winner is not None:
		return True, winner

	for row in board:
		for spot in row:
			if spot == EMPTY:
				return False, None

	return True, None


def get_valid_moves(board):
	"""Returns a list of valid moves (moves in the center area or near other pieces)"""
	valid_locations = []
	for rowNum in range(3):
		for colNum in range(3):
			if board[rowNum][colNum] == EMPTY:
				valid_locations.append([rowNum, colNum])
	return valid_locations


def copy_of_board(board):
	"""Returns a copy of the given board"""
	return list(map(list, board))
