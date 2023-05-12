import pygame
from typing import Tuple
from .board import Board
from .constants import BLACK, WHITE, WIDTH, HEIGHT
from .button import Button

class GuiElements():
    '''Handles all the GUI elements excluding the Board, such as text and buttons'''

    def __init__(self, window:pygame.Surface, with_board:bool=False, board:Board=None):
        '''Creates a GuiElements object'''
        self.text_elements = [] # list of tuples (text, pygame.Surface, coordinates)  ##### should change to dict   text : [list of coordinate/font pairs]
        self.button_elements = [] # list of Buttons
        self.visible = True
        if with_board:
            self.board = board if board else Board()
        else:
            self.board = None
        self.window = window

    def hide(self) -> None:
        '''Hide all the elements'''
        self.visible = False

    def show(self) -> None:
        '''Show all the elements'''
        self.visible = True

    def add_text_element(self, 
        text_content:str, 
        coordinates: Tuple[int, int], 
        text_color: Tuple[int, int, int] = BLACK, 
        bg_color: Tuple[int, int, int] = None,
        surface: pygame.Surface = None
    ) -> bool:
        '''Adds text element to the list of text elements'''
        if coordinates[0] < WIDTH and coordinates[1] < HEIGHT:
            if not surface:
                font = pygame.font.Font('freesansbold.ttf', 20)
                surface = font.render(text_content, True, text_color, bg_color)
            self.text_elements.append((text_content, surface, coordinates))
            return True
        else:
            return False

    def add_button_element(self, 
        rectange_parameters: Tuple[int, int, int, int], 
        button_text: str = None, 
        color: Tuple[int, int, int] = WHITE, 
        button_text_color: Tuple[int, int, int] = BLACK
    ) -> bool:
        '''Adds a button element to the list of button elements'''
        if rectange_parameters[0] < WIDTH and rectange_parameters[1] < HEIGHT:
            if button_text:
                self.add_text_element(
                    button_text, 
                    (rectange_parameters[0] + rectange_parameters[2]//2, rectange_parameters[1] + rectange_parameters[3]//2), 
                    button_text_color
                )
            # self.button_elements.append((color, rectange_parameters, button_text))
            self.button_elements.append(Button(color, rectange_parameters, self.window, button_text))
            return True
        else:
            return False

    def play_move_on_board(self, row:int, col:int, player:str) -> None:
        '''Adds a piece to the board at the specified row and column'''
        self.board.play_move(row, col, player)

    def remove_text_element(self, text:str) -> bool:
        '''Removes a text element from the list of text elements'''
        for text_element in self.text_elements:
            if text_element[0] == text:
                self.text_elements.remove(text_element)
                return True
        return False

    def remove_button_element_by_text(self, button_text:str) -> bool:
        '''Removes a button element from the list of button elements, with the button text as the identifier'''
        self.remove_text_element(button_text)
        for button_element in self.button_elements:
            if button_element.text == button_text:
                self.button_elements.remove(button_element)
                return True
        return False

    def remove_button_element_by_coord(self, coordinates:Tuple[int, int]) -> bool:
        '''Removes a button element from the list of button elements, with the button coordinates as the identifier'''
        for button_element in self.button_elements:
            if button_element.rectangle_parameters[:2] == coordinates:
                self.button_elements.remove(button_element)
                return True
        return False

    def reset_board(self) -> None:
        '''Clears the board of all Piece circles'''
        self.board = Board()

    def draw(self) -> Button:
        '''Draws all the GUI elements'''
        if self.visible == False:
            return None
        buttons_pressed = None
        if self.board:
            self.board.draw(self.window)
        for button_element in self.button_elements:
            # pygame.draw.rect(self.window, button_element[0], button_element[1])
            button_element.draw()
            if button_element.clicked:
                buttons_pressed = button_element

        for text, surface, coordinates in self.text_elements:
            textRect = surface.get_rect()
            textRect.center = coordinates
            self.window.blit(surface, textRect)
        
        return buttons_pressed

        