from wordhunt.board import Board, populate_diagram_squares


# Class representing the default 4x4 board
#	_____________________	<-- board index layout
#	|__0_|__1_|__2_|__3_|	_____________
#	|__4_|__5_|__6_|__7_|	|_0_|_1_|_2_|	<-- direction layout
#	|__8_|__9_|_10_|_11_|	|_7_|_X_|_3_|
#	|_12_|_13_|_14_|_15_|	|_6_|_5_|_4_|


class SmallSquareBoard(Board):
	diagram_output_height = 7
	row_sizes = [4, 4, 4, 4]
	name = "4x4"

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

	def letter_indices_layout(self):
		out_str = '''
		_____________________
		|__1_|__2_|__3_|__4_|
		|__5_|__6_|__7_|__8_|
		|__9_|_10_|_11_|_12_|
		|_13_|_14_|_15_|_16_|'''
		return out_str

	def board_letters_layout(self):
		out_str = ""
		for ind, letter in enumerate(self.lb):
			out_str += f"{letter.char} "
			if ind % 4 == 3:
				# on right side, go to next line
				out_str += "\n"
		return out_str

	def build_diagram(self, positions, word, word_num):
		squares = populate_diagram_squares(16, positions)
		out_str = "_____________________\n"
		for row_start in [0, 4, 8, 12]:
			row_str = "|"
			for i in range(row_start, row_start + 4):
				row_str += f"{squares[i]}|"
			if row_start == 4:
				# if on second output row, print the word info
				row_str += f"    {word_num}:   {word}"
			out_str += row_str + "\n"
		return out_str
