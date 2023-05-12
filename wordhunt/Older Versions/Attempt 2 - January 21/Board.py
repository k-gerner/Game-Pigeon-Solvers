# class that represents a board and whether or not each spot has been visited or not
class Board(object):
	visitedBoard = [[False, False, False, False]]*4
	def __init__(self):
		pass
	def resetVisitedBoard(self):
		self.visitedBoard = [[False, False, False, False]]*4
	def markVisited(self, row, col):
		self.visitedBoard[row][col] = True
	def haveVisited(self, row, col):
		return self.visitedBoard[row][col]
	def setVisitedBoard(self, board):
		self.visitedBoard = Board
	def copyOfBoard(self):
		copyB = Board()
		copyB.setVisitedBoard(visitedBoard.copy())
		return copy