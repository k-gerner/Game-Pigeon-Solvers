from __future__ import division
import math
import sys
import pygame


class MyGame(object):
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.bg_color = 0, 0, 0

        font = pygame.font.Font(None, 100)

        self.text = font.render("text that should appear", True, (238, 58, 140))


        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)


    def run(self):
        running = True
        while running:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                running = False

            elif event.type == self.REFRESH:
                self.draw()

            else:
                pass 

    def draw(self):
        self.screen.fill(self.bg_color)

        self.screen.blit(self.text, [400,300])

        pygame.display.flip()


MyGame().run()
pygame.quit()
sys.exit()