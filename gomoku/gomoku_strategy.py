# Contains AI strategy and board manipulation methods

import math  # for infinities
import random  # for randomizing valid moves list in minimax
import sys  # for better progress bar formatting
from gomoku.gomoku_player import GomokuPlayer  # super class

#### DO NOT MODIFY ####
EMPTY, BLACK, WHITE = '.', 'X', 'O'
BLACK_HASH_ROW_NUM, WHITE_HASH_ROW_NUM = 0, 1
MAX, MIN = True, False  # to be used in minimax
WIN_SCORE = 1000000000  # large enough to always be the preferred outcome
#######################
####### MODIFY ########
MAX_NEIGHBOR_DIST = 2  # max distance from an already played piece that we want to check if open
MAX_NUM_MOVES_TO_EVALUATE = 15  # most moves we want to evaluate at once for any given board
MAX_DEPTH = 6  # max number of moves ahead to calculate
#######################


# class for the A.I.
class GomokuStrategy(GomokuPlayer):

	def __init__(self, color, board_dimension=13):
		"""Initializes the board attributes"""
		super().__init__(color, board_dimension)
		self.GAME_OVER = False
		self.AI_COLOR = color
		self.HUMAN_COLOR = opponent_of(color)
		# RANDOM_HASH_TABLE will be used for Zobrist Hashing.
		# Table has DIM * DIM * 2 entries, with each being a random number that will 
		# represent a number for if a certain piece is played in a certain position 
		# on the board. This will be used for XORing in the Zobrist Hashing.
		self.RANDOM_HASH_TABLE = create_hash_table(board_dimension)
		# BOARD_STATE_DICT will be a map that maps board-state hashes to a list containing
		# important information about the board at that board-state (the score)
		# NOTE this transposition table will be cleared between different depth searches.
		# Maintaining the transposition table between different depth searches could help prune
		# even further, but it would require me to define some minimum score that determines whether
		# or not it would be worth it to search this path at a deeper depth
		self.BOARD_STATE_DICT = {}
		self.black_threats_scores = {
			'.XXXX.' : 10000,   # 4 double open, next move guaranteed win
			'.XXXX'  : 100,     # 4 single open
			'XXXX.'  : 100,     # 4 single open
			'X.XXX'	 : 90,		# 1-3 single open
			'XX.XX'	 : 85,		# 2-2 single open
			'XXX.X'	 : 90,		# 1-3 single open
			'.XXX.'	 : 30,		# 3 double open
			'OXXXX.' : 80,		# 4 single open
			'.XXXXO' : 80,		# 4 single open
			'.X.XX.' : 25,		# broken 3
			'.XX.X.' : 25		# broken 3
		}
		self.white_threats_scores = {
			'.OOOO.' : 10000,   # 4 double open, next move guaranteed win
			'.OOOO'  : 100,     # 4 single open
			'OOOO.'  : 100, 	# 4 single open
			'O.OOO'	 : 90,		# 1-3 single open
			'OO.OO'	 : 85,		# 2-2 single open
			'OOO.O'	 : 90,		# 1-3 single open
			'.OOO.'	 : 30,		# 3 double open
			'XOOOO.' : 80,		# 4 single open
			'.OOOOX' : 80,		# 4 single open
			'.O.OO.' : 25,		# broken 3
			'.OO.O.' : 25		# broken 3
		}
		self.position_weights_matrix = create_board_position_weights(board_dimension)

	def create_zobrist_value_for_new_move(self, move, color, prev_zobrist_value):
		"""Gives an updated Zobrist value for a board after a new move is played"""
		row, col = move
		hash_row = BLACK_HASH_ROW_NUM if color == BLACK else WHITE_HASH_ROW_NUM
		hash_val = self.RANDOM_HASH_TABLE[hash_row][row*self.BOARD_DIMENSION + col]
		return prev_zobrist_value ^ hash_val  # ^ = XOR operator

	def check_game_state(self, board):
		"""Sets the GAME_OVER var to True if there is a winner"""
		if self.is_terminal(board)[0]:
			self.GAME_OVER = True

	def is_terminal(self, board):
		"""
		Checks if the current board state is Game Over
		Returns a tuple, with [0] being the True or False value
		[1] being the winning color (None if neither color wins)
		"""
		winner = self.find_winner(board)
		if winner is not None:
			return True, winner
		
		for row in board:
			for spot in row:
				if spot == EMPTY:
					return False, None

		return True, None

	def find_winner(self, board):
		"""
		Checks if there is a winner
		returns the color of the winner if there is one, otherwise None
		"""
		# Check horizontal
		for row in board:
			for col in range(self.BOARD_DIMENSION - 4):
				if row[col] == row[col+1] == row[col+2] == row[col+3] == row[col+4] != EMPTY:
					return row[col]

		# Check vertical
		for c in range(self.BOARD_DIMENSION):
			for r in range(self.BOARD_DIMENSION - 4):
				if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == board[r+4][c] != EMPTY:
					return board[r][c]

		# Check diagonal from top left to bottom right
		for c in range(self.BOARD_DIMENSION - 4):
			for r in range(self.BOARD_DIMENSION - 4):
				if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == board[r+4][c+4] != EMPTY:
					return board[r][c]

		# Check diagonal from top right to bottom left
		for c in range(self.BOARD_DIMENSION - 4):
			for r in range(4, self.BOARD_DIMENSION):
				if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == board[r-4][c+4] != EMPTY:
					return board[r][c]

		return None

	def is_coordinate_in_board_range(self, coord):
		"""Checks if the coordinate is valid on the board"""
		row_num = coord[0]
		col_num = coord[1]
		if row_num % self.BOARD_DIMENSION == row_num and col_num % self.BOARD_DIMENSION == col_num:
			return True
		else:
			return False

	def check_if_move_caused_game_over(self, board, move):
		"""
		Checks the spaces in outward directions to see if the move given caused a win
		returns the winner in [0] (BLACK, WHITE, or None if no winner)
		returns True or False in [1] whether or not the game is over
		"""
		empty_spot_seen = False
		color = board[move[0]][move[1]]
		direction_vectors_list = [[1, -1], [1, 0], [1, 1], [0, 1]]
		for direction_vector in direction_vectors_list:
			num_in_a_row = 1
			curr_coordinates_forward = move.copy()
			curr_coordinates_backward = move.copy()
			forward_check_still_valid = True
			backward_check_still_valid = True
			outward_spaces_checked = 0
			while outward_spaces_checked < 4 and num_in_a_row < 5 and (forward_check_still_valid or backward_check_still_valid):
				outward_spaces_checked += 1
				if forward_check_still_valid:
					# keep looking in the forward direction
					curr_coordinates_forward = [a + b for a, b in zip(curr_coordinates_forward, direction_vector)]  # adds the direction vector
					if self.is_coordinate_in_board_range(curr_coordinates_forward):
						curr_forward_spot = board[curr_coordinates_forward[0]][curr_coordinates_forward[1]]
						if curr_forward_spot == color:
							num_in_a_row += 1
						else:
							if curr_forward_spot == EMPTY:
								empty_spot_seen = True
							forward_check_still_valid = False
					else:
						forward_check_still_valid = False

				if backward_check_still_valid:
					curr_coordinates_backward = [a - b for a, b in zip(curr_coordinates_backward, direction_vector)]  # subtracts the direction vector
					if self.is_coordinate_in_board_range(curr_coordinates_backward):
						curr_backward_spot = board[curr_coordinates_backward[0]][curr_coordinates_backward[1]]
						if curr_backward_spot == color:
							num_in_a_row += 1
						else:
							if curr_backward_spot == EMPTY:
								empty_spot_seen = True
							backward_check_still_valid = False
					else:
						backward_check_still_valid = False
			if num_in_a_row >= 5:
				return color, True
		# if we reach here, the move did not cause a win
		if empty_spot_seen:
			return None, False
		for row in board:
			for spot in row:
				if spot == EMPTY:
					# found an empty spot
					return None, False
		return None, True

	def get_valid_moves(self, board):
		"""Returns a list of valid moves (moves in the center area or near other pieces)"""

		# Will allow me to slightly prioritize checking the spots that are closer to 
		# other pieces by placing them in separate lists
		lists_of_valids = [] 
		for _ in range(MAX_NEIGHBOR_DIST):
			lists_of_valids.append([]) 

		empties_found_so_far = set()  # used to make sure we don't double-count empty spots

		# locate all the spots with pieces
		filled_locations = []
		for r in range(self.BOARD_DIMENSION):
			for c in range(self.BOARD_DIMENSION):
				if board[r][c] != EMPTY:
					filled_locations.append([r, c])

		def locate_empty_near_spots(filled_coord, dist_from_piece):
			"""Finds all the empty spots near this coordinate and adds them to the list of valid spots"""
			row, col = filled_coord
			for i in range(-dist_from_piece, dist_from_piece + 1):  # e.g. -1, 0, 1
				for j in range(-dist_from_piece, dist_from_piece + 1):  # e.g. -1, 0, 1
					if i != dist_from_piece and i != -dist_from_piece and j != dist_from_piece and j != -dist_from_piece:
						# if not in the right distance circle
						continue
					curr_row, curr_col = row + i, col + j
					if not self.is_coordinate_in_board_range((curr_row, curr_col)):
						# if outside the board range
						continue
					neighbor_spot = board[curr_row][curr_col]
					neighbor_coord_as_tuple = (curr_row, curr_col)
					if neighbor_spot == EMPTY and neighbor_coord_as_tuple not in empties_found_so_far:
						# if there is an empty spot here and we haven't validated it yet
						empties_found_so_far.add(neighbor_coord_as_tuple)
						lists_of_valids[dist_from_piece - 1].append([curr_row, curr_col])

		# check each distance level around each filled piece
		for distFromPiece in range(1, MAX_NEIGHBOR_DIST + 1):
			for filledCoord in filled_locations:
				locate_empty_near_spots(filledCoord, distFromPiece)

		# shuffle the moves in each distance level
		# note this will not change the order of the distances, just the moves inside each distance level
		for valid_list in lists_of_valids:
			random.shuffle(valid_list)

		# combine the lists into one big list
		valid_locations = [item for inner_list in lists_of_valids for item in inner_list]

		if len(valid_locations) == 0 and board[self.BOARD_DIMENSION//2][self.BOARD_DIMENSION//2] == EMPTY:
			# If there are no valid moves evaluated (due to no pieces played yet), but the center is open
			# This will occur when the AI is black and has the first move
			return [[self.BOARD_DIMENSION//2, self.BOARD_DIMENSION//2]]

		# return the best locations from all the valid locations
		return self.find_best_valid_moves(valid_locations, board)

	def find_best_valid_moves(self, valid_moves, board):
		"""Takes in all the spaces that were deemed valid and selects the ones that have the most potential"""
		if len(valid_moves) <= MAX_NUM_MOVES_TO_EVALUATE:
			# no need to decrease quantity
			return valid_moves

		def section_contains_threats(piece_color, section_string):
			"""
			Evaluates each length 5 and length 6 section of spots in the board for threats
			Returns True or False depending on whether a threat was found
			"""
			threat_dictionary = self.black_threats_scores if piece_color == BLACK else self.white_threats_scores
			if len(section_string) == 5:
				# if the section is only 5 spaces
				if section_string in threat_dictionary:
					return True
				return False
			for i in range(len(section_string) - 5):
				section6 = section_string[i:i+6]
				front_section5 = section6[:-1]
				if section6 in threat_dictionary:
					return True
				if front_section5 in threat_dictionary:
					return True
				if i == len(section_string) - 6:
					# if at the last 6-piece section, we want to check the final 5 spots as well
					back_section5 = section6[1:]
					if back_section5 in threat_dictionary:
						return True
			return False

		moves_with_scores = []  # each element in the form:  [moveX, moveY], score

		direction_vectors_list = [[1, -1], [1, 0], [1, 1], [0, 1]]
		for move in valid_moves:
			move_score = 0
			for direction_vector in direction_vectors_list:
				forward_score, backward_score = 0, 0
				if self.is_coordinate_in_board_range([move[0] + direction_vector[0], move[1] + direction_vector[1]]):
					forward_check_still_valid = True
					forward_piece_color = board[move[0] + direction_vector[0]][move[1] + direction_vector[1]]  # looks at first piece in forward direction
				else:
					forward_check_still_valid = False
					forward_piece_color = None

				if self.is_coordinate_in_board_range([move[0] - direction_vector[0], move[1] - direction_vector[1]]):
					backward_check_still_valid = True
					backward_piece_color = board[move[0] - direction_vector[0]][move[1] - direction_vector[1]]  # looks at first piece in backward direction
				else:
					backward_check_still_valid = False
					backward_piece_color = None

				num_forward_player_pieces, num_backward_player_pieces = 0, 0  # number of the piece we have seen in a direction
				curr_coordinates_forward, curr_coordinates_backward = move.copy(), move.copy()
				outward_spaces_checked = 0
				forward_distance_reached, backward_distance_reached = 0, 0  # how many spots until a block
				num_forward_empties_before_piece, num_backward_empties_before_piece = 0, 0  # number of empty spots before seeing a player piece
				forward_direction_str, backward_direction_str = '', ''  # string representations of the board in each direction
				
				# now will look at most 4 spaces forward in the forward and backward direction and evaluate them
				while outward_spaces_checked < 4 and (forward_check_still_valid or backward_check_still_valid):
					outward_spaces_checked += 1
					if forward_check_still_valid:
						# keep looking in the forward direction
						curr_coordinates_forward = [a + b for a, b in zip(curr_coordinates_forward, direction_vector)]  # adds the direction vector
						if self.is_coordinate_in_board_range(curr_coordinates_forward):
							curr_piece = board[curr_coordinates_forward[0]][curr_coordinates_forward[1]]
							
							if forward_piece_color == EMPTY:
								# if we have not found a player piece yet
								forward_direction_str += curr_piece
								forward_distance_reached += 1
								if curr_piece == EMPTY:
									num_forward_empties_before_piece += 1
								else:
									# if the current spot we are looking at is the first player piece we have seen
									forward_piece_color = curr_piece
									num_forward_player_pieces += 1
									forward_score += (5 - outward_spaces_checked)

							elif forward_piece_color == curr_piece:
								# current piece is the player piece that we are searching for
								forward_direction_str += curr_piece
								forward_distance_reached += 1
								num_forward_player_pieces += 1
								forward_score += (5 - outward_spaces_checked) * (2 ** (2 * (num_forward_player_pieces - 1)))

							else:
								# the current spot does not contain the piece we are searching for
								if curr_piece == EMPTY:
									forward_direction_str += curr_piece
									forward_distance_reached += 1
									forward_score += (5 - outward_spaces_checked)
								else:
									# if we have found the opposing color to the piece we are searching for
									forward_check_still_valid = False
						else:
							forward_check_still_valid = False

					if backward_check_still_valid:
						# keep looking in the backward direction
						curr_coordinates_backward = [a - b for a, b in zip(curr_coordinates_backward, direction_vector)]  # subtracts the direction vector
						if self.is_coordinate_in_board_range(curr_coordinates_backward):
							curr_piece = board[curr_coordinates_backward[0]][curr_coordinates_backward[1]]
							
							if backward_piece_color == EMPTY:
								# if we have not found a player piece yet
								backward_direction_str += curr_piece
								backward_distance_reached += 1
								if curr_piece == EMPTY:
									num_backward_empties_before_piece += 1
								else:
									# if the current spot we are looking at is the first player piece we have seen
									backward_piece_color = curr_piece
									num_backward_player_pieces += 1
									backward_score += (5 - outward_spaces_checked)

							elif backward_piece_color == curr_piece:
								# current piece is the player piece that we are searching for
								backward_direction_str += curr_piece
								backward_distance_reached += 1
								num_backward_player_pieces += 1
								backward_score += (5 - outward_spaces_checked) * (2 ** (2 * (num_backward_player_pieces - 1)))

							else:
								# the current spot does not contain the piece we are searching for
								if curr_piece == EMPTY:
									backward_direction_str += curr_piece
									backward_distance_reached += 1
									backward_score += (5 - outward_spaces_checked)
								else:
									# if we have found the opposing color to the piece we are searching for
									backward_check_still_valid = False
						else:
							backward_check_still_valid = False

				direction_vector_score = forward_score + backward_score
				if forward_piece_color == backward_piece_color:
					# if the closest piece in each direction was the same color
					if forward_distance_reached + 1 + backward_distance_reached < 5:
						# if there is less than a 5 piece section here
						direction_vector_score = 0
					else:
						threat_multiplier = 1
						if forward_piece_color != EMPTY and forward_piece_color is not None:
							# if we actually found a piece 
							full_section_string = backward_direction_str + forward_piece_color + forward_direction_str  # add in the imaginary piece to see if a threat is produced
							if section_contains_threats(forward_piece_color, full_section_string):
								threat_multiplier = 2

						direction_vector_score += max(forward_score, backward_score) * threat_multiplier
				else:
					# if the closest piece in each direction were different colors
					if forward_distance_reached + 1 + num_backward_empties_before_piece < 5 and backward_distance_reached + 1 + num_forward_empties_before_piece < 5:
						# if there is less than a 5 piece section here
						direction_vector_score = 0
					else:
						threat_multiplier = 1

						if opponent_of(forward_piece_color) == backward_piece_color and forward_piece_color is not None and backward_piece_color is not None:
							# if the pieces in each direction are opposing colors (i.e. neither are empty or out of bounds)
							if num_backward_empties_before_piece == 0:
								# if the first spot in the backward direction is a player piece
							 	forward_section_str = forward_piece_color + forward_direction_str
							else:
								# if the first spot in the backward direction is empty, we want to add an empty
								# spot to the front of this, since threats may have 0 or 1 spaces at the start/end
								forward_section_str = "." + forward_piece_color + forward_direction_str
							if num_forward_empties_before_piece == 0:
								# if the first spot in the forward direction is a player piece
							 	backward_section_str = backward_piece_color + backward_direction_str
							else:
								# if the first spot in the forward direction is empty, we want to add an empty
								# spot to the front of this, since threats may have 0 or 1 spaces at the start/end
								backward_section_str = "." + backward_piece_color + backward_direction_str

							if section_contains_threats(forward_piece_color, forward_section_str) or section_contains_threats(backward_piece_color, backward_section_str):
								threat_multiplier = 2

						else:
							# one of the directions is all empty spaces, and the other contains at least one player piece
							# OR one of the directions is out of bounds
							if forward_piece_color is None:
								# if the forward direction is out of bounds
								total_section_str = backward_piece_color + backward_direction_str
								evaluating_piece_color = backward_piece_color
							elif backward_piece_color is None:
								# if the backward direction is out of bounds
								total_section_str = forward_piece_color + forward_direction_str
								evaluating_piece_color = forward_piece_color
							else:
								if forward_piece_color == EMPTY:
									# if the forward direction is all the empties
									total_section_str = "." + backward_piece_color + backward_direction_str
									evaluating_piece_color = backward_piece_color
								else:
									# if the backward direction is all the empties
									total_section_str = "." + forward_piece_color + forward_direction_str
									evaluating_piece_color = forward_piece_color
							
							if section_contains_threats(evaluating_piece_color, total_section_str):
								threat_multiplier = 2

						direction_vector_score += max(forward_score, backward_score) * threat_multiplier

				move_score += direction_vector_score
			moves_with_scores.append([move, move_score])

		moves_with_scores.sort(key=lambda x: -x[1])  # sort in descending order by evaluated score
		highest_evaluated_moves = []
		for i in range(MAX_NUM_MOVES_TO_EVALUATE):
			highest_evaluated_moves.append(moves_with_scores[i][0])

		return highest_evaluated_moves

	def get_move(self, board):
		"""Calculates the best move for the AI for the given board"""
		move_row, move_col, score = -123, -123, -123  # placeholders
		for i in range(1, MAX_DEPTH + 1):  # iterative deepening
			# this will prioritize game winning move sets that occur with less total moves
			move_row, move_col, score = self.minimax(board, 0, MAX, -math.inf, math.inf, i, 0)
			self.BOARD_STATE_DICT.clear()  # clear the dict after every depth increase
			if score >= WIN_SCORE:
				break
		return move_row, move_col

	def minimax(self, board, depth, max_or_min, alpha, beta, local_max_depth, zobrist_value_for_board):
		"""
		Recursively finds the best move for a given board
		Returns the row in [0], column in [1], and score of the board in [2]
		"""
		if depth == local_max_depth:
			player_with_turn_after_max_depth = self.AI_COLOR if local_max_depth % 2 == 0 else self.HUMAN_COLOR
			board_scores = self.score_board(board, self.HUMAN_COLOR, self.AI_COLOR, player_with_turn_after_max_depth)
			human_score = board_scores[0]
			ai_score = board_scores[1]
			return None, None, ai_score - human_score
		
		valid_moves = self.get_valid_moves(board)
		if len(valid_moves) == 0:
			return -1, -1, 0
		if depth == 0 and len(valid_moves) == 1:
			return valid_moves[0][0], valid_moves[0][1], 0
		if max_or_min == MAX:
			# want to maximize this move
			score = -math.inf
			best_move = valid_moves[0]  # default best move
			if depth == 0:
				# on the top level of search, printing progress bar
				percent_complete = 0
				moves_checked = 0
				bar_complete_multiplier = 0
				print('\r[%s%s] %d%% (%d/%d moves checked) @ maxDepth = %d' % ("=" * bar_complete_multiplier, "-" * (25-bar_complete_multiplier), percent_complete, moves_checked, len(valid_moves), local_max_depth), end="")

			for move in valid_moves:
				if depth == 0:
					# print progress bar
					percent_complete = int((moves_checked/len(valid_moves))*100)
					bar_complete_multiplier = percent_complete // 4
					print('\r[%s%s] %d%% (%d/%d moves checked) @ maxDepth = %d' % ("=" * bar_complete_multiplier, "-" * (25-bar_complete_multiplier), percent_complete, moves_checked, len(valid_moves), local_max_depth), end="")
					moves_checked += 1

				board_copy = copy_of_board(board)  # list(map(list, board)) # copies board
				perform_move(board_copy, move[0], move[1], self.AI_COLOR)
				new_zobrist_value = self.create_zobrist_value_for_new_move(move, self.AI_COLOR, zobrist_value_for_board)
				if depth >= 2 and new_zobrist_value in self.BOARD_STATE_DICT:
					# if we've already evaluated the score of this board state
					# no chance of repeat boards until at least depth = 2
					updated_score = self.BOARD_STATE_DICT[new_zobrist_value]
				else:
					winner, game_over = self.check_if_move_caused_game_over(board_copy, move)
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
							_, __, updated_score = self.minimax(board_copy, depth + 1, MIN, alpha, beta, local_max_depth, new_zobrist_value)
					if depth >= 2:
						self.BOARD_STATE_DICT[new_zobrist_value] = updated_score
				if updated_score > score:
					score = updated_score
					best_move = move
				alpha = max(alpha, score)
				if alpha >= beta:
					break  # pruning
			if depth == 0:
				# clear progress bar print-out
				sys.stdout.write('\033[2K\033[1G')
			return best_move[0], best_move[1], score
		else: 
			# maxOrMin == MIN
			# want to minimize this move
			score = math.inf
			best_move_for_human = valid_moves[0]
			for move in valid_moves:
				board_copy = copy_of_board(board)  # copies board
				perform_move(board_copy, move[0], move[1], self.HUMAN_COLOR)
				new_zobrist_value = self.create_zobrist_value_for_new_move(move, self.HUMAN_COLOR, zobrist_value_for_board)
				if depth >= 2 and new_zobrist_value in self.BOARD_STATE_DICT:
					updated_score = self.BOARD_STATE_DICT[new_zobrist_value]
				else:
					winner, game_over = self.check_if_move_caused_game_over(board_copy, move)
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
							_, __, updated_score = self.minimax(board_copy, depth + 1, MAX, alpha, beta, local_max_depth, new_zobrist_value)
					if depth >= 2:
						self.BOARD_STATE_DICT[new_zobrist_value] = updated_score
				if updated_score < score:
					score = updated_score
					best_move_for_human = move
				beta = min(beta, score)
				if beta <= alpha:
					break  # pruning
			return best_move_for_human[0], best_move_for_human[1], score

	def score_sections(self, board, color_of_evaluator, color_of_enemy, player_with_turn_after_max_depth):
		"""Scores all the different horizontal/vertical/diagonal sections on the board"""
		evaluator_score = 0
		enemy_score = 0
		evaluator_trap_indicators = [0, 0, 0, 0]
		enemy_trap_indicators = [0, 0, 0, 0]
		if color_of_evaluator == BLACK:
			evaluator_scores_dict = self.black_threats_scores
			enemy_scores_dict = self.white_threats_scores
		else:
			evaluator_scores_dict = self.white_threats_scores
			enemy_scores_dict = self.black_threats_scores

		# Check horizontal
		for c in range(self.BOARD_DIMENSION - 5):
			for r in range(self.BOARD_DIMENSION):
				section6 = "".join(board[r][c:c + 6])
				section5 = section6[:-1]  # first 5 spaces of section 6
				if section6 in evaluator_scores_dict:
					evaluator_score += evaluator_scores_dict[section6]
					evaluator_trap_indicators[0] = 1
				elif section6 in enemy_scores_dict:
					enemy_score += enemy_scores_dict[section6]
					enemy_trap_indicators[0] = 1
				if section5 in evaluator_scores_dict:
					evaluator_score += evaluator_scores_dict[section5]
					evaluator_trap_indicators[0] = 1
				elif section5 in enemy_scores_dict:
					enemy_score += enemy_scores_dict[section5]
					enemy_trap_indicators[0] = 1
				if c == self.BOARD_DIMENSION - 6:
					# if in last section of row
					section5 = section6[1:]  # check the rightmost 5 section of the row
					if section5 in evaluator_scores_dict:
						evaluator_score += evaluator_scores_dict[section5]
						evaluator_trap_indicators[0] = 1
					elif section5 in enemy_scores_dict:
						enemy_score += enemy_scores_dict[section5]
						enemy_trap_indicators[0] = 1

		# Check vertical
		for c in range(self.BOARD_DIMENSION):
			for r in range(self.BOARD_DIMENSION - 5):
				section6 = ''
				for i in range(6):
					section6 += board[r + i][c]
				section5 = section6[:-1]  # first 5 spaces of section 6
				if section6 in evaluator_scores_dict:
					evaluator_score += evaluator_scores_dict[section6]
					evaluator_trap_indicators[1] = 1
				elif section6 in enemy_scores_dict:
					enemy_score += enemy_scores_dict[section6]
					enemy_trap_indicators[1] = 1
				if section5 in evaluator_scores_dict:
					evaluator_score += evaluator_scores_dict[section5]
					evaluator_trap_indicators[1] = 1
				elif section5 in enemy_scores_dict:
					enemy_score += enemy_scores_dict[section5]
					enemy_trap_indicators[1] = 1
				if r == self.BOARD_DIMENSION - 6:
					# if in last section of col
					section5 = section6[1:]  # check the bottom 5 section of the col
					if section5 in evaluator_scores_dict:
						evaluator_score += evaluator_scores_dict[section5]
						evaluator_trap_indicators[1] = 1
					elif section5 in enemy_scores_dict:
						enemy_score += enemy_scores_dict[section5]
						enemy_trap_indicators[1] = 1

		# Check diagonal from top left to bottom right
		for c in range(self.BOARD_DIMENSION - 5):
			for r in range(self.BOARD_DIMENSION - 5):
				section6 = ''
				for i in range(6):
					section6 += board[r + i][c + i]
				section5 = section6[:-1]
				if section6 in evaluator_scores_dict:
					evaluator_score += evaluator_scores_dict[section6]
					evaluator_trap_indicators[2] = 1
				elif section6 in enemy_scores_dict:
					enemy_score += enemy_scores_dict[section6]
					enemy_trap_indicators[2] = 1
				if section5 in evaluator_scores_dict:
					evaluator_score += evaluator_scores_dict[section5]
					evaluator_trap_indicators[2] = 1
				elif section5 in enemy_scores_dict:
					enemy_score += enemy_scores_dict[section5]
					enemy_trap_indicators[2] = 1
				if c == self.BOARD_DIMENSION - 6 or r == self.BOARD_DIMENSION - 6:
					# if in last section of this diagonal path
					section5 = section6[1:]  # check the border section
					if section5 in evaluator_scores_dict:
						evaluator_score += evaluator_scores_dict[section5]
						evaluator_trap_indicators[2] = 1
					elif section5 in enemy_scores_dict:
						enemy_score += enemy_scores_dict[section5]
						enemy_trap_indicators[2] = 1
		
		# Check diagonal from top right to bottom left
		for c in range(self.BOARD_DIMENSION - 5):
			for r in range(5, self.BOARD_DIMENSION):
				section6 = ''
				for i in range(6):
					section6 += board[r - i][c + i]
				section5 = section6[:-1]
				if section6 in evaluator_scores_dict:
					evaluator_score += evaluator_scores_dict[section6]
					evaluator_trap_indicators[3] = 1
				elif section6 in enemy_scores_dict:
					enemy_score += enemy_scores_dict[section6]
					enemy_trap_indicators[3] = 1
				if section5 in evaluator_scores_dict:
					evaluator_score += evaluator_scores_dict[section5]
					evaluator_trap_indicators[3] = 1
				elif section5 in enemy_scores_dict:
					enemy_score += enemy_scores_dict[section5]
					enemy_trap_indicators[3] = 1
				if c == self.BOARD_DIMENSION - 6 or r == 0:
					# if in last section of this diagonal path
					section5 = section6[1:]  # check the border section
					if section5 in evaluator_scores_dict:
						evaluator_score += evaluator_scores_dict[section5]
						evaluator_trap_indicators[3] = 1
					elif section5 in enemy_scores_dict:
						enemy_score += enemy_scores_dict[section5]
						enemy_trap_indicators[3] = 1

		# manually check the remaining unchecked length-5 corner sections 
		top_left, top_right, bottom_right, bottom_left = '', '', '', ''
		for i in range(5):
			top_left += board[4-i][i]
			top_right += board[i][self.BOARD_DIMENSION - (5-i)]
			bottom_right += board[self.BOARD_DIMENSION - i - 1][self.BOARD_DIMENSION - (5-i)]
			bottom_left += board[self.BOARD_DIMENSION - (5-i)][i]
		corner_counter = 1
		for section in [top_left, top_right, bottom_right, bottom_left]:
			if section in evaluator_scores_dict:
				if section.count(color_of_evaluator) == 4:
					# since a 3-piece-trap is not actually a trap in this section
					evaluator_score += evaluator_scores_dict[section]
					evaluator_trap_indicators[(corner_counter % 2) + 2] = 1
				else:
					evaluator_score += (evaluator_scores_dict[section] // 2)  # 3 piece 'traps' aren't as valuable here
			elif section in enemy_scores_dict:
				if section.count(color_of_enemy) == 4:
					# since a 3-piece-trap is not actually a trap in this section
					enemy_score += enemy_scores_dict[section]
					enemy_trap_indicators[(corner_counter % 2) + 2] = 1
				else:
					enemy_score += (enemy_scores_dict[section] // 2)  # 3 piece 'traps' aren't as valuable here
			corner_counter += 1

		number_of_evaluator_traps = sum(evaluator_trap_indicators)
		number_of_enemy_traps = sum(enemy_trap_indicators)

		# if traps found in multiple directions, weight this very heavily
		if number_of_evaluator_traps > 1:
			evaluator_score *= 4
		if number_of_enemy_traps > 1:
			enemy_score *= 4

		# if the player who is set to play next has trap sequences worth more, they will probably win, so give a big bonus
		if player_with_turn_after_max_depth == color_of_evaluator and number_of_evaluator_traps >= 1:
			evaluator_score *= 4
			if evaluator_score > enemy_score:
				return 25 * evaluator_score, enemy_score
		elif player_with_turn_after_max_depth == color_of_enemy and number_of_enemy_traps >= 1:
			enemy_score *= 4
			if enemy_score > evaluator_score:
				return evaluator_score, 25 * enemy_score

		# if both players have traps, check which player has the BETTER trap(s)
		if number_of_evaluator_traps >= 1 and number_of_enemy_traps >= 1:
			if evaluator_score > enemy_score:
				evaluator_score *= 5
			elif enemy_score > evaluator_score:
				enemy_score *= 5

		return evaluator_score, enemy_score

	def score_position_weights(self, board, color_of_evaluator, color_of_enemy):
		"""Scores the board based on the weights of the individual locations (center preferred)"""
		evaluator_score = 0
		enemy_score = 0
		for row in range(self.BOARD_DIMENSION):
			for col in range(self.BOARD_DIMENSION):
				curr_spot = board[row][col]
				if curr_spot == color_of_evaluator:
					evaluator_score += self.position_weights_matrix[row][col]
				elif curr_spot == color_of_enemy:
					enemy_score += self.position_weights_matrix[row][col]
		return evaluator_score, enemy_score

	def score_board(self, board, color_of_evaluator, color_of_enemy, player_with_turn_after_max_depth):
		"""
		Scores the entire board by looking at each section of spots,
		as well as the individual piece positions
		"""
		sections_scores = self.score_sections(board, color_of_evaluator, color_of_enemy, player_with_turn_after_max_depth)
		position_weight_scores = self.score_position_weights(board, color_of_evaluator, color_of_enemy)
		evaluator_score = sections_scores[0] + position_weight_scores[0]
		enemy_score = sections_scores[1] + position_weight_scores[1]
		return evaluator_score, enemy_score


def opponent_of(color):
	"""Get the opposing color"""
	return WHITE if color == BLACK else BLACK


def perform_move(board, row, col, color):
	"""Performs a given move on the board"""
	board[row][col] = color


def copy_of_board(board):
	"""Returns a copy of the given board"""
	return list(map(list, board))


def create_board_position_weights(dim):
	"""
	Create the position weights matrix for a board of dimension `dim`
	Center weighted heavier
	"""
	position_weights_matrix = []
	for i in range(dim):
		position_weights_matrix.append([0]*dim)  # create dim x dim matrix of 0s
	center_index = dim//2
	for i in range(dim//2):
		for row in range(center_index - i, center_index + i + 1):
			for col in range(center_index - i, center_index + i + 1):
				position_weights_matrix[row][col] += 3
	return position_weights_matrix


def create_hash_table(dimension):
	"""Fills a 2 by dimension board with random 64 bit integers"""
	table = []  # 2D
	for color in range(2):
		color_location_list = []
		for boardPos in range(dimension * dimension):
			color_location_list.append(random.getrandbits(64))
		table.append(color_location_list)
	return table
