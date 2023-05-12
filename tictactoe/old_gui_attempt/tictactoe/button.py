import pygame
from typing import Tuple

class Button():
    '''GUI Button element'''

    def __init__(self, color:Tuple[int, int, int], rectangle_parameters:Tuple[int, int, int, int], window:pygame.Surface, text:str="(no text)"):
        '''Creates the Button object'''
        self.color = color
        self.rectangle_parameters = rectangle_parameters
        self.window = window
        self.clicked = False
        self.text = text

    def draw(self):
        '''Draw the button'''
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        x, y, width, height = self.rectangle_parameters
        if x < mouse_pos[0] < x+width and y < mouse_pos[1] < y+height:
            if click[0] == 1 and not self.clicked:
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(self.window, self.color, self.rectangle_parameters)
