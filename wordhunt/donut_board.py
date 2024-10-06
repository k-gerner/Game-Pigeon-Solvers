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