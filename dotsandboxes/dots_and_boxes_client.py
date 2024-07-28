# Kyle Gerner
# Started 7.16.2024
# Dots and Boxes, client facing

from datetime import datetime
import sys
import dotsandboxes.printer as pr
from dotsandboxes.dots_and_boxes_player import DotsAndBoxesPlayer
from dotsandboxes.dots_and_boxes_board import DotsAndBoxesBoard
from dotsandboxes.constants import USER, OPP
from dotsandboxes.constants import LEFT, UP, RIGHT, DOWN
from util.terminaloutput.colors import NO_COLOR, YELLOW_COLOR, GREEN_COLOR, BLUE_COLOR, RED_COLOR, ORANGE_COLOR
from util.save.saving import path_to_save_file, allow_save
from util.aiduel.dueling import get_dueling_ai_class

SAVE_FILENAME = path_to_save_file("dotsandboxes_save.txt")

# Output printing symbols
DOT_ICON = "o"
LINE_VERT = "|"
LINE_HORIZ = "--"

# Relevant to game state
board_history = []


class HumanPlayer(DotsAndBoxesPlayer):

	def __init__(self, player_id):
		super().__init__(player_id, is_ai=False)

	def get_moves(self, board):
		"""Takes in the user's input and returns the move"""
		move = input("It's your turn, which spot would you like to play?\t").strip().upper()
		while True:
			if move == 'Q':
				end_game()
			elif move == 'S':
				save_game(board, self.player_id)
				move = input("It's your turn, which spot would you like to play?\t").strip().upper()
			elif move == 'QS' or move == 'SQ':
				save_game(board, self.player_id)
				end_game()
			elif move == 'H':
				print("HISTORY NOT IMPLEMENTED YET!")
				move = input("input move:  ").strip().upper()
			else:
				square_index = move.rstrip('LURD ')
				side = move[len(square_index):].strip()
				valid_format = square_index.isdigit() and side in [LEFT, UP, RIGHT, DOWN]
				if not valid_format:
					move = pr.err_in("Please enter a valid move:\t").strip().upper()
					continue
				square_index_int = int(square_index)
				if not square_index_int < (board.size - 1) ** 2:
					move = pr.err_in("Not in range. Please enter a valid move:\t").strip().upper()
					continue
				if not board.is_square_edge_open(square_index_int, side):
					move = pr.err_in("That spot is already taken! Try again:\t").strip().upper()
					continue
				return [(square_index_int, side)]


def end_game(winner=None):
	print("(end game not implemented yet)")
	print("\nThanks for playing!")
	exit(0)


def save_game(board, turn):
	pass
	# if not allow_save(SAVE_FILENAME):
	# 	return
	# with open(SAVE_FILENAME, 'w') as saveFile:
	# 	saveFile.write("This file contains the save state of a previously played game.\n")
	# 	saveFile.write("Modifying this file may cause issues with loading the save state.\n\n")
	# 	time_of_save = datetime.now().strftime("%m/%d/%Y at %I:%M:%S %p")
	# 	saveFile.write(time_of_save + "\n\n")
	# 	saveFile.write("SAVE STATE:\n")
	# 	for row in board:
	# 		saveFile.write(" ".join(row) + "\n")
	# 	saveFile.write(f"User piece: " + USER_PIECE + "\n")
	# 	saveFile.write("Opponent piece: " + OPPONENT_PIECE + "\n")
	# 	saveFile.write("Turn: " + turn)
	# pr.info("The game has been saved!")


def load_saved_game():
	pass


def print_move_history(num_previous):
	pass


def switch_turn(player):
	return USER if player == OPP else OPP


def get_board_size_input():
	size = input("Which size board (vertex width)? (4, 5 or 6):\t").strip().upper()
	while True:
		if size == 'Q':
			end_game()
		elif size == '':
			pr.info("Using default board size of 4!")
			return 4
		if not size.isdigit() or int(size) not in [4, 5, 6]:
			size = pr.err_in("Invalid size. Options are 4, 5 or 6:\t")
			continue
		return int(size)


def get_color_mappings():
	blue = pr.color_text(BLUE_COLOR, "BLUE")
	red = pr.color_text(RED_COLOR, "RED")
	color = input(f"Would you like to be {blue} (b) or {red} (r)?:\t").strip().upper()
	while True:
		if color == 'Q':
			end_game()
		elif color == '':
			blue = pr.color_text(BLUE_COLOR, "BLUE")
			pr.info(f"Using default color {blue}!")
			return {
				USER: BLUE_COLOR,
				OPP: RED_COLOR
			}
		if not color in ['B', 'R']:
			size = pr.err_in("Invalid color. Options are {blue} (b) or {red} (r):\t").strip().upper()
			continue
		if color == 'B':
			return {
				USER: BLUE_COLOR,
				OPP: RED_COLOR
			}
		else:
			return {
				USER: RED_COLOR,
				OPP: BLUE_COLOR
			}



def run():
	if "-d" in sys.argv or "-aiDuel" in sys.argv:
		UserPlayerClass = get_dueling_ai_class(DotsAndBoxesPlayer, "DotsAndBoxesStrategy")
		pr.info("You are in AI Duel Mode!", leading_new_lines=1)
		ai_duel_mode = True
	else:
		UserPlayerClass = HumanPlayer
		ai_duel_mode = False

	pr.print_ascii_art()
	pr.print_game_rules()
	print("SAVED GAME NOT IMPLEMENTED YET")

	# board history goes here

	user_player_name = "Your AI" if ai_duel_mode else "You"
	ai_player_name = "My AI" if ai_duel_mode else "AI"
	player_names = {
		USER: user_player_name,
		OPP: ai_player_name
	}
	players = {
		USER: UserPlayerClass(USER),
		OPP: HumanPlayer(OPP)
		# OPP: DotsAndBoxesStrategy(OPP)
	}
	time_taken_per_player = {
		USER: [user_player_name, 0, 0],  # [player name, total time, num moves]
		OPP: [ai_player_name, 0, 0]
	}

	board_size = get_board_size_input()
	player_colors = get_color_mappings()
	board = DotsAndBoxesBoard(board_size)
	pr.print_board(board)

	# Blue goes first
	turn = USER if player_colors[USER] == BLUE_COLOR else OPP
	while not board.is_full():
		player = players[turn]
		if player.is_ai:
			user_input = input(f"{player_names[turn]}'s turn, press enter for it to play.\t")
			while user_input in ['Q', 'S', 'QS', 'SQ', 'H']:
				if user_input == 'Q':
					end_game()
				elif user_input == 'S':
					save_game(board, turn)
					user_input = input("Press enter to continue. ").strip().upper()
					# erasePreviousLines(2)
				elif user_input == 'QS' or user_input == 'SQ':
					save_game(board, turn)
					end_game()
				# elif user_input == 'H':
				# 	user_input, linesWrittenToConsole = getBoardHistoryInputFromUser(BOARD, turn, True,
				# 																	linesWrittenToConsole)
		moves = player.get_moves(board)
		moves_str = ', '.join(pr.color_text(f"{square_index}{side}", player_colors[turn]) for square_index, side in moves)
		print(f"{player_names[turn]} played: {moves_str}")
		for move in moves:
			board.draw_square_edge(move[0], move[1], turn)
		turn = switch_turn(turn)
		pr.print_board(board)

	user_score = board.score(USER)
	opp_score = board.score(OPP)
	print("Final score:")
	print(f"{pr.color_text(player_names[USER.player_id], player_colors[USER.player_id])}: {user_score}")
	print(f"{pr.color_text(player_names[OPP.player_id], player_colors[OPP.player_id])}: {opp_score}")





	# temp testing stuff below

	# h = HumanPlayer(USER)
	# board = DotsAndBoxesBoard(4)
	# pr.print_board(board)
	# h.get_move(board)
	# pr.tmp()



	# TODO!!!!
	# maybe make the board store data in a graph structure?
	# the squares could be the nodes and the edges would connect them
	# essentially the main difference in this approach would be
	# storing the square neighbors in the Square object
	# tbh now that I think about it more it may not make much of a difference
	# still worth thinking about though
	# what we need to keep track of for the AI:
	# - all available edges
	# - how a given move will affect other squares
	# - score
	# -


