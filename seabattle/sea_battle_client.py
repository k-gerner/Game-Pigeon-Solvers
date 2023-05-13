# Kyle Gerner
# Started 9.5.2021
# Sea Battle AI (Battleship clone)
from datetime import datetime
from util.terminaloutput.colors import GREEN_COLOR as DESTROY_COLOR, \
	YELLOW_COLOR as HIT_COLOR,\
	RED_COLOR as MISS_COLOR, \
	DARK_GREY_BACKGROUND as MOST_RECENT_HIGHLIGHT_COLOR, \
	DARK_PURPLE_COLOR as OPTIMAL_COLOR, \
	NO_COLOR
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL
from util.terminaloutput.erasing import erasePreviousLines
from util.save.saving import path_to_save_file
import math
import os
import sys

# Board characters
DESTROY = "D"
EMPTY = "-"
HIT = "H"
MISS = "^"

# Globals that can be changed throughout execution
DENSITY_PYRAMID = []  # created later; level 'i' has i integers that represent the score for a location if there are i spaces open in a row/column
game_board = []  # created later
REMAINING_SHIPS = {  # ship_length: num_remaining
	1: 4,
	2: 3,
	3: 2,
	4: 1
}
SIZE = 10  # size of board
COLUMN_LABELS = []  # Letters that correspond to the columns; Gets set when board is created

ERASE_MODE_ON = True
SAVE_FILENAME = path_to_save_file("sea_battle_save.txt")

BOARD_OUTPUT_HEIGHT = -1  # Height of the output from printing the board; Gets set when board is created
SPACE_DENSITY_TABLE_OUTPUT_HEIGHT = -1  # Height of the output from printing the space density table; Gets set when board is created


def create_game_board(dimension):
	"""Creates the gameBoard with the specified number of rows and columns"""
	global REMAINING_SHIPS
	for row_num in range(dimension):
		game_board.append([EMPTY] * dimension)
	if dimension == 10:
		return
	elif dimension == 9:
		REMAINING_SHIPS = {
			3: 5,
			4: 3
		}
	elif dimension == 8:
		REMAINING_SHIPS = {
			2: 3,
			3: 3,
			4: 1
		}
	else:
		print(f"{ERROR_SYMBOL} Board can only be 8x8, 9x9, or 10x10.")
		print("Terminating session.")
		exit(0)


def print_board(most_recent_move=None, optimal_locations=None):
	"""
	Print the game board in a readable format
	"""
	if optimal_locations is None:
		optimal_locations = []
	print("\n\t    %s\n" % " ".join(COLUMN_LABELS))
	ships_remain = []
	for length in list(reversed(sorted(REMAINING_SHIPS.keys()))):
		ships_remain.append([length, REMAINING_SHIPS[length]])
	for rowNum in range(SIZE):
		print("\t%d%s| " % (rowNum+1, "" if rowNum > 8 else " "), end = '')
		for colNum in range(SIZE):
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


def print_space_densities(color_mode=True):
	"""
	Prints out the space densities chart in a readable format
	"""
	def get_color(value, max_val, min_val):
		"""
		Get the color that corresponds to the given value
		"""
		if value == max_val:
			return OPTIMAL_COLOR  # blue
		elif value == 0:
			return MISS_COLOR  # red
		total_range = max(max_val - min_val, 1)
		percentage = 100 * ((value - min_val) / total_range)
		if percentage > 75:
			return DESTROY_COLOR # green
		elif percentage > 40:
			return HIT_COLOR # yellow
		else:
			return "\u001b[38;5;208m"  # orange

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
				print(f"{COLOR}%s{NO_COLOR}" % (str(int(value)) + (4-int(math.log10(value)))*" "), end='')
		print("|")
	print("   %s\n" % ("-"*55))


def game_over():
	"""
	Checks if the game is over
	"""
	if not any(EMPTY in row for row in game_board):
		return True
	for ship_size in REMAINING_SHIPS:
		if REMAINING_SHIPS[ship_size] > 0:
			return False
	return True


def save_game():
	"""Saves the given board state to a save file"""
	if os.path.exists(SAVE_FILENAME):
		with open(SAVE_FILENAME, 'r') as saveFile:
			try:
				timeOfPreviousSave = saveFile.readlines()[3].strip()
				overwrite = input(f"{INFO_SYMBOL} A save state already exists from {timeOfPreviousSave}.\nIs it okay to overwrite it? (y/n)\t").strip().lower()
				erasePreviousLines(1)
				while overwrite not in ['y', 'n']:
					erasePreviousLines(1)
					overwrite = input(f"{ERROR_SYMBOL} Invalid input. Is it okay to overwrite the existing save state? (y/n)\t").strip().lower()
				erasePreviousLines(1)
				if overwrite == 'n':
					print(f"{INFO_SYMBOL} The current game state will not be saved.")
					return
			except IndexError:
				pass
	with open(SAVE_FILENAME, 'w') as saveFile:
		saveFile.write("This file contains the save state of a previously played game.\n")
		saveFile.write("Modifying this file may cause issues with loading the save state.\n\n")
		timeOfSave = datetime.now().strftime("%m/%d/%Y at %I:%M:%S %p")
		saveFile.write(timeOfSave + "\n\n")
		saveFile.write("SAVE STATE:\n")
		for row in game_board:
			saveFile.write(" ".join(row) + "\n")
		saveFile.write("Ships remaining:\n")
		for shipSize, numShips in REMAINING_SHIPS.items():
			saveFile.write(f"{shipSize}: {numShips}\n")
		saveFile.write("END")
	print(f"{INFO_SYMBOL} The game has been saved!")


def validateLoadedSaveState(board):
	"""Make sure the state loaded from the save file is valid. Returns a boolean"""
	board_dimension = len(board)
	if board_dimension not in [8, 9, 10]:
		print(f"{ERROR_SYMBOL} Invalid board size!")
		return False
	for row in board:
		if len(row) != board_dimension:
			print(f"{ERROR_SYMBOL} Board is not square!")
			return False
		for spot in row:
			if spot not in [DESTROY, HIT, MISS, EMPTY]:
				print(f"{ERROR_SYMBOL} Board contains invalid pieces!")
				return False
	for ship_size, num_ships in REMAINING_SHIPS.items():
		if not 1 <= ship_size <= 4:
			print(f"{ERROR_SYMBOL} Invalid ship size: {ship_size}")
			return False
		if not num_ships > 0:
			print(f"{ERROR_SYMBOL} Invalid number of ships remaining for size {ship_size}: {num_ships}")
			return False
	return True


def loadSavedGame():
	"""Try to load the saved game data. Returns boolean for if the save was successful."""
	global game_board
	with open(SAVE_FILENAME, 'r') as saveFile:
		try:
			linesFromSaveFile = saveFile.readlines()
			timeOfPreviousSave = linesFromSaveFile[3].strip()
			useExistingSave = input(f"{INFO_SYMBOL} Would you like to load the saved game from {timeOfPreviousSave}? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			if useExistingSave != 'y':
				print(f"{INFO_SYMBOL} Starting a new game...")
				return
			lineNum = 0
			currentLine = linesFromSaveFile[lineNum].strip()
			while currentLine != "SAVE STATE:":
				lineNum += 1
				currentLine = linesFromSaveFile[lineNum].strip()
			lineNum += 1

			currentLine = linesFromSaveFile[lineNum].strip()
			board_from_save_file = []
			while not currentLine.startswith("Ships remaining:"):
				board_from_save_file.append(currentLine.split())
				lineNum += 1
				currentLine = linesFromSaveFile[lineNum].strip()
			lineNum += 1

			currentLine = linesFromSaveFile[lineNum].strip()
			while not currentLine.startswith("END"):
				ship_size, num_ships = currentLine.split(":")[:2]
				REMAINING_SHIPS[int(ship_size.strip())] = int(num_ships.strip())
				lineNum += 1
				currentLine = linesFromSaveFile[lineNum].strip()

			if not validateLoadedSaveState(board_from_save_file):
				raise ValueError
			game_board = board_from_save_file
			deleteSaveFile = input(f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			fileDeletedText = ""
			if deleteSaveFile == 'y':
				os.remove(SAVE_FILENAME)
				fileDeletedText = "Save file deleted. "
			print(f"{INFO_SYMBOL} {fileDeletedText}Resuming saved game...")
			return True
		except:
			print(f"{ERROR_SYMBOL} There was an issue reading from the save file. Starting a new game...")
			return False


def create_density_pyramid():
	"""
	Create a pyramid-shaped 2D list that contains the scores for each index given an open sequence of n spaces.
	This will make the generate_space_densities function faster
	"""
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
	"""
	Generate a board where each space has densities that relate to the number of ways ships could be placed there
	NOTE: The implementation is ugly, but it works. I was trying to get this done as quick as possible.
	"""
	def fill_list_with_density_pyramid_data(arr, start_index, sequence_length):
		"""
		Take data from the density pyramid and populate a portion of the given list with that data
		"""
		data = DENSITY_PYRAMID[sequence_length - 1]
		for i in range(sequence_length):
			arr[i + start_index] += data[i]

	def get_num_open_neighbors_in_direction(arr, start_index, ship_size):
		"""
		Find the number of open spaces in each direction from the starting index
		Returns a tuple of the # spaces in the positive direction, and negative direction respectively
		"""
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

	def get_num_immediate_neighbors(row, col):
		"""
		Find the number of open spaces that are immediately next to the specified coordinate.
		0 < num_open < 8
		"""
		num_open = 0
		for row_add in [-1, 0, 1]:
			for col_add in [-1, 0, 1]:
				if row_add == col_add == 0:
					continue
				if 0 <= row + row_add < SIZE and 0 <= col + col_add < SIZE and game_board[row+row_add][col+col_add] == EMPTY:
					num_open += 1
		return num_open


	space_densities = []
	for i in range(SIZE):
		space_densities.append([0]*SIZE)

	# Look at horizontal open space and fill space_densities accordingly
	for row_index in range(SIZE):
		row = game_board[row_index]
		next_unavailable_index = 0
		next_open_spot = 0
		evaluating_row = True
		while evaluating_row:
			while next_open_spot < SIZE and row[next_open_spot] in [MISS, DESTROY]:
				next_open_spot += 1
			if next_open_spot == SIZE:
				break
			while next_unavailable_index < SIZE and row[next_unavailable_index] in [EMPTY, HIT]:
				next_unavailable_index += 1
			fill_list_with_density_pyramid_data(space_densities[row_index], next_open_spot, next_unavailable_index - next_open_spot)
			if next_unavailable_index == SIZE:
				evaluating_row = False
			next_open_spot = next_unavailable_index + 1
			next_unavailable_index += 1

	# Look at vertical open space and fill space_densities accordingly
	for col_index in range(SIZE):
		col = [row[col_index] for row in game_board]
		next_unavailable_index = 0
		next_open_spot = 0
		evaluating_col = True
		while evaluating_col:
			while next_open_spot < SIZE and col[next_open_spot] in [MISS, DESTROY]:
				next_open_spot += 1
			if next_open_spot == SIZE:
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

	# Give preference to spots where a hit/sink would clear the most space on the board (spaces with more open immediate neighbors)
	for row_index in range(SIZE):
		for col_index in range(SIZE):
			space_densities[row_index][col_index] *= (1 + 0.05 * get_num_immediate_neighbors(row_index, col_index))

	# high scores for partially-sunken ships; also change hits to 0 scores
	largest_remaining_ship_size = max(ship_size for ship_size, num_left in REMAINING_SHIPS.items() if num_left > 0)
	max_density = max(max(val) for val in space_densities)
	for row_index in range(SIZE):
		for col_index in range(SIZE):
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
						space_densities[row_index - 1][col_index] = (max_density + upward_space) * (1 + 0.02 * get_num_immediate_neighbors(row_index-1, col_index))
						# space_densities[row_index - 1][col_index] *= (upward_space + 1)
					if row_index + 1 < SIZE and game_board[row_index+1][col_index] == EMPTY:
						space_densities[row_index + 1][col_index] = (max_density + downward_space) * (1 + 0.02 * get_num_immediate_neighbors(row_index+1, col_index))
						# space_densities[row_index + 1][col_index] *= (downward_space + 1)
				elif (0 <= col_index - 1 and game_board[row_index][col_index - 1] == HIT) or (col_index + 1 < SIZE and game_board[row_index][col_index + 1] == HIT):
					# ship aligned horizontally
					rightward_space, leftward_space = get_num_open_neighbors_in_direction(
						game_board[row_index], col_index, largest_remaining_ship_size
					)
					if 0 <= col_index - 1 and game_board[row_index][col_index - 1] == EMPTY:
						space_densities[row_index][col_index - 1] = (max_density + leftward_space) * (1 + 0.02 * get_num_immediate_neighbors(row_index, col_index-1))
						# space_densities[row_index][col_index - 1] *= (leftward_space + 1)
					if col_index + 1 < SIZE and game_board[row_index][col_index + 1] == EMPTY:
						space_densities[row_index][col_index + 1] = (max_density + rightward_space) * (1 + 0.02 * get_num_immediate_neighbors(row_index, col_index+1))
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
						space_densities[row_index - 1][col_index] = (max_density + upward_space) * (1 + 0.02 * get_num_immediate_neighbors(row_index-1, col_index))
						# space_densities[row_index - 1][col_index] *= (upward_space + 1)
					if row_index + 1 < SIZE and game_board[row_index+1][col_index] == EMPTY:
						space_densities[row_index + 1][col_index] = (max_density + downward_space) * (1 + 0.02 * get_num_immediate_neighbors(row_index+1, col_index))
						# space_densities[row_index + 1][col_index] *= (downward_space + 1)
					if 0 <= col_index - 1 and game_board[row_index][col_index - 1] == EMPTY:
						space_densities[row_index][col_index - 1] = (max_density + leftward_space) * (1 + 0.02 * get_num_immediate_neighbors(row_index, col_index-1))
						# space_densities[row_index][col_index - 1] *= (leftward_space + 1)
					if col_index + 1 < SIZE and game_board[row_index][col_index + 1] == EMPTY:
						space_densities[row_index][col_index + 1] = (max_density + rightward_space) * (1 + 0.02 * get_num_immediate_neighbors(row_index, col_index+1))
						# space_densities[row_index][col_index + 1] *= (rightward_space + 1)

	return space_densities


def get_optimal_moves():
	"""
	Get a list of the coordinates of the best moves
	"""
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


def sink_ship(row, col):
	"""
    Changes the game board to display that a ship has sunk
    Updates the density pyramid
    Updates the ships remaining totals
    """
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
	except KeyError:
		possible_lengths = str(list(REMAINING_SHIPS.keys()))[1:-1]
		print(f"Looks like there was some confusion. Ships can only be one of the following lengths: {possible_lengths}")
		print("Terminating session.")
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


def get_player_move():
	"""Takes in the user's input and performs that move on the board, returns the coordinates of the move"""
	spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (COLUMN_LABELS[-1], SIZE)).strip().upper()
	erasePreviousLines(1)
	linesToErase = BOARD_OUTPUT_HEIGHT + 2
	while True:
		if spot == 'Q':
			print("\nThanks for playing!\n")
			exit(0)
		elif spot == 'D':
			erasePreviousLines(linesToErase)
			print_space_densities()
			linesToErase = SPACE_DENSITY_TABLE_OUTPUT_HEIGHT
			print("The space densities table is shown above. To show the game board, type 'b'")
			spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (COLUMN_LABELS[-1], SIZE)).strip().upper()
			erasePreviousLines(2)
		elif spot == "B":
			erasePreviousLines(linesToErase)
			print_board(optimal_locations=get_optimal_moves())
			print("\nThe current game board is shown above.")
			linesToErase = BOARD_OUTPUT_HEIGHT + 2
			spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (COLUMN_LABELS[-1], SIZE)).strip().upper()
			erasePreviousLines(1)
		elif spot == 'S':
			save_game()
			spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (COLUMN_LABELS[-1], SIZE)).strip().upper()
			erasePreviousLines(2)
		elif len(spot) >= 4 or len(spot) == 0 or spot[0] not in COLUMN_LABELS or not spot[1:].isdigit() or int(spot[1:]) > SIZE or int(spot[1:]) < 1:
			spot = input(f"{ERROR_SYMBOL} Invalid input. Please try again.\t").strip().upper()
			erasePreviousLines(1)
		elif game_board[int(spot[1:]) - 1][COLUMN_LABELS.index(spot[0])] != EMPTY:
			spot = input(f"{ERROR_SYMBOL} That spot is already taken, please choose another:\t").strip().upper()
			erasePreviousLines(1)
		else:
			optimal_locations = get_optimal_moves()
			row = int(spot[1:]) - 1
			col = COLUMN_LABELS.index(spot[0])
			if [row, col] not in optimal_locations:
				fail_safe = input(f"{ERROR_SYMBOL} {spot} is not in the list of optimal moves. Are you sure you want to make that move? (y/n)\t").strip().upper()
				erasePreviousLines(1)
				while fail_safe not in ["Y", "N"]:
					fail_safe = input(f"{ERROR_SYMBOL} Please enter 'y' or 'n':\t").strip().upper()
					erasePreviousLines(1)
				if  fail_safe == "N":
					spot = input("Phew! Okay, where would you like to play? (A1 - %s%d):\t" % (COLUMN_LABELS[-1], SIZE)).strip().upper()
					erasePreviousLines(1)
				else:
					break
			else:
				break
	if linesToErase == SPACE_DENSITY_TABLE_OUTPUT_HEIGHT:
		print()
	return [row, col]


def run():
	"""
	Main method that prompts the user for input
	"""
	global SIZE, BOARD_OUTPUT_HEIGHT, SPACE_DENSITY_TABLE_OUTPUT_HEIGHT, COLUMN_LABELS
	os.system("") # allows colored terminal to work on Windows OS
	if len(sys.argv) == 2 and sys.argv[1] in ["-e", "-eraseModeOff"]:
		global ERASE_MODE_ON
		ERASE_MODE_ON = False
	print("""
   _____              ____        _   _   _      
  / ____|            |  _ \\      | | | | | |     
 | (___   ___  __ _  | |_) | __ _| |_| |_| | ___ 
  \\___ \\ / _ \\/ _` | |  _ < / _` | __| __| |/ _ \\
  ____) |  __/ (_| | | |_) | (_| | |_| |_| |  __/
 |_____/ \\___|\\__,_| |____/ \\__,_|\\__|\\__|_|\\___|
 """)
	print("The default board size is 10x10.")
	print("To show the color-coded space density table, type 'd' at the move selection prompt.")
	print("To re-display the current game board, type 'b' at the move selection prompt.")
	print("To save the game, type 's' at the move selection prompt.")
	print("To quit, type 'q' at any prompt.\n")

	useSavedGame = False
	if os.path.exists(SAVE_FILENAME):
		useSavedGame = loadSavedGame()
	board_dimension = len(game_board)

	if not useSavedGame:
		board_dimension = input("What is the dimension of the board (8, 9, or 10)? (Default is 10x10)\nEnter a single number:\t").strip()
		erasePreviousLines(2)
		if board_dimension.isdigit() and int(board_dimension) in [8, 9, 10]:
			print("The board will be %sx%s!" % (board_dimension, board_dimension))
		else:
			board_dimension = 10
			print(f"{ERROR_SYMBOL} Invalid input. The board will be 10x10!")
		create_game_board(int(board_dimension))
	SIZE = int(board_dimension)
	BOARD_OUTPUT_HEIGHT = SIZE + 4
	SPACE_DENSITY_TABLE_OUTPUT_HEIGHT = SIZE + 5
	COLUMN_LABELS = list(map(chr, range(65, 65 + SIZE)))

	create_density_pyramid()
	best_move_coordinates_list = get_optimal_moves()
	print_board(optimal_locations=best_move_coordinates_list)
	while True:
		if len(best_move_coordinates_list) > 1:
			words = ["spots", "are", "have"]
		else:
			words = ["spot", "is", "has"]
		print(f"\nThe %s that %s most likely to contain a ship %s been colored {OPTIMAL_COLOR}blue{NO_COLOR}." % (words[0], words[1], words[2]))
		most_recent_move = get_player_move()
		row, col = most_recent_move
		erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
		print_board([row, col], best_move_coordinates_list)
		print("\nThe selected move has been highlighted.")
		outcome = input(f"Was that shot a miss (M), a partial-hit (H), or a sink (S)?\t").strip().upper()
		erasePreviousLines(1)
		while outcome not in ['Q', 'H', 'S', 'M']:
			outcome = input(f"{ERROR_SYMBOL} Invalid input. Try again:\t").strip().upper()
			erasePreviousLines(1)
		if outcome == 'M':
			game_board[row][col] = MISS
		elif outcome == "H":
			game_board[row][col] = HIT
		elif outcome == "S":
			sink_ship(row, col)
		else: # outcome = Q
			print("\nThanks for playing!\n")
			exit(0)

		if game_over():
			break
		best_move_coordinates_list = get_optimal_moves()
		erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
		print_board([row, col], best_move_coordinates_list)

	erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
	print_board(most_recent_move)
	print("\nGood job, you won!\n")
