# Kyle Gerner
# 2.24.2021
from util.terminaloutput.colors import YELLOW_COLOR, color_text

class Board(object):
	""" Parent class different representations of a Word Hunt board """
	diagram_output_height = 0
	row_sizes = None
	name = None

	def __init__(self, letters_arr):
		""" takes in an array of Letter objects and sets lb """
		self.lb = letters_arr  # lb = letter board
		self.directionDict = {
			0: self.peekUpperLeft,
			1: self.peekUp,
			2: self.peekUpperRight,
			3: self.peekRight,
			4: self.peekLowerRight,
			5: self.peekDown,
			6: self.peekLowerLeft,
			7: self.peekLeft
		}

	def copyBoard(self):
		""" return a copy of the board as is """
		new_arr = []
		for i in self.lb:
			new_arr.append(i.copyLetter())
		return self.__class__(new_arr)

	def peekUpperLeft(self, pos):
		""" look at letter to the upper left but do not mark as visited """
		raise NotImplementedError

	def peekUp(self, pos):
		""" look at letter above but do not mark as visited """
		raise NotImplementedError

	def peekUpperRight(self, pos):
		""" look at letter to the upper right but do not mark as visited """
		raise NotImplementedError

	def peekRight(self, pos):
		""" look at letter to the right but do not mark as visited"""
		raise NotImplementedError

	def peekLowerRight(self, pos):
		""" look at letter to the lower right but do not mark as visited """
		raise NotImplementedError

	def peekDown(self, pos):
		""" look at letter below but do not mark as visited """
		raise NotImplementedError

	def peekLowerLeft(self, pos):
		""" look at letter to lower left but do not mark as visited """
		raise NotImplementedError

	def peekLeft(self, pos):
		""" look at letter to the left but do not mark as visited"""
		raise NotImplementedError

	def build_diagram(self, positions, word, word_num):
		""" returns the string representation of the board """
		raise NotImplementedError

	def letter_indices_layout(self):
		"""
		returns the string representation the indices of letters on the board;
		only available for square boards
		"""
		raise NotImplementedError

	def board_letters_layout(self):
		"""
		returns the string representation of the letters on the board
		"""
		raise NotImplementedError

	def visit_direction(self, pos, dir):
		"""
		look at letter in specified direction and mark as visited
		returns -1 on fail
		"""
		visited_letter = self.directionDict[dir](pos)  # calls the correct function depending on value of dir
		if visited_letter == -1 or visited_letter.visited:
			# if unable to look that direction or the letter was already visited
			return -1
		visited_letter.markVisited()
		return visited_letter


def populate_diagram_squares(size, positions):
	"""
	Fills a list of strings representing board tiles' inner text
	"""
	squares = ["____"] * size
	for letter_count, letter_pos in enumerate(positions, 1):
		left_underscores = "__" if letter_count < 10 else "_"
		if letter_count == 1:
			colored_count = color_text(str(letter_count), YELLOW_COLOR)
			squares[letter_pos] = f"{left_underscores}{colored_count}_"
		else:
			squares[letter_pos] = f"{left_underscores}{letter_count}_"
	return squares
