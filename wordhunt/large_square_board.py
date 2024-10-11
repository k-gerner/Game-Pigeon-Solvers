from wordhunt.board import Board

# Class representing the 5x5 board
#	__________________________	<-- board index layout
#	|__0_|__1_|__2_|__3_|__4_|	_____________
#	|__5_|__6_|__7_|__8_|__9_|	|_0_|_1_|_2_|	<-- direction layout
#	|_10_|_11_|_12_|_13_|_14_|	|_7_|_X_|_3_|
#	|_15_|_16_|_17_|_18_|_19_|	|_6_|_5_|_4_|
#	|_20_|_21_|_22_|_23_|_24_|


class LargeSquareBoard(Board):

	def __init__(self, lettersArr):
		super().__init__(lettersArr)

	def peekUpperLeft(self, pos):
		if pos % 5 == 0 or pos <= 4:
			# if on left edge or on upper edge
			return -1
		return self.lb[pos - 6]

	def peekUp(self, pos):
		if pos <= 4:
			# if on upper edge
			return -1
		return self.lb[pos - 5]

	def peekUpperRight(self, pos):
		if pos <= 4 or pos % 5 == 4:
			# if on upper edge or on right edge
			return -1
		return self.lb[pos - 4]

	def peekRight(self, pos):
		if pos % 5 == 4:
			# if on right edge
			return -1
		return self.lb[pos + 1]

	def peekLowerRight(self, pos):
		if pos >= 20 or pos % 5 == 4:
			# if on lower edge or on right edge
			return -1
		return self.lb[pos + 6]

	def peekDown(self, pos):
		if pos >= 20:
			# if on lower edge
			return -1
		return self.lb[pos + 5]

	def peekLowerLeft(self, pos):
		if pos % 5 == 0 or pos >= 20:
			# if on left edge or on lower edge
			return -1
		return self.lb[pos + 4]

	def peekLeft(self, pos):
		if pos % 5 == 0:
			# if on left edge
			return -1
		return self.lb[pos - 1]