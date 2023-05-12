import pygame
from .constants import BLACK, SQUARE_SIZE, EMPTY_BORDER

class Piece():
    '''Graphics for the piece on the board'''

    PADDING = 30
    # OUTLINE = 2 # not needed for Tic Tac Toe

    def __init__(self, row:int, col:int, player:str):
        '''Creates new Piece object'''
        self.row = row
        self.col = col
        self.player = player # X or O
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        '''Calculates the coordinates of the piece on the GUI'''
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 + EMPTY_BORDER
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2 + EMPTY_BORDER

    def draw(self, window:pygame.Surface):
        '''Draws the piece on the board'''
        if self.player == 'X':
            pygame.draw.line(window, BLACK, (self.x - SQUARE_SIZE // 4, self.y - SQUARE_SIZE // 4), (self.x + SQUARE_SIZE // 4, self.y + SQUARE_SIZE // 4), width=10)
            pygame.draw.line(window, BLACK, (self.x - SQUARE_SIZE // 4, self.y + SQUARE_SIZE // 4), (self.x + SQUARE_SIZE // 4, self.y - SQUARE_SIZE // 4), width=10)
        elif self.player == 'O':
            radius = SQUARE_SIZE//2 - self.PADDING
            # pygame.draw.circle(window, BLACK, (self.x, self.y), radius + OUTLINE, width=1) # don't need for Tic Tac Toe
            pygame.draw.circle(window, BLACK, (self.x, self.y), radius, width=8)
            
    def __repr__(self):
        '''For debugging'''
        return str(self.player) + " at (" + str(self.row) + ", " + str(self.col) + ")"
            