# Kyle Gerner
# Started 3.22.2021
# Gomoku solver, client facing
from datetime import datetime
from util.terminaloutput.colors import GREEN_COLOR, RED_COLOR, NO_COLOR, \
	DARK_GREY_BACKGROUND as MOST_RECENT_HIGHLIGHT_COLOR, color_text
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL, error, info
from util.terminaloutput.erasing import erasePreviousLines
from util.save.saving import path_to_save_file, allow_save
from util.aiduel.dueling import get_dueling_ai_class

from gomoku.gomoku_strategy import GomokuStrategy, opponent_of, perform_move, copy_of_board
import time
import os
import sys
from gomoku.gomoku_player import GomokuPlayer

EMPTY, BLACK, WHITE = '.', 'X', 'O'
game_board = []  # created later
user_piece = None

BOARD_OUTPUT_HEIGHT = -1
BOARD_DIMENSION = 10
TIME_TAKEN_PER_PLAYER = {}
COLUMN_LABELS = "<Will be filled later>"
SAVE_FILENAME = path_to_save_file("gomoku_save.txt")
BOARD_HISTORY = []  # [highlightCoordinates, board]


# class for the Human player
class HumanPlayer(GomokuPlayer):

	def __init__(self, color):
		super().__init__(color, is_ai=False)

	def get_move(self, board):
		"""Takes in the user's input and returns the move"""
		spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (COLUMN_LABELS[-1], len(board))).strip().upper()
		erasePreviousLines(1)
		while True:
			if spot == 'Q':
				print_average_time_taken_by_players()
				print("\nThanks for playing!\n")
				exit(0)
			elif spot == 'S':
				save_game(board, self.color)
				spot = input("Enter a coordinates for a move, or press 'q' to quit:\t").strip().upper()
				erasePreviousLines(2)
			elif spot == 'H':
				spot = get_board_history_input_from_user(is_ai=False)
			elif len(spot) >= 4 or len(spot) == 0 or spot[0] not in COLUMN_LABELS or not spot[1:].isdigit() or int(spot[1:]) > len(board) or int(spot[1:]) < 1:
				spot = input(f"{ERROR_SYMBOL} Invalid input. Please try again.\t").strip().upper()
				erasePreviousLines(1)
			elif board[int(spot[1:]) - 1][COLUMN_LABELS.index(spot[0])] != EMPTY:
				spot = input(f"{ERROR_SYMBOL} That spot is already taken, please choose another:\t").strip().upper()
				erasePreviousLines(1)
			else:
				break
		row = int(spot[1:]) - 1
		col = COLUMN_LABELS.index(spot[0])
		return row, col


def create_empty_game_board(dimension):
	"""Creates the game_board with the specified number of rows and columns"""
	for i in range(dimension):
		row = []
		for j in range(dimension):
			row.append(EMPTY)
		game_board.append(row)


def print_game_board(highlight_coordinates=None, board=None):
	"""Prints the game_board in a human-readable format"""
	if highlight_coordinates is None:
		highlight_coordinates = []
	if board is None:
		board = game_board
	print("\n\t    %s" % " ".join(COLUMN_LABELS))
	for row_num in range(len(board)):
		print("\t%d%s| " % (row_num+1, "" if row_num > 8 else " "), end='')
		for col_num in range(len(board[row_num])):
			spot = board[row_num][col_num]
			piece_color = MOST_RECENT_HIGHLIGHT_COLOR if [row_num, col_num] in highlight_coordinates else ''
			piece_color += GREEN_COLOR if spot == user_piece else RED_COLOR
			if spot == EMPTY:
				print(f"{spot} ", end='')
			else:
				print(f"{piece_color}{spot}{NO_COLOR} ", end='')
		print("")
	print()


def print_move_history(num_moves_previous):
	"""Prints the move history of the current game"""
	while True:
		print_game_board(BOARD_HISTORY[-(num_moves_previous + 1)][0], BOARD_HISTORY[-(num_moves_previous + 1)][1])
		if num_moves_previous == 0:
			return
		print("(%d move%s before current board state)\n" % (num_moves_previous, "s" if num_moves_previous != 1 else ""))
		num_moves_previous -= 1
		user_input = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
		erasePreviousLines(1)
		if user_input == 'q':
			erasePreviousLines(2)
			print_average_time_taken_by_players()
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
			erasePreviousLines(BOARD_DIMENSION + 3)
			print_game_board(BOARD_HISTORY[-1][0])
			user_input = input(f"{INFO_SYMBOL} You're back in play mode. {next_move_prompt}   ").strip().upper()
			erasePreviousLines(1)
			print("\n")  # make this output the same height as the other options
		else:
			user_input = input(f"{ERROR_SYMBOL} Invalid input. {next_move_prompt}   ").strip().upper()
			erasePreviousLines(1)
	return user_input


def print_ascii_title_art():
	"""Prints the fancy text when you start the program"""
	print('\n\t    _  __     _      _')
	print('\t   | |/ /   _| | ___( )___')
	print('\t   | \' / | | | |/ _ \\// __|')
	print('\t   | . \\ |_| | |  __/ \\__ \\')
	print('\t   |_|\\_\\__, |_|\\___| |___/')
	print('   ___\t        |___/        _               _    ___')
	print(' / ___| ___  _ __ ___   ___ | | ___   _     / \\  |_ _|')
	print('| |  _ / _ \\| \'_ ` _ \\ / _ \\| |/ / | | |   / _ \\  | |')
	print('| |_| | (_) | | | | | | (_) |   <| |_| |  / ___ \\ | |')
	print(' \\____|\\___/|_| |_| |_|\\___/|_|\\\\_\\__,_| /_/   \\_\\___|\n')


def print_average_time_taken_by_players():
	"""Prints out the average time taken per move for each player"""
	opponent_piece = opponent_of(user_piece)
	user_time_taken = round(TIME_TAKEN_PER_PLAYER[user_piece][1]/max(1, TIME_TAKEN_PER_PLAYER[user_piece][2]), 2)
	ai_time_taken = round(TIME_TAKEN_PER_PLAYER[opponent_piece][1]/max(1, TIME_TAKEN_PER_PLAYER[opponent_piece][2]), 2)
	print("Average time taken per move:")
	print(f"{color_text(TIME_TAKEN_PER_PLAYER[user_piece][0], GREEN_COLOR)}: {user_time_taken}s")
	print(f"{color_text(TIME_TAKEN_PER_PLAYER[opponent_piece][0], RED_COLOR)}: {ai_time_taken}s")


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
		for row in board:
			save_file.write(" ".join(row) + "\n")
		save_file.write(f"User piece: " + str(user_piece) + "\n")
		save_file.write("Opponent piece: " + opponent_of(user_piece) + "\n")
		save_file.write("Turn: " + turn)
	info("The game has been saved!")


def validate_loaded_save_state(board, piece, turn):
	"""Make sure the state loaded from the save file is valid. Returns a boolean"""
	if piece not in [BLACK, WHITE]:
		error("Invalid user piece!")
		return False
	if turn not in [BLACK, WHITE]:
		error("Invalid player turn!")
		return False
	board_dimension = len(board)
	if not 6 < board_dimension < 100:
		error("Invalid board dimension!")
		return False
	for row in board:
		if len(row) != board_dimension:
			error("Board is not square!")
			return False
		if row.count(EMPTY) + row.count(BLACK) + row.count(WHITE) != board_dimension:
			error("Board contains invalid pieces!")
			return False
	return True


def load_saved_game():
	"""Try to load the saved game data"""
	global user_piece, game_board
	with open(SAVE_FILENAME, 'r') as saveFile:
		try:
			lines_from_save_file = saveFile.readlines()
			time_of_previous_save = lines_from_save_file[3].strip()
			use_existing_save = input(f"{INFO_SYMBOL} Would you like to load the saved game from {time_of_previous_save}? (y/n)\t").strip().lower()
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
			board = []
			while not current_line.startswith("User piece"):
				board.append(current_line.split())
				line_num += 1
				current_line = lines_from_save_file[line_num].strip()
			user_piece = current_line.split(": ")[1].strip()
			line_num += 2
			current_line = lines_from_save_file[line_num].strip()
			turn = current_line.split(": ")[1].strip()
			if not validate_loaded_save_state(board, user_piece, turn):
				raise ValueError
			game_board = board
			delete_save_file = input(f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			file_deleted_text = ""
			if delete_save_file == 'y':
				os.remove(SAVE_FILENAME)
				file_deleted_text = "Save file deleted. "
			info(f"{file_deleted_text}Resuming saved game...")
			return turn
		except Exception:
			error("There was an issue reading from the save file. Starting a new game...")
			return None


def run():
	"""Main method that runs through the gameplay and setup"""
	global game_board, user_piece, BOARD_OUTPUT_HEIGHT, COLUMN_LABELS, TIME_TAKEN_PER_PLAYER, BOARD_DIMENSION
	if "-d" in sys.argv or "-aiDuel" in sys.argv:
		UserPlayerClass = get_dueling_ai_class(GomokuPlayer, "GomokuStrategy")
		print()
		info("You are in AI Duel Mode!")
		ai_duel_mode = True
	else:
		UserPlayerClass = HumanPlayer
		ai_duel_mode = False

	print_ascii_title_art()

	turn = BLACK
	use_saved_game = False
	if os.path.exists(SAVE_FILENAME):
		turn_from_save_file = load_saved_game()
		if turn_from_save_file is not None:
			turn = turn_from_save_file
			use_saved_game = True
			BOARD_HISTORY.append([[], copy_of_board(game_board)])

	user_player_name = "Your AI" if ai_duel_mode else "You"
	ai_player_name = "My AI" if ai_duel_mode else "AI"
	if use_saved_game:
		opponent_piece = opponent_of(user_piece)
		board_dimension = len(game_board)
	else:
		board_dimension = input("What is the dimension of the board? (Default is 13x13)\nEnter a single odd number:\t").strip()
		erasePreviousLines(2)
		if board_dimension.isdigit() and int(board_dimension) % 2 == 1 and 6 < int(board_dimension) < 100:
			board_dimension = int(board_dimension)
			print("The board will be %dx%d!" % (board_dimension, board_dimension))
		else:
			board_dimension = 13
			error("Invalid input. The board will be 13x13!")
		create_empty_game_board(int(board_dimension))

		player_color_input = input("Would you like to be BLACK ('b') or WHITE ('w')? (black goes first!):\t").strip().lower()
		erasePreviousLines(2)
		if player_color_input == 'b':
			user_piece = BLACK
			opponent_piece = WHITE
			print(f"{user_player_name} will be {color_text('BLACK', GREEN_COLOR)}!")
		else:
			user_piece = WHITE
			opponent_piece = BLACK
			if player_color_input == 'w':
				print(f"{user_player_name} will be {color_text('WHITE', GREEN_COLOR)}!")
			else:
				error(f"Invalid input. {user_player_name} will be {color_text('WHITE', GREEN_COLOR)}!")

	TIME_TAKEN_PER_PLAYER = {
		user_piece: [user_player_name, 0, 0],    # [player name, total time, num moves]
		opponent_piece: [ai_player_name, 0, 0]
	}
	COLUMN_LABELS = list(map(chr, range(65, 65 + board_dimension)))
	BOARD_DIMENSION = board_dimension
	BOARD_OUTPUT_HEIGHT = board_dimension + 5
	player_names = {user_piece: user_player_name, opponent_piece: ai_player_name}
	players = {opponent_piece: GomokuStrategy(opponent_piece, board_dimension), user_piece: UserPlayerClass(user_piece)}

	print(f"\n{user_player_name}: {GREEN_COLOR}{user_piece}{NO_COLOR}\t{ai_player_name}: {RED_COLOR}{opponent_piece}{NO_COLOR}")
	print("Type 'q' to quit.")
	print("Type 's' to save the game.")
	print("Type 'h' to see previous moves.")
	print_game_board()
	print("\n")

	game_over, winner = False, None

	while not game_over:
		name_of_current_player = player_names[turn]
		current_player = players[turn]
		if current_player.is_ai:
			user_input = input(f"{name_of_current_player}'s turn, press enter for it to play.\t").strip().upper()
			erasePreviousLines(1)
			while user_input in ['Q', 'S', 'H']:
				if user_input == 'Q':
					print_average_time_taken_by_players()
					print("\nThanks for playing!\n")
					exit(0)
				elif user_input == 'H':
					user_input = get_board_history_input_from_user(is_ai=True)
				else:
					save_game(game_board, turn)
					user_input = input(f"Press enter for {name_of_current_player} to play, or press 'q' to quit:\t").strip().upper()
					erasePreviousLines(2)
		start_time = time.time()
		row_played, col_played = current_player.get_move(game_board)
		end_time = time.time()
		total_time_taken_for_move = end_time - start_time
		TIME_TAKEN_PER_PLAYER[turn][1] += total_time_taken_for_move
		TIME_TAKEN_PER_PLAYER[turn][2] += 1
		minutes_taken = int(total_time_taken_for_move) // 60
		seconds_taken = total_time_taken_for_move % 60
		time_taken_output_str = ("  (%dm " % minutes_taken if minutes_taken > 0 else "  (") + ("%.2fs)" % seconds_taken) if current_player.is_ai else ""
		perform_move(game_board, row_played, col_played, turn)
		BOARD_HISTORY.append([[[row_played, col_played]], copy_of_board(game_board)])
		erasePreviousLines(BOARD_OUTPUT_HEIGHT)
		print_game_board([[row_played, col_played]])
		move_formatted = COLUMN_LABELS[col_played] + str(row_played + 1)
		print("%s played in spot %s%s\n" % (name_of_current_player, move_formatted, time_taken_output_str))
		turn = opponent_of(turn)
		game_over, winner = players[opponent_piece].is_terminal(game_board)

	if winner is None:
		print("Nobody wins, it's a tie!")
	else:
		highlight_color = GREEN_COLOR if winner == user_piece else RED_COLOR
		winner_color_name = "BLACK" if winner == BLACK else "WHITE"
		print(f"{color_text(winner_color_name, highlight_color)} wins!\n")
	print_average_time_taken_by_players()
	print("\nThanks for playing!\n")
