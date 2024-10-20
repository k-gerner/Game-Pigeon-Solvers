from wordhunt.board import Board, populate_diagram_squares

# Class representing the 5x5 board
#	__________________________	<-- board index layout
#	|__0_|__1_|__2_|__3_|__4_|	_____________
#	|__5_|__6_|__7_|__8_|__9_|	|_0_|_1_|_2_|	<-- direction layout
#	|_10_|_11_|_12_|_13_|_14_|	|_7_|_X_|_3_|
#	|_15_|_16_|_17_|_18_|_19_|	|_6_|_5_|_4_|
#	|_20_|_21_|_22_|_23_|_24_|


class LargeSquareBoard(Board):
	diagram_output_height = 8
	row_sizes = [5, 5, 5, 5, 5]
	name = "5x5"

	def __init__(self, letters_arr):
		super().__init__(letters_arr)

	def peek_upper_left(self, pos):
		if pos % 5 == 0 or pos <= 4:
			# if on left edge or on upper edge
			return -1
		return self.lb[pos - 6]

	def peek_up(self, pos):
		if pos <= 4:
			# if on upper edge
			return -1
		return self.lb[pos - 5]

	def peek_upper_right(self, pos):
		if pos <= 4 or pos % 5 == 4:
			# if on upper edge or on right edge
			return -1
		return self.lb[pos - 4]

	def peek_right(self, pos):
		if pos % 5 == 4:
			# if on right edge
			return -1
		return self.lb[pos + 1]

	def peek_lower_right(self, pos):
		if pos >= 20 or pos % 5 == 4:
			# if on lower edge or on right edge
			return -1
		return self.lb[pos + 6]

	def peek_down(self, pos):
		if pos >= 20:
			# if on lower edge
			return -1
		return self.lb[pos + 5]

	def peek_lower_left(self, pos):
		if pos % 5 == 0 or pos >= 20:
			# if on left edge or on lower edge
			return -1
		return self.lb[pos + 4]

	def peek_left(self, pos):
		if pos % 5 == 0:
			# if on left edge
			return -1
		return self.lb[pos - 1]

	def letter_indices_layout(self):
		out_str = '''
		__________________________
		|__1_|__2_|__3_|__4_|__5_|
		|__6_|__7_|__8_|__9_|_10_|
		|_11_|_12_|_13_|_14_|_15_|
		|_16_|_17_|_18_|_19_|_20_|
		|_21_|_22_|_23_|_24_|_25_|'''
		return out_str

	def board_letters_layout(self):
		out_str = ""
		for ind, letter in enumerate(self.lb):
			out_str += f"{letter.char} "
			if ind % 5 == 4:
				# on right side, go to next line
				out_str += "\n"
		return out_str

	def build_diagram(self, positions, word, word_num):
		squares = populate_diagram_squares(25, positions)
		out_str = "__________________________\n"
		for row_start in [0, 5, 10, 15, 20]:
			row_str = "|"
			for i in range(row_start, row_start + 5):
				row_str += f"{squares[i]}|"
			if row_start == 10:
				# if on third output row, print the word info
				row_str += f"    {word_num}:   {word}"
			out_str += row_str + "\n"
		return out_str