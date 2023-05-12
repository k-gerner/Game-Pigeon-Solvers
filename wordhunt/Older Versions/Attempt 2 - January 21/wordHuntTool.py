# started 11.26.2020
# NOT COMPLETED
from Board import Board

lettersBoard = []  # matrix that contains rows of letters in the game board
validWords = set() # set of words that are valid to be entered

# read in the user's input for the board letters
def readInBoard():
	print("Please enter each row of letters (one row at a time) in the format \"a b c d\"")
	for i in range(4):
		row = []
		letters = input("Row %d of letters:\t" % (i+1))
		letters = letters.lower()
		lettersSplit = letters.split()
		for letter in lettersSplit:
			row.append(letter)
		lettersBoard.append(row)
	print("\nThe table is: ")
	printBoard()

# prints the letter board in a user-readable format
def printBoard():
	for row in lettersBoard:
		for let in row:
			print("%c " % let.upper(), end='')
		print("")
	print("")

# get a list of cords for valid neighboring spots
def getValidNeighborIndices(rowNum, colNum, visitedBoard):
	isTopRow = rowNum == 0
	isBottomRow = rowNum == 3
	isLeftCol = colNum == 0
	isRightCol = colNum == 3
	cordSet = set() # set of tuples in the form rowNum, colNum
	if not isLeftCol: 
		if not visitedBoard.haveVisited(rowNum, colNum-1): 
			cordSet.add((rowNum, colNum-1)) # left neighbor
			visitedBoard.markVisited(rowNum, colNum-1)
		if not isTopRow and not visitedBoard.haveVisited(rowNum-1, colNum-1):
			cordSet.add((rowNum-1, colNum-1)) # diag upper left neighbor
			visitedBoard.markVisited(rowNum-1, colNum-1)
		if not isBottomRow and not visitedBoard.haveVisited(rowNum+1, colNum-1):
			cordSet.add((rowNum+1, colNum-1)) # diag lower left neighbor
			visitedBoard.markVisited(rowNum+1, colNum-1)
	if not isRightCol:
		if not visitedBoard.haveVisited(rowNum, colNum+1):
			cordSet.add((rowNum, colNum+1)) # right neighbor
			visitedBoard.markVisited(rowNum, colNum+1)
		if not isTopRow and not visitedBoard.haveVisited(rowNum-1, colNum+1):
			cordSet.add((rowNum-1, colNum+1)) # diag upper right neighbor
			visitedBoard.markVisited(rowNum-1, colNum+1)
		if not isBottomRow and not visitedBoard.haveVisited(rowNum+1, colNum+1):
			cordSet.add((rowNum+1, colNum+1)) # diag lower right neighbor
			visitedBoard.markVisited(rowNum+1, colNum+1)
	if not isTopRow:
		if not visitedBoard.haveVisited(rowNum-1, colNum):
			cordSet.add((rowNum-1, colNum)) # upper neighbor
			visitedBoard.markVisited(rowNum-1, colNum)
		if not isLeftCol and not visitedBoard.haveVisited(rowNum-1, colNum-1):
			cordSet.add((rowNum-1, colNum-1)) # diag upper left neighbor
			visitedBoard.markVisited(rowNum-1, colNum-1)
		if not isRightCol and not visitedBoard.haveVisited(rowNum-1, colNum+1):
			cordSet.add((rowNum-1, colNum+1)) # diag upper right neighbor
			visitedBoard.markVisited(rowNum-1, colNum+1)
	if not isBottomRow:
		if not visitedBoard.haveVisited(rowNum+1, colNum):
			cordSet.add((rowNum+1, colNum)) # lower neighbor
			visitedBoard.markVisited(rowNum+1, colNum)
		if not isLeftCol and not visitedBoard.haveVisited(rowNum+1, colNum-1):
			cordSet.add((rowNum+1, colNum-1)) # diag lower left neighbor
			visitedBoard.markVisited(rowNum+1, colNum-1)
		if not isRightCol and not visitedBoard.haveVisited(rowNum+1, colNum+1):
			cordSet.add((rowNum+1, colNum+1)) # diag lower right neighbor
			visitedBoard.markVisited(rowNum+1, colNum+1)
	return list(cordSet)

def getValidWords(row, col):
	availableCords = []
	for cords in getValidNeighborIndices(row, col, Board()):
		availableCords.append(cords)
	# call some recusive method that probably will implement a stack or something
	return [] # placeholder. Should return a list of valid words



# find the words that can be inputted for points
def findWords(filename):
	ifile = open(filename, "r")
	for rowNum in range(len(lettersBoard)):
		row = lettersBoard[rowNum]
		for colNum in range(len(row)):
			validWordsForThisCord = getValidWords(rowNum, colNum)
			for word in validWordsForThisCord:
				validWords.add(word)


		


print("Note: This code was designed for the 4x4 (default) board size.")
print("THIS IMPLEMENTATION HAS NOT BEEN FINISHED.\n")
version = input("Use old version (more words, may not be in dictionary)? (type 'y' for yes)  ")
filename = ""
if version == 'y':
	filename = "letters7.txt"
else:
	filename = "letters7_better.txt"
readInBoard()
# findWords(filename)
gameBoard = Board()
for i in range(4):
	for j in range(4):
		print("Valid neighbor indices for row %d, col %d are:" % (i, j))
		print(str(getValidNeighborIndices(i, j, gameBoard)))



