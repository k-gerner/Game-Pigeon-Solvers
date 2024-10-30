# Kyle Gerner
# Started 7.15.22
# Contains AI strategy and board manipulation methods
import math
from othello.othello_player import OthelloPlayer
from functools import cmp_to_key
from collections import defaultdict

# String representations of the board pieces
BLACK = "0"
WHITE = "O"
EMPTY = "."

##### MODIFIABLE #####
BOARD_DIMENSION = 8                 # Range: 4 to 26
MAX_DEPTH = 7                       # Recommended: 5 to 8
MAX_VALID_MOVES_TO_EVALUATE = 20    # Recommended: 12 to 20
######################

WIN_SCORE = 1000000000
CORNER_COORDINATES = {(0, 0), (0, BOARD_DIMENSION - 1), (BOARD_DIMENSION - 1, 0),
                      (BOARD_DIMENSION - 1, BOARD_DIMENSION - 1)}
CORNER_ADJACENT_COORDINATES = {(0, 1), (1, 1), (1, 0),
                               (0, BOARD_DIMENSION - 2), (1, BOARD_DIMENSION - 2), (1, BOARD_DIMENSION - 1),
                               (BOARD_DIMENSION - 2, 0), (BOARD_DIMENSION - 2, 1), (BOARD_DIMENSION - 1, 1),
                               (BOARD_DIMENSION - 1, BOARD_DIMENSION - 2),
                               (BOARD_DIMENSION - 2, BOARD_DIMENSION - 2),
                               (BOARD_DIMENSION - 2, BOARD_DIMENSION - 1)}


class OthelloStrategy(OthelloPlayer):
    """Where all the calculations are performed to find the best move"""

    def __init__(self, color):
        super().__init__(color)
        self.ai_color = color
        self.enemy_color = opponent_of(color)
        self.moves_played = 0
        self.num_boards_evaluated = 0
        self.positions_scores = {}
        self.build_position_scores_dictionary()

    def build_position_scores_dictionary(self):
        """Builds the dictionary that maps coordinate positions to scores"""
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                position_score = evaluate_position(row, col)
                self.positions_scores[(row, col)] = position_score

    def get_move(self, board):
        """Gets the best move for the AI on the given board"""
        self.moves_played = BOARD_DIMENSION ** 2 - number_of_piece_on_board(EMPTY, board)
        self.num_boards_evaluated = 0
        row, col = self.minimax(self.ai_color, -math.inf, math.inf, 0, board)[:2]
        return row, col

    def minimax(self, turn, alpha, beta, depth, board, no_move_for_opponent=False):
        """Recursively searches the move tree to find the best move. Prunes when optimal."""
        if depth == MAX_DEPTH or depth + self.moves_played == BOARD_DIMENSION ** 2:
            self.num_boards_evaluated += 1
            return -1, -1, self.evaluate_board(board, depth)
        valid_moves = get_valid_moves(turn, board)
        valid_moves.sort(key=validMoveSortKey)
        if len(valid_moves) > MAX_VALID_MOVES_TO_EVALUATE:
            # check a maximum of MAX_VALID_MOVES_TO_EVALUATE moves per board state
            valid_moves = valid_moves[:MAX_VALID_MOVES_TO_EVALUATE]
        if len(valid_moves) == 0:
            if no_move_for_opponent:
                self.num_boards_evaluated += 1
                return -1, -1, self.evaluate_board(board, BOARD_DIMENSION ** 2 - self.moves_played)
            return self.minimax(opponent_of(turn), alpha, beta, depth, board, no_move_for_opponent=True)
        if turn == self.ai_color:
            # maximize
            high_score = -math.inf
            best_row, best_col = valid_moves[0]
            for row, col in valid_moves:
                board_copy = copy_of_board(board)  # possible bottleneck
                play_move(turn, row, col, board_copy)
                _, __, score = self.minimax(opponent_of(turn), alpha, beta, depth + 1, board_copy)
                if score > high_score:
                    high_score = score
                    best_row = row
                    best_col = col
                alpha = max(alpha, high_score)
                if alpha >= beta:
                    break
            return best_row, best_col, high_score
        else:
            # minimize
            low_score = math.inf
            best_row, best_col = valid_moves[0]
            for row, col in valid_moves:
                board_copy = copy_of_board(board)  # possible bottleneck
                play_move(turn, row, col, board_copy)
                _, __, score = self.minimax(opponent_of(turn), alpha, beta, depth + 1, board_copy)
                if score < low_score:
                    low_score = score
                    best_row = row
                    best_col = col
                beta = min(beta, low_score)
                if beta <= alpha:
                    break
            return best_row, best_col, low_score

    def evaluate_board(self, board, additional_pieces_played):
        """Assigns a value to the board state based on how good it is for the AI"""
        spots_remaining = BOARD_DIMENSION**2 - (additional_pieces_played + self.moves_played)
        if spots_remaining == 0:
            ai_score, human_score = current_score(self.ai_color, board)
            if ai_score > human_score:
                return WIN_SCORE
            elif ai_score < human_score:
                return -WIN_SCORE
            else:
                return 0

        scores = defaultdict(int)
        num_occurrences = defaultdict(int)
        for rowIndex in range(BOARD_DIMENSION):
            for colIndex in range(BOARD_DIMENSION):
                piece = board[rowIndex][colIndex]
                score = self.positions_scores[(rowIndex, colIndex)]
                scores[piece] += score
                num_occurrences[piece] += 1

        scores[self.ai_color] += evaluate_board_by_filled_rows(board, self.ai_color)
        scores[self.enemy_color] += evaluate_board_by_filled_rows(board, self.enemy_color)
        if spots_remaining <= 15:
            scores[self.ai_color] *= (1 + (num_occurrences[self.ai_color]/(spots_remaining*25)))
            scores[self.enemy_color] *= (1 + (num_occurrences[self.enemy_color]/(spots_remaining*25)))
        return scores[self.ai_color] - scores[self.enemy_color]


def copy_of_board(board):
    """Returns a copy of the given board"""
    return list(map(list, board))  # use numpy if this becomes bottleneck


def evaluate_position(row, col):
    """Gets the score of a position on the board"""
    move = row, col
    if move in CORNER_COORDINATES:
        return 10
    elif move in CORNER_ADJACENT_COORDINATES:
        return -8
    elif row in [0, BOARD_DIMENSION - 1] or col in [0, BOARD_DIMENSION - 1]:
        # on outer border
        return 6
    elif row in [1, BOARD_DIMENSION - 2] or col in [1, BOARD_DIMENSION - 2]:
        # one space inside of outer border
        return -7
    else:
        return 0


def evaluate_board_by_filled_rows(board, color):
    """
    Evaluates all the stretches of length BOARD_DIMENSION (rows, columns, and the two longest diagonals), as
    it is very beneficial to have long stretches of friendly pieces in the same row/column/diagonal
    """
    score = 0
    # evaluate each row to see if any of them are completely filled or almost completely filled
    for row in board:
        non_friendly_count = BOARD_DIMENSION - row.count(color)
        if non_friendly_count == 0:
            score += 17
        elif non_friendly_count == 1:
            score += 8

    # evaluate each column
    for colNum in range(BOARD_DIMENSION):
        non_friendly_count = 0
        for rowNum in range(BOARD_DIMENSION):
            if board[rowNum][colNum] != color:
                non_friendly_count += 1
                if non_friendly_count >= 2:
                    break
        if non_friendly_count == 0:
            score += 17
        elif non_friendly_count == 1:
            score += 8

    # evaluate top left to bottom right diagonal
    non_friendly_count = 0
    for index in range(BOARD_DIMENSION):
        if board[index][index] != color:
            non_friendly_count += 1
            if non_friendly_count >= 2:
                break
    if non_friendly_count == 0:
        score += 25
    elif non_friendly_count == 1:
        score += 16

    # evaluate top right to bottom left diagonal
    non_friendly_count = 0
    for index in range(BOARD_DIMENSION):
        if board[index][BOARD_DIMENSION - index - 1] != color:
            non_friendly_count += 1
            if non_friendly_count >= 2:
                break
    if non_friendly_count == 0:
        score += 25
    elif non_friendly_count == 1:
        score += 16

    return score


def valid_moves_comparator(move1, move2):
    """
    Defines a way to sort two possible moves.
    Penalizes corner-adjacent moves
    Prioritizes corners first, then edge pieces (unless corner adjacent)
    """
    move1_score = evaluate_position(move1[0], move1[1])
    move2_score = evaluate_position(move2[0], move2[1])
    if move1_score > move2_score:
        return -1
    elif move1_score < move2_score:
        return 1
    else:
        return 0


def piece_at(row, col, board):
    """Gets the piece at the given coordinate"""
    return board[row][col]


def opponent_of(piece):
    """Gets the string representation of the opposing piece"""
    if piece == BLACK:
        return WHITE
    elif piece == WHITE:
        return BLACK
    else:
        raise ValueError(f"Invalid value passed to opponentOf({piece})")


def number_of_piece_on_board(piece, board):
    """Gets the number of the given piece that are on the board"""
    count = 0
    for row in board:
        count += row.count(piece)
    return count


def current_score(user_piece, board):
    """Gets the score of the game, returning {userPiece}'s score in [0] and opposing score in [1]"""
    enemy = opponent_of(user_piece)
    score, enemy_score = 0, 0
    for row in board:
        for spot in row:
            if spot == user_piece:
                score += 1
            elif spot == enemy:
                enemy_score += 1
    return score, enemy_score


def is_move_in_range(row, col):
    """Checks if the given coordinates are in range of the board"""
    return 0 <= row < BOARD_DIMENSION and 0 <= col < BOARD_DIMENSION


def is_move_valid(piece, row, col, board, confirmed_in_range=False):
    """Determines if a move is valid for the given color"""
    if not confirmed_in_range and not is_move_in_range(row, col) or board[row][col] != EMPTY:
        return False
    for rowIncrement in [-1, 0, 1]:
        for colIncrement in [-1, 0, 1]:
            if rowIncrement == colIncrement == 0:
                continue
            row_to_check = row + rowIncrement
            col_to_check = col + colIncrement
            seen_enemy_piece = False
            while is_move_in_range(row_to_check, col_to_check) \
                    and board[row_to_check][col_to_check] == opponent_of(piece):
                seen_enemy_piece = True
                row_to_check += rowIncrement
                col_to_check += colIncrement
            if seen_enemy_piece and is_move_in_range(row_to_check, col_to_check) \
                    and board[row_to_check][col_to_check] == piece:
                return True
    return False


def has_valid_moves(piece, board):
    """Checks if the given color has any available moves"""
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if is_move_valid(piece, row, col, board, confirmed_in_range=True):
                return True
    return False


def get_valid_moves(piece, board):
    """Gets a list of coordinates [row ,col] of valid moves for the given color"""
    valid_moves = []
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if is_move_valid(piece, row, col, board, confirmed_in_range=True):
                valid_moves.append([row, col])
    return valid_moves


def play_move(piece, row, col, board):
    """Adds a piece to the board and flips all the captured pieces"""
    if is_move_in_range(row, col) and board[row][col] == EMPTY:
        board[row][col] = piece
        convert_captured_pieces(piece, row, col, board)
    else:
        raise ValueError(f"{piece} tried to play in invalid spot ({row}, {col})!")


def convert_captured_pieces(piece, row, col, board):
    """Converts the captured opposing pieces to the given color"""
    for rowIncrement in [-1, 0, 1]:
        for colIncrement in [-1, 0, 1]:
            if rowIncrement == colIncrement == 0:
                continue
            row_to_eval = row + rowIncrement
            col_to_eval = col + colIncrement
            enemy_piece_coordinates = []
            while True:
                if not is_move_in_range(row_to_eval, col_to_eval) or board[row_to_eval][col_to_eval] == EMPTY:
                    enemy_piece_coordinates.clear()
                    break
                elif board[row_to_eval][col_to_eval] == piece:
                    break
                enemy_piece_coordinates.append([row_to_eval, col_to_eval])
                row_to_eval += rowIncrement
                col_to_eval += colIncrement
            for r, c in enemy_piece_coordinates:
                board[r][c] = piece


def check_game_over(board):
    """Checks if all spaces on the board are filled"""
    black_count, white_count = 0, 0
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            piece = piece_at(row, col, board)
            if piece == EMPTY:
                return False, None
            elif piece == BLACK:
                black_count += 1
            else:
                white_count += 1

    if black_count > white_count:
        return True, BLACK
    elif white_count > black_count:
        return True, WHITE
    else:
        return True, None


# sets the sorting key for valid move comparisons
validMoveSortKey = cmp_to_key(valid_moves_comparator)
