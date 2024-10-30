# Kyle Gerner
# Started 7.15.22
# Othello AI, client facing
import os
import sys
import time
from datetime import datetime
from util.terminaloutput.colors import NO_COLOR, YELLOW_COLOR, GREEN_COLOR, BLUE_COLOR, RED_COLOR, ORANGE_COLOR, \
    DARK_GREY_BACKGROUND as HIGHLIGHT
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL, error, info
from util.terminaloutput.erasing import erase_previous_lines
from util.save.saving import path_to_save_file, allow_save
from util.aiduel.dueling import get_dueling_ai_class

from othello.othello_strategy import OthelloStrategy, copy_of_board, BOARD_DIMENSION, get_valid_moves, opponent_of, \
    play_move, current_score, check_game_over, number_of_piece_on_board, piece_at, has_valid_moves, is_move_valid, is_move_in_range
from othello.othello_player import OthelloPlayer

BLACK = "0"
WHITE = "O"
EMPTY = "."

# Escape sequences for terminal color output

# Miscellaneous
COLUMN_LABELS = list(map(chr, range(65, 65 + BOARD_DIMENSION)))
BOARD_OUTLINE_HEIGHT = 4
SAVE_FILENAME = path_to_save_file("othello_save.txt")
TIME_TAKEN_PER_PLAYER = {}
USER_COLOR = GREEN_COLOR
AI_COLOR = RED_COLOR

# Relevant to game state
BOARD = []
BOARD_HISTORY = []
USER_PIECE = BLACK      # may be changed in game setup
OPPONENT_PIECE = WHITE  # may be changed in game setup

# class for the Human player
class HumanPlayer(OthelloPlayer):

    def __init__(self, color):
        super().__init__(color, is_ai=False)

    def get_move(self, board):
        """Takes in the user's input and returns the move"""
        coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
            COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
        erase_previous_lines(1)
        lines_written_to_console = BOARD_DIMENSION + 6
        while True:
            if coord == 'Q':
                end_game()
            elif coord == 'S':
                save_game(board, self.color)
                coord = input("It's your turn, which spot would you like to play? (A1 - %s%d):\t" % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
                erase_previous_lines(2)
            elif coord == 'QS' or coord == 'SQ':
                save_game(board, self.color)
                end_game()
            elif coord == 'H':
                coord, lines_written_to_console = get_board_history_input_from_user(board, self.color, False, lines_written_to_console)
            elif len(coord) in ([2] if BOARD_DIMENSION < 10 else [2, 3]) and coord[0] in COLUMN_LABELS and \
                    coord[1:].isdigit() and int(coord[1:]) in range(1, BOARD_DIMENSION + 1):
                row, col = int(coord[1]) - 1, COLUMN_LABELS.index(coord[0])
                if is_move_valid(self.color, row, col, board):
                    erase_previous_lines(lines_written_to_console)
                    print_board()
                    print("\n")
                    return row, col
                elif is_move_in_range(row, col) and piece_at(row, col, board) != EMPTY:
                    coord = input(
                        f"{ERROR_SYMBOL} That spot is already taken! Please choose a different spot:   ").strip().upper()
                    erase_previous_lines(1)
                else:
                    coord = input(f"{ERROR_SYMBOL} Please choose one of the highlighted spaces:   ").strip().upper()
                    erase_previous_lines(1)
            else:
                coord = input(f"{ERROR_SYMBOL} Please enter a valid move (A1 - %s%d):   " % (
                    COLUMN_LABELS[-1], BOARD_DIMENSION)).strip().upper()
                erase_previous_lines(1)


def print_board(highlighted_coordinates=None, board=None):
    """Prints the gameBoard in a human-readable format"""
    if highlighted_coordinates is None:
        highlighted_coordinates = []
    if board is None:
        board = BOARD
    print("\n\t    %s" % " ".join(COLUMN_LABELS))
    for row_num in range(BOARD_DIMENSION):
        print("\t%d%s| " % (row_num + 1, "" if row_num > 8 else " "), end='')
        for col_num in range(BOARD_DIMENSION):
            piece = piece_at(row_num, col_num, board)
            piece_color = HIGHLIGHT if [row_num, col_num] in highlighted_coordinates else ''
            piece_color += text_color_of(piece)
            print(f"{piece_color}%s{NO_COLOR} " % piece, end='')
        if row_num == BOARD_DIMENSION // 2:
            moves_remaining = number_of_piece_on_board(EMPTY, board)
            if moves_remaining <= 5:
                moves_remaining_color = ORANGE_COLOR
            elif moves_remaining <= 10:
                moves_remaining_color = YELLOW_COLOR
            else:
                moves_remaining_color = NO_COLOR
            print(f"   {moves_remaining_color}{moves_remaining} turn{'' if moves_remaining == 1 else 's'} remain{'s' if moves_remaining == 1 else ''}.{NO_COLOR}", end='')
        print()
    user_score, ai_score = current_score(USER_PIECE, board)
    additional_indent = " " * ((2 + (2 * (BOARD_DIMENSION // 2 - 1))) - (1 if user_score >= 10 else 0))
    print(f"\t{additional_indent}{USER_COLOR}{user_score}{NO_COLOR} to {AI_COLOR}{ai_score}{NO_COLOR}\n")


def print_move_history(num_moves_previous):
    """Prints the move history of the current game"""
    while True:
        print_board(BOARD_HISTORY[-(num_moves_previous + 1)][0], BOARD_HISTORY[-(num_moves_previous + 1)][1])
        if num_moves_previous == 0:
            return
        print("(%d move%s before current board state)" % (num_moves_previous, "s" if num_moves_previous != 1 else ""))
        num_moves_previous -= 1
        user_input = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
        if user_input == 'q':
            end_game()
        elif user_input == 'e':
            erase_previous_lines(2)
            return
        else:
            erase_previous_lines(BOARD_DIMENSION + BOARD_OUTLINE_HEIGHT + 2)


def get_board_history_input_from_user(board, turn, is_ai, lines_written_to_console):
    """
    Prompts the user for input for how far the board history function.
    Returns the user's input for the next move, and the new value for linesWrittenToConsole
    """
    next_move_prompt = "Press enter to continue." if is_ai else "Enter a valid move to play:"
    if len(BOARD_HISTORY) < 2:
        user_input = input(f"No previous moves to see. {next_move_prompt}   ").strip().upper()
        erase_previous_lines(1)
    else:
        num_moves_previous = input(f"How many moves ago do you want to see? (1 to {len(BOARD_HISTORY) - 1})  ").strip()
        if num_moves_previous.isdigit() and 1 <= int(num_moves_previous) <= len(BOARD_HISTORY) - 1:
            lines_written_to_console += 1
            erase_previous_lines(lines_written_to_console)
            print_move_history(int(num_moves_previous))
            erase_previous_lines(BOARD_DIMENSION + BOARD_OUTLINE_HEIGHT)
            print_board(get_valid_moves(turn, board))
            user_input = input(f"{INFO_SYMBOL} You're back in play mode. {next_move_prompt}   ").strip().upper()
            erase_previous_lines(1)
            lines_written_to_console = BOARD_DIMENSION + 4
        else:
            user_input = input(f"{ERROR_SYMBOL} Invalid input. {next_move_prompt}   ").strip().upper()
            erase_previous_lines(2)
    return user_input, lines_written_to_console


def text_color_of(piece):
    """Gets the text color of the given piece, or an empty string if no piece given"""
    if piece == USER_PIECE:
        return USER_COLOR
    elif piece == OPPONENT_PIECE:
        return AI_COLOR
    else:
        return ""


def name_of_piece_color(piece):
    """Gets the name of the color of the given piece"""
    if piece == BLACK:
        return "BLACK"
    elif piece == WHITE:
        return "WHITE"
    else:
        return "EMPTY"


def end_game(winner=None):
    """Ends the game"""
    if winner:
        text_color = text_color_of(winner)
        color_name = name_of_piece_color(winner)
        print(f"\n{text_color}{color_name}{NO_COLOR} wins!\n")
    else:
        print("\nThe game ended in a draw!\n")
    user_time_taken = round(TIME_TAKEN_PER_PLAYER[USER_PIECE][1]/max(1, TIME_TAKEN_PER_PLAYER[USER_PIECE][2]), 2)
    ai_time_taken = round(TIME_TAKEN_PER_PLAYER[OPPONENT_PIECE][1]/max(1, TIME_TAKEN_PER_PLAYER[OPPONENT_PIECE][2]), 2)
    print("Average time taken per move:")
    print(f"{USER_COLOR}{TIME_TAKEN_PER_PLAYER[USER_PIECE][0]}{NO_COLOR}: {user_time_taken}s")
    print(f"{AI_COLOR}{TIME_TAKEN_PER_PLAYER[OPPONENT_PIECE][0]}{NO_COLOR}: {ai_time_taken}s")
    print("\nThanks for playing!")
    exit(0)


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
        save_file.write(f"User piece: " + USER_PIECE + "\n")
        save_file.write("Opponent piece: " + OPPONENT_PIECE + "\n")
        save_file.write("Turn: " + turn)
    info(f"The game has been saved!")


def print_game_rules():
    """Gives the user the option to view the rules of the game"""
    print("\nType 'q' at any move prompt to quit the game.")
    print("Type 's' save the game.")
    print("Type 'h' to see previous moves.")
    print("AI constants are modifiable in the othello_strategy.py file.")
    show_rules = input("Would you like to see the rules? (y/n)   ").strip().lower()
    erase_previous_lines(1)
    if show_rules == 'q':
        print("\nThanks for playing!")
        exit(0)
    elif show_rules == 'y':
        print("""
    - OBJECTIVE: Have more pieces on the board than the opponent when all spaces are full
    - TURNS: Black will go first. Each player will take turns placing one piece each turn
    - GAMEPLAY: Trap enemy pieces between two friendly pieces to convert them to friendly pieces
        """)


def print_ascii_title_art():
    """Prints the fancy text when you start the program"""
    print("""
             _  __     _      _
            | |/ /    | |    ( )
            | ' /_   _| | ___|/ ___
            |  <| | | | |/ _ \ / __|
            | . \ |_| | |  __/ \__ \\
            |_|\_\__, |_|\___| |___/
 _____  _   _     __/ |_ _                  _____
/  __ \\| | | |   |___/| | |           /\\   |_   _|
| |  | | |_| |__   ___| | | ___      /  \\    | |
| |  | | __| '_ \\ / _ \\ | |/ _ \\    / /\\ \\   | |
| |__| | |_| | | |  __/ | | (_) |  / ____ \\ _| |_
\\_____/ \\__|_| |_|\\___|_|_|\\___/  /_/    \\_\\_____|
    """)


def load_saved_game():
    """Try to load the saved game data"""
    with open(SAVE_FILENAME, 'r') as saveFile:
        try:
            lines_from_save_file = saveFile.readlines()
            time_of_previous_save = lines_from_save_file[3].strip()
            use_existing_save = input(f"{INFO_SYMBOL} Would you like to load the saved game from {time_of_previous_save}? (y/n)\t").strip().lower()
            erase_previous_lines(1)
            if use_existing_save != 'y':
                info(f"Starting a new game...")
                return None, None, None
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
            delete_save_file = input(f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
            erase_previous_lines(1)
            file_deleted_text = ""
            if delete_save_file == 'y':
                os.remove(SAVE_FILENAME)
                file_deleted_text = "Save file deleted. "
            info(f"{file_deleted_text}Resuming saved game...")
            return board, user_piece, turn
        except Exception:
            error(f"There was an issue reading from the save file. Starting a new game...")
            return None, None, None


def validate_loaded_save_state(board, piece, turn):
    """Make sure the state loaded from the save file is valid. Returns a boolean"""
    if len(board) != BOARD_DIMENSION:
        error(f"Board dimension does not match!")
        return False
    if piece not in [BLACK, WHITE]:
        error(f"Invalid user piece!")
        return False
    if turn not in [BLACK, WHITE]:
        error(f"Invalid player turn!")
        return False
    board_dimension = len(board)
    for row in board:
        if len(row) != board_dimension:
            error(f"Board is not square!")
            return False
        if row.count(EMPTY) + row.count(BLACK) + row.count(WHITE) != board_dimension:
            error(f"Board contains invalid pieces!")
            return False
    return True


def get_user_piece_color_input():
    """Gets input from the user to determine which color they will be"""
    color_input = input("Would you like to be BLACK ('b') or WHITE ('w')?   ").strip().lower()
    erase_previous_lines(1)
    color = BLACK if color_input == 'b' else WHITE
    if color == BLACK:
        print(f"You will be BLACK {USER_COLOR}{BLACK}{NO_COLOR}!")
    else:
        print(f"You will be WHITE {USER_COLOR}{WHITE}{NO_COLOR}!")
    print(f"Your pieces are shown in {USER_COLOR}%s{NO_COLOR}!" % (
        "blue" if USER_COLOR == BLUE_COLOR else "green"))
    print(f"Enemy pieces are shown in {AI_COLOR}%s{NO_COLOR}!" % (
        "orange" if AI_COLOR == ORANGE_COLOR else "red"))
    return color


def create_new_board():
    """Creates the initial game board state"""
    board = [[EMPTY for _ in range(BOARD_DIMENSION)] for __ in range(BOARD_DIMENSION)]
    board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2 - 1] = WHITE
    board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2] = WHITE
    board[BOARD_DIMENSION // 2][BOARD_DIMENSION // 2] = BLACK
    board[BOARD_DIMENSION // 2 - 1][BOARD_DIMENSION // 2 - 1] = BLACK
    return board


def run():
    global BOARD, USER_PIECE, OPPONENT_PIECE, TIME_TAKEN_PER_PLAYER
    if "-cb" in sys.argv or "-colorblindMode" in sys.argv:
        global AI_COLOR, USER_COLOR
        AI_COLOR = ORANGE_COLOR
        USER_COLOR = BLUE_COLOR
    if "-d" in sys.argv or "-aiDuel" in sys.argv:
        UserPlayerClass = get_dueling_ai_class(OthelloPlayer, "OthelloStrategy")
        print()
        info("You are in AI Duel Mode!")
        ai_duel_mode = True
    else:
        UserPlayerClass = HumanPlayer
        ai_duel_mode = False

    print_ascii_title_art()
    print_game_rules()

    use_saved_game = False
    if os.path.exists(SAVE_FILENAME):
        BOARD, USER_PIECE, turn = load_saved_game()
        if turn is not None:
            use_saved_game = True
    if not use_saved_game:
        USER_PIECE = get_user_piece_color_input()
        BOARD = create_new_board()
        turn = BLACK
    BOARD_HISTORY.append([[], copy_of_board(BOARD)])
    OPPONENT_PIECE = opponent_of(USER_PIECE)
    user_player_name = "Your AI" if ai_duel_mode else "You"
    ai_player_name = "My AI" if ai_duel_mode else "AI"
    player_names = {USER_PIECE: user_player_name, OPPONENT_PIECE: ai_player_name}
    players = {
        USER_PIECE: UserPlayerClass(USER_PIECE),
        OPPONENT_PIECE: OthelloStrategy(OPPONENT_PIECE)
    }
    TIME_TAKEN_PER_PLAYER = {
        USER_PIECE: [user_player_name, 0, 0],    # [player name, total time, num moves]
        OPPONENT_PIECE: [ai_player_name, 0, 0]
    }

    print_board(get_valid_moves(turn, BOARD))
    print("\n")

    num_valid_moves_in_a_row = 0
    game_over, winner = False, None
    while not game_over:
        lines_written_to_console = BOARD_DIMENSION + 6
        if has_valid_moves(turn, BOARD):
            num_valid_moves_in_a_row = 0
            name_of_current_player = player_names[turn]
            current_player = players[turn]
            if current_player.is_ai:
                user_input = input(f"{name_of_current_player}'s turn, press enter for it to play.\t").strip().upper()
                erase_previous_lines(1)
                while user_input in ['Q', 'S', 'QS', 'SQ', 'H']:
                    if user_input == 'Q':
                        end_game()
                    elif user_input == 'S':
                        save_game(BOARD, turn)
                        user_input = input("Press enter to continue. ").strip().upper()
                        erase_previous_lines(2)
                    elif user_input == 'QS' or user_input == 'SQ':
                        save_game(BOARD, turn)
                        end_game()
                    elif user_input == 'H':
                        user_input, lines_written_to_console = get_board_history_input_from_user(BOARD, turn, True, lines_written_to_console)
            start_time = time.time()
            row, col = current_player.get_move(BOARD)
            end_time = time.time()
            time_to_play_move = (end_time - start_time)
            TIME_TAKEN_PER_PLAYER[turn][1] += time_to_play_move
            TIME_TAKEN_PER_PLAYER[turn][2] += 1
            time_to_play_move = round(time_to_play_move, 2)
            play_move(turn, row, col, BOARD)
            BOARD_HISTORY.append([[[row, col]], copy_of_board(BOARD)])
            erase_previous_lines(lines_written_to_console)
            print_board([[row, col]] + get_valid_moves(opponent_of(turn), BOARD))
            if current_player.is_ai:
                additional_output = "  (%0.2f sec" % time_to_play_move
                if hasattr(current_player, 'numBoardsEvaluated'):
                    additional_output += ", %d possible futures)" % current_player.numBoardsEvaluated
                else:
                    additional_output += ")"
            else:
                additional_output = ""
            move_output_formatted = COLUMN_LABELS[col] + str(row + 1)
            print(f"{name_of_current_player} played in spot {move_output_formatted}{additional_output}\n")

        else:
            num_valid_moves_in_a_row += 1
            if num_valid_moves_in_a_row == 2:
                print("Neither player has any valid moves left!")
                user_score, ai_score = current_score(USER_PIECE, BOARD)
                if user_score > ai_score:
                    end_game(USER_PIECE)
                elif ai_score > user_score:
                    end_game(OPPONENT_PIECE)
                else:
                    end_game()
            no_valid_moves_color = text_color_of(turn)
            play_again_color = text_color_of(opponent_of(turn))
            erase_previous_lines(2)
            info_text = f"{no_valid_moves_color}{name_of_piece_color(turn)}{NO_COLOR} " \
                        f"has no valid moves this turn! " \
                        f"{play_again_color}{name_of_piece_color(opponent_of(turn))}{NO_COLOR} will play again.\n"
            info(info_text)
        game_over, winner = check_game_over(BOARD)
        turn = opponent_of(turn)
    end_game(winner)
