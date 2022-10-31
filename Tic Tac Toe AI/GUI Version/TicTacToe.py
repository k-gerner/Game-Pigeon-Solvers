# Tic Tac Toe AI GUI and game runner
# Kyle G 10.30.2022
import pygame as pg
import os

X_TURN, O_TURN = 'X', 'O'

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


def board_rectangles(surface):
    """Gets a list of the rectangles that cover the board spaces, for checking hit detection"""
    left_indent = 0.085 * surface.get_width()  # empty space from left of screen
    top_indent = 0.08 * surface.get_height()  # empty space from top of screen
    space_width = 0.27 * surface.get_width()
    space_height = 0.27 * surface.get_height()
    divider_width = 0.015 * surface.get_width()
    rectangles = []  # holds the rectangles in order left-to-right, top-to-bottom
    y = top_indent
    for row in range(3):
        x = left_indent
        for col in range(3):
            width = 0.9*space_width if col == -1 else space_width
            rectangles.append(pg.Rect(x, y, width, space_height))
            x += width + divider_width
        y += space_height + divider_width
    return rectangles


def opponent_of(turn):
    """Get the opponent of given turn"""
    if turn == X_TURN:
        return O_TURN
    elif turn == O_TURN:
        return X_TURN
    else:
        return None


def main():
    """Main runner"""
    pg.display.set_caption("Tic Tac Toe")
    images = load_all_images()
    # draw the board surface
    board_image = images["board"]
    board_area = pg.Surface((WINDOW_WIDTH, 0.8*WINDOW_HEIGHT))
    board_area.fill(BACKGROUND_COLOR)
    board_area.blit(pg.transform.scale(board_image, board_area.get_size()), (0, 0))
    # draw the text box surface
    text_area = pg.Surface((WINDOW_WIDTH, 0.2*WINDOW_HEIGHT))
    text_area.fill(pg.color.Color("Black"))
    # paint the board and text box onto the screen
    screen.blit(board_area, (0, 0))
    screen.blit(text_area, (0, 0.8*WINDOW_HEIGHT))
    board_space_rectangles = board_rectangles(board_area)

    clock = pg.time.Clock()
    going = True
    turn = X_TURN
    player_turn = X_TURN
    opponent_turn = O_TURN
    move_was_played = False
    while going:
        clock.tick(30)  # 30 FPS
        events_list = pg.event.get()
        for event in events_list:
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    going = False
            elif event.type == pg.MOUSEBUTTONUP:
                if turn == player_turn:
                    mouse_pos = pg.mouse.get_pos()
                    clicked_rect_index = None
                    for index, space in enumerate(board_space_rectangles):
                        if space.collidepoint(mouse_pos):
                            clicked_rect_index = index
                            move_was_played = True
                            break
                    if clicked_rect_index is not None:
                        print(f"Clicked rect at index {clicked_rect_index}")
                        print("Press SPACE to be reset to player turn")

        pg.display.flip()  # update the display
        if move_was_played:
            turn = opponent_of(turn)
            move_was_played = False



if __name__ == "__main__":
    main()
