# Kyle Gerner
# 3.12.2021
# Tool for Game Pigeon's 'Word Bites' puzzle game

from functools import cmp_to_key
from util.terminaloutput.colors import NO_COLOR, BLUE_COLOR, YELLOW_COLOR
from util.terminaloutput.symbols import ERROR_SYMBOL, error
from util.terminaloutput.erasing import erasePreviousLines

# directional constants
HORIZONTAL = 'H'
VERTICAL = 'V'

# display mode constants
LIST = 0
DIAGRAM = 1

# globals
MAX_LENGTHS = {HORIZONTAL: 8, VERTICAL: 9}  # max length of the words in each direction
DISPLAY_MODE = DIAGRAM  # default display mode
horizPieces = []  # list of horizontal letter groupings
vertPieces = []   # list of vertical letter groupings
singleLetterPieces = []  # list of letter groupings made up of a single letter
englishWords = set()  # LARGE set that will contain every possible word. Using set for O(1) lookup
wordStarts = set()  # set that holds every starting character sequence of every valid word
validWordsOnly = set()  # set of only the valid word strings (no tuple pairing)
validsWithDetails = set()  # contains the words and direction, as well as index of list of pieces from piecesList if in DIAGRAM mode
piecesList = []  # used to keep the list of pieces for a valid word (in DIAGRAM mode), since lists cannot be hashed in the set

LIST_MODE_DIRECTION_COLORS = {HORIZONTAL: BLUE_COLOR, VERTICAL: YELLOW_COLOR}
MORE_INFO_OUTPUT_HEIGHT = 30

WORD_LIST_FILEPATH = 'wordbites/letters9.txt'


def read_in_board():
	"""Read in the user's input for the board pieces"""
	versions = [('Single Letter', singleLetterPieces), 
				('Horizontal', horizPieces), 
				('Vertical', vertPieces)]
	for pair in versions:
		if versions.index(pair) + 1 < len(versions):
			next_input = "start inputting %s pieces." % versions[versions.index(pair) + 1][0]
		else:
			next_input = "calculate best piece combinations."
		print("\nPlease enter each %s piece, with each piece on its own line.\n" % pair[0] +
			  "When you are done with %s pieces, press 'enter' on an empty line\n" % pair[0] +
			  "to %s\n" % next_input)
		count = 1
		piece_str = input("%s piece #1:\t" % pair[0]).strip().lower()
		while len(piece_str) != 0:
			if not piece_str.isalpha():
				erasePreviousLines(1)
				piece_str = input(f"{ERROR_SYMBOL} Please make sure your input only contains letters.\t").strip().lower()
			else:
				if len(piece_str) != 2 and pair[0] != 'Single Letter':
					erasePreviousLines(1)
					piece_str = input(f"{ERROR_SYMBOL} All %s pieces should be 2 letters long.\t" % pair[0]).strip().lower()
				elif pair[0] == 'Single Letter' and len(piece_str) > 1:
					erasePreviousLines(1)
					piece_str = input(f"{ERROR_SYMBOL} You should be entering a single letter right now.\t").strip().lower()
				else:
					pair[1].append(piece_str)
					count += 1
					piece_str = input("%s piece #%d:\t" % (pair[0], count)).strip().lower()
		erasePreviousLines(6)
		erasePreviousLines(len(pair[1]))
		piece_list_output = ", ".join(pair[1])
		print(f"{pair[0]} pieces: {piece_list_output}")


def find_words():
	"""Calls the recursive find_words_in_direction method for each direction (H and V)"""
	find_words_in_direction(singleLetterPieces, horizPieces, vertPieces, "", HORIZONTAL, [])
	find_words_in_direction(singleLetterPieces, horizPieces, vertPieces, "", VERTICAL, [])


def find_words_in_direction(singles, horiz, vert, curr_str, direction, curr_tuples):
	"""Find all the valid words for a board in a certain direction"""
	if len(curr_str) > MAX_LENGTHS[direction]:
		# word too long
		return
	if len(curr_str) >= 3 and curr_str not in wordStarts:
		# not the beginning of a word so stop searching this expansion
		return
	if curr_str in englishWords and curr_str not in validWordsOnly:
		# valid word that hasn't been found yet
		validWordsOnly.add(curr_str)
		if DISPLAY_MODE == DIAGRAM:
			pieces_list_index = len(piecesList)
			piecesList.append(curr_tuples)
			tup = curr_str, direction, pieces_list_index
		else:
			tup = curr_str, direction
		validsWithDetails.add(tup)
	for i in range(len(singles)):
		# copy_tuples will keep track of the pieces for a word in DIAGRAM mode, is unnecessary in LIST mode
		if DISPLAY_MODE == DIAGRAM:
			copy_tuples = curr_tuples.copy()
			copy_tuples.append(singles[i])
		else:
			copy_tuples = []
		find_words_in_direction(singles[:i] + singles[i + 1:], horiz, vert, curr_str + singles[i], direction, copy_tuples)
	for j in range(len(horiz)):
		if DISPLAY_MODE == DIAGRAM:
			copy_tuples = curr_tuples.copy()
			copy_tuples.append(horiz[j])
		else:
			copy_tuples = []
		if direction == HORIZONTAL:
			find_words_in_direction(singles, horiz[:j] + horiz[j + 1:], vert, curr_str + horiz[j], direction, copy_tuples)
		else:
			for horizLetter in horiz[j]:
				find_words_in_direction(singles, horiz[:j] + horiz[j + 1:], vert, curr_str + horizLetter, direction, copy_tuples)
	for k in range(len(vert)):
		if DISPLAY_MODE == DIAGRAM:
			copy_tuples = curr_tuples.copy()
			copy_tuples.append(vert[k])
		else:
			copy_tuples = []
		if direction == HORIZONTAL:
			for vertLetter in vert[k]:
				find_words_in_direction(singles, horiz, vert[:k] + vert[k + 1:], curr_str + vertLetter, direction, copy_tuples)
		else:
			find_words_in_direction(singles, horiz, vert[:k] + vert[k + 1:], curr_str + vert[k], direction, copy_tuples)


def word_compare(a, b):
	"""For custom sorting of valid words; sorts longest to shortest, and alphabetically"""
	if len(a[0]) < len(b[0]):
		return 1
	elif len(a[0]) == len(b[0]):
		if a[0] > b[0]: 
			return 1
		elif a[0] < b[0]:
			return -1
		return 0
	return -1


def print_output(words):
	"""Print the valid words in whichever mode the user selected"""
	count = 1
	print("\n%d word%s found.\n" % (len(words), '' if len(words) == 1 else 's'))
	if DISPLAY_MODE == LIST:
		print("   #  |   Word \t|  Direction\n" +
			  "-------------------------------")
		cmd = ''
		while cmd != 'q':
			if count > 1:
				# if not the first time printing words to output
				erasePreviousLines(12)
			if cmd == 'a':
				while count <= len(words):
					dir_spacing = " "*5 + " "*(9-len(words[count - 1][0]))
					direction = words[count - 1][1]
					direction_letter_output = LIST_MODE_DIRECTION_COLORS[direction] + direction + NO_COLOR
					print("%d.\t%s%s%s" % (count, words[count - 1][0], dir_spacing, direction_letter_output))
					count += 1
				print("\nThanks for using my Word Bites Tool!\n")
				return
			for i in range(10):
				dir_spacing = " "*5 + " "*(9-len(words[count - 1][0]))
				direction = words[count - 1][1]
				direction_letter_output = LIST_MODE_DIRECTION_COLORS[direction] + direction + NO_COLOR
				print("%d.\t%s%s%s" % (count, words[count - 1][0], dir_spacing, direction_letter_output))
				count += 1
				if count - 1 == len(words):
					# if reached the end of the list
					print("\nNo more words. Thanks for using my Word Bites Tool!\n")
					return
			if count + 8 < len(words):
				grammar = "next 10 words"
			else:
				words_left = len(words) - count + 1
				if words_left > 1:
					grammar = "final %d words" % words_left
				else:
					grammar = "final word"
			cmd = input("\nPress enter for %s, or 'q' to quit, or 'a' for all:\t" % grammar).strip().lower()
		erasePreviousLines(1)
		print("Thanks for using my Word Bites Tool!\n")
	else:
		# DISPLAY_MODE = DIAGRAM
		# NOTE: This display mode was written to conform with the Game Pigeon Word Bites 
		# 		pieces standards, which means all pieces are either length 1 or 2
		word_num = 1
		lines_to_erase_from_previous_output = 0
		for wordItem in words:
			if word_num > 1:
				# if not first time through
				if input("\nPress enter for next word, or 'q' to quit:\t").strip().lower() == 'q':
					erasePreviousLines(1)
					print("Thanks for using my Word Bites Tool!\n")
					exit(0)
			erasePreviousLines(lines_to_erase_from_previous_output)
			lines_to_erase_from_previous_output = 3
			# create copies of the pieces lists because they will be edited in the next part
			singe_pieces_copy, horiz_pieces_copy, vert_pieces_copy = singleLetterPieces.copy(), horizPieces.copy(), vertPieces.copy()
			word, direction, pieces = wordItem[0], wordItem[1], piecesList[wordItem[2]]
			word_with_number = "%d:   %s" % (word_num, word)
			print()
			if direction == HORIZONTAL:
				# if word is horizontal
				index_in_word = 0
				line_above, line, line_below = "\t", "\t", "\t"
				for piece in pieces:
					if piece in vert_pieces_copy:
						# if the piece is a vertical piece
						vert_pieces_copy.remove(piece)
						if piece.index(word[index_in_word]) == 0:
							# if top letter is in word
							above, cur, below = "  ", piece[0] + " ", piece[1] + " "
						else:
							# bottom letter in word
							above, cur, below = piece[0] + " ", piece[1] + " ", " "
						index_in_word += 1
					elif piece in horiz_pieces_copy:
						# if the piece is a horizontal piece
						horiz_pieces_copy.remove(piece)
						above, cur, below = "   ", piece + " ", "   "
						index_in_word += 2
					else:
						# piece is a single letter
						singe_pieces_copy.remove(piece)
						above, cur, below = "  ", piece + " ", "  "
						index_in_word += 1
					line_above += above
					line += cur 
					line_below += below
				after_word_tabs = "\t" * (3 - (len(line) - 1)//8)
				print(f"{line_above}\n{line}{after_word_tabs}{word_with_number}\n{line_below}\n")
				lines_to_erase_from_previous_output += 4
			else:
				# if word is vertical
				index_in_word = 0
				line_left, line, line_right = "", "", ""
				for piece in pieces:
					if piece in horiz_pieces_copy:
						# if the piece is a horizonal piece
						horiz_pieces_copy.remove(piece)
						if piece.index(word[index_in_word]) == 0:
							# if left letter is in word
							left, cur, right = " ", piece[0], piece[1]
						else:
							# right letter in word
							left, cur, right = piece[0], piece[1], " "
						index_in_word += 1
					elif piece in vert_pieces_copy:
						# if the piece is a vertical piece
						vert_pieces_copy.remove(piece)
						left, cur, right = "  ", piece, "  "
						index_in_word += 2
					else:
						# piece is a single letter
						singe_pieces_copy.remove(piece)
						left, cur, right = " ", piece, " "
						index_in_word += 1
					line_left += left
					line += cur 
					line_right += right
				vertical_outputs = rotate_strings_to_vertical(line_left, line, line_right)
				index_of_full_word_output = max(int(len(vertical_outputs) / 2) - 1, 1)
				count = 0
				for line in vertical_outputs:
					if count == index_of_full_word_output:
						line += "\t\t\t%s" % word_with_number
					print(line)  # 3\t
					count += 1
				lines_to_erase_from_previous_output += len(vertical_outputs)
			word_num += 1


def rotate_strings_to_vertical(left_str, middle_str, right_str):
	"""Takes in 3 strings and 'rotates' them so that they print vertically"""
	horiz_strings = []
	for i in range(len(left_str)):
		horiz_str = "\t%s %s %s" % (left_str[i], middle_str[i], right_str[i])
		horiz_strings.append(horiz_str)
	return horiz_strings


def print_mode_info():
	"""Show the user further information about the different modes available for printing word list"""
	print("------------------------------------------------------------\n" + 
		  "------------------------------------------------------------")
	print("There are two available display modes:\n")
	print("List Mode is one large list, where each word has its own row:\n")
	print("   #  |   Word 	|  Direction\n" +
		  "-------------------------------\n" + 
		  f"1:\tathetised\t{YELLOW_COLOR}V{NO_COLOR}\n" +
		  f"2:\tbirthdays\t{YELLOW_COLOR}V{NO_COLOR}\n" +
		  f"3:\tdiameters\t{BLUE_COLOR}H{NO_COLOR}\n" +
		  " .\t    .\t\t .\n"*3)
	print("Diagram Mode feeds the user 1 word at a time, and displays a\n" + 
		  "visual representation of how to arrange the board pieces:\n")
	print("\t  a l\n\t  t\n\to h\n\t  e\t\t1:   athetised\n\t  t\n\t  i n\n\t  s\n\t  e\n\t  d\n")
	print("Press enter for next word.")


def run():
	"""main method - fills english words sets and calls other functions"""
	global DISPLAY_MODE
	# initial setup
	print("\nWelcome to Kyle's Word Bites Solver!")
	try:
		input_file = open(WORD_LIST_FILEPATH, 'r')
		for word in input_file:
			stripped_word = word.strip()
			if len(stripped_word) > max(MAX_LENGTHS.values()):
				continue
			englishWords.add(stripped_word)
			# add each word start to the set of word starts
			for i in range(3, len(stripped_word) + 1):
				wordStarts.add(stripped_word[:i])
		input_file.close()
	except FileNotFoundError:
		print()
		error(f"Could not open word list file. Please make sure {WORD_LIST_FILEPATH.split('/')[-1]} is in the Word Bites directory.\n")
		exit(0)

	# display mode select
	mode_select = input("\nUse Diagram Mode (d) or List Mode (l)? Type 'i' for more info:\t").strip().lower()
	erasePreviousLines(2)
	if mode_select == 'i':
		print_mode_info()
		mode_select = input("\nUse Diagram Mode (d) or List Mode (l)?\n").strip().lower()
		erasePreviousLines(MORE_INFO_OUTPUT_HEIGHT + 2)
	if mode_select == 'l':
		DISPLAY_MODE = LIST
		print("\nWords will be displayed in List Mode.")
	else:
		print("\nWords will be displayed in Diagram Mode.")

	# read in user input and use it to calculate best piece combinations
	read_in_board()
	find_words()
	word_cmp_key = cmp_to_key(word_compare)
	valid_words = sorted(list(validsWithDetails), key=word_cmp_key)
	if len(valid_words) == 0:
		error("There were no valid words for the board.")
		exit(0)
	print_output(valid_words)
