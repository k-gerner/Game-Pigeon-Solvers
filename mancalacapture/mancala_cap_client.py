# Kyle Gerner
# Started 11.19.2022
# Mancala Capture, client facing
import os
import sys
import time
from datetime import datetime
from util.terminaloutput.colors import RED_COLOR, GREEN_COLOR, NO_COLOR, color_text
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL, info
from util.terminaloutput.erasing import erasePreviousLines
from util.save.saving import path_to_save_file, allow_save
from util.aiduel.dueling import get_dueling_ai_class
from mancalacapture.mancala_player import MancalaPlayer
from mancalacapture.board_functions import get_index_of_opposite_hole, push_all_pebbles_to_bank, winning_player_bank_index, \
	is_board_terminal, perform_move
from mancalacapture.constants import POCKETS_PER_SIDE, BOARD_OUTPUT_HEIGHT, PLAYER1_BANK_INDEX, PLAYER2_BANK_INDEX, \
	SIDE_INDENT_STR, LEFT_SIDE_ARROW, RIGHT_SIDE_ARROW, BOARD_SIZE
from mancalacapture.mancala_cap_strategy import MancalaStrategy

USE_REVERSED_PRINT_LAYOUT = False
BOARD = [4] * 6 + [0] + [4] * 6 + [0]
PLAYER1_ID = 1
PLAYER2_ID = 2
SAVE_FILENAME = path_to_save_file("mancala_cap_save.txt")
BOARD_HISTORY = []  # [highlightPocketIndex, playerId, board]


# class for the Human player
class HumanPlayer(MancalaPlayer):

	def __init__(self, bank_index=6):
		super().__init__(bank_index, is_ai=False)

	def get_move(self, board):
		"""Takes in the user's input and returns the index on the board for the selected move"""
		spot = input(f"It's your turn, which spot would you like to play? (1 - {POCKETS_PER_SIDE}):\t").strip().upper()
		erasePreviousLines(1)
		while True:
			if spot == 'Q':
				print("\nThanks for playing!\n")
				exit(0)
			elif spot == 'F':
				global USE_REVERSED_PRINT_LAYOUT
				USE_REVERSED_PRINT_LAYOUT = not USE_REVERSED_PRINT_LAYOUT
				erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
				print_board(board)
				print("\n")
				spot = input(
					f"Board print layout changed. Which spot would you like to play? (1 - {POCKETS_PER_SIDE}):\t").strip().upper()
				erasePreviousLines(1)
			elif spot == 'S':
				save_game(board, PLAYER1_ID)
				spot = input("Enter a coordinates for a move, or press 'q' to quit:\t").strip().upper()
				erasePreviousLines(2)
			elif spot == 'H':
				spot = get_board_history_input_from_user(is_ai=False)
			elif not spot.isdigit() or int(spot) < 1 or int(spot) > 6:
				spot = input(f"{ERROR_SYMBOL} Please enter a number 1 - {POCKETS_PER_SIDE}:\t").strip().upper()
				erasePreviousLines(1)
			elif board[int(spot) - 1] == 0:
				spot = input(f"{ERROR_SYMBOL} That pocket is empty! Please try again:\t").strip().upper()
				erasePreviousLines(1)
			else:
				break

		return int(spot) - 1


def print_board(board, player_id=None, move=None):
	"""Prints the game board"""
	# orientation
	arrow_index = -1
	if USE_REVERSED_PRINT_LAYOUT:
		top_bank_index = PLAYER1_BANK_INDEX
		bottom_bank_index = PLAYER2_BANK_INDEX
		left_side_player_id = PLAYER2_ID
		top_left_pocket_index = POCKETS_PER_SIDE + 1  # which index is printed in the top left corner of the printed board
		left_side_color = RED_COLOR
		right_side_color = GREEN_COLOR
		if move is not None:
			arrow_index = move if move > POCKETS_PER_SIDE else get_index_of_opposite_hole(move)
	else:
		top_bank_index = PLAYER2_BANK_INDEX
		bottom_bank_index = PLAYER1_BANK_INDEX
		left_side_player_id = PLAYER1_ID
		top_left_pocket_index = 0
		left_side_color = GREEN_COLOR
		right_side_color = RED_COLOR
		if move is not None:
			arrow_index = move if move < POCKETS_PER_SIDE else get_index_of_opposite_hole(move)

	print()
	print(SIDE_INDENT_STR + " " * 5 + f"{right_side_color}{board[top_bank_index]}{NO_COLOR}")  # top bank
	print(SIDE_INDENT_STR + "___________")
	for index in range(top_left_pocket_index, top_left_pocket_index + POCKETS_PER_SIDE):
		left_side_str_prefix = SIDE_INDENT_STR  # may change to arrow
		right_side_str_suffix = ""  # may change to arrow
		if index == arrow_index:
			if player_id == left_side_player_id:
				left_side_str_prefix = LEFT_SIDE_ARROW
			else:
				right_side_str_suffix = RIGHT_SIDE_ARROW

		left_side_str = left_side_str_prefix + " " * 2 \
					  + f"{left_side_color}{board[index]}{NO_COLOR}" \
					  + (" " if board[index] >= 10 else "  ")
		right_side_str = (" " if board[get_index_of_opposite_hole(index)] >= 10 else "  ") \
					   + f"{right_side_color}{board[get_index_of_opposite_hole(index)]}{NO_COLOR}" \
					   + right_side_str_suffix
		print(SIDE_INDENT_STR + "     |     ")
		print(left_side_str + str(min(index, get_index_of_opposite_hole(index)) + 1) + right_side_str)
		print(SIDE_INDENT_STR + "_____|_____")
	print("\n" + SIDE_INDENT_STR + " " * 5 + f"{left_side_color}{board[bottom_bank_index]}{NO_COLOR}\n")  # bottom bank


def opponent_of(player_id):
	"""Gets the id opponent of the given id"""
	return PLAYER1_ID if player_id == PLAYER2_ID else PLAYER2_ID


def print_average_time_taken_by_players(time_taken_per_player):
	"""Prints out the average time taken per move for each player"""
	user_time_taken = round(time_taken_per_player[PLAYER1_ID][1] / max(1, time_taken_per_player[PLAYER1_ID][2]), 2)
	ai_time_taken = round(time_taken_per_player[PLAYER2_ID][1] / max(1, time_taken_per_player[PLAYER2_ID][2]), 2)
	print("Average time taken per move:")
	print(f"{color_text(str(time_taken_per_player[PLAYER1_ID][0]), GREEN_COLOR)}: {user_time_taken}s")
	print(f"{color_text(str(time_taken_per_player[PLAYER2_ID][0]), RED_COLOR)}: {ai_time_taken}s")


def print_ascii_art():
	"""Prints the Mancala Capture Ascii Art"""
	print("""
  __  __                       _       
 |  \/  |                     | |      
 | \  / | __ _ _ __   ___ __ _| | __ _ 
 | |\/| |/ _` | '_ \ / __/ _` | |/ _` |
 | |  | | (_| | | | | (_| (_| | | (_| |
 |_|__|_|\__,_|_| |_|\___\__,_|_|\__,_|
  / ____|          | |                 
 | |     __ _ _ __ | |_ _   _ _ __ ___ 
 | |    / _` | '_ \| __| | | | '__/ _ \ 
 | |___| (_| | |_) | |_| |_| | | |  __/
  \_____\__,_| .__/ \__|\__,_|_|  \___|
             | |                       
             |_|  
    """)


def save_game(board, turn):
	"""Saves the given board state to a save file"""
	if not allow_save(SAVE_FILENAME):
		return
	with open(SAVE_FILENAME, 'w') as save_file:
		save_file.write("This file contains the save state of a previously played game.\n")
		save_file.write("Modifying this file may cause issues with loading the save state.\n\n")
		time_of_save = datetime.now().strftime("%m/%d/%Y at %I:%M:%S %p")
		save_file.write(time_of_save + "\n\n")
		save_file.write("SAVE STATE:\n")
		save_file.write(f"   {board[PLAYER2_BANK_INDEX]}\n")  # opponent bank
		for row in range(len(board) // 2 - 1):  # playable caves; default 1 - 6
			save_file.write(
				str(board[row]) + (" | " if board[row] >= 10 else "  | ") + str(board[-1 * (row + 2)]) + "\n")
		save_file.write(f"   {str(board[PLAYER1_BANK_INDEX])}\n")  # player bank
		save_file.write(f"Turn: {turn}")
	info("The game has been saved!")


def validate_loaded_save_state(board, turn):
	"""Make sure the state loaded from the save file is valid. Returns a boolean"""
	if turn not in [PLAYER1_ID, PLAYER2_ID]:
		print(f"{ERROR_SYMBOL} Invalid player turn!")
		return False
	if len(board) % 2 != 0:
		print(f"{ERROR_SYMBOL} Please ensure each player has a bank and the same number of pockets!")
		return False
	num_rows = len(board) // 2 - 1
	if num_rows != POCKETS_PER_SIDE:
		print(f"{ERROR_SYMBOL} # Rows must be {POCKETS_PER_SIDE}! Was {num_rows}")
		return False
	for spot in board:
		if spot < 0:
			print(f"{ERROR_SYMBOL} Pockets cannot have a negative amount of pebbles!")
			return False
	return True


def load_saved_game():
	"""Try to load the saved game data"""
	global BOARD
	with open(SAVE_FILENAME, 'r') as save_file:
		try:
			lines_from_save_file = save_file.readlines()
			time_of_previous_save = lines_from_save_file[3].strip()
			use_existing_save = input(
				f"{INFO_SYMBOL} Would you like to load the saved game from {time_of_previous_save}? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			if use_existing_save != 'y':
				info("Starting a new game...")
				return
			line_num = 0
			current_line = lines_from_save_file[line_num].strip()
			while current_line != "SAVE STATE:":
				line_num += 1
				current_line = lines_from_save_file[line_num].strip()
			line_num += 1
			current_line = lines_from_save_file[line_num].strip()

			opponent_bank = [int(current_line.strip())]
			line_num += 1
			current_line = lines_from_save_file[line_num].strip()

			user_pockets = []
			opponent_pockets = []
			while "|" in current_line:
				user_pockets.append(int(current_line.split("|")[0].strip()))
				opponent_pockets.append(int(current_line.split("|")[1].strip()))
				line_num += 1
				current_line = lines_from_save_file[line_num].strip()
			user_bank = [int(current_line.strip())]
			board = user_pockets + user_bank + opponent_pockets + opponent_bank

			while not current_line.startswith("Turn:"):
				line_num += 1
				current_line = lines_from_save_file[line_num].strip()
			turn = int(current_line.split()[1])

			if not validate_loaded_save_state(board, turn):
				raise ValueError
			BOARD = board
			delete_save_file = input(
				f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			file_deleted_text = ""
			if delete_save_file == 'y':
				os.remove(SAVE_FILENAME)
				file_deleted_text = "Save file deleted."
			info(f"{file_deleted_text} Resuming saved game...")
			return turn
		except Exception:
			print(f"{ERROR_SYMBOL} There was an issue reading from the save file. Starting a new game...")
			return None


def print_move_history(num_moves_previous):
	"""Prints the move history of the current game"""
	while True:
		erasePreviousLines(2)
		print_board(BOARD_HISTORY[-(num_moves_previous + 1)][2], BOARD_HISTORY[-(num_moves_previous + 1)][1],
					BOARD_HISTORY[-(num_moves_previous + 1)][0])
		if num_moves_previous == 0:
			return
		print("(%d move%s before current board state)\n" % (num_moves_previous, "s" if num_moves_previous != 1 else ""))
		num_moves_previous -= 1
		user_input = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
		erasePreviousLines(1)
		if user_input == 'q':
			erasePreviousLines(2)
			print("\nThanks for playing!\n")
			exit(0)
		elif user_input == 'e':
			erasePreviousLines(2)
			return
		else:
			erasePreviousLines(BOARD_OUTPUT_HEIGHT)


def get_board_history_input_from_user(is_ai):
	"""
    Prompts the user for input for how far the board history function.
    Returns the user's input for the next move
    """
	next_move_prompt = "Press enter to continue." if is_ai else "Enter a valid move to play:"
	if len(BOARD_HISTORY) < 2:
		user_input = input(f"{INFO_SYMBOL} No previous moves to see. {next_move_prompt}   ").strip().upper()
		erasePreviousLines(1)
	else:
		num_moves_previous = input(f"How many moves ago do you want to see? (1 to {len(BOARD_HISTORY) - 1})  ").strip()
		erasePreviousLines(1)
		if num_moves_previous.isdigit() and 1 <= int(num_moves_previous) <= len(BOARD_HISTORY) - 1:
			erasePreviousLines(BOARD_OUTPUT_HEIGHT)
			print_move_history(int(num_moves_previous))
			erasePreviousLines(BOARD_OUTPUT_HEIGHT)
			print_board(BOARD_HISTORY[-1][2], BOARD_HISTORY[-1][1], BOARD_HISTORY[-1][0])
			user_input = input(f"{INFO_SYMBOL} You're back in play mode. {next_move_prompt}   ").strip().upper()
			erasePreviousLines(1)
			print("\n")  # make this output the same height as the other options
		else:
			user_input = input(f"{ERROR_SYMBOL} Invalid input. {next_move_prompt}   ").strip().upper()
			erasePreviousLines(1)
	return user_input


def run():
	if "-d" in sys.argv or "-aiDuel" in sys.argv:
		UserPlayerClass = get_dueling_ai_class(MancalaPlayer, "MancalaStrategy")
		print()
		info("You are in AI Duel Mode!")
		ai_duel_mode = True
	else:
		UserPlayerClass = HumanPlayer
		ai_duel_mode = False
	print_ascii_art()

	players = {  # remove hardcode values later
		PLAYER1_ID: UserPlayerClass(PLAYER1_BANK_INDEX),
		PLAYER2_ID: MancalaStrategy(PLAYER2_BANK_INDEX)
	}
	name_of_player1 = "Your AI" if ai_duel_mode else "Human"
	name_of_player2 = "My AI" if ai_duel_mode else "AI"
	player_names = {
		PLAYER1_ID: name_of_player1,
		PLAYER2_ID: name_of_player2
	}
	time_taken_per_player = {
		PLAYER1_ID: [name_of_player1, 0, 0],  # [player name, total time, num moves]
		PLAYER2_ID: [name_of_player2, 0, 0]
	}

	turn = PLAYER1_ID
	use_saved_game = False
	if os.path.exists(SAVE_FILENAME):
		turn_from_save_file = load_saved_game()
		if turn_from_save_file is not None:
			turn = turn_from_save_file
			use_saved_game = True
			BOARD_HISTORY.append([-1, turn, BOARD.copy()])

	if not use_saved_game:
		user_go_first = input("Would you like to go first? (y/n):\t").strip().upper()
		erasePreviousLines(1)
		if user_go_first == "Y":
			turn = PLAYER1_ID
			print("%s will go first!" % player_names[turn])
		else:
			turn = PLAYER2_ID
			print("%s will go first!" % player_names[turn])

	print("Type 'q' to quit.")
	print("Type 'f' to flip the board orientation 180 degrees.")
	print("Type 's' to save the game.")
	print("Type 'h' to see previous moves.")

	game_over = False
	print_board(BOARD)
	print("\n")
	extra_lines_printed = 2
	while not game_over:
		name_of_current_player = player_names[turn]
		current_player = players[turn]
		if current_player.is_ai:
			user_input = input(f"{name_of_current_player}'s turn, press enter for it to play.\t").strip().upper()
			erasePreviousLines(1)
			while user_input in ['Q', 'H', 'F', 'S']:
				if user_input == 'Q':
					print_average_time_taken_by_players(time_taken_per_player)
					print("\nThanks for playing!\n")
					exit(0)
				elif user_input == 'H':
					user_input = get_board_history_input_from_user(is_ai=True)
				elif user_input == 'F':
					global USE_REVERSED_PRINT_LAYOUT
					USE_REVERSED_PRINT_LAYOUT = not USE_REVERSED_PRINT_LAYOUT
					erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
					print_board(BOARD)
					print("\n")
					user_input = input(f"Board print layout changed. Press enter to continue:\t").strip().upper()
					erasePreviousLines(1)
				else:
					save_game(BOARD, turn)
					user_input = input(
						f"Press enter for {name_of_current_player} to play, or press 'q' to quit:\t").strip().upper()
					erasePreviousLines(2)

		start_time = time.time()
		chosen_move = current_player.get_move(BOARD)
		end_time = time.time()
		total_time_taken_for_move = end_time - start_time
		time_taken_per_player[turn][1] += total_time_taken_for_move
		time_taken_per_player[turn][2] += 1
		minutes_taken = int(total_time_taken_for_move) // 60
		seconds_taken = total_time_taken_for_move % 60
		time_taken_output_str = ("  (%dm " if minutes_taken > 0 else "  (") + (
				"%.2fs)" % seconds_taken) if current_player.is_ai else ""
		final_pebble_location = perform_move(BOARD, chosen_move, current_player.bankIndex)
		BOARD_HISTORY.append([chosen_move, turn, BOARD.copy()])
		erasePreviousLines(BOARD_OUTPUT_HEIGHT + extra_lines_printed)
		print_board(BOARD, turn, chosen_move)
		move_formatted = str(min(BOARD_SIZE - 2 - chosen_move, chosen_move) + 1)
		print("%s played in spot %s%s. " % (name_of_current_player, move_formatted, time_taken_output_str), end='')
		if final_pebble_location != current_player.bankIndex:
			print("\n")
			turn = opponent_of(turn)
		else:
			print("%s's move ended in their bank, so they get another turn.\n" % name_of_current_player)
		extra_lines_printed = 2
		game_over = is_board_terminal(BOARD)

	push_all_pebbles_to_bank(BOARD)
	erasePreviousLines(BOARD_OUTPUT_HEIGHT + extra_lines_printed)
	print_board(BOARD)
	winner_id = PLAYER1_ID if winning_player_bank_index(BOARD) == PLAYER1_BANK_INDEX else PLAYER2_ID
	if winner_id is None:
		print("It's a tie!\n")
	else:
		print("%s wins!\n" % player_names[winner_id])
	print_average_time_taken_by_players(time_taken_per_player)
