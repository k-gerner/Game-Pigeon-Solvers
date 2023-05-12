import pygame
from typing import Tuple
from .constants import BLACK, WHITE, ROWS, COLS, SQUARE_SIZE, EMPTY_BORDER 
from .piece import Piece

class Board():
    '''GUI for the Tic Tac Toe board'''

    def __init__(self):
        '''Creates a Board object'''
        board = []
        # no pieces on board to start
        for row in range(ROWS):
            board.append([])
            for col in range(COLS):
                # if adding piece:
                    # board[row].append(Piece(row, col, player))
                # else:
                board[row].append(None) # empty
        self.board = board

    def draw_squares(self, window:pygame.Surface):
        '''Draws the board outline (#)'''
        # window.fill(BLACK)
        # for row in range(ROWS):
        #     for col in range(COLS):
        #         pygame.draw.rect(window, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE - 10, SQUARE_SIZE - 10)) 
        window.fill(WHITE)
        pygame.draw.line(window, BLACK, (EMPTY_BORDER, SQUARE_SIZE + EMPTY_BORDER), (3 * SQUARE_SIZE + EMPTY_BORDER, SQUARE_SIZE + EMPTY_BORDER), width=10)
        pygame.draw.line(window, BLACK, (EMPTY_BORDER, 2 * SQUARE_SIZE + EMPTY_BORDER), (3 * SQUARE_SIZE + EMPTY_BORDER, 2 * SQUARE_SIZE + EMPTY_BORDER), width=10)
        pygame.draw.line(window, BLACK, (SQUARE_SIZE + EMPTY_BORDER, EMPTY_BORDER), (SQUARE_SIZE + EMPTY_BORDER, 3 * SQUARE_SIZE + EMPTY_BORDER), width=10)
        pygame.draw.line(window, BLACK, (2 * SQUARE_SIZE + EMPTY_BORDER, EMPTY_BORDER), (2 * SQUARE_SIZE + EMPTY_BORDER, 3 * SQUARE_SIZE + EMPTY_BORDER), width=10)


    def draw(self, window:pygame.Surface):
        '''Draws the board and the pieces on it'''
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != None:
                    piece.draw(window)

    def get_piece(self, row:int, col:int):
        '''Get what piece is at a row/column on the board'''
        return self.board[row][col]

    def play_move(self, row:int, col:int, player:str):
        '''Adds a piece to the board at the specified row and column'''
        piece = Piece(row, col, player)
        self.board[row][col] = piece 

        # if gameOver:
        #   draw line through winning pieces

    def draw_winner(self, start_coordinates:Tuple[int, int], end_coordinates:Tuple[int, int]):
        '''Draws the winning line on the board from the specified board coordinates'''
        pass

    