# Kyle Gerner
# Started 7.16.2024
# Dots and Boxes, client facing

import dotsandboxes.printer as pr
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL
from util.terminaloutput.colors import NO_COLOR, YELLOW_COLOR, GREEN_COLOR, BLUE_COLOR, RED_COLOR, ORANGE_COLOR

# Output printing symbols
DOT_ICON = "o"
LINE_VERT = "|"
LINE_HORIZ = "--"

# Relevant to game state
board = []
board_history = []
user, opponent = 0, 1

# Misc
USER_COLOR = BLUE_COLOR
OPP_COLOR = RED_COLOR


class HumanPlayer():
	pass


def print_game_rules():
	"""Gives the user the option to view the rules of the game"""
	pass


def save_game(board, turn):
	pass


def load_saved_game():
	pass


def print_move_history(num_previous):
	pass


def run():
	global board, user, opponent
	pr.tmp()


