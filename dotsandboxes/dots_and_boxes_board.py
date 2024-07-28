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
			for i in range((size - 1) ** 2):
				sq.append(Square())
			self.squares = sq
			num_edges = 2 * (size**2 - size)
			self.edges = [OPEN]*num_edges
		else:
			self.squares = squares
			self.edges = edges

	def copy(self):
		"""Returns a copy of the board"""
		squares_copy = []
		for sq in self.squares:
			squares_copy.append(sq.copy())
		return DotsAndBoxesBoard(self.size, squares_copy, self.edges.copy())

	def score(self, player):
		"""Get the score for the given player"""
		score = 0
		for sq in self.squares:
			if sq.owner == player:
				score += 1
		return score

	def available_edges(self):
		"""Gets a list of available edges"""
		available = []
		for count, val in enumerate(self.edges):
			if val == OPEN:
				available.append(count)
		return available

	def available_square_indices(self):
		"""Returns a list of the indices of uncaptured squares"""
		available = []
		for count, sq in enumerate(self.squares):
			if not sq.is_captured():
				available.append(count)
		return available

	def is_square_edge_open(self, square_index:int, side:Direction):
		"""Whether the specified square has the specified side available"""
		sq = self.squares[square_index]
		return sq.is_valid_side(side)

	def is_edge_open(self, edge_index:int):
		"""Whether the edge at the given index is available"""
		return self.edges[edge_index] == OPEN

	def draw_edge(self, edge_index, player):
		"""Returns an array of the indices of captured squares from this edge (edge-format)"""
		captured_squares = []
		bordering_squares = EDGE_SQUARE_MAPS[self.size][edge_index]
		for sq_index in bordering_squares:
			if self.squares[sq_index].mark_edge(): # ERROR HERE - NEED TO CONVERT. MAYBE ADD NEW CONVERSION IN UTIL.PY
				captured_squares.append(sq_index, player)
		self.edges[edge_index] = player
		return captured_squares

	def draw_square_edge(self, square_index, side, player):
		"""Returns an array of the indices of captured squares from this edge (square-side-format)"""
		captured_squares = []
		if self.squares[square_index].mark_edge(side, player):
			captured_squares.append(square_index)
		neighbor_square_index, neighbor_dir = neighbor_square(square_index, side, self.size)
		if neighbor_square_index is not None:
			if self.squares[neighbor_square_index].mark_edge(neighbor_dir, player):
				captured_squares.append(neighbor_square_index)

		edge_index = square_to_edge(square_index, side, self.size)
		self.edges[edge_index] = player
		return captured_squares

	def is_full(self):
		for sq in self.squares:
			if not sq.is_captured():
				return False
		return True


class Square:
	"""Represents each square on the board"""

	def __init__(self, edge_owners=None, owner=OPEN):
		# LEFT, UP, RIGHT, DOWN
		if edge_owners:
			self.edge_owners = edge_owners
			self.open_edges = sum(1 for owner in self.edge_owners.values() if owner != OPEN)
		else:
			self.edge_owners = {
				LEFT: OPEN,
				UP: OPEN,
				RIGHT: OPEN,
				DOWN: OPEN
			}
			self.open_edges = 4
		self.owner = owner

	def is_valid_side(self, side):
		return self.edge_owners[side] == OPEN

	def is_captured(self):
		return self.owner != OPEN

	def get_edge_owner(self, side):
		return self.edge_owners[side]

	def mark_edge(self, edge, player):
		"""Returns True if the square is captured, False if not"""
		assert edge in self.edge_owners.keys()
		self.edge_owners[edge] = player
		self.open_edges -= 1
		if self.open_edges == 0:
			self.owner = player
			return True
		return False

	def copy(self):
		return Square(self.edge_owners, self.owner)

