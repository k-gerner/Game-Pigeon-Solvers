from dotsandboxes.util import edge_square_mapping
from util.terminaloutput.colors import NO_COLOR, BLUE_COLOR, RED_COLOR

# Square owner constants
OPEN, USER, OPP = 0, 1, 2

# Side name constants
LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3

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
