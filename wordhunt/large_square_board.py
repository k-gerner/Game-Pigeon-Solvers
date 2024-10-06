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