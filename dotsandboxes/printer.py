from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL
from util.terminaloutput.colors import NO_COLOR
from dotsandboxes.constants import OPEN, USER, OPP, PLAYER_COLORS, EDGE_SQUARE_MAPS

HORIZ_EDGE = "______"
TOP_EDGES_SPLITTER = "_"
VERT_EDGE = "|"
CAPTURE_FILL = "XXXXXX"
OPEN_FILL = "      "


def _partition_list(arr, chunk_size):
	partitioned = []
	for i in range(len(arr) // chunk_size):
		chunk = arr[i * chunk_size : (i + 1) * chunk_size]
		partitioned.append(chunk)
	return partitioned


def _inner_square_text(square_index, is_open, is_top):
	"""
	'XXXXXX' if captured, top or bottom
	'  12  ' if top of square and uncaptured
	'______' if bottom of square and uncaptured
	"""
	if not is_open:
		return CAPTURE_FILL
	if not is_top:
		return HORIZ_EDGE
	s = "  "
	s += str(square_index)
	s += "  " if square_index >= 10 else "   "
	return s


def print_board(board):
	horiz_edges_chunks = _partition_list(board.edges[:len(board.edges) // 2], board.size - 1)
	vert_edges_chunks = _partition_list(board.edges[len(board.edges) // 2:], board.size)
	vert_edges_index_chunks = _partition_list(range(len(board.edges) // 2, len(board.edges)), board.size)
	output = ""
	# first calculate the text for the top row of edges
	top_row = f"{color_text(TOP_EDGES_SPLITTER, PLAYER_COLORS[horiz_edges_chunks[0][0]])}"
	for edge in horiz_edges_chunks[0]:
		top_row += color_text(HORIZ_EDGE + TOP_EDGES_SPLITTER, PLAYER_COLORS[edge])
	output += top_row + "\n"

	# draw the remaining squares and edges
	for square_row in range(board.size - 1):
		# each square is two lines high
		row_text = ""
		for is_top in [True, False]:
			row_text += f"{color_text(VERT_EDGE, PLAYER_COLORS[vert_edges_chunks[square_row][0]])}"
			for vert_edge_index in vert_edges_index_chunks[square_row][1:]:
				# get the index of the square to the left of this edge
				square_index = EDGE_SQUARE_MAPS[board.size][vert_edge_index][0]
				square = board.squares[square_index]
				square_is_open = not square.is_captured()
				inner_text = _inner_square_text(square_index, square_is_open, is_top)

				if is_top or square.is_captured():
					text_color = PLAYER_COLORS[square.owner]
				else:
					text_color = PLAYER_COLORS[board.edges[vert_edge_index]]
				edge_color = PLAYER_COLORS[board.edges[vert_edge_index]]
				square_text = color_text(inner_text, text_color) + color_text(VERT_EDGE, edge_color)
				row_text += square_text
			row_text += "\n"
		output += row_text
	print(output)


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
