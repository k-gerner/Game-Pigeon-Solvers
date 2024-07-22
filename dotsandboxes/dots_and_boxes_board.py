from dotsandboxes.constants import *


class DotsAndBoxesBoard:
	# 2(n^2 - n) total squares
	# 0 - (n^2 - n - 1) = horizontal sides
	# (n^2 -n) - (2(n^2 - n) - 1) = vertical sides
	# (n-1) sides per horizontal row
	# n sides per vertical row
	# num squares = (n - 1)^2

	def __init__(self, size, squares=None, edges=None):
		self.size = size  # dots in each row/col
		if not squares:
			sq = []
			for i in range(size*size):
				sq.append(Square())
			self.squares = sq
			num_edges = 2 * (size**2 - size)
			self.edges = [OPEN]*num_edges
		else:
			self.squares = squares
			self.edges = edges

	def copy(self):
		squares_copy = []
		for sq in self.squares:
			squares_copy.append(sq.copy())
		return DotsAndBoxesBoard(self.size, squares_copy, self.edges.copy())

	def score(self, player):
		score = 0
		for sq in self.squares:
			if sq.owner == player:
				score += 1
		return score

	def available_edges(self):
		available = []
		for count, val in enumerate(self.edges):
			if val == OPEN:
				available.append(count)
		return available

	def available_squares(self):
		available = []
		for count, sq in enumerate(self.squares):
			if not sq.is_captured():
				available.append(count)
		return available

	def draw_edge(self, edge_index, player):
		"""Returns an array of the indices of captured squares from this edge"""
		captured_squares = []
		bordering_squares = EDGE_SQUARE_MAPS[self.size][edge_index]
		for sq_index in bordering_squares:
			if self.squares[sq_index].mark_edge():
				captured_squares.append(sq_index, player)
		self.edges[edge_index] = player


class Square:
	"""Represents each square on the board"""

	def __init__(self, open_edges=None, owner=OPEN):
		# LEFT, UP, RIGHT, DOWN
		if open_edges:
			self.open_edges = open_edges
		else:
			self.open_edges = {LEFT, UP, RIGHT, DOWN}
		self.owner = owner

	def is_valid_side(self, side):
		return side in self.open_edges

	def is_captured(self):
		return self.owner != OPEN

	def mark_edge(self, edge, player):
		"""Returns True if the square is captured, False if not"""
		assert edge in self.open_edges
		self.open_edges.remove(edge)
		if len(self.open_edges) == 0:
			self.owner = player
			return True
		return False

	def copy(self):
		return Square(self.open_edges, self.owner)

