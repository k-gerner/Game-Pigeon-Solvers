# Kyle Gerner
# 10.6.2024

from wordhunt.board import Board


# Class representing the donut shaped board
#	      ______________		<-- board index layout
#	 ____|__0_|__1_|__2_|____	_____________
#	|__3_|__4_|__5_|__6_|__7_|	|_0_|_1_|_2_|	<-- direction layout
#	|__8_|__9_|_10_|_11_|_12_|	|_7_|_X_|_3_|
#	|_13_|_14_|_15_|_16_|_17_|	|_6_|_5_|_4_|
#	     |_18_|_19_|_20_|


class DonutBoard(Board):

	def __init__(self, lettersArr):
		super().__init__(lettersArr)

	def peekUpperLeft(self, pos):
		if pos <= 4 or pos in {8, 13}:
			return -1
		elif pos >= 18 or 5 <= pos <= 7:
			return self.lb[pos - 5]
		else:
			return self.lb[pos - 6]

	def peekUp(self, pos):
		if pos <= 3 or pos == 7:
			return -1
		elif 4 <= pos <= 6 or pos >= 18:
			return self.lb[pos - 4]
		else:
			return self.lb[pos - 5]

	def peekUpperRight(self, pos):
		if pos <= 2 or pos in {6, 7, 12, 17}:
			return -1
		elif pos >= 18 or 3 <= pos <= 5:
			return self.lb[pos - 3]
		else:
			return self.lb[pos - 4]

	def peekRight(self, pos):
		if pos % 5 == 2 or pos == 20:
			return -1
		else:
			return self.lb[pos + 1]

	def peekLowerRight(self, pos):
		if pos >= 16 or pos in {7, 12}:
			return -1
		elif 0 <= pos <= 2 or 13 <= pos <= 15:
			return self.lb[pos + 5]
		else:
			return self.lb[pos + 6]

	def peekDown(self, pos):
		if pos == 13 or pos >= 17:
			return -1
		elif 0 <= pos <= 2 or 14 <= pos <= 16:
			return self.lb[pos + 4]
		else:
			return self.lb[pos + 5]

	def peekLowerLeft(self, pos):
		if pos % 5 == 3 or pos >= 18 or pos == 14:
			return -1
		elif pos <= 2 or 15 <= pos <= 17:
			return self.lb[pos + 3]
		else:
			return self.lb[pos + 4]

	def peekLeft(self, pos):
		if pos % 5 == 3 or pos == 0:
			return -1
		else:
			return self.lb[pos - 1]
