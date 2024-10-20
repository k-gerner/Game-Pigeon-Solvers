# Kyle Gerner
# 10.6.2024

from wordhunt.board import Board, populate_diagram_squares

# Class representing the X-Cross shaped board
#	___________    ___________	<-- board index layout
#	|__0_|__1_|____|__2_|__3_|	_____________
#	|__4_|__5_|__6_|__7_|__8_|	|_0_|_1_|_2_|	<-- direction layout
#	 ____|__9_|_10_|_11_|____  	|_7_|_X_|_3_|
#	|_12_|_13_|_14_|_15_|_16_|	|_6_|_5_|_4_|
#	|_17_|_18_|    |_19_|_20_|


class CrossBoard(Board):
	diagram_output_height = 8
	row_sizes = [4, 5, 3, 5, 4]
	name = "Cross"

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

	def letter_indices_layout(self):
		out_str = '''
	___________    ___________
	|__1_|__2_|____|__3_|__4_|
	|__5_|__6_|__7_|__8_|__9_|
	 ____|__10_|_11_|_12_|____
	|_13_|_14_|_15_|_16_|_17_|
	|_18_|_19_|    |_20_|_21_|'''
		return out_str

	def board_letters_layout(self):
		out_str = f"{self.lb[0].char} {self.lb[1].char}   {self.lb[2].char} {self.lb[3].char}\n"
		out_str += ''.join(f" {self.lb[i].char}" for i in range(4, 9))[1:] + '\n'
		out_str += f"  {self.lb[9].char} {self.lb[10].char} {self.lb[11].char}\n"
		out_str += ''.join(f" {self.lb[i].char}" for i in range(12, 17))[1:] + '\n'
		out_str += f"{self.lb[17].char} {self.lb[18].char}   {self.lb[19].char} {self.lb[20].char}\n"
		return out_str


	def build_diagram(self, positions, word, word_num):
		squares = populate_diagram_squares(21, positions)
		out_str = "___________    ___________\n"
		out_str += f"|{squares[0]}|{squares[1]}|____|{squares[2]}|{squares[3]}|\n"
		out_str += f"|{squares[4]}|{squares[5]}|{squares[6]}|{squares[7]}|{squares[8]}|\n"
		out_str += f" ____|{squares[9]}|{squares[10]}|{squares[11]}|____    {word_num}:   {word}\n"
		out_str += f"|{squares[12]}|{squares[13]}|{squares[14]}|{squares[15]}|{squares[16]}|\n"
		out_str += f"|{squares[17]}|{squares[18]}|    |{squares[19]}|{squares[20]}|\n"
		return out_str
