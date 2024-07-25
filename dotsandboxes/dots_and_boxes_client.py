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

# Misc
USER_COLOR = BLUE_COLOR
OPP_COLOR = RED_COLOR


class HumanPlayer(DotsAndBoxesPlayer):

	def __init__(self, player_id):
		super().__init__(player_id, is_ai=False)

	def get_move(self, board):
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
				valid_format = square_index.isdigit() and side in ['L', 'U', 'R', 'D']
				if not valid_format:
					move = pr.err_in("Please enter a valid move:\t").strip().upper()
					continue
				square_index_int = int(square_index)
				if not square_index_int < (board.size - 1) ** 2:
					move = pr.err_in("Not in range. Please enter a valid move:\t").strip().upper()
					continue
				if not board.is_open(square_index_int, side):
					move = pr.err_in("That spot is already taken! Try again:\t").strip().upper()
					continue
				return square_index_int, side


def end_game(winner=None):
	print("(end game not implemented yet)")
	print("\nThanks for playing!")
	exit(0)


def save_game(board, turn):
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

	# temp testing stuff below

	h = HumanPlayer(USER)
	board = DotsAndBoxesBoard(4)
	pr.print_board(board)
	h.get_move(board)
	pr.tmp()
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


