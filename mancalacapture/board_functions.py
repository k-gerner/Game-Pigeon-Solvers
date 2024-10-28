# Contains board manipulation methods
from mancalacapture.constants import PLAYER1_BANK_INDEX, PLAYER2_BANK_INDEX, POCKETS_PER_SIDE, BOARD_SIZE
from util.terminaloutput.symbols import error


def push_all_pebbles_to_bank(board):
    """Called when one side of the board has 0 pebbles. Moves all pebbles to the corresponding bank"""
    player1_pebbles = 0
    for index, numPebbles in enumerate(board[:PLAYER1_BANK_INDEX]):
        player1_pebbles += numPebbles
        board[PLAYER1_BANK_INDEX - POCKETS_PER_SIDE + index] = 0
    board[PLAYER1_BANK_INDEX] += player1_pebbles
    player2_pebbles = 0
    for index, numPebbles in enumerate(board[PLAYER1_BANK_INDEX + 1: PLAYER2_BANK_INDEX]):
        player2_pebbles += numPebbles
        board[PLAYER2_BANK_INDEX - POCKETS_PER_SIDE + index] = 0
    board[PLAYER2_BANK_INDEX] += player2_pebbles


def is_board_terminal(board):
    """Checks if the board state represents games over"""
    return sum(board[:PLAYER1_BANK_INDEX]) == 0 or sum(board[PLAYER1_BANK_INDEX + 1: PLAYER2_BANK_INDEX]) == 0


def winning_player_bank_index(board):
    """Returns the bank index of the player with the most pebbles, or none if it's tied"""
    if board[PLAYER1_BANK_INDEX] > board[PLAYER2_BANK_INDEX]:
        return PLAYER1_BANK_INDEX
    elif board[PLAYER1_BANK_INDEX] < board[PLAYER2_BANK_INDEX]:
        return PLAYER2_BANK_INDEX
    else:
        return None


def perform_move(board, move, bank_index):
    """Performs a given move on the board. Returns the index of the final pebble placed"""
    if bank_index < move:
        error("Chosen move is on the wrong side of the board!")
        exit(0)
    num_pebbles = board[move]
    board[move] = 0
    curr_index = move
    while num_pebbles > 0:
        curr_index = (curr_index + 1) % BOARD_SIZE
        if (curr_index + POCKETS_PER_SIDE + 1) % BOARD_SIZE == bank_index:
            # if curr_index is the opposing player's bank
            continue
        board[curr_index] += 1
        num_pebbles -= 1
    # check if final pebble landed in empty spot on the caller's side of the board
    if board[curr_index] == 1 and (bank_index - POCKETS_PER_SIDE <= curr_index < bank_index) and board[get_index_of_opposite_hole(curr_index)] > 0:
        opposite_hole_index = get_index_of_opposite_hole(curr_index)
        board[bank_index] += board[opposite_hole_index] + board[curr_index]
        board[curr_index] = 0
        board[opposite_hole_index] = 0
    return curr_index


def get_index_of_opposite_hole(index):
    """Get the index of the hole on the opposite side of the board from the given index"""
    return (BOARD_SIZE - 2) - index


def get_valid_moves(board, player_bank_index):
    """Gets the indices of the valid moves for the player with the given bank index"""
    moves = []
    for index in range(player_bank_index - POCKETS_PER_SIDE, player_bank_index):
        if board[index] > 0:
            moves.append(index)
    return moves
