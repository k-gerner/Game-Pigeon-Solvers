from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL
from util.terminaloutput.colors import NO_COLOR
from dotsandboxes.constants import OPEN, USER, OPP, PLAYER_COLORS, EDGE_SQUARE_MAPS, LEFT, UP, RIGHT, DOWN

SQUARE_HEIGHT = 3
SQUARE_WIDTH = SQUARE_HEIGHT * 3
HORIZ_EDGE = "_" * SQUARE_WIDTH
TOP_EDGES_SPLITTER = " "
VERT_EDGE = "|"
CAPTURE_FILL = "X" * SQUARE_WIDTH
OPEN_FILL = " " * SQUARE_WIDTH
CAPTURED_TEXT = "X"


def _partition_list(arr, chunk_size):
	partitioned = []
	for i in range(len(arr) // chunk_size):
		chunk = arr[i * chunk_size : (i + 1) * chunk_size]
		partitioned.append(chunk)
	return partitioned


# def _inner_square_text(square_index, is_open, is_top):
# 	"""
# 	'XXXXXX' if captured, top or bottom
# 	'  12  ' if top of square and uncaptured
# 	'______' if bottom of square and uncaptured
# 	"""
# 	if not is_open:
# 		return CAPTURE_FILL
# 	if not is_top:
# 		return HORIZ_EDGE
# 	s = "    "
# 	s += str(square_index)
# 	s += "   " if square_index >= 10 else "    "
# 	return s


# def print_board_old(board):
# 	horiz_edges_chunks = _partition_list(board.edges[:len(board.edges) // 2], board.size - 1)
# 	vert_edges_chunks = _partition_list(board.edges[len(board.edges) // 2:], board.size)
# 	vert_edges_index_chunks = _partition_list(range(len(board.edges) // 2, len(board.edges)), board.size)
# 	output = ""
# 	# first calculate the text for the top row of edges
# 	top_row = f"{color_text(TOP_EDGES_SPLITTER, PLAYER_COLORS[horiz_edges_chunks[0][0]])}"
# 	for edge in horiz_edges_chunks[0]:
# 		top_row += color_text(HORIZ_EDGE + TOP_EDGES_SPLITTER, PLAYER_COLORS[edge])
# 	output += top_row + "\n"
#
# 	# draw the remaining squares and edges
# 	for square_row in range(board.size - 1):
# 		# each square is two lines high
# 		row_text = ""
# 		for is_top in [True, False]:
# 			# start by including left-most edge
# 			row_text += f"{color_text(VERT_EDGE, PLAYER_COLORS[vert_edges_chunks[square_row][0]])}"
# 			for vert_edge_index in vert_edges_index_chunks[square_row][1:]:
# 				# get the index of the square to the left of this edge
# 				square_index = EDGE_SQUARE_MAPS[board.size][vert_edge_index][0]
# 				square = board.squares[square_index]
# 				square_is_open = not square.is_captured()
# 				inner_text = _inner_square_text(square_index, square_is_open, is_top)
#
# 				if is_top or square.is_captured():
# 					text_color = PLAYER_COLORS[square.owner]
# 				else:
# 					text_color = PLAYER_COLORS[board.edges[vert_edge_index]]
# 				edge_color = PLAYER_COLORS[board.edges[vert_edge_index]]
# 				square_text = color_text(inner_text, text_color) + color_text(VERT_EDGE, edge_color)
# 				row_text += square_text
# 			row_text += "\n"
# 		output += row_text
# 	print(output)


def square_number_str(square_index, owner):
	left_empty_fill = OPEN_FILL[:(SQUARE_WIDTH - 1) // 2]
	if owner == OPEN:
		number_text = str(square_index)
	else:
		number_text = CAPTURED_TEXT
	right_empty_fill = OPEN_FILL  # this will be trimmed when returning
	return (left_empty_fill + number_text + right_empty_fill)[:SQUARE_WIDTH]


def print_board(board):
	# Get 2-D array where each inner list is a row of squares
	square_rows = _partition_list(board.squares, board.size - 1)
	output = ""
	top_row_text = f"{color_text(TOP_EDGES_SPLITTER, PLAYER_COLORS[square_rows[0][0].get_edge_owner(UP)])}"
	for sq in square_rows[0]:
		top_row_text += color_text(HORIZ_EDGE + TOP_EDGES_SPLITTER, PLAYER_COLORS[sq.get_edge_owner(UP)])
	output += top_row_text + "\n"
	for sq_row_index, square_row in enumerate(square_rows):
		square_row_text = ""
		# each row of squares is SQUARE_HEIGHT rows of text tall
		for inner_line_index in range(SQUARE_HEIGHT):
			square_row_text += f"{color_text(VERT_EDGE, PLAYER_COLORS[square_row[0].get_edge_owner(LEFT)])}"
			for sq_index_in_row, square in enumerate(square_row):
				if inner_line_index == SQUARE_HEIGHT - 1:
					# last inner line
					inner_text = color_text(HORIZ_EDGE, PLAYER_COLORS[square.get_edge_owner(DOWN)])
				elif inner_line_index == SQUARE_HEIGHT // 2:
					# center line, for number or X
					square_index = sq_row_index * len(square_row) + sq_index_in_row
					inner_text = color_text(square_number_str(square_index, square.owner), PLAYER_COLORS[square.owner])
				else:
					# not center or bottom, so use open fill
					inner_text = OPEN_FILL
				square_row_text += inner_text
				right_edge = color_text(VERT_EDGE, PLAYER_COLORS[square.get_edge_owner(RIGHT)])
				square_row_text += right_edge
			square_row_text += "\n"
		output += square_row_text
	print(output)

	# TODO: FINISH THIS. THE CURRENT PRINT BOARD HAS PRINTING ISSUES.
	# ALSO - THE MARK EDGE MAY HAVE AN ISSUE IN THE BOARD (?)



def print_ascii_art():
	"""Prints the Dots and Boxes Ascii Art"""
	print("""
  _____        _                 
 |  __ \      | |         ___    
 | |  | | ___ | |_ ___   ( _ )   
 | |  | |/ _ \| __/ __|  / _ \/\ 
 | |__| | (_) | |_\__ \ | (_>  < 
 |_____/ \___/ \__|___/  \___/\/ 
 |  _ \                          
 | |_) | _____  _____  ___       
 |  _ < / _ \ \/ / _ \/ __|      
 | |_) | (_) >  <  __/\__ \      
 |____/ \___/_/\_\___||___/    
 """)


def print_game_rules():
	"""Gives the user the option to view the rules of the game"""
	print("GAME RULES NOT IMPLEMENTED")


def _err_text(text, leading_new_lines=0, trailing_new_lines=0):
	return "\n" * leading_new_lines + f"{ERROR_SYMBOL} {text}" + "\n" * trailing_new_lines


def err(text, leading_new_lines=0, trailing_new_lines=0):
	error_msg = _err_text(text, leading_new_lines, trailing_new_lines)
	print(error_msg)


def err_in(text, leading_new_lines=0, trailing_new_lines=0):
	error_msg = _err_text(text, leading_new_lines, trailing_new_lines)
	return input(error_msg)


def _info_text(text, leading_new_lines=0, trailing_new_lines=0):
	return "\n" * leading_new_lines + f"{INFO_SYMBOL} {text}" + "\n" * trailing_new_lines


def info(text, leading_new_lines=0, trailing_new_lines=0):
	info_msg = _info_text(text, leading_new_lines, trailing_new_lines)
	print(info_msg)


def info_in(text, leading_new_lines=0, trailing_new_lines=0):
	info_msg = _info_text(text, leading_new_lines, trailing_new_lines)
	return input(info_msg)


def color_text(text, color):
	return f"{color}{text}{NO_COLOR}"

def tmp():
	from dotsandboxes.dots_and_boxes_board import DotsAndBoxesBoard
	board = DotsAndBoxesBoard(6)
	print_board(board)
