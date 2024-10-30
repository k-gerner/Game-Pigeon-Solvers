# Kyle Gerner 
# Started 3.18.21
# Connect 4 Solver, client facing
import os
import sys
import time
from util.terminaloutput.colors import YELLOW_COLOR, RED_COLOR, BLUE_COLOR, GREEN_COLOR, NO_COLOR, GREY_COLOR, color_text
from util.terminaloutput.erasing import erase_previous_lines
from util.terminaloutput.symbols import ERROR_SYMBOL, INFO_SYMBOL, error, info
from util.save.saving import path_to_save_file, allow_save
from util.aiduel.dueling import get_dueling_ai_class
from datetime import datetime
from connect4.connect4_player import Connect4Player
from connect4.connect4_strategy import Connect4Strategy, opponent_of, perform_move, check_if_game_over, is_valid_move, \
    copy_of_board

BOARD_OUTPUT_HEIGHT = 9

SAVE_FILENAME = path_to_save_file("connect4_save.txt")
BOARD_HISTORY = []  # [board, highlightCoordinates]

EMPTY, RED, YELLOW = '.', 'o', '@'
game_board = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],  # bottom row
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]]  # top row
user_piece = YELLOW
TIME_TAKEN_PER_PLAYER = {}


# class for the Human player
class HumanPlayer(Connect4Player):

    def __init__(self, color):
        super().__init__(color, is_ai=False)

    def get_move(self, board):
        """Takes in the user's input and returns the move"""
        col = input("It's your turn, which column would you like to play? (1-7):\t").strip().lower()
        erase_previous_lines(1)
        while True:
            if col == 'q':
                end_game()
            elif col == 'h':
                col = get_board_history_input_from_user(is_ai=False)
            elif col == 's':
                save_game(self.color)
                col = input("Which column would you like to play? (1-7):\t").strip().lower()
                erase_previous_lines(2)
            elif not col.isdigit() or int(col) not in range(1, 8):
                col = input(f"{ERROR_SYMBOL} Invalid input. Please enter a number 1 through 7:\t")
                erase_previous_lines(1)
            elif not is_valid_move(game_board, int(col) - 1):
                col = input(f"{ERROR_SYMBOL} That column is full, please choose another:\t")
                erase_previous_lines(1)
            else:
                break
        erase_previous_lines(1)
        return int(col) - 1


def get_highlight_color_for_piece(piece):
    """Gets the color highlight color for a given piece"""
    if piece == RED:
        return RED_COLOR
    elif piece == YELLOW:
        return YELLOW_COLOR
    else:
        return NO_COLOR


def print_board(board, recent_move=None):
    """Prints the given game board"""
    column_color = NO_COLOR
    print("\n   ", end='')
    for i in range(7):
        if i == recent_move:
            column_color = GREEN_COLOR
        elif not is_valid_move(board, i):
            column_color = GREY_COLOR
        print(f"{column_color}{i+1}{NO_COLOR} ", end='')
        column_color = NO_COLOR
    print()
    for row_num in range(len(board) - 1, -1, -1):
        print(f" {color_text('|', BLUE_COLOR)} ", end='')
        for spot in board[row_num]:
            piece_color = get_highlight_color_for_piece(spot)
            print(f"{color_text(spot, piece_color)} ", end='')
        print(color_text('|', BLUE_COLOR))
    print(" " + f"{BLUE_COLOR}%s{NO_COLOR}" % "-" * 17)


def print_move_history(num_moves_previous):
    """Prints the move history of the current game"""
    while True:
        print_board(BOARD_HISTORY[-(num_moves_previous + 1)][0], BOARD_HISTORY[-(num_moves_previous + 1)][1])
        if num_moves_previous == 0:
            return
        print("(%d move%s before current board state)\n" % (num_moves_previous, "s" if num_moves_previous != 1 else ""))
        num_moves_previous -= 1
        user_input = input("Press enter for next move, or 'e' to return to game.  ").strip().lower()
        erase_previous_lines(1)
        if user_input == 'q':
            erase_previous_lines(2)
            end_game()
        elif user_input == 'e':
            erase_previous_lines(2)
            return
        else:
            erase_previous_lines(BOARD_OUTPUT_HEIGHT + 2)


def get_board_history_input_from_user(is_ai):
    """
    Prompts the user for input for how far the board history function.
    Returns the user's input for the next move
    """
    next_move_prompt = "Press enter to continue." if is_ai else "Enter a valid move to play:"
    if len(BOARD_HISTORY) < 2:
        user_input = input(f"{INFO_SYMBOL} No previous moves to see. {next_move_prompt}   ").strip().lower()
        erase_previous_lines(1)
    else:
        num_moves_previous = input(f"How many moves ago do you want to see? (1 to {len(BOARD_HISTORY) - 1})  ").strip()
        erase_previous_lines(1)
        if num_moves_previous.isdigit() and 1 <= int(num_moves_previous) <= len(BOARD_HISTORY) - 1:
            erase_previous_lines(BOARD_OUTPUT_HEIGHT + 2)
            print_move_history(int(num_moves_previous))
            erase_previous_lines(BOARD_OUTPUT_HEIGHT)
            print_board(BOARD_HISTORY[-1][0], BOARD_HISTORY[-1][1])
            user_input = input(f"{INFO_SYMBOL} You're back in play mode. {next_move_prompt}   ").strip().lower()
            erase_previous_lines(1)
            print("\n")  # make this output the same height as the other options
        else:
            user_input = input(f"{ERROR_SYMBOL} Invalid input. {next_move_prompt}   ").strip().lower()
            erase_previous_lines(1)
    return user_input


def end_game():
    """Ends the game"""
    opponent_piece = opponent_of(user_piece)
    user_time_taken = round(TIME_TAKEN_PER_PLAYER[user_piece][1]/max(1, TIME_TAKEN_PER_PLAYER[user_piece][2]), 2)
    ai_time_taken = round(TIME_TAKEN_PER_PLAYER[opponent_piece][1]/max(1, TIME_TAKEN_PER_PLAYER[opponent_piece][2]), 2)
    print("Average time taken per move:")
    print(f"{color_text(str(TIME_TAKEN_PER_PLAYER[user_piece][0]), GREEN_COLOR)}: {user_time_taken}s")
    print(f"{color_text(str(TIME_TAKEN_PER_PLAYER[opponent_piece][0]), RED_COLOR)}: {ai_time_taken}s")
    print("\nThanks for playing!\n")
    exit(0)


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
        for row in game_board:
            save_file.write(" ".join(row) + "\n")
        save_file.write("User piece: " + str(user_piece) + "\n")
        save_file.write("Opponent piece: " + opponent_of(user_piece) + "\n")
        save_file.write("Turn: " + turn)
    info("The game has been saved!")


def validate_loaded_save_state(board, piece, turn):
    """Make sure the state loaded from the save file is valid. Returns a boolean"""
    if piece not in [RED, YELLOW]:
        error("Invalid user piece!")
        return False
    if turn not in [RED, YELLOW]:
        error("Invalid player turn!")
        return False
    for row in board:
        if len(row) != 7:
            error("Invalid board!")
            return False
        if row.count(EMPTY) + row.count(RED) + row.count(YELLOW) != 7:
            error("Board contains invalid pieces!")
            return False
    return True


def load_saved_game():
    """Try to load the saved game data"""
    global user_piece, game_board
    with open(SAVE_FILENAME, 'r') as saveFile:
        try:
            lines_from_save_file = saveFile.readlines()
            time_of_prev_save = lines_from_save_file[3].strip()
            use_existing_save = input(f"{INFO_SYMBOL} Would you like to load the saved game from {time_of_prev_save}? (y/n)\t").strip().lower()
            erase_previous_lines(1)
            if use_existing_save != 'y':
                info("Starting a new game...\n")
                return
            line_num = 0
            current_line = lines_from_save_file[line_num].strip()
            while current_line != "SAVE STATE:":
                line_num += 1
                current_line = lines_from_save_file[line_num].strip()
            line_num += 1
            current_line = lines_from_save_file[line_num].strip()
            board_from_save_file = []
            while not current_line.startswith("User piece"):
                board_from_save_file.append(current_line.split())
                line_num += 1
                current_line = lines_from_save_file[line_num].strip()
            user_piece = current_line.split(": ")[1].strip()
            line_num += 2
            current_line = lines_from_save_file[line_num].strip()
            turn = current_line.split(": ")[1].strip()
            if not validate_loaded_save_state(board_from_save_file, user_piece, turn):
                raise ValueError
            game_board = board_from_save_file
            delete_save_file = input(f"{INFO_SYMBOL} Saved game was successfully loaded! Delete the save file? (y/n)\t").strip().lower()
            erase_previous_lines(1)
            file_deleted_text = ""
            if delete_save_file == 'y':
                os.remove(SAVE_FILENAME)
                file_deleted_text = "Save file deleted. "
            info(f"{file_deleted_text}Resuming saved game...\n")
            return turn
        except Exception:
            error("There was an issue reading from the save file. Starting a new game...\n")
            return None


def print_ascii_title_art():
    """Prints the fancy text when you start the program"""
    print("""
   _____                            _     _  _   
  / ____|                          | |   | || |  
 | |     ___  _ __  _ __   ___  ___| |_  | || |_ 
 | |    / _ \| '_ \| '_ \ / _ \/ __| __| |__   _|
 | |___| (_) | | | | | | |  __/ (__| |_     | |  
  \_____\___/|_| |_|_| |_|\___|\___|\__|    |_|      
    """)


def run():
    """main method that prompts the user for input"""
    global user_piece, TIME_TAKEN_PER_PLAYER
    if "-d" in sys.argv or "-aiDuel" in sys.argv:
        UserPlayerClass = get_dueling_ai_class(Connect4Player, "Connect4Strategy")
        print()
        info("You are in AI Duel Mode!")
        ai_duel_mode = True
    else:
        UserPlayerClass = HumanPlayer
        ai_duel_mode = False
    print("\nWelcome to Kyle's Connect 4 AI!")
    print_ascii_title_art()
    user_player_name = "Your AI" if ai_duel_mode else "You"
    ai_player_name = "My AI" if ai_duel_mode else "AI"

    turn = YELLOW
    use_saved_game = False
    if os.path.exists(SAVE_FILENAME):
        turn_from_save_file = load_saved_game()
        if turn_from_save_file is not None:
            turn = turn_from_save_file
            opponent_piece = opponent_of(user_piece)
            use_saved_game = True
            BOARD_HISTORY.append([copy_of_board(game_board), None])
    if not use_saved_game:
        user_piece_input = input(
            "Would you like to be RED ('r') or YELLOW ('y')? (yellow goes first!):\t").strip().lower()
        erase_previous_lines(1)
        if user_piece_input == 'r':
            user_piece = RED
            opponent_piece = YELLOW
            print(f"{user_player_name} will be {RED_COLOR}RED{NO_COLOR}!")
        elif user_piece_input == 'y':
            user_piece = YELLOW
            opponent_piece = RED
            print(f"{user_player_name} will be {YELLOW_COLOR}YELLOW{NO_COLOR}!")
        else:
            user_piece = RED
            opponent_piece = YELLOW
            error(f"Invalid input. {user_player_name} will be {color_text('RED', RED_COLOR)}!")

    TIME_TAKEN_PER_PLAYER = {
        user_piece: [user_player_name, 0, 0],    # [player name, total time, num moves]
        opponent_piece: [ai_player_name, 0, 0]
    }
    user_highlight_color = get_highlight_color_for_piece(user_piece)
    opponent_highlight_color = get_highlight_color_for_piece(opponent_piece)
    print(f"{user_player_name}: {user_highlight_color}{user_piece}{NO_COLOR}\t{ai_player_name}: {opponent_highlight_color}{opponent_piece}{NO_COLOR}")
    player_names = {opponent_piece: ai_player_name, user_piece: user_player_name}
    players = {opponent_piece: Connect4Strategy(opponent_piece), user_piece: UserPlayerClass(user_piece)}
    game_over = False
    winning_piece = None
    print("Type 's' at any prompt to save the game.")
    print("Type 'h' to see previous moves.")
    print("Type 'q' at any prompt to quit.")
    print_board(game_board)
    print()
    first_turn = True
    while not game_over:
        name_of_current_player = player_names[turn]
        current_player = players[turn]
        if current_player.is_ai:
            user_input = input(f"{name_of_current_player}'s turn, press enter for it to play.\t").strip().lower()
            erase_previous_lines(1)
            while user_input in ['q', 's', 'h']:
                if user_input == 'q':
                    end_game()
                elif user_input == 'h':
                    user_input = get_board_history_input_from_user(is_ai=True)
                else:
                    save_game(current_player.color)
                    user_input = input(f"{name_of_current_player}'s turn, press enter for it to play.\t").strip().lower()
                    erase_previous_lines(2)

            erase_previous_lines(1)
        start_time = time.time()
        column = current_player.get_move(game_board)
        endTime = time.time()
        total_time_taken_for_move = endTime - start_time
        TIME_TAKEN_PER_PLAYER[turn][1] += total_time_taken_for_move
        TIME_TAKEN_PER_PLAYER[turn][2] += 1
        perform_move(game_board, column, turn)
        BOARD_HISTORY.append([copy_of_board(game_board), column])
        erase_previous_lines(BOARD_OUTPUT_HEIGHT + (0 if first_turn else 1))
        print_board(game_board, column)
        print(f"{name_of_current_player} played in spot {column + 1}\n")
        turn = opponent_of(turn)  # switch the turn
        first_turn = False
        game_over, winning_piece = check_if_game_over(game_board)

    if winning_piece is None:
        print("The game ended in a tie!\n")
    elif winning_piece == RED:
        print(f"{RED_COLOR}RED{NO_COLOR} wins!\n")
    else:
        print(f"{YELLOW_COLOR}YELLOW{NO_COLOR} wins!\n")
    end_game()
