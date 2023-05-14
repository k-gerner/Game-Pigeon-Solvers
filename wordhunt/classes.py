# Kyle Gerner
# 2.24.2021

# class that represents a board
class Board(object):
	#	_____________________	<-- board index layout
	#	|__0_|__1_|__2_|__3_|	_____________
	#	|__4_|__5_|__6_|__7_|	|_0_|_1_|_2_|	<-- direction layout
	#	|__8_|__9_|_10_|_11_|	|_7_|_X_|_3_|
	#	|_12_|_13_|_14_|_15_|	|_6_|_5_|_4_|
	
	# takes in an array of Letter objects and sets lb 
	def __init__(self, lettersArr): 
		self.lb = lettersArr # lb = letter board

	# return a copy of the board as is 
	def copyBoard(self):
		newArr = []
		for i in self.lb:
			newArr.append(i.copyLetter())
		return Board(newArr)

	# look at letter to the upper left but do not mark as visited
	def peekUpperLeft(self, pos):
		if pos % 4 == 0 or pos <= 3: 
			# if on left edge or on upper edge
			return -1 
		return self.lb[pos - 5]

	# look at letter above but do not mark as visited
	def peekUp(self, pos):
		if pos <= 3: 
			# if on upper edge
			return -1 
		return self.lb[pos - 4]
	
	# look at letter to the upper right but do not mark as visited
	def peekUpperRight(self, pos):
		if pos <= 3 or pos % 4 == 3: 
			# if on upper edge or on right edge
			return -1 
		return self.lb[pos - 3]
	
	# look at letter to the right but do not mark as visited
	def peekRight(self, pos):
		if pos % 4 == 3: 
			# if on right edge
			return -1 
		return self.lb[pos + 1]
	
	# look at letter to the lower right but do not mark as visited
	def peekLowerRight(self, pos):
		if pos >= 12 or pos % 4 == 3: 
			# if on lower edge or on right edge
			return -1 
		return self.lb[pos + 5]
	
	# look at letter below but do not mark as visited
	def peekDown(self, pos):
		if pos >= 12: 
			# if on lower edge
			return -1 
		return self.lb[pos + 4]
	
	# look at letter to lower left but do not mark as visited
	def peekLowerLeft(self, pos):
		if pos % 4 == 0 or pos >= 12: 
			# if on left edge or on lower edge
			return -1 
		return self.lb[pos + 3]
	
	# look at letter to the left but do not mark as visited
	def peekLeft(self, pos):
		if pos % 4 == 0: 
			# if on left edge
			return -1 
		return self.lb[pos - 1]
	
	# look at letter in specified direction and DO mark as visited, -1 on fail
	def visitDirection(self, pos, dir):
		directionDict = {
			0 : self.peekUpperLeft,
			1 : self.peekUp,
			2 : self.peekUpperRight,
			3 : self.peekRight,
			4 : self.peekLowerRight,
			5 : self.peekDown,
			6 : self.peekLowerLeft,
			7 : self.peekLeft
		}
		visitedLetter = directionDict[dir](pos) # calls the correct function depending on value of dir
		if visitedLetter == -1 or visitedLetter.visited: 
			# if unable to look that direction or the letter was already visited
			return -1
		visitedLetter.markVisited()
		return visitedLetter




# class that represents each single char letter piece on the board
class Letter(object):
	# takes in a char value and an optional visited argument
	def __init__(self, ch, index, visit=False):
		self.char = ch
		self.pos = index
		self.visited = visit
	
	# returns a new letter object with same values as this one
	def copyLetter(self):
		return Letter(self.char, self.pos, self.visited)
	
	# mark letter as visited
	def markVisited(self):
		self.visited = True
