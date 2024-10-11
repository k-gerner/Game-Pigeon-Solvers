# Kyle Gerner
# 10.6.2024

from wordhunt.board import Board

# Class representing the X-Cross shaped board
#	___________    ___________	<-- board index layout
#	|__0_|__1_|____|__2_|__3_|	_____________
#	|__4_|__5_|__6_|__7_|__8_|	|_0_|_1_|_2_|	<-- direction layout
#	     |__9_|_10_|_11_|     	|_7_|_X_|_3_|
#	|_12_|_13_|_14_|_15_|_16_|	|_6_|_5_|_4_|
#	|_17_|_18_|    |_19_|_20_|


class CrossBoard(Board):

	def __init__(self, lettersArr):
		super().__init__(lettersArr)

	def peekUpperLeft(self, pos):
		if pos <= 4 or pos in {7, 12, 13, 17}:
			return -1
		elif pos in {8, 18}:
			return self.lb[pos - 6]
		else:
			return self.lb[pos - 5]

	def peekUp(self, pos):
		if pos <= 3 or pos in {6, 12, 16}:
			return -1
		elif pos in {7, 8, 17, 18}:
			return self.lb[pos - 5]
		else:
			return self.lb[pos - 4]

	def peekUpperRight(self, pos):
		if pos <= 3 or pos in {5, 8, 15, 16, 20}:
			return -1
		elif pos in {6, 7, 17, 18}:
			return self.lb[pos - 4]
		else:
			return self.lb[pos - 3]

	def peekRight(self, pos):
		if pos in {1, 3, 8, 11, 16, 18, 20}:
			return -1
		else:
			return self.lb[pos + 1]

	def peekLowerRight(self, pos):
		if pos >= 16 or pos in {3, 7, 8, 13}:
			return -1
		elif pos in {2, 12}:
			return self.lb[pos + 6]
		else:
			return self.lb[pos + 5]

	def peekDown(self, pos):
		if pos >= 17 or pos in {4, 8, 14}:
			return -1
		elif pos in {2, 3, 12, 13}:
			return self.lb[pos + 5]
		else:
			return self.lb[pos + 4]

	def peekLowerLeft(self, pos):
		if pos >= 17 or pos in {0, 4, 5, 12, 15}:
			return -1
		elif pos in {2, 3, 13, 14}:
			return self.lb[pos + 4]
		else:
			return self.lb[pos + 3]

	def peekLeft(self, pos):
		if pos in {0, 2, 4, 9, 12, 17, 19}:
			return -1
		else:
			return self.lb[pos - 1]
