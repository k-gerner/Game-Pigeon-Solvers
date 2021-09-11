# Kyle Gerner
# Started 9.5.2021
# Sea Battle AI (Battleship clone)

import itertools
import math
import os

# Board characters
DESTROY = "D"
EMPTY = "-"
HIT = "H"
MISS = "^"

# Globals that can be changed throughout execution
DENSITY_PYRAMID = [] # created later; level 'i' has i integers that represent the score for a location if there are i spaces open in a row/column
game_board = [] # created later
REMAINING_SHIPS = { # ship_length: num_remaining
	1: 4,
	2: 3,
	3: 2,
	4: 1
}
SIZE = 10 # size of board

# Colors (final)
DESTROY_COLOR = '\033[92m' # green
HIT_COLOR = "\u001b[38;5;226m" # yellow
MISS_COLOR = '\033[91m' # red
MOST_RECENT_HIGHLIGHT_COLOR = '\u001b[48;5;238m' # dark grey; to make lighter, increase 238 to anything 255 or below
NO_COLOR = '\033[0m' # white
OPTIMAL_COLOR = '\033[34m' # blue


def create_game_board(dimension):
	'''Creates the gameBoard with the specified number of rows and columns'''
	global SIZE
	global REMAINING_SHIPS
	SIZE = dimension
	for row_num in range(SIZE):
		game_board.append([EMPTY] * SIZE)
	if dimension == 10:
		return
	elif dimension == 9:
		REMAINING_SHIPS = {
			3: 5,
			4: 3
		}
	else:
		# 8x8
		REMAINING_SHIPS = {
			2: 3,
			3: 3,
			4: 1
		}



def print_board(most_recent_move = None, optimal_locations = []):
	'''
	Print the game board in a readable format
	'''
	columnLabels = list(map(chr, range(65, 65 + SIZE)))
	print("\n\t    %s\n" % " ".join(columnLabels))
	ships_remain = []
	for length in list(reversed(sorted(REMAINING_SHIPS.keys()))):
		ships_remain.append([length, REMAINING_SHIPS[length]])
	for rowNum in range(SIZE):
		print("\t%d%s| " % (rowNum+1, "" if rowNum > 8 else " "), end = '')
		for colNum in range(SIZE):
			# print("%s " % spot, end='')
			spot = game_board[rowNum][colNum]
			pieceColor = MOST_RECENT_HIGHLIGHT_COLOR if [rowNum, colNum] == most_recent_move else ''
			if spot == HIT:
				pieceColor += HIT_COLOR
			elif spot == MISS:
				pieceColor += MISS_COLOR
			elif spot == DESTROY:
				pieceColor += DESTROY_COLOR
			elif [rowNum, colNum] in optimal_locations:
				pieceColor += OPTIMAL_COLOR
			else:
				pieceColor += NO_COLOR
			print(f"{pieceColor}%s{NO_COLOR} " % spot, end = '')
		if rowNum == 0:
			print("\tRemaining ships:")
		elif rowNum == 2:
			print("\t%dx  %s" % (ships_remain[0][1], "S"*ships_remain[0][0]))
		elif rowNum == 4:
			print("\t%dx  %s" % (ships_remain[1][1], "S"*ships_remain[1][0]))
		elif rowNum == 6 and len(ships_remain) > 2:
			print("\t%dx  %s" % (ships_remain[2][1], "S"*ships_remain[2][0]))
		elif rowNum == 8 and len(ships_remain) > 3:
			print("\t%dx  %s" % (ships_remain[3][1], "S"*ships_remain[3][0]))
		else:
			print("")
	print()

def print_space_densities(color_mode = False):
	'''
	Prints out the space densities chart in a readable format
	'''
	def get_color(value, max_val, min_val):
		'''
		Get the color that corresponds to the given value
		'''
		if value == max_val:
			return OPTIMAL_COLOR # blue
		elif value == 0:
			return MISS_COLOR # red
		total_range = max(max_val - min_val, 1)
		percentage = 100 * ((value - min_val) / total_range)
		if percentage > 75:
			return DESTROY_COLOR # green
		elif percentage > 40:
			return HIT_COLOR # yellow
		else:
			return "\u001b[38;5;208m" # orange

	space_densities = generate_space_densities()
	max_score, min_score = -1, 100000
	for row in space_densities:
		for val in row:
			if val > 0:
				if val < min_score:
					min_score = val
				if val > max_score:
					max_score = val
	print("\n   ", end='')
	for letter in list(map(chr, range(65, 65 + SIZE))):
		print(f"    {letter}", end='')
	print("\n   %s" % ("-"*55))
	for row_index in range(len(space_densities)):
		row = space_densities[row_index]
		print("%s%d |   " % (" " if row_index < 9 else "", row_index + 1), end='')
		for value in row:
			if color_mode:
				COLOR = get_color(value, max_score, min_score)
			else:
				COLOR = NO_COLOR
			if value == 0:
				print(f"{COLOR}0{NO_COLOR}    ", end='')
			else:
				print(f"{COLOR}%s{NO_COLOR}" % (str(value) + (4-int(math.log10(value)))*" "), end='')
		print("|")
	print("   %s\n" % ("-"*55))

def game_over():
	'''
	Checks if the game is over
	'''
	for ship_size in REMAINING_SHIPS:
		if REMAINING_SHIPS[ship_size] > 0:
			return False
	return True

def create_density_pyramid():
	'''
	Create a pyramid-shaped 2D list that contains the scores for each index given an open sequence of n spaces.
	This will make the generate_space_densities function faster
	'''
	remaining_ships = []
	for key in REMAINING_SHIPS:
		num_remaining = REMAINING_SHIPS[key]
		if num_remaining > 0:
			remaining_ships.append([key, num_remaining])
	DENSITY_PYRAMID.clear()
	for level in range(1, SIZE+1):
		row = [0] * level
		for ship_data in remaining_ships:
			ship_size, num_remaining = ship_data
			for index in range(level + 1 - ship_size):
				right_index = index + ship_size - 1
				for space in range(index, right_index + 1):
					row[space] += num_remaining
		DENSITY_PYRAMID.append(row)

def generate_space_densities():
	'''
	Generate a board where each space has densities that relate to the number of ways ships could be placed there
	NOTE: The implementation is ugly, but it works. I was trying to get this done as quick as possible.
	'''
	def fill_list_with_density_pyramid_data(arr, start_index, sequence_length):
		'''
		Take data from the density pyramid and populate a portion of the given list with that data
		'''
		data = DENSITY_PYRAMID[sequence_length - 1]
		for i in range(sequence_length):
			arr[i + start_index] += data[i]

	def get_num_open_neighbors_in_direction(arr, start_index, ship_size):
		'''
		Find the number of open spaces in each direction from the starting index
		Returns a tuple of the # spaces in the positive direction, and negative direction respectively
		'''
		pos, neg = 0, 0
		hits_in_pos_dir = 1
		hits_in_neg_dir = 1

		index = start_index + 1
		while index < len(arr) and arr[index] == HIT and hits_in_pos_dir < ship_size - 1:
			hits_in_pos_dir += 1
			index += 1
		index = start_index - 1
		while index >= 0 and arr[index] == HIT and hits_in_neg_dir < ship_size - 1:
			hits_in_neg_dir += 1
			index -= 1

		index = start_index + 1
		while index < len(arr) and arr[index] == EMPTY and pos < ship_size - hits_in_neg_dir:
			pos += 1
			index += 1
		index = start_index - 1
		while index >= 0 and arr[index] == EMPTY and neg < ship_size - hits_in_pos_dir:
			neg += 1
			index -= 1
		return pos, neg

	space_densities = []
	for i in range(SIZE):
		space_densities.append([0]*SIZE)

	# horizontal
	for row_index in range(SIZE):
		row = game_board[row_index]
		next_unavailable_index = 0
		next_open_spot = 0
		evaluating_row = True
		while evaluating_row:
			while next_open_spot < SIZE and row[next_open_spot] in [MISS, DESTROY]:
				next_open_spot += 1
			if next_open_spot == SIZE:
				evaluating_row = False
				break
			while next_unavailable_index < SIZE and row[next_unavailable_index] in [EMPTY, HIT]:
				next_unavailable_index += 1
			fill_list_with_density_pyramid_data(space_densities[row_index], next_open_spot, next_unavailable_index - next_open_spot)
			if next_unavailable_index == SIZE:
				evaluating_row = False
			next_open_spot = next_unavailable_index + 1
			next_unavailable_index += 1

	# vertical
	for col_index in range(SIZE):
		col = [row[col_index] for row in game_board]
		next_unavailable_index = 0
		next_open_spot = 0
		evaluating_col = True
		while evaluating_col:
			while next_open_spot < SIZE and col[next_open_spot] in [MISS, DESTROY]:
				next_open_spot += 1
			if next_open_spot == SIZE:
				evaluating_col = False
				break
			while next_unavailable_index < SIZE and col[next_unavailable_index] in [EMPTY, HIT]:
				next_unavailable_index += 1
			density_col = [0]*SIZE
			fill_list_with_density_pyramid_data(density_col, next_open_spot, next_unavailable_index - next_open_spot)
			for row_index in range(SIZE):
				space_densities[row_index][col_index] += density_col[row_index]
			if next_unavailable_index == SIZE:
				evaluating_col = False
			next_open_spot = next_unavailable_index + 1
			next_unavailable_index += 1

	# high scores for partially-sunken ships; also change hits to 0 scores
	largest_remaining_ship_size = 4
	while REMAINING_SHIPS[largest_remaining_ship_size] == 0:
		largest_remaining_ship_size -= 1
	max_density = max(max(val) for val in space_densities)
	for row_index in range(SIZE):
		for col_index in range(SIZE):
			if row_index == 0 and col_index == 4:
				y = 0
			spot = game_board[row_index][col_index]
			if spot == HIT:
				space_densities[row_index][col_index] = 0
				if (0 <= row_index - 1 and game_board[row_index - 1][col_index] == HIT) or (row_index + 1 < SIZE and game_board[row_index + 1][col_index] == HIT):
					# ship aligned vertically
					col = [row[col_index] for row in game_board]
					downward_space, upward_space = get_num_open_neighbors_in_direction(
						col, row_index, largest_remaining_ship_size
					)
					if 0 <= row_index - 1 and game_board[row_index-1][col_index] == EMPTY:
						space_densities[row_index - 1][col_index] = max_density + upward_space
						# space_densities[row_index - 1][col_index] *= (upward_space + 1)
					if row_index + 1 < SIZE and game_board[row_index+1][col_index] == EMPTY:
						space_densities[row_index + 1][col_index] = max_density + downward_space
						# space_densities[row_index + 1][col_index] *= (downward_space + 1)
				elif (0 <= col_index - 1 and game_board[row_index][col_index - 1] == HIT) or (col_index + 1 < SIZE and game_board[row_index][col_index + 1] == HIT):
					# ship aligned horizontally
					rightward_space, leftward_space = get_num_open_neighbors_in_direction(
						game_board[row_index], col_index, largest_remaining_ship_size
					)
					if 0 <= col_index - 1 and game_board[row_index][col_index - 1] == EMPTY:
						space_densities[row_index][col_index - 1] = max_density + leftward_space
						# space_densities[row_index][col_index - 1] *= (leftward_space + 1)
					if col_index + 1 < SIZE and game_board[row_index][col_index + 1] == EMPTY:
						space_densities[row_index][col_index + 1] = max_density + rightward_space
						# space_densities[row_index][col_index + 1] *= (rightward_space + 1)
				else:
					# no neighboring spaces have been hit, so we don't know the alignment of the ship
					col = [row[col_index] for row in game_board]
					downward_space, upward_space = get_num_open_neighbors_in_direction(
						col, row_index, largest_remaining_ship_size
					)
					rightward_space, leftward_space = get_num_open_neighbors_in_direction(
						game_board[row_index], col_index, largest_remaining_ship_size
					)
					if 0 <= row_index - 1 and game_board[row_index-1][col_index] == EMPTY:
						space_densities[row_index - 1][col_index] = max_density + upward_space
						# space_densities[row_index - 1][col_index] *= (upward_space + 1)
					if row_index + 1 < SIZE and game_board[row_index+1][col_index] == EMPTY:
						space_densities[row_index + 1][col_index] = max_density + downward_space
						# space_densities[row_index + 1][col_index] *= (downward_space + 1)
					if 0 <= col_index - 1 and game_board[row_index][col_index - 1] == EMPTY:
						space_densities[row_index][col_index - 1] = max_density + leftward_space
						# space_densities[row_index][col_index - 1] *= (leftward_space + 1)
					if col_index + 1 < SIZE and game_board[row_index][col_index + 1] == EMPTY:
						space_densities[row_index][col_index + 1] = max_density + rightward_space
						# space_densities[row_index][col_index + 1] *= (rightward_space + 1)

	return space_densities

def get_optimal_moves():
	'''
	Get a list of the coordinates of the best moves
	'''
	space_densities = generate_space_densities()
	max_score = -1
	best_move_coordinates = []
	for row_index in range(SIZE):
		for col_index in range(SIZE):
			density_score = space_densities[row_index][col_index]
			if density_score == max_score:
				best_move_coordinates.append([row_index,col_index])
			elif density_score > max_score:
				max_score = density_score
				best_move_coordinates = [[row_index, col_index]]
	return best_move_coordinates

def player_move():
	'''Takes in the user's input and performs that move on the board, returns the move'''

	def sink_ship(row, col):
		'''
		Changes the game board to display that a ship has sunk
		Updates the density pyramid
		Updates the ships remaining totals
		'''
		game_board[row][col] = DESTROY
		dir_increments = [ 
			[0, -1], # left
			[0, 1],  # right
			[-1, 0], # down
			[1, 0] 	 # up
		]
		sunken_coordinates = [[row, col]]
		for direction_pair in dir_increments:
			vert_add, horiz_add = direction_pair
			row_incremented, col_incremented = row, col
			while 0 <= (row_incremented + vert_add) < SIZE and 0 <= col_incremented + horiz_add < SIZE:
				# while in range of board
				spot = game_board[row_incremented + vert_add][col_incremented + horiz_add]
				if spot == HIT:
					game_board[row_incremented + vert_add][col_incremented + horiz_add] = DESTROY
					sunken_coordinates.append([row_incremented + vert_add, col_incremented + horiz_add])
					row_incremented += vert_add
					col_incremented += horiz_add
				else:
					break
		try:
			sunken_ship_size = len(sunken_coordinates)
			REMAINING_SHIPS[sunken_ship_size] -= 1
			create_density_pyramid()
		except:
			print("Looks like there was some confusion. Ships can only be 1 - 4 units long.\nTerminating session.")
			exit(0)

		sunken_neighbor_distances = [
			[0, -1],  # left
			[0, 1],   # right
			[-1, 0],  # down
			[1, 0],   # up
			[-1, -1], # lower left
			[-1, 1],  # lower right
			[1, -1],  # upper left
			[1, 1]    # upper right
		]
		for coord in sunken_coordinates:
			for increment in sunken_neighbor_distances:
				new_row, new_col = coord[0] + increment[0], coord[1] + increment[1]
				if 0 <= new_row < SIZE and 0 <= new_col < SIZE and game_board[new_row][new_col] == EMPTY:
					game_board[new_row][new_col] = MISS

	columnLabels = list(map(chr, range(65, 65 + SIZE)))
	spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (columnLabels[-1], SIZE)).strip().upper()
	while True:
		if spot == 'Q':
			print("\nThanks for playing!\n")
			exit(0)
		elif spot == 'SD' or spot == "SDC":
			print_space_densities(spot == "SDC")
			print("The space densities table is shown above.")
			spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (columnLabels[-1], SIZE)).strip().upper()
		elif spot == "SB":
			print_board(optimal_locations=get_optimal_moves())
			print("The current game board is shown above.")
			spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (columnLabels[-1], SIZE)).strip().upper()
		elif len(spot) >= 4 or len(spot) == 0 or spot[0] not in columnLabels or not spot[1:].isdigit() or int(spot[1:]) > SIZE or int(spot[1:]) < 1:
			spot = input("Invalid input. Please try again.\t").strip().upper()
		elif game_board[int(spot[1:]) - 1][columnLabels.index(spot[0])] != EMPTY:
			spot = input("That spot is already taken, please choose another:\t").strip().upper()
		else:
			optimal_locations = get_optimal_moves()
			row = int(spot[1:]) - 1
			col = columnLabels.index(spot[0])
			if [row, col] not in optimal_locations:
				fail_safe = input(f"{spot} is not in the list of optimal moves. Are you sure you want to make that move? (y/n)\t").strip().upper()
				while fail_safe not in ["Y", "N"]:
					fail_safe = input("Please enter 'y' or 'n':\t").strip().upper()
				if  fail_safe == "N":
					spot = input("Phew! Okay, where would you like to play? (A1 - %s%d):\t" % (columnLabels[-1], SIZE)).strip().upper()
				else:
					break
			else:
				break
	outcome = input("Was that shot a miss (M), a partial-hit (H), or a sink (S)?\t").strip().upper()
	while True:
		if outcome == 'Q':
			print("\nThanks for playing!\n")
			exit(0)
		elif outcome == "H":
			game_board[row][col] = HIT
			break
		elif outcome == "S":
			sink_ship(row, col)
			break
		elif outcome == "M":
			game_board[row][col] = MISS
			break
		else:
			outcome = input("Invalid input. Try again:\t").strip().upper()
	return [row, col]

def main():
	'''
	Main method
	'''

	os.system("") # allows colored terminal to work on Windows OS
	print("""
   _____              ____        _   _   _      
  / ____|            |  _ \\      | | | | | |     
 | (___   ___  __ _  | |_) | __ _| |_| |_| | ___ 
  \\___ \\ / _ \\/ _` | |  _ < / _` | __| __| |/ _ \\
  ____) |  __/ (_| | | |_) | (_| | |_| |_| |  __/
 |_____/ \\___|\\__,_| |____/ \\__,_|\\__|\\__|_|\\___|
 """)
	print("The default board size is 10x10.")
	print("To show the space density table, type 'sd' at the move selection prompt.")
	print("To color the space density table, type 'sdc' at the move selection prompt.")
	print("To re-display the current game board, type 'sb' at the move selection prompt.")
	print("To quit, type 'q' at any prompt.\n")

	board_dimension = input("What is the dimension of the board (8, 9, or 10)? (Default is 10x10)\nEnter a single number:\t").strip()
	if board_dimension.isdigit() and int(board_dimension) in [8, 9, 10]:
		print("The board will be %sx%s!" % (board_dimension, board_dimension))
	else:
		board_dimension = 10
		print("Invalid input. The board will be 10x10!")
	create_game_board(int(board_dimension))
	create_density_pyramid()

	most_recent_move = None
	while not game_over():
		print_board(most_recent_move)
		best_move_coordinates_list = get_optimal_moves()
		cont = input("Press enter to show optimal moves for the current board. ").strip().lower()
		if cont == 'q':
			print("\nThanks for playing!\n")
			exit(0)
		print_board(most_recent_move, best_move_coordinates_list)
		if len(best_move_coordinates_list) > 1:
			words = ["spots", "are", "have"]
		else:
			words = ["spot", "is", "has"]
		print(f"\nThe %s that %s most likely to contain a ship %s been colored {OPTIMAL_COLOR}blue{NO_COLOR}." % (words[0], words[1], words[2]))
		most_recent_move = player_move()

	print_board(most_recent_move)
	print("\nGood job, you won!\n")


if __name__ == "__main__":
	main()

