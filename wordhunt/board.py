# Kyle Gerner
# 2.24.2021

# Parent class different representations of a Word Hunt board
class Board(object):

	# takes in an array of Letter objects and sets lb
	def __init__(self, lettersArr):
		self.lb = lettersArr  # lb = letter board
		self.directionDict = {
			0: self.peekUpperLeft,
			1: self.peekUp,
			2: self.peekUpperRight,
			3: self.peekRight,
			4: self.peekLowerRight,
			5: self.peekDown,
			6: self.peekLowerLeft,
			7: self.peekLeft
		}

	# return a copy of the board as is
	def copyBoard(self):
		newArr = []
		for i in self.lb:
			newArr.append(i.copyLetter())
		return self.__class__(newArr)

	# look at letter to the upper left but do not mark as visited
	def peekUpperLeft(self, pos):
		raise NotImplementedError

	# look at letter above but do not mark as visited
	def peekUp(self, pos):
		raise NotImplementedError

	# look at letter to the upper right but do not mark as visited
	def peekUpperRight(self, pos):
		raise NotImplementedError

	# look at letter to the right but do not mark as visited
	def peekRight(self, pos):
		raise NotImplementedError

	# look at letter to the lower right but do not mark as visited
	def peekLowerRight(self, pos):
		raise NotImplementedError

	# look at letter below but do not mark as visited
	def peekDown(self, pos):
		raise NotImplementedError

	# look at letter to lower left but do not mark as visited
	def peekLowerLeft(self, pos):
		raise NotImplementedError

	# look at letter to the left but do not mark as visited
	def peekLeft(self, pos):
		raise NotImplementedError

	def display_board(self, word, positions):
		raise NotImplementedError

	# look at letter in specified direction and DO mark as visited, -1 on fail
	def visitDirection(self, pos, dir):
		visitedLetter = self.directionDict[dir](pos)  # calls the correct function depending on value of dir
		if visitedLetter == -1 or visitedLetter.visited:
			# if unable to look that direction or the letter was already visited
			return -1
		visitedLetter.markVisited()
		return visitedLetter
