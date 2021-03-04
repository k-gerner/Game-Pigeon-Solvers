# Kyle Gerner
# 2.24.2021
# Tool for Game Pigeon's 'Word Hunt' puzzle game

from classes import Board, Letter
from functools import cmp_to_key

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

englishWords = set() # LARGE set that will contain every possible word. Using set for O(1) lookup
validWordsOnly = set() # set of only the valid word strings (no tuple pairing)
valids = set() # set of valid words paired with their starting position ( pos, word )
MAX_LENGTH = 10 # max length of the words to find; can be changed by user input
positionsList = [] # used to keep the lists of positions in diagram mode, since nested lists cannot be hashed
wordStarts = set() # set that holds every valid part of every word from beginning to some point in the middle

# read in the user's input for the board letters
def readInBoard():
	print("Please enter each row of letters (one row at a time) in the format \"a b c d\"")
	inputLetters = []
	for i in range(4):
		while(True):
			letters = input("Row %d of letters:\t" % (i+1))
			letters = letters.lower()
			lettersSplit = letters.split()
			allSingleChar = True
			for l in lettersSplit:
				if len(l) > 1: 
					allSingleChar = False
			if allSingleChar:
				if len(lettersSplit) == 4:
					# if exactly 4 single letters entered
					break
			print("Invalid input. Please type that row again.")
		for letter in lettersSplit:
			inputLetters.append(letter)
	letterObjs = []
	for i in range(len(inputLetters)):
		letterObjs.append(Letter(inputLetters[i], i))
	board = Board(letterObjs)
	return board

# prints the letter board in a user-readable format
def printBoard(board):
	ind = 0
	for letter in board.lb:
		print("%c " % letter.char, end='')
		if ind % 4 == 3:
			# on right side, print new line
			print("")
		ind += 1
	print("")

# show the user further information about the different modes available for printing word list
def printModeInfo():
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
	# print("\t  .\n\t  .\n\t  .\n")
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

# for custom sorting of valid words
def word_compare(a, b):
	if len(a[1]) < len(b[1]):
		return -1
	elif len(a[1]) == len(b[1]):
		if a[1] > b[1]: 
			return -1
		elif a[1] < b[1]:
			return 1
		return 0
	return 1

# populate 'valid' set
def findValidWords(board, mode):
	for letter in board.lb:
		letter.markVisited()
		if mode == LIST:
			findValidFrom(board, letter.char, letter, 1, letter.pos, LIST)
		else:
			findValidFrom(board, letter.char, letter, 1, [], DIAGRAM)
		letter.visited = False # so later iterations don't have it marked already

# find all the valid words from this letter
def findValidFrom(board, word, letter, length, pos, mode):
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

# print the output in the format chosen by the user
def printOutput(validWords, mode):
	print("%d words were found." % len(validWords))
	if mode == LIST:
		# list mode
		print("\n   X  |   Word \t|  Starting Position on Board\n" + 
		      "----------------------------------------------")
		place = 1
		for pair in validWords:
			# pair[0] = start pos
			# pair[1] = word
			print("%d:\t%s\t %d" % (place, pair[1], pair[0] + 1))
			place += 1
	else:
		# diagram mode
		place = 1
		for pair in validWords:
			# pair[0] = index in positionsList of this word's list of tile locations
			# pair[1] = word
			if place > 1:
				# if not first time through
				next = input("\nPress enter for next word, or 'q' to quit\t")
				if next == 'q':
					break
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
			place += 1
		print("No more words, thanks for using my Word Hunt Tool!")



# main method
def main():
	# initial setup
	global MAX_LENGTH
	print("\nNote: This code was designed for the 4x4 (default) board size.")
	maxLen = input("\nDefault max word length is 10. Note this allocates about\n" + 
				   "16MB of space for word sets. If you wish to change it, enter\n"  +
				   "the desired maximum word length (3 <= L <= 10):\t").rstrip()
	if maxLen.isnumeric():
		if int(maxLen) > 10 or int(maxLen) < 3:
			print("Invalid length. Using default (10) instead.")
		else:
			MAX_LENGTH = int(maxLen)
			print("New max word length is %d." % MAX_LENGTH)
	else:
		print("Using default max word length (10).")
	filename = 'letters10.txt'
	# filename = input("What word list file would you like as input?\t")
	try :
		inputFile = open(filename, 'r')
	except:
		print("\nCould not open the file. Please make sure %s is in the current directory, and run this file from inside the current directory.\n" % filename)
		exit(0)
	trueCount = 0
	falseCount = 0
	for word in inputFile:
		strippedWord = word.rstrip() #removes newline char
		if len(strippedWord) > MAX_LENGTH:
			continue
		englishWords.add(strippedWord)
		# add each word start to the set of word starts
		for i in range(3, len(strippedWord) + 1):
			wordStarts.add(strippedWord[:i])
	inputFile.close()

	# display mode select
	outputMode = LIST
	modeSelect = input("\nUse Diagram Mode? 'y' for yes, 'i' for more info:\n").rstrip()
	while modeSelect == 'i':
		printModeInfo()
		modeSelect = input("\nUse Diagram Mode? 'y' for yes, 'i' for more info:\n").rstrip()
	if modeSelect == 'y':
		outputMode = DIAGRAM
		print("\nWords will be displayed in Diagram Mode.")
	else:
		print("\nWords will be displayed in List Mode.")

	# read in user board input
	board = readInBoard()
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
	word_cmp_key = cmp_to_key(word_compare)
	findValidWords(board, outputMode)
	validWords = sorted(list(valids), key=word_cmp_key, reverse=True)
	if len(validWords) == 0:
		print("There were no valid words for the board.")
		exit(0)
	printOutput(validWords, outputMode)


if __name__ == '__main__':
	main()