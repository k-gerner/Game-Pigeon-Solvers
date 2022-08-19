# Kyle Gerner 
# Started 3.18.21
# Connect 4 Solver, client facing 
import strategy
import os
import sys

YELLOW_COLOR = "\u001b[38;5;226m"  # yellow
RED_COLOR = '\033[91m'             # red
BLUE_COLOR = "\u001b[38;5;39m"     # blue
GREEN_COLOR = "\x1B[38;5;47m"      # green
GREY_COLOR = "\x1B[38;5;247m"       # grey
NO_COLOR = '\033[0m'               # white

ERASE_MODE_ON = True
BOARD_OUTPUT_HEIGHT = 9

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


def printBoard(board, recentMove=None):
    '''Prints the given game board'''
    columnColor = NO_COLOR
    print("\n   ", end='')
    for i in range(7):
        if i == recentMove:
            columnColor = GREEN_COLOR
        elif not ai.isValidMove(board, i):
            columnColor = GREY_COLOR
        print(f"{columnColor}{i+1}{NO_COLOR} ", end='')
        columnColor = NO_COLOR
    print()
    for rowNum in range(len(board) - 1, -1, -1):
        print(f" {BLUE_COLOR}|{NO_COLOR} ", end='')
        for spot in board[rowNum]:
            if spot == RED:
                pieceColor = RED_COLOR
            elif spot == YELLOW:
                pieceColor = YELLOW_COLOR
            else:
                pieceColor = NO_COLOR
            print(f"{pieceColor}%s{NO_COLOR} " % spot, end='')
        print(f"{BLUE_COLOR}|{NO_COLOR}")
    print(" " + f"{BLUE_COLOR}%s{NO_COLOR}" % "-" * 17)


def getPlayerMove():
    '''Takes in the user's input and performs that move on the board'''
    col = input("It's your turn, which column would you like to play? (1-7):\t").strip().lower()
    while True:
        if col == 'q':
            erasePreviousLines(1)
            print("Thanks for playing!")
            exit(0)
        elif not col.isdigit() or int(col) not in range(1, 8):
            erasePreviousLines(1)
            col = input("Invalid input. Please enter a number 1 through 7:\t")
        elif not ai.isValidMove(gameBoard, int(col) - 1):
            erasePreviousLines(1)
            col = input("That column is full, please choose another:\t")
        else:
            break
    erasePreviousLines(2)
    return int(col) - 1


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
    print("Type 'q' at any prompt to quit.")
    print(f"You: {playerHighlightColor}{playerPiece}{NO_COLOR}\tAI: {aiHighlightColor}{ai.opponentOf(playerPiece)}{NO_COLOR}")
    ai.setPlayerColor(playerPiece)
    turn = YELLOW
    gameOver = False
    winningPiece = None
    printBoard(gameBoard)
    print()
    firstTurn = True
    while not gameOver:
        if turn == playerPiece:
            move = getPlayerMove()
            erasePreviousLines(0)
        else:
            userInput = input("It's the AI's turn, press enter for it to play.\t").strip().lower()
            if userInput == 'q':
                erasePreviousLines(1)
                print("Thanks for playing!")
                exit(0)
            erasePreviousLines(2)
            move = ai.playBestMove(gameBoard)
        ai.performMove(gameBoard, move, turn)
        erasePreviousLines(BOARD_OUTPUT_HEIGHT + (0 if firstTurn else 1))
        printBoard(gameBoard, move)
        print("%s played in spot %d\n" % ("You" if turn == playerPiece else "AI", move + 1))
        turn = ai.opponentOf(turn)  # switch the turn
        firstTurn = False
        gameOver, winningPiece = ai.checkIfGameOver(gameBoard)

    if winningPiece == RED:
        print(f"{RED_COLOR}RED{NO_COLOR} wins!\n")
    elif winningPiece == YELLOW:
        print(f"{YELLOW_COLOR}YELLOW{NO_COLOR} wins!\n")
    else:
        print("The game ended in a tie!\n")


if __name__ == "__main__":
    main()
