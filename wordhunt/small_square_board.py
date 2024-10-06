from wordhunt.board import Board

# Class representing the default 4x4 board
#	_____________________	<-- board index layout
#	|__0_|__1_|__2_|__3_|	_____________
#	|__4_|__5_|__6_|__7_|	|_0_|_1_|_2_|	<-- direction layout
#	|__8_|__9_|_10_|_11_|	|_7_|_X_|_3_|
#	|_12_|_13_|_14_|_15_|	|_6_|_5_|_4_|


class SmallSquareBoard(Board):

	def __init__(self, lettersArr):
		super().__init__(lettersArr)

	def peekUpperLeft(self, pos):
		if pos % 4 == 0 or pos <= 3:
			# if on left edge or on upper edge
			return -1
		return self.lb[pos - 5]

	def peekUp(self, pos):
		if pos <= 3:
			# if on upper edge
			return -1
		return self.lb[pos - 4]

	def peekUpperRight(self, pos):
		if pos <= 3 or pos % 4 == 3:
			# if on upper edge or on right edge
			return -1
		return self.lb[pos - 3]

	def peekRight(self, pos):
		if pos % 4 == 3:
			# if on right edge
			return -1
		return self.lb[pos + 1]

	def peekLowerRight(self, pos):
		if pos >= 12 or pos % 4 == 3:
			# if on lower edge or on right edge
			return -1
		return self.lb[pos + 5]

	def peekDown(self, pos):
		if pos >= 12:
			# if on lower edge
			return -1
		return self.lb[pos + 4]

	def peekLowerLeft(self, pos):
		if pos % 4 == 0 or pos >= 12:
			# if on left edge or on lower edge
			return -1
		return self.lb[pos + 3]

	def peekLeft(self, pos):
		if pos % 4 == 0:
			# if on left edge
			return -1
		return self.lb[pos - 1]
