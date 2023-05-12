import pygame
from typing import Tuple
from .constants import X_PIECE, O_PIECE, EMPTY
from .gui_elements import GuiElements
from .strategy import Strategy

class Game():
    '''Handles the backend rules of the Tic Tac Toe game'''

    def __init__(self, window:pygame.Surface, player_piece:str):
        '''Creates a Game object'''
        self.window = window
        self.gui = GuiElements(self.window, with_board=True) # not sure if this is the way i should be doing this
        self.setup_game(player_piece)
        
    def setup_game(self, player_piece:str) -> None:
        '''Set the instance variables to default values'''
        self.turn = X_PIECE
        self.player_piece = player_piece
        self.game_board = [
            [EMPTY, EMPTY, EMPTY], 
			[EMPTY, EMPTY, EMPTY], 
			[EMPTY, EMPTY, EMPTY]]
        self.strategy = Strategy(humanColor=player_piece)

    def display(self) -> None:
        '''Redraws the board display'''
        self.gui.draw()
        # pygame.display.update()

    def reset_game(self, player_piece:str=None) -> None:
        '''Resets the game board'''
        self.gui.reset_board()
        self.turn = X_PIECE
        if player_piece:
            self.setup_game(player_piece)
        else:
            self.setup_game(self.player_piece)

    def play_move(self, row:int, col:int) -> bool:
        '''Plays the move at the given row and column'''
        if not (0 <= row < 3) or not (0 <= col < 3) or self.game_board[row][col] != EMPTY:
            return False
        self.gui.play_move_on_board(row, col, self.turn)
        # self.game_board[row][col] = self.turn
        self.strategy.performMove(self.game_board, row, col, self.turn)
        self.change_turn()
        self.gui.draw()
        pygame.display.update()
        print("self.game_board =")
        for row in self.game_board: print(row)
        return True


    def change_turn(self) -> None:
        '''Switch which player's turn it is'''
        self.turn = self.strategy.opponentOf(self.turn)

    def play_ai_move(self) -> None:
        ai_move = self.strategy.findBestMove(self.game_board)
        self.play_move(ai_move[0], ai_move[1])

    def is_over(self) -> Tuple[bool, str]:
        '''Checks if the game is over, and returns the winner if so'''
        return self.strategy.isTerminal(self.game_board)

