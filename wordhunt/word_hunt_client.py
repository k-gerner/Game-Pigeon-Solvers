# Kyle Gerner
# 2.24.2021
# Tool for Game Pigeon's 'Word Hunt' puzzle game

from wordhunt.small_square_board import SmallSquareBoard
from wordhunt.large_square_board import LargeSquareBoard
from wordhunt.donut_board import DonutBoard
from wordhunt.cross_board import CrossBoard
from wordhunt.letter import Letter
from util.terminaloutput.symbols import info, error
from util.terminaloutput.erasing import erasePreviousLines
from util.terminaloutput.colors import color_text
from functools import cmp_to_key
from textwrap import dedent
import sys

# Direction Constants #
UP_LEFT = 0 	# _____________
UP = 1 			# |_0_|_1_|_2_|	<-- direction layout
UP_RIGHT = 2    # |_7_|_X_|_3_|
RIGHT = 3 		# |_6_|_5_|_4_|
DOWN_RIGHT = 4
DOWN = 5
DOWN_LEFT = 6
LEFT = 7
DIRECTIONS = [UP_LEFT, UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT]
########################
# Mode Constants #
LIST = 0
DIAGRAM = 1
##################

WORDS_LIST_FILEPATH = "wordhunt/letters10.txt"
MORE_INFO_OUTPUT_HEIGHT = 26
DIAGRAM_OUTPUT_HEIGHT = 6
MIN_LENGTH = 3

english_words = set()  # LARGE set that will contain every possible word. Using set for O(1) lookup
valid_words_only = set()  # set of only the valid word strings (no tuple pairing)
valids = set()  # set of valid words paired with their starting position ( pos, word )
positions_list = []  # used to keep the lists of positions in diagram mode, since nested lists cannot be hashed
word_starts = set()  # set that holds every valid part of every word from beginning to some point in the middle


def read_in_board(board_clazz):
	"""Read in the user's input for the board letters"""
	print("Please enter each row of letters (one row at a time) in the format \"a b c d\"")
	input_letters = []
	if not board_clazz.row_sizes:
		error("Board class must have row_sizes attribute.")
		exit(0)
	for row_num, row_size in enumerate(board_clazz.row_sizes, 1):
		letters = input(f"Row {row_num} of letters ({row_size}):\t").lower()
		while True:
			letters_split = letters.split()
			if len(letters_split) == row_size:
				# if correct number of letters entered
				if all(len(letter) == 1 for letter in letters_split):
					# if all single characters
					break
			erasePreviousLines(1)
			letters = input(f"Invalid input. Please try again ({row_size}):\t").lower()
		for letter in letters_split:
			input_letters.append(letter)
	letter_objs = []
	for i in range(len(input_letters)):
		letter_objs.append(Letter(input_letters[i], i))
	board = board_clazz(letter_objs)
	erasePreviousLines(5)
	return board


def print_mode_info():
	"""Show the user further information about the different modes available for printing word list"""
	print(("-" * 60 + "\n")*2 + "There are two available display modes:\n")
	# list mode
	print("List Mode is one large list, where each word has its own row:\n")
	print("   #  |   Word \t|  Starting Position on Board\n" +
		  "----------------------------------------------")
	place = 1
	sample = [(3, "altoona"), (12, "holman"), (5, "teflon"), (1, "along")]
	for pair in sample:
		print("%d:\t%s\t %d" % (place, pair[1], pair[0]))
		place += 1
	print(" .\t  .\t .\n" * 3)
	# diagram mode
	print("\nDiagram Mode feeds the user 1 word at a time, and displays a\n" +
		  "board with the tile positions marked in order:\n")
	print("_____________________")
	print("|____|____|____|__7_|")
	print("|____|__3_|__5_|__6_|\t1:   altoona")
	print("|____|__4_|__2_|____|")
	print(f"|____|____|____|__{color_text('1')}_|")
	print("Press enter for next word.")


def word_compare(a, b):
	"""For custom sorting of valid words"""
	if len(a[1]) < len(b[1]):
		return -1
	elif len(a[1]) == len(b[1]):
		if a[1] > b[1]:
			return -1
		elif a[1] < b[1]:
			return 1
		return 0
	return 1


def read_in_words(max_length):
	""" Reads in the words from the word list file """
	try:
		input_file = open(WORDS_LIST_FILEPATH, 'r')
		for word in input_file:
			stripped_word = word.strip()  # removes newline char
			if len(stripped_word) > max_length or len(stripped_word) < MIN_LENGTH:
				continue
			english_words.add(stripped_word)
			# add each word start to the set of word starts
			for i in range(3, len(stripped_word) + 1):
				word_starts.add(stripped_word[:i])
		input_file.close()
	except FileNotFoundError:
		file_name = WORDS_LIST_FILEPATH.split('/')[-1]
		error(f"Could not open the file. Please make sure {file_name} is in the Word Hunt directory.\n")
		exit(0)


def find_valid_words(board, mode, max_length):
	"""Populate 'valid' set"""
	for letter in board.lb:
		letter.markVisited()
		if mode == LIST:
			find_valid_from(board, letter.char, letter, 1, letter.pos, LIST, max_length)
		else:
			find_valid_from(board, letter.char, letter, 1, [], DIAGRAM, max_length)
		letter.visited = False  # so later iterations don't have it marked already


def find_valid_from(board, word, letter, length, pos, mode, max_length):
	"""Find all the valid words from this letter"""
	# pos = position of starting letter (in list mode), or list of positions (in diagram mode)
	global positions_list
	if mode == DIAGRAM:
		pos.append(letter.pos)
	if length >= 3 and word not in word_starts:
		# if the current letter sequence is not the start of any word in the word set
		return
	if word in english_words and word not in valid_words_only:
		# valid word that hasn't been found yet
		valid_words_only.add(word)
		if mode == DIAGRAM:
			positions_list_index = len(positions_list)
			positions_list.append(pos)
			tup = (positions_list_index, word)
		else:
			tup = (pos, word)
		valids.add(tup)
	if length >= max_length:
		# if max word size
		return
	for direc in DIRECTIONS:
		board_copy = board.copy_board()
		neighbor_letter = board_copy.visit_direction(letter.pos, direc)
		if neighbor_letter != -1:
			# if non-visited neighbor letter exists
			pos_arg = pos.copy() if mode == DIAGRAM else pos
			find_valid_from(board_copy, word + neighbor_letter.char, neighbor_letter, length + 1, pos_arg, mode, max_length)


def print_output(valid_words, mode, board):
	"""Print the output in the format chosen by the user"""
	print("%d words were found." % len(valid_words))
	if mode == LIST:
		# list mode
		print("\n   #  |   Word \t|  Starting Position on Board\n" +
		      "----------------------------------------------")
		word_index = 0
		while True:
			for pair in valid_words[word_index : word_index + 10]:
				# pair[0] = start pos
				# pair[1] = word
				num_spaces_to_indent_index = 14 - len(pair[1])
				print("%d:\t%s%s%d" % (word_index + 1, pair[1], " " * num_spaces_to_indent_index, pair[0] + 1))
				word_index += 1
			if word_index == len(valid_words):
				break
			user_input = input("\nPress enter to see the next %d words, or 'q' to quit.\t").strip().lower()
			if user_input == 'q':
				erasePreviousLines(1)
				print("Thanks for using my Word Hunt Tool!\n")
				exit(0)
			erasePreviousLines(12)
		print()

	else:
		# diagram mode
		for word_num, pair in enumerate(valid_words, 1):
			# pair[0] = index in positions_list of this word's list of tile locations
			# pair[1] = word
			if word_num > 1:
				# if not first time through
				user_input = input("Press enter for next word, or 'q' to quit\t").strip().lower()
				erasePreviousLines(1)
				if user_input == 'q':
					print("Thanks for using my Word Hunt Tool!\n")
					exit(0)
				erasePreviousLines(board.diagram_output_height)
			positions = positions_list[pair[0]]
			word = pair[1]
			print(board.build_diagram(positions, word, word_num) + "\n")
	print("No more words, thanks for using my Word Hunt Tool!\n")


def get_board_class_from_args():
	"""
	Gets the board class specified in the command line
	params if set, or None if not specified
	"""
	board_map = {
		"4x4": SmallSquareBoard,
		"5x5": LargeSquareBoard,
		"cross": CrossBoard,
		"donut": DonutBoard
	}
	for arg in sys.argv:
		if arg.startswith("--board=") and (board_selection := arg.split("=")[1]) in board_map.keys():
			return board_map[board_selection]
	return None


def get_board_class():
	"""
	Gets the user's board selection.
	Returns the board class
	"""
	board_class = get_board_class_from_args()
	if not board_class:
		print(dedent("""
		               . . .  
		. . . .      . . . . .
		. . . .      . .   . .
		. . . .      . . . . .
		. . . .        . . .
		[1] - 4x4   [2] - Donut
		   
		. .   . .    . . . . .
		. . . . .    . . . . .
		  . . .      . . . . .
		. . . . .    . . . . .
		. .   . .    . . . . .
		[3] - Cross  [4] - 5x5
		"""))
		layout_num = input("Which board layout would you like to use? [1 - 4]\n").strip()
		erasePreviousLines(17)
		if not layout_num.isdigit() or not (1 <= int(layout_num) <= 4):
			info(f"Using default {SmallSquareBoard.name} board layout.")
			return SmallSquareBoard
		board_map = {
			1: SmallSquareBoard,
			2: DonutBoard,
			3: CrossBoard,
			4: LargeSquareBoard
		}
		board_class = board_map[int(layout_num)]
	info(f"Using the {board_class.name} board layout.")
	return board_class


def get_display_mode_from_args():
	"""
	Gets the display mode specified in the command line
	params if set, or None if not specified
	"""
	display_mode_map = {
		"list": LIST,
		"diagram": DIAGRAM
	}
	for arg in sys.argv:
		if arg.startswith("--display=") and (mode := arg.split("=")[1]) in display_mode_map.keys():
			return display_mode_map[mode]
	return None


def get_display_mode():
	display_mode = get_display_mode_from_args()
	if not display_mode:
		mode_select = input("\nUse Diagram Mode (d) or List Mode (l)? Type 'i' for more info:\t").strip().lower()
		erasePreviousLines(2)
		if mode_select == 'i':
			print_mode_info()
			mode_select = input("\nUse Diagram Mode (d) or List Mode (l)?\t").strip().lower()
			erasePreviousLines(MORE_INFO_OUTPUT_HEIGHT + 2)
		if mode_select == 'l':
			display_mode = LIST
		else:
			display_mode = DIAGRAM
	if display_mode == LIST:
		info("Words will be displayed in List Mode.\n")
	else:
		info("Words will be displayed in Diagram Mode.\n")
	return display_mode


def get_max_word_length():
	"""Gets the max word length specified from the command line, or default if not specified"""
	for arg in sys.argv:
		if arg.startswith("--maxWordLength=") and (val := arg.split("=")[1]).isdigit() and 3 <= int(val) <= 10:
			max_length = int(val)
			info(f"Using max word length of {max_length}.")
			return max_length
	info(f"Using default max word length of 10.")
	return 10


def run():
	print("Welcome to Kyle's Word Hunt solver!")
	board_class = get_board_class()
	max_length = get_max_word_length()
	read_in_words(max_length)
	output_mode = get_display_mode()

	board = read_in_board(board_class)

	print("\nThe board is: ")
	print(board.board_letters_layout())
	if output_mode == LIST:
		print(dedent(board.letter_indices_layout()))
		print("\n^ Letter tile index positions\n")
	find_valid_words(board, output_mode, max_length)
	valid_words_sorted = sorted(list(valids), key=cmp_to_key(word_compare), reverse=True)
	if len(valid_words_sorted) == 0:
		error("There were no valid words for the board.")
		exit(0)
	print_output(valid_words_sorted, output_mode, board)
