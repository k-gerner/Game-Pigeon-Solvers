# Tic Tac Toe AI client facing
# Kyle G 6.6.2021

from tictactoe.tictactoe_player import TicTacToePlayer
from tictactoe.tictactoe_strategy import TicTacToeStrategy, opponent_of, is_terminal, perform_move, copy_of_board
from util.terminaloutput.colors import GREEN_COLOR, RED_COLOR, NO_COLOR
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL, error, info
from util.terminaloutput.erasing import erasePreviousLines
from util.terminaloutput.colors import color_text
from util.save.saving import path_to_save_file, allow_save
from util.aiduel.dueling import get_dueling_ai_class
from datetime import datetime
import os
import sys

EMPTY, X_PIECE, O_PIECE = ' ', 'X', 'O'
ROW_LABELS = "ABC"
gameBoard = [[EMPTY, EMPTY, EMPTY], 
			 [EMPTY, EMPTY, EMPTY],
			 [EMPTY, EMPTY, EMPTY]]
USER_PIECE = X_PIECE

BOARD_OUTPUT_HEIGHT = 7

SAVE_FILENAME = path_to_save_file("tictactoe_save.txt")
BOARD_HISTORY = []

# class for the Human player
class HumanPlayer(TicTacToePlayer):

	def __init__(self, color):
		super().__init__(color, is_ai=False)

	def get_move(self, board):
		"""Takes in the user's input and returns the move"""
		spot = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (ROW_LABELS[-1], len(board))).strip().upper()
		erasePreviousLines(1)
		while True:
			if spot == 'Q':
				print("\nThanks for playing!\n")
				exit(0)
			elif spot == 'H':
				spot = get_board_history_input_from_user(False)
			elif spot == 'S':
				save_game(self.color)
				spot = input("Which spot would you like to play? (A1 - %s%d):\t" % (ROW_LABELS[-1], len(board))).strip().upper()
				erasePreviousLines(2)
			elif len(spot) >= 3 or len(spot) == 0 or spot[0] not in ROW_LABELS or not spot[1:].isdigit() or int(spot[1:]) > len(board) or int(spot[1:]) < 1:
				spot = input(f"{ERROR_SYMBOL} Invalid input. Please try again.\t").strip().upper()
				erasePreviousLines(1)
			elif board[ROW_LABELS.index(spot[0])][int(spot[1:]) - 1] != EMPTY:
				spot = input(f"{ERROR_SYMBOL} That spot is already taken, please choose another:\t").strip().upper()
				erasePreviousLines(1)
			else:
				break
		row = ROW_LABELS.index(spot[0])
		col = int(spot[1:]) - 1
		return row, col


def print_game_board(board=None):
	"""Prints the gameBoard in a human-readable format"""
	if board is None:
		board = gameBoard
	print()
	for rowNum in range(len(board)):
		row = board[rowNum]
		print("\t%s  " % ROW_LABELS[rowNum], end='')
		for colNum in range(len(row)):
			piece = board[rowNum][colNum]
			if piece == EMPTY:
				piece_color = NO_COLOR
			elif piece == USER_PIECE:
				piece_color = GREEN_COLOR
			else:
				piece_color = RED_COLOR
			print(f" {piece_color}%s{NO_COLOR} %s" % (piece, '|' if colNum < 2 else '\n'), end='')
		if rowNum < 2:
			print("\t   ---+---+---")
	print("\t    1   2   3\n")


def print_move_history(num_moves_previous):
	"""Prints the move history of the current game"""
	while True:
		print_game_board(BOARD_HISTORY[-(num_moves_previous + 1)])
		if num_moves_previous == 0:
			return
		print("(%d move%s before current board state)\n" % (num_moves_previous, "s" if num_moves_previous != 1 else ""))
		num_moves_previous -= 1
		user_input = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
		erasePreviousLines(1)
		if user_input == 'q':
			erasePreviousLines(2)
			print("Thanks for playing!\n")
			exit(0)
		elif user_input == 'e':
			erasePreviousLines(2)
			return
		else:
			erasePreviousLines(BOARD_OUTPUT_HEIGHT + 3)


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
			erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
			print_move_history(int(num_moves_previous))
			erasePreviousLines(BOARD_OUTPUT_HEIGHT + 1)
			print_game_board(BOARD_HISTORY[-1])
			user_input = input(f"{INFO_SYMBOL} You're back in play mode. {next_move_prompt}   ").strip().upper()
			erasePreviousLines(2)
			print("\n")  # make this output the same height as the other options
		else:
			user_input = input(f"{ERROR_SYMBOL} Invalid input. {next_move_prompt}   ").strip().upper()
			erasePreviousLines(1)
	return user_input


def save_game(turn):
	"""Saves the given board state to a save file"""
	if not allow_save(SAVE_FILENAME):
		return
	with open(SAVE_FILENAME, 'w') as save_file:
		save_file.write("This file contains the save state of a previously played game.\n")
		save_file.write("Modifying this file may cause issues with loading the save state.\n\n")
		time_of_save = datetime.now().strftime("%m/%d/%Y at %I:%M:%S %p")
		save_file.write(time_of_save + "\n\n")
		save_file.write("SAVE STATE:\n")
		for row in gameBoard:
			row_with_different_empty_character = row.copy()
			for index, piece in enumerate(row_with_different_empty_character):
				if piece == EMPTY:
					# replace EMPTY character with '-' so it can be parsed correctly when loading save
					row_with_different_empty_character[index] = "-"
			save_file.write(" ".join(row_with_different_empty_character) + "\n")
		save_file.write("User piece: " + str(USER_PIECE) + "\n")
		save_file.write("Opponent piece: " + opponent_of(USER_PIECE) + "\n")
		save_file.write("Turn: " + turn)
	info("The game has been saved!")


def validate_loaded_save_state(board, piece, turn):
	"""Make sure the state loaded from the save file is valid. Returns a boolean"""
	if piece not in [X_PIECE, O_PIECE]:
		error("Invalid user piece!")
		return False
	if turn not in [X_PIECE, O_PIECE]:
		error("Invalid player turn!")
		return False
	for row in board:
		if len(row) != 3:
			error("Invalid board!")
			return False
		if row.count(EMPTY) + row.count(X_PIECE) + row.count(O_PIECE) != 3:
			error("Board contains invalid pieces!")
			return False
	return True


def load_saved_game():
	"""Try to load the saved game data"""
	global gameBoard
	with open(SAVE_FILENAME, 'r') as saveFile:
		try:
			lines_from_save_file = saveFile.readlines()
			time_of_previous_save = lines_from_save_file[3].strip()
			use_existing_save = input(f"{INFO_SYMBOL} Would you like to load the saved game from {time_of_previous_save}? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			if use_existing_save != 'y':
				info("Starting a new game...\n")
				return None, None
			line_num = 0
			current_line = lines_from_save_file[line_num].strip()
			while current_line != "SAVE STATE:":
				line_num += 1
				current_line = lines_from_save_file[line_num].strip()
			line_num += 1
			current_line = lines_from_save_file[line_num].strip()
			board_from_save_file = []
			while not current_line.startswith("User piece"):
				pieces_in_row = current_line.split()
				for index, piece in enumerate(pieces_in_row):
					if piece == "-":
						pieces_in_row[index] = EMPTY
				board_from_save_file.append(pieces_in_row)
				line_num += 1
				current_line = lines_from_save_file[line_num].strip()
			user_piece = current_line.split(": ")[1].strip()
			line_num += 2
			current_line = lines_from_save_file[line_num].strip()
			turn = current_line.split(": ")[1].strip()
			if not validate_loaded_save_state(board_from_save_file, user_piece, turn):
				raise ValueError
			gameBoard = board_from_save_file
			delete_save_file = input(f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
			erasePreviousLines(1)
			file_deleted_text = ""
			if delete_save_file == 'y':
				os.remove(SAVE_FILENAME)
				file_deleted_text = "Save file deleted. "
			info(f"{file_deleted_text}Resuming saved game...\n")
			return turn, user_piece
		except Exception:
			error("There was an issue reading from the save file. Starting a new game...\n")
			return None, None


def run():
	"""main method that prompts the user for input"""
	global gameBoard, USER_PIECE
	players = {}
	if "-d" in sys.argv or "-aiDuel" in sys.argv:
		UserPlayerClass = get_dueling_ai_class(TicTacToePlayer, "TicTacToeStrategy")
		print(f"\n{INFO_SYMBOL} You are in AI Duel Mode!")
		ai_duel_mode = True
	else:
		UserPlayerClass = HumanPlayer
		ai_duel_mode = False
	print("""
  _______ _        _______           _______                    _____ 
 |__   __(_)      |__   __|         |__   __|             /\\   |_   _|
    | |   _  ___     | | __ _  ___     | | ___   ___     /  \\    | |  
    | |  | |/ __|    | |/ _` |/ __|    | |/ _ \\ / _ \\   / /\\ \\   | |  
    | |  | | (__     | | (_| | (__     | | (_) |  __/  / ____ \\ _| |_ 
    |_|  |_|\\___|    |_|\\__,_|\\___|    |_|\\___/ \\___| /_/    \\_\\_____|
                                                                      
                                                                      
		""")
	print("Type 's' at any prompt to save the game.")
	print("Type 'h' to see previous moves.")
	print("Press 'q' at any point to quit.")

	turn = X_PIECE
	use_saved_game = False
	if os.path.exists(SAVE_FILENAME):
		turn_from_save_file, USER_PIECE = load_saved_game()
		if turn_from_save_file is not None:
			turn = turn_from_save_file
			opponent_piece = opponent_of(USER_PIECE)
			use_saved_game = True
			BOARD_HISTORY.append(copy_of_board(gameBoard))
	if not use_saved_game:
		user_piece_select = input("\nDo you want to be X or O? (X goes first)\t").strip().lower()
		erasePreviousLines(1)
		while user_piece_select not in ['x', 'o']:
			if user_piece_select == 'q':
				print("Thanks for playing!\n")
				exit(0)
			user_piece_select = input(f"{ERROR_SYMBOL} Invalid input. Please choose either X or O:\t").strip().lower()
			erasePreviousLines(1)
		if user_piece_select == 'x':
			USER_PIECE = X_PIECE
			opponent_piece = O_PIECE
		else:
			USER_PIECE = O_PIECE
			opponent_piece = X_PIECE
	print(f"{'Your AI' if ai_duel_mode else 'Human'}: {color_text(USER_PIECE, GREEN_COLOR)}")
	print(f"{'My AI' if ai_duel_mode else 'AI'}: {color_text(opponent_piece, RED_COLOR)}")

	players[opponent_piece] = TicTacToeStrategy(opponent_piece)
	players[USER_PIECE] = UserPlayerClass(USER_PIECE)

	print_game_board()

	first_turn = True
	game_over, winner = False, None
	while not game_over:
		if ai_duel_mode:
			name_of_player = "My AI" if turn == opponent_piece else "Your AI"
		else:
			name_of_player = "AI" if turn == opponent_piece else "You"
		current_player = players[turn]
		if current_player.is_ai:
			user_input = input(f"{name_of_player}'s turn, press enter for it to play.\t").strip().upper()
			erasePreviousLines(1)
			while user_input in ['Q', 'S', 'H']:
				if user_input == 'Q':
					print("\nThanks for playing!\n")
					exit(0)
				elif user_input == 'H':
					user_input = get_board_history_input_from_user(True)
				else:
					save_game(turn)
					user_input = input(f"{name_of_player}'s turn, press enter for it to play.\t").strip().upper()
					erasePreviousLines(2)
		row_played, col_played = current_player.get_move(gameBoard)
		perform_move(gameBoard, row_played, col_played, turn)
		BOARD_HISTORY.append(copy_of_board(gameBoard))
		erasePreviousLines(BOARD_OUTPUT_HEIGHT + (1 if first_turn else 2))
		first_turn = False
		print_game_board()
		move_formatted = ROW_LABELS[row_played] + str(col_played + 1)
		print(f"{name_of_player} played in spot {move_formatted}")
		turn = opponent_of(turn)
		game_over, winner = is_terminal(gameBoard)

	if winner is None:
		print("Nobody wins, it's a tie!\n")
	else:
		highlight_color = GREEN_COLOR if winner == USER_PIECE else RED_COLOR
		print(f"{color_text(winner, highlight_color)} player wins!\n")
