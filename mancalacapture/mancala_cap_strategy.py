# Contains AI strategy
import math  # for infinities
import random  # for randomizing valid moves list in minimax
from mancalacapture.board_functions import get_valid_moves, perform_move, is_board_terminal, push_all_pebbles_to_bank, \
	winning_player_bank_index
from mancalacapture.constants import TOTAL_PEBBLES, POCKETS_PER_SIDE, BOARD_SIZE
from mancalacapture.mancala_player import MancalaPlayer  # super class

MAX_DEPTH = 10  # max number of moves ahead to calculate
MAX, MIN = True, False  # to be used in minimax


# class for the A.I.
class MancalaStrategy(MancalaPlayer):

	def __init__(self, bank_index=13):
		super().__init__(bank_index)
		self.opponentBankIndex = (bank_index + POCKETS_PER_SIDE + 1) % BOARD_SIZE

	def get_move(self, board):
		"""Calculates the best move for the AI for the given board"""
		move, score = -123, -123  # placeholders
		for i in range(1, MAX_DEPTH + 1):  # iterative deepening
			# this will prioritize game winning move sequences that finish in less moves
			move, score = self.minimax(board, 0, MAX, -math.inf, math.inf, i)
			if score > 900:
				break
		return move

	def score_board(self, board):
		"""Scores the board"""
		player_bank_score = board[self.bankIndex]
		opponent_bank_score = board[self.opponentBankIndex]
		if player_bank_score > TOTAL_PEBBLES / 2:
			player_bank_score += 1000
		elif opponent_bank_score > TOTAL_PEBBLES / 2:
			opponent_bank_score += 1000
		player_pockets = board[self.bankIndex - POCKETS_PER_SIDE: self.bankIndex]
		opponent_pockets = board[self.opponentBankIndex - POCKETS_PER_SIDE: self.opponentBankIndex]
		player_score = player_bank_score + score_pockets(player_pockets)
		opponent_score = opponent_bank_score + score_pockets(opponent_pockets)
		return player_score - opponent_score

	def minimax(self, board, depth, max_or_min, alpha, beta, local_max_depth):
		"""
        Recursively finds the best move for a given board
        Returns the move index in [0] and score of the board in [1]
        """
		# random.shuffle(valid_moves)
		if is_board_terminal(board):
			push_all_pebbles_to_bank(board)
			winning_bank_index = winning_player_bank_index(board)
			if winning_bank_index == self.bankIndex:
				return None, 2000
			elif winning_bank_index is None:
				return None, 0
			else:
				return None, -2000
		if depth == local_max_depth:
			return None, self.score_board(board)
		if max_or_min == MAX:
			# want to maximize this move
			valid_moves = get_valid_moves(board, self.bankIndex)
			score = -math.inf
			best_move = valid_moves[0]  # default best move
			for move in valid_moves:
				board_copy = board.copy()
				perform_move(board_copy, move, self.bankIndex)
				_, updated_score = self.minimax(board_copy, depth + 1, MIN, alpha, beta, local_max_depth)
				if updated_score > score:
					score = updated_score
					best_move = move
				alpha = max(alpha, score)
				if alpha >= beta:
					break  # pruning
			return best_move, score
		else:
			# want to minimize this move
			valid_moves = get_valid_moves(board, self.opponentBankIndex)
			score = math.inf
			best_move_for_opponent = valid_moves[0]
			for move in valid_moves:
				board_copy = board.copy()
				perform_move(board_copy, move, self.opponentBankIndex)
				_, updated_score = self.minimax(board_copy, depth + 1, MAX, alpha, beta, local_max_depth)
				if updated_score < score:
					score = updated_score
					best_move_for_opponent = move
				beta = min(beta, score)
				if beta <= alpha:
					break  # pruning
			return best_move_for_opponent, score


def score_pockets(pockets):
	"""Assigns a score for the given pocket layout. Favors pebbles further away from player bank"""
	score = 0
	multiplier = 0.3
	step_down = (multiplier - 0.1) / POCKETS_PER_SIDE
	for pebbles in pockets:
		score += pebbles * multiplier
		multiplier -= step_down
	return score
