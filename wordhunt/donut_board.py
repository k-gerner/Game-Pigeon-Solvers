# Kyle Gerner
# 10.6.2024

from wordhunt.board import Board, populate_diagram_squares


# Class representing the donut shaped board
#	     ________________		<-- board index layout
#	 ____|__0_|__1_|__2_|____	_____________
#	|__3_|__4_|__5_|__6_|__7_|	|_0_|_1_|_2_|	<-- direction layout
#	|__8_|__9_|    |_10_|_11_|	|_7_|_X_|_3_|
#	|_12_|_13_|_14_|_15_|_16_|	|_6_|_5_|_4_|
#	     |_17_|_18_|_19_|


class DonutBoard(Board):
	diagram_output_height = 8
	row_sizes = [3, 5, 4, 5, 3]
	name = "Donut"

	def __init__(self, lettersArr):
		super().__init__(lettersArr)

	def peekUpperLeft(self, pos):
		if pos <= 4 or pos in {8, 12, 15}:
			return -1
		elif pos in {9, 16}:
			return self.lb[pos - 6]
		else:
			return self.lb[pos - 5]

	def peekUp(self, pos):
		if pos <= 3 or pos in {7, 14}:
			return -1
		elif pos in {8, 9, 15, 16}:
			return self.lb[pos - 5]
		else:
			return self.lb[pos - 4]

	def peekUpperRight(self, pos):
		if pos <= 2 or pos in {6, 7, 11, 13, 16}:
			return -1
		elif pos in {8, 9, 14, 15}:
			return self.lb[pos - 4]
		else:
			return self.lb[pos - 3]

	def peekRight(self, pos):
		if pos in {2, 7, 9, 11, 16, 19}:
			return -1
		else:
			return self.lb[pos + 1]

	def peekLowerRight(self, pos):
		if pos >= 15 or pos in {4, 7, 11}:
			return -1
		elif pos in {3, 10}:
			return self.lb[pos + 6]
		else:
			return self.lb[pos + 5]

	def peekDown(self, pos):
		if pos >= 16 or pos in {5, 12}:
			return -1
		elif pos in {3, 4, 10, 11}:
			return self.lb[pos + 5]
		else:
			return self.lb[pos + 4]

	def peekLowerLeft(self, pos):
		if pos >= 17 or pos in {3, 6, 8, 12, 13}:
			return -1
		elif pos in {4, 5, 10, 11}:
			return self.lb[pos + 4]
		else:
			return self.lb[pos + 3]

	def peekLeft(self, pos):
		if pos in {0, 3, 8, 10, 12, 17}:
			return -1
		else:
			return self.lb[pos - 1]

	def board_letters_layout(self):
		out_str = f"  {self.lb[0].char} {self.lb[1].char} {self.lb[2].char}\n"
		out_str += ''.join(f" {self.lb[i].char}" for i in range(3, 8))[1:] + '\n'
		out_str += f"{self.lb[8].char} {self.lb[9].char}   {self.lb[10].char} {self.lb[11].char}\n"
		out_str += ''.join(f" {self.lb[i].char}" for i in range(12, 17))[1:] + '\n'
		out_str += f"  {self.lb[17].char} {self.lb[18].char} {self.lb[19].char}"
		return out_str

	def build_diagram(self, positions, word, word_num):
		squares = populate_diagram_squares(21, positions)
		# populate top row
		out_str = "     ________________\n"
		out_str += f" ____|{squares[0]}|{squares[1]}|{squares[2]}|____\n"
		out_str += f"|{squares[3]}|{squares[4]}|{squares[5]}|{squares[6]}|{squares[7]}|\n"
		out_str += f"|{squares[8]}|{squares[9]}|    |{squares[10]}|{squares[11]}|    {word_num}:   {word}\n"
		out_str += f"|{squares[12]}|{squares[13]}|{squares[14]}|{squares[15]}|{squares[16]}|\n"
		out_str += f"     |{squares[17]}|{squares[18]}|{squares[19]}|\n"
		return out_str

