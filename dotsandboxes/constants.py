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


def neighbor_square(row, col, direction, board_size):
	"""
	Returns a tuple of (neighbor_row, neighbor_col, neighbor_direction),
	or (None, None, None) if there is no neighbor
	"""
	squares_dimension = board_size - 1
	has_no_neighbor = (col == 0 and direction == LEFT) or (
			col == squares_dimension - 1 and direction == RIGHT) or (
							  row == 0 and direction == UP) or (
							  row == squares_dimension - 1 and direction == DOWN)
	if has_no_neighbor:
		return None, None, None
	elif direction == LEFT:
		return row, col - 1, RIGHT
	elif direction == UP:
		return row - 1, col, DOWN
	elif direction == RIGHT:
		return row, col + 1, LEFT
	else:
		return row + 1, col, UP


def square_to_edge(row, col, direction, board_size):
	"""
	Returns the index of the edge the corresponds to the given square and direction
	"""
	if direction == UP:
		return (row * (board_size - 1)) + col
	elif direction == DOWN:
		return (row * board_size) + col
	elif direction == LEFT:
		offset = (board_size ** 2 - board_size) + row
		overall_index = (row * (board_size - 1)) + col
		return overall_index + offset
	else:
		offset = (board_size ** 2 - board_size) + row + 1
		overall_index = (row * (board_size - 1)) + col
		return overall_index + offset
