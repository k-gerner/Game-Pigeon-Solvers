# Tic Tac Toe AI GUI and game runner
# Kyle G 10.30.2022
import pygame as pg
import os

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = (222, 210, 173)  # tan
DATA_DIRECTORY = os.path.join(os.path.split(os.path.abspath(__file__))[0], "data")

pg.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SCALED)

def load_all_images(colorKey=(255,0,255), accept=(".png", ".jpg", ".bmp")):
    """
    Loads all the images for the game.
    Returns a dictionary mapping filename to image asset
    """
    graphics = {}
    for filename in os.listdir(DATA_DIRECTORY):
        name, file_extension = os.path.splitext(filename)
        if file_extension.lower() in accept:
            img = pg.image.load(os.path.join(DATA_DIRECTORY, filename))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorKey)
            graphics[name] = img
    return graphics


def main():
    """Main runner"""
    pg.display.set_caption("Tic Tac Toe")
    images = load_all_images()
    board = images["board"]
    screen.fill(BACKGROUND_COLOR)
    screen.blit(pg.transform.scale(board, (WINDOW_WIDTH, 0.8*WINDOW_HEIGHT)), (0, 0))
    pg.draw.rect(screen, pg.color.Color("Black"), (0, 0.8*WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT))

    clock = pg.time.Clock()
    going = True
    while going:
        clock.tick(30)  # 30 FPS
        events_list = pg.event.get()
        for event in events_list:
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    going = False
        pg.display.flip()  # update the display



if __name__ == "__main__":
    main()
