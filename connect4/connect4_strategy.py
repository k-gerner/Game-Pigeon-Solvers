# strategy.py sort of working
# Kyle Gerner 3.18.21
# Contains AI strategy and board manipulation methods

import math  # for infinities
import random  # for randomizing valid moves list in minimax
from connect4.connect4_player import Connect4Player  # super class

EMPTY, RED, YELLOW = '.', 'o', '@'
NUM_ROWS, NUM_COLS = 6, 7
MAX_DEPTH = 6  # max number of moves ahead to calculate
MAX, MIN = True, False  # to be used in minimax
WIN_SCORE = 1000000  # large enough to always be the preferred outcome


# class for the A.I.
class Connect4Strategy(Connect4Player):

	def __init__(self, color):
		super().__init__(color)
		self.AI_COLOR = color
		self.HUMAN_COLOR = opponent_of(color)

	def get_move(self, board):
		"""Calculates the best move for the AI for the given board"""
		move, score = -123, -123  # placeholders
		for i in range(1, MAX_DEPTH + 1):  # iterative deepening
			# this will prioritize game winning move sequences that finish in less moves
			move, score = self.minimax(board, 0, MAX, -math.inf, math.inf, i)
			if score == WIN_SCORE:
				break
		return move

	def minimax(self, board, depth, max_or_min, alpha, beta, local_max_depth):
		"""
		Recursively finds the best move for a given board
		Returns the column in [0] and score of the board in [1]
		"""
		valid_moves = get_valid_moves(board)
		random.shuffle(valid_moves)
		game_over, winner = check_if_game_over(board)
		if game_over:
			if winner == self.AI_COLOR:
				return None, WIN_SCORE
			elif winner == self.HUMAN_COLOR:
				return None, -1 * WIN_SCORE
			else:
				# no winner
				return None, 0
		if depth == local_max_depth:
			return None, score_board(board, self.AI_COLOR)
		if max_or_min == MAX:
			# want to maximize this move
			score = -math.inf
			best_move = valid_moves[0]  # default best move
			for move in valid_moves:
				board_copy = copy_of_board(board)
				perform_move(board_copy, move, self.AI_COLOR)
				_, updated_score = self.minimax(board_copy, depth + 1, MIN, alpha, beta, local_max_depth)
				if updated_score > score:
					score = updated_score
					best_move = move
				alpha = max(alpha, score)
				# if depth == 0:
				# 	print("Score for slot %d = %d. Max depth = %d" % (move, updated_score, localMaxDepth))
				if alpha >= beta:
					break  # pruning
			return best_move, score
		else:
			# want to minimize this move
			score = math.inf
			best_move_for_human = valid_moves[0]
			for move in valid_moves:
				board_copy = copy_of_board(board)
				perform_move(board_copy, move, self.HUMAN_COLOR)
				_, updated_score = self.minimax(board_copy, depth + 1, MAX, alpha, beta, local_max_depth)
				if updated_score < score:
					score = updated_score
					best_move_for_human = move
				beta = min(beta, score)
				if beta <= alpha:
					break  # pruning
			return best_move_for_human, score


def score_board(board, color):
	"""Scores the entire board"""
	score = 0

	# Give a slight bonus to pieces in the center column
	for r in range(NUM_ROWS):
		if board[r][NUM_COLS // 2] == color:
			score += 2

	# Check horizontal
	for c in range(NUM_COLS - 3):
		for r in range(NUM_ROWS):
			score += score_section(board[r][c:c + 4], color)

	# Check vertical
	for c in range(NUM_COLS):
		for r in range(NUM_ROWS - 3):
			section = []
			for i in range(4):
				section.append(board[r + i][c])
			score += score_section(section, color)

	# Check diagonal from bottom left to top right
	for c in range(NUM_COLS - 3):
		for r in range(NUM_ROWS - 3):
			section = []
			for i in range(4):
				section.append(board[r + i][c + i])
			score += score_section(section, color)

	# Check diagonal from bottom right to top left
	for c in range(NUM_COLS - 3):
		for r in range(3, NUM_ROWS):
			section = []
			for i in range(4):
				section.append(board[r - i][c + i])
			score += score_section(section, color)

	return score


def score_section(section, color):
	"""Looks at the given length 4 section and scores it"""
	opponent_color = opponent_of(color)
	num_my_color = section.count(color)
	num_opp_color = section.count(opponent_color)
	num_empty = section.count(EMPTY)

	if num_my_color == 4:
		return WIN_SCORE
	elif num_my_color == 3 and num_empty == 1:
		return 10
	elif num_my_color == 2 and num_empty == 2:
		return 5
	elif num_opp_color == 3 and num_empty == 1:
		return -8
	elif num_opp_color == 2 and num_empty == 2:
		return -3
	else:
		return 0


def find_winner(board):
	"""
    Checks if there is a winner
    returns the color of the winner if there is one, otherwise None
    """
	# Check horizontal
	for c in range(NUM_COLS - 3):
		for r in range(NUM_ROWS):
			if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] != EMPTY:
				return board[r][c]

	# Check vertical
	for c in range(NUM_COLS):
		for r in range(NUM_ROWS - 3):
			if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] != EMPTY:
				return board[r][c]

	# Check diagonal from bottom left to top right
	for c in range(NUM_COLS - 3):
		for r in range(NUM_ROWS - 3):
			if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] != EMPTY:
				return board[r][c]

	# Check diagonal from bottom right to top left
	for c in range(NUM_COLS - 3):
		for r in range(3, NUM_ROWS):
			if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] != EMPTY:
				return board[r][c]

	return None


def is_valid_move(board, col):
	"""Checks if the column is full"""
	return board[NUM_ROWS - 1][col] == EMPTY


def get_valid_moves(board):
	"""Returns a list of valid moves"""
	valid_cols = []
	for c in range(NUM_COLS):
		if is_valid_move(board, c):
			valid_cols.append(c)
	return valid_cols


def check_if_game_over(board):
	"""
    Checks if the current board state is Game Over
    Returns a tuple, with [0] being the True or False value
    [1] being the winning color (None if neither color wins)
    """
	winner = find_winner(board)
	if winner is not None:
		return True, winner
	elif len(get_valid_moves(board)) == 0:
		return True, None
	else:
		return False, None


def opponent_of(color):
	"""Get the opposing color"""
	return RED if color == YELLOW else YELLOW


def perform_move(board, col, color):
	"""Performs a given move on the board"""
	row_of_placement = 0
	for row in board:
		if row[col] == EMPTY:
			break
		row_of_placement += 1
	board[row_of_placement][col] = color


def copy_of_board(board):
	"""Returns a copy of the given board"""
	return list(map(list, board))
