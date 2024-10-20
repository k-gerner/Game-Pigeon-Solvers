# Kyle Gerner
# 2.24.2021

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
