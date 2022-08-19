# Kyle Gerner 
# Started 3.18.21
# Connect 4 Solver, client facing 
import strategy
import os
import sys

YELLOW_COLOR = "\u001b[38;5;226m"  # yellow
RED_COLOR = '\033[91m'  # red
BLUE_COLOR = "\u001b[38;5;39m"  # blue
NO_COLOR = '\033[0m'  # white

ERASE_MODE_ON = True
BOARD_OUTPUT_HEIGHT = 7

CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'

EMPTY, RED, YELLOW = '.', 'o', '@'
gameBoard = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],  # bottom row
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]]  # top row
playerPiece = YELLOW
ai = strategy.Strategy()


def printBoard(board):
    '''Prints the given game board'''
    print("\n  1 2 3 4 5 6 7")
    for rowNum in range(len(board) - 1, -1, -1):
        print(f"{BLUE_COLOR}|{NO_COLOR} ", end='')
        for spot in board[rowNum]:
            if spot == RED:
                pieceColor = RED_COLOR
            elif spot == YELLOW:
                pieceColor = YELLOW_COLOR
            else:
                pieceColor = NO_COLOR
            print(f"{pieceColor}%s{NO_COLOR} " % spot, end='')
        print(f"{BLUE_COLOR}|{NO_COLOR}")
    print(f"{BLUE_COLOR}%s{NO_COLOR}" % "-" * 17)


def getPlayerMove():
    '''Takes in the user's input and performs that move on the board'''
    col = input("It's your turn, which column would you like to play? (1-7):\t")
    while True:
        if not col.isdigit() or int(col.strip()) not in range(1, 8):
            col = input("Invalid input. Please enter a number 1 through 7:\t")
        elif not ai.isValidMove(gameBoard, int(col) - 1):
            col = input("That column is full, please choose another:\t")
        else:
            break
    ai.performMove(gameBoard, int(col) - 1, playerPiece)


def erasePreviousLines(numLines, overrideEraseMode=False):
    """Erases the specified previous number of lines from the terminal"""
    eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
    if eraseMode:
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')


def main():
    '''main method that prompts the user for input'''
    global playerPiece
    os.system("")  # allows colored terminal to work on Windows OS
    if len(sys.argv) == 2 and sys.argv[1] in ["-e", "-eraseModeOff"]:
        global ERASE_MODE_ON
        ERASE_MODE_ON = False
    print("\nWelcome to Kyle's Connect 4 AI!")
    playerPieceInput = input(
        "Would you like to be RED ('r') or YELLOW ('y')? (yellow goes first!):\t").strip().lower()
    if playerPieceInput == 'r':
        playerPiece = RED
        playerHighlightColor = RED_COLOR
        aiHighlightColor = YELLOW_COLOR
        print(f"You will be {RED_COLOR}RED{NO_COLOR}!")
    elif playerPieceInput == 'y':
        playerHighlightColor = YELLOW_COLOR
        aiHighlightColor = RED_COLOR
        print(f"You will be {YELLOW_COLOR}YELLOW{NO_COLOR}!")
    else:
        playerPiece = RED
        playerHighlightColor = RED_COLOR
        aiHighlightColor = YELLOW_COLOR
        print(f"Invalid input. You'll be {RED_COLOR}RED{NO_COLOR}!")
    print(f"You: {playerHighlightColor}{playerPiece}{NO_COLOR}\tAI: {aiHighlightColor}{ai.opponentOf(playerPiece)}{NO_COLOR}")
    ai.setPlayerColor(playerPiece)
    turn = YELLOW
    gameOver = False
    winningPiece = None
    while not gameOver:
        printBoard(gameBoard)
        if turn == playerPiece:
            getPlayerMove()
        else:
            ai_move = ai.playBestMove(gameBoard)
            print("\nAI played in spot %d" % (ai_move + 1))
        turn = ai.opponentOf(turn)  # switch the turn
        gameOver, winningPiece = ai.checkIfGameOver(gameBoard)

    printBoard(gameBoard)
    if winningPiece == RED:
        print(f"{RED_COLOR}RED{NO_COLOR} wins!")
    elif winningPiece == YELLOW:
        print(f"{YELLOW_COLOR}YELLOW{NO_COLOR} wins!")
    else:
        print("The game ended in a tie!")


if __name__ == "__main__":
    main()
