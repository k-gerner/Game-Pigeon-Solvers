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