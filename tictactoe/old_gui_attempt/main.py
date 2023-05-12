import pygame
from typing import Tuple
from tictactoe.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, EMPTY_BORDER, X_PIECE, O_PIECE
from tictactoe.game import Game
from tictactoe.gui_elements import GuiElements

FPS = 60 # max refresh rate
PIECE_SELECTION, MID_GAME, END_GAME = 1, 2, 3

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")


def choose_piece() -> str:
    '''Asks the user which piece they want to play as'''
    piece_selection_gui = GuiElements(WINDOW)
    button_width, button_height = 100, 100
    piece_selection_gui.add_button_element((WIDTH/2 - button_width/2, HEIGHT/4 - button_height/2, button_width, button_height), "X")
    piece_selection_gui.add_button_element((WIDTH/2 - button_width/2, HEIGHT * 3/4 - button_height/2, button_width, button_height), "O")

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        button_pressed = piece_selection_gui.draw()
        if button_pressed:
            print(button_pressed.text)
            # print(button_pressed.rectangle_parameters)
            return button_pressed.text
        pygame.display.update()
    pygame.quit()
    quit()
    

def run_game(player_piece:str) -> str:
    '''Starts the game and handles the GUI display for the game'''

    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW, player_piece)
    board_changed = False

    instructions_gui = GuiElements(WINDOW)
    instructions_gui.add_text_element("Press Enter for the AI to play its move.", (WIDTH//2, HEIGHT - 50))
    instructions_gui.hide()

    calculate_ai_move = False
    game_over = False

    while run:
        clock.tick(FPS)
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            continue

        if board_changed:
            print("checking if game over...")
            game_over, winner = game.is_over()
            board_changed = False
            if game_over:
                print("GAME OVER")
                print(instructions_gui.remove_text_element("Press Enter for the AI to play its move."))
                if winner:
                    instructions_gui.add_text_element(f"{winner} wins!", (WIDTH//2, HEIGHT - 50))
                else:
                    instructions_gui.add_text_element("It's a tie!", (WIDTH//2, HEIGHT - 50))
                game.display()
                instructions_gui.draw()
                pygame.display.update()
                # return winner
                continue

        if game.turn == player_piece:
            instructions_gui.hide()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(mouse_position)
                    game.play_move(row, col)
                    board_changed = True
    
        else:
            instructions_gui.show()
            if calculate_ai_move:
                print("now calculating ai move...")
                game.play_ai_move()
                calculate_ai_move = False
                board_changed = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        calculate_ai_move = True
            
        game.display()
        instructions_gui.draw()
        pygame.display.update()
    
    pygame.quit()
    quit()



def get_row_col_from_mouse(position) -> Tuple[int, int]:
    '''Gets the row and column that the mouse is currently hovering over'''
    x, y = position
    row = (y - EMPTY_BORDER) // SQUARE_SIZE
    col = (x - EMPTY_BORDER) // SQUARE_SIZE
    return row, col

# def text_objects(text, font):
#     textSurface = font.render(text, True, BLACK)
#     return textSurface, textSurface.get_rect()

def main() -> None:
    '''Handles pygame display. Runs everything.'''
    pygame.init()
    display_mode = PIECE_SELECTION


    player_piece = None
    winner = None


    while True:
        if display_mode == PIECE_SELECTION:
            print("currently in piece selection")
            player_piece = choose_piece()
            display_mode = MID_GAME
        else: # display_mode == MID_GAME:
            print("game has started")
            winner = run_game(player_piece)
            if winner: print("%s wins!" % winner)
            else: print("Tie!")
            quit()
            # display_mode = END_GAME

        # elif display_mode == END_GAME:
        #     pass




main()






    # def beepboop(self):
    #     '''main method that prompts the user for input'''

    #     ai = Strategy(X_PIECE if self.human_piece == O_PIECE else O_PIECE)

    #     if not ai.GAME_OVER:
    #         if turn == playerPiece:
    #             recentMove = getPlayerMove()
    #             gameBoard[recentMove[0]][recentMove[1]] = playerPiece
    #             ai.checkGameState(gameBoard)
    #         else:
    #             # AI's turn
    #             userInput = input("It's the AI's turn, press enter for it to play.\t").strip().lower()
    #             if userInput == 'q':
    #                 print("\nThanks for playing!\n")
    #                 exit(0)
    #             recentMove = ai.findBestMove(gameBoard)
    #             ai_move_formatted = 'ABC'[recentMove[0]] + str(recentMove[1] + 1)
    #             print("AI played in spot %s\n" % ai_move_formatted)
    #         printGameBoard()
    #         turn = ai.opponentOf(turn)

    #     boardCompletelyFilled = True
    #     for row in gameBoard:
    #         for spot in row:
    #             if spot == EMPTY:
    #                 boardCompletelyFilled = False
    #                 break
                    
    #     if boardCompletelyFilled:
    #         print("Nobody wins, it's a tie!\n")
    #     else:
    #         winner = "X" if ai.opponentOf(turn) == X_PIECE else "O"
    #         print("%s player wins!\n" % winner)

