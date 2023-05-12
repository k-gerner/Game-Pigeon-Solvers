# Contains board manipulation methods
from constants import *


def pushAllPebblesToBank(board):
    """Called when one side of the board has 0 pebbles. Moves all pebbles to the corresponding bank"""
    player1Pebbles = 0
    for index, numPebbles in enumerate(board[:PLAYER1_BANK_INDEX]):
        player1Pebbles += numPebbles
        board[PLAYER1_BANK_INDEX - POCKETS_PER_SIDE + index] = 0
    board[PLAYER1_BANK_INDEX] += player1Pebbles
    player2Pebbles = 0
    for index, numPebbles in enumerate(board[PLAYER1_BANK_INDEX + 1 : PLAYER2_BANK_INDEX]):
        player2Pebbles += numPebbles
        board[PLAYER2_BANK_INDEX - POCKETS_PER_SIDE + index] = 0
    board[PLAYER2_BANK_INDEX] += player2Pebbles


def isBoardTerminal(board):
    """Checks if the board state represents games over"""
    return sum(board[:PLAYER1_BANK_INDEX]) == 0 or sum(board[PLAYER1_BANK_INDEX + 1 : PLAYER2_BANK_INDEX]) == 0


def winningPlayerBankIndex(board):
    """Returns the bank index of the player with the most pebbles, or none if it's tied"""
    if board[PLAYER1_BANK_INDEX] > board[PLAYER2_BANK_INDEX]:
        return PLAYER1_BANK_INDEX
    elif board[PLAYER1_BANK_INDEX] < board[PLAYER2_BANK_INDEX]:
        return PLAYER2_BANK_INDEX
    else:
        return None


def performMove(board, move, bankIndex):
    """Performs a given move on the board. Returns the index of the final pebble placed"""
    if bankIndex < move:
        print(f"{ERROR_SYMBOL} Chosen move is on the wrong side of the board!")
        exit(0)
    numPebbles = board[move]
    board[move] = 0
    currIndex = move
    while numPebbles > 0:
        currIndex = (currIndex + 1) % BOARD_SIZE
        if (currIndex + POCKETS_PER_SIDE + 1) % BOARD_SIZE == bankIndex:
            # if currIndex is the opposing player's bank
            continue
        board[currIndex] += 1
        numPebbles -= 1
    # check if final pebble landed in empty spot on the caller's side of the board
    if board[currIndex] == 1 and (bankIndex - POCKETS_PER_SIDE <= currIndex < bankIndex) and board[getIndexOfOppositeHole(currIndex)] > 0:
        oppositeHoleIndex = getIndexOfOppositeHole(currIndex)
        board[bankIndex] += board[oppositeHoleIndex] + board[currIndex]
        board[currIndex] = 0
        board[oppositeHoleIndex] = 0
    return currIndex


def getIndexOfOppositeHole(index):
    """Get the index of the hole on the opposite side of the board from the given index"""
    return (BOARD_SIZE - 2) - index


def getValidMoves(board, playerBankIndex):
    """Gets the indices of the valid moves for the player with the given bank index"""
    moves = []
    for index in range(playerBankIndex - POCKETS_PER_SIDE, playerBankIndex):
        if board[index] > 0:
            moves.append(index)
    return moves
