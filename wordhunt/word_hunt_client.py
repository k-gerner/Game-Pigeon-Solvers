# Kyle Gerner
# 2.24.2021
# Tool for Game Pigeon's 'Word Hunt' puzzle game

from wordhunt.small_square_board import SmallSquareBoard
from wordhunt.letter import Letter
from util.terminaloutput.symbols import ERROR_SYMBOL, WARN_SYMBOL, INFO_SYMBOL
from util.terminaloutput.erasing import erasePreviousLines
from functools import cmp_to_key
import os
import sys

# Direction Constants #
UPLEFT = 0 	# _____________
UP = 1 		# |_0_|_1_|_2_|	<-- direction layout
UPRIGHT = 2	# |_7_|_X_|_3_|
RIGHT = 3 	# |_6_|_5_|_4_|
DOWNRIGHT = 4
DOWN = 5
DOWNLEFT = 6
LEFT = 7
DIRECTIONS = [UPLEFT, UP, UPRIGHT, RIGHT, DOWNRIGHT, DOWN, DOWNLEFT, LEFT]
########################
# Mode Constants #
LIST = 0
DIAGRAM = 1
##################

WORDS_LIST_FILEPATH = "wordhunt/letters10.txt"
MORE_INFO_OUTPUT_HEIGHT = 26
DIAGRAM_OUTPUT_HEIGHT = 6

englishWords = set() # LARGE set that will contain every possible word. Using set for O(1) lookup
validWordsOnly = set() # set of only the valid word strings (no tuple pairing)
valids = set() # set of valid words paired with their starting position ( pos, word )
MAX_LENGTH = 10 # max length of the words to find; can be changed by user input
positionsList = [] # used to keep the lists of positions in diagram mode, since nested lists cannot be hashed
wordStarts = set() # set that holds every valid part of every word from beginning to some point in the middle


def readInBoard(board_clazz, row_sizes):
	"""Read in the user's input for the board letters"""
	print("Please enter each row of letters (one row at a time) in the format \"a b c d\"")
	input_letters = []
	for i in range(len(row_sizes)):
		letters = input("Row %d of letters:\t" % (i+1)).lower()
		while True:
			letters_split = letters.split()
			if len(letters_split) == row_sizes[i]:
				# if correct number of letters entered
				if all(len(letter) == 1 for letter in letters_split):
					# if all single characters
					break
			erasePreviousLines(1)
			letters = input("Invalid input. Please try again:\t").lower()
		for letter in letters_split:
			input_letters.append(letter)
	letter_objs = []
	for i in range(len(input_letters)):
		letter_objs.append(Letter(input_letters[i], i))
	board = board_clazz(letter_objs)
	return board


def printBoard(board):
	"""Prints the letter board in a user-readable format"""
	ind = 0
	for letter in board.lb:
		print("%c " % letter.char, end='')
		if ind % 4 == 3:
			# on right side, print new line
			print("")
		ind += 1
	print("")


def printModeInfo():
	"""Show the user further information about the different modes available for printing word list"""
	print(("-" * 60 + "\n")*2 + "There are two available display modes:\n")
	# list mode
	print("List Mode is one large list, where each word has its own row:\n")
	print("   X  |   Word \t|  Starting Position on Board\n" + 
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
	print("|____|____|____|__1_|")
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


def findValidWords(board, mode):
	"""Populate 'valid' set"""
	for letter in board.lb:
		letter.markVisited()
		if mode == LIST:
			findValidFrom(board, letter.char, letter, 1, letter.pos, LIST)
		else:
			findValidFrom(board, letter.char, letter, 1, [], DIAGRAM)
		letter.visited = False # so later iterations don't have it marked already


def findValidFrom(board, word, letter, length, pos, mode):
	"""Find all the valid words from this letter"""
	# pos = position of starting letter (in list mode), or list of positions (in diagram mode)
	global positionsList
	if mode == DIAGRAM: 
		pos.append(letter.pos)
	if length >= 3 and word not in wordStarts:
		# if the current letter sequence is not the start of any word in the word set
		return
	if word in englishWords and word not in validWordsOnly:
		# valid word that hasn't been found yet
		validWordsOnly.add(word)
		if mode == DIAGRAM:
			positionsListIndex = len(positionsList)
			positionsList.append(pos)
			tup = (positionsListIndex, word)
		else:
			tup = (pos, word)
		valids.add(tup)
	if length >= MAX_LENGTH:
		# if max word size
		return
	for direc in DIRECTIONS:
		copyBoard = board.copyBoard()
		neighborLetter = copyBoard.visitDirection(letter.pos, direc)
		if neighborLetter != -1:
			# if non-visited neighbor letter exists
			posArg = pos.copy() if mode == DIAGRAM else pos
			findValidFrom(copyBoard, word + neighborLetter.char, neighborLetter, length + 1, posArg, mode)


def printOutput(validWords, mode):
	"""Print the output in the format chosen by the user"""
	print("%d words were found." % len(validWords))
	if mode == LIST:
		# list mode
		print("\n   #  |   Word \t|  Starting Position on Board\n" +
		      "----------------------------------------------")
		wordIndex = 0
		while True:
			for pair in validWords[wordIndex : wordIndex + 10]:
				# pair[0] = start pos
				# pair[1] = word
				numSpacesToIndentIndexOutput = 14 - len(pair[1])
				print("%d:\t%s%s%d" % (wordIndex + 1, pair[1], " " * numSpacesToIndentIndexOutput, pair[0] + 1))
				wordIndex += 1
			if wordIndex == len(validWords):
				break
			userInput = input("\nPress enter to see the next %d words, or 'q' to quit.\t").strip().lower()
			if userInput == 'q':
				erasePreviousLines(1)
				print("Thanks for using my Word Hunt Tool!\n")
				exit(0)
			erasePreviousLines(12)
		print()

	else:
		# diagram mode
		place = 1
		for pair in validWords:
			# pair[0] = index in positionsList of this word's list of tile locations
			# pair[1] = word
			if place > 1:
				# if not first time through
				next = input("Press enter for next word, or 'q' to quit\t")
				if next == 'q':
					erasePreviousLines(1)
					print("Thanks for using my Word Hunt Tool!\n")
					exit(0)
				erasePreviousLines(DIAGRAM_OUTPUT_HEIGHT + 1)
			squares = ["____"] * 16
			letterPos = 1
			# populate the board strings
			positions = positionsList[pair[0]]
			for pos in positions:
				leftUnderscores = "__" if letterPos < 10 else "_"
				squares[pos] = leftUnderscores + str(letterPos) + "_"
				letterPos += 1
			# print the board
			print("_____________________")
			index = 0
			outStr = "|"
			for sq in squares:
				outStr += sq + "|"
				if index % 4 == 3:
					# if on far right
					if index == 7:
						# if on second output row, print the word info
						print(outStr + "\t%d:   %s" % (place, pair[1]))
					else:
						print(outStr)
					outStr = "|"
				index += 1
			print()
			place += 1
	print("No more words, thanks for using my Word Hunt Tool!\n")


def get_board_size_values():
	layout = input("Which board layout would you like to use? [1 - 4]\n").strip()
	erasePreviousLines(2)
	if layout == "1":
		print(f"{INFO_SYMBOL} Using the 4x4 board layout.")
		return SmallSquareBoard, [4, 4, 4, 4]
	elif layout == "2":
		raise NotImplementedError("Sorry, this board layout is not yet supported.")
	elif layout == "3":
		raise NotImplementedError("Sorry, this board layout is not yet supported.")
	elif layout == "4":
		raise NotImplementedError("Sorry, this board layout is not yet supported.")
	else:
		print(f"{WARN_SYMBOL} Using default 4x4 board layout.")
		return SmallSquareBoard, [4, 4, 4, 4]


def run():
	# initial setup
	global MAX_LENGTH
	print("Welcome to Kyle's Word Hunt solver!")
	board_class, row_sizes = get_board_size_values()
	maxLen = input("\nDefault max word length is 10. If you wish to change it, enter\n"  +
				   "the desired maximum word length (3 <= L <= 10):\t").strip()
	erasePreviousLines(3)
	if maxLen.isdigit():
		if int(maxLen) > 10 or int(maxLen) < 3:
			print(f"{ERROR_SYMBOL} Invalid length. Using default (10) instead.")
		else:
			MAX_LENGTH = int(maxLen)
			print("New max word length is %d." % MAX_LENGTH)
	else:
		print(f"{WARN_SYMBOL} Using default max word length (10).")
	# filename = input("What word list file would you like as input?\t")
	try :
		inputFile = open(WORDS_LIST_FILEPATH, 'r')
		for word in inputFile:
			strippedWord = word.strip() # removes newline char
			if len(strippedWord) > MAX_LENGTH:
				continue
			englishWords.add(strippedWord)
			# add each word start to the set of word starts
			for i in range(3, len(strippedWord) + 1):
				wordStarts.add(strippedWord[:i])
		inputFile.close()
	except FileNotFoundError:
		print(f"\n{ERROR_SYMBOL} Could not open the file. Please make sure {WORDS_LIST_FILEPATH.split('/')[-1]} is in the Word Hunt directory.\n")
		exit(0)

	# display mode select
	modeSelect = input("\nUse Diagram Mode (d) or List Mode (l)? Type 'i' for more info:\t").strip().lower()
	erasePreviousLines(2)
	if modeSelect == 'i':
		printModeInfo()
		modeSelect = input("\nUse Diagram Mode (d) or List Mode (l)?\t").strip().lower()
		erasePreviousLines(MORE_INFO_OUTPUT_HEIGHT + 2)
	if modeSelect == 'l':
		outputMode = LIST
		print("\nWords will be displayed in List Mode.")
	else:
		outputMode = DIAGRAM
		print("\nWords will be displayed in Diagram Mode.")

	# read in user board input
	board = readInBoard(board_class, row_sizes)
	erasePreviousLines(5)
	print("\nThe board is: ")
	printBoard(board)
	if outputMode == LIST:
		print("\n_____________________\n" + 
				"|__1_|__2_|__3_|__4_|\n" + 
				"|__5_|__6_|__7_|__8_|	<-- board index layout\n" +
				"|__9_|_10_|_11_|_12_|\n" + 
				"|_13_|_14_|_15_|_16_|\n\n" + 
				"^ The above table displays the numbering of the positions\n" + 
				"  which correspond to each word's start position.\n")
	findValidWords(board, outputMode)
	word_cmp_key = cmp_to_key(word_compare)
	validWords = sorted(list(valids), key=word_cmp_key, reverse=True)
	if len(validWords) == 0:
		print(f"{ERROR_SYMBOL} There were no valid words for the board.")
		exit(0)
	printOutput(validWords, outputMode)
