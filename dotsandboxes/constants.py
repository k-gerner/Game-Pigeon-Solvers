from typing import Literal
from dotsandboxes.util import edge_square_mapping
from util.terminaloutput.colors import NO_COLOR, BLUE_COLOR, RED_COLOR

# Square owner constants
OPEN, USER, OPP = 0, 1, 2

# Side name constants
LEFT, UP, RIGHT, DOWN = 'L', 'U', 'R', 'D'

EDGE_SQUARE_MAPS = {
	4: edge_square_mapping(4),
	5: edge_square_mapping(5),
	6: edge_square_mapping(6)
}

PLAYER_COLORS = {
	OPEN: NO_COLOR,
	USER: BLUE_COLOR,
	OPP: RED_COLOR
}

Direction = Literal[LEFT, UP, RIGHT, DOWN]


def neighbor_square(square_index, direction, board_size):
	"""
	Returns a tuple of (neighbor_square_index, neighbor_direction),
	or (None, None) if there is no neighbor
	"""
	squares_dimension = board_size - 1
	col = square_index % squares_dimension
	has_no_neighbor = (col == 0 and direction == LEFT) or (
			col == squares_dimension - 1 and direction == RIGHT) or (
							  square_index < squares_dimension and direction == UP) or (
							  square_index + squares_dimension > squares_dimension ** 2 and direction == DOWN)
	if has_no_neighbor:
		return None, None
	elif direction == LEFT:
		return square_index - 1, RIGHT
	elif direction == UP:
		return square_index - squares_dimension, DOWN
	elif direction == RIGHT:
		return square_index + 1, LEFT
	else:
		return square_index + squares_dimension, UP


def square_to_edge(square_index, direction, board_size):
	"""
	Returns the index of the edge the corresponds to the given square and direction
	"""
	if direction == UP:
		return square_index
	elif direction == DOWN:
		return square_index + (board_size - 1)
	elif direction == LEFT:
		row = square_index // (board_size - 1)
		offset = (board_size ** 2 - board_size) + row
		return square_index + offset
	else:
		row = square_index // (board_size - 1)
		offset = (board_size ** 2 - board_size) + row + 1
		return square_index + offset
