# Kyle Gerner
# Started 11.19.2022
# Mancala Capture, client facing
GREEN_COLOR = '\033[92m'	 # green
RED_COLOR = '\033[91m'		 # red
NO_COLOR = '\033[0m' 		 # white
BLUE_COLOR = '\033[38;5;39m' # blue

ERASE_MODE_ON = True
CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"
INFO_SYMBOL = f"{BLUE_COLOR}<!>{NO_COLOR}"
#  __13__
# 0   |   12
# 1   |   11
# 2   |   10
# 3   |   9
# 4   |   8
# 5 __|__ 7
#     6
USER_BANK_INDEX = 6
OPPONENT_BANK_INDEX = 13
BOARD = [4]*6 + [0] + [10]*6 + [0]

def printBoard(board, turn):
    """Prints the game board"""
    SIDE_INDENT = " " * 10
    print(" "*10 + f"{RED_COLOR}{board[13]}{NO_COLOR}")  # enemy's bank
    print(" "* 4 + " ___________")
    for index in range(6):
        userSideStr = " "*7 + f"{GREEN_COLOR}{board[index]}{NO_COLOR}" + (" " if board[index] >= 10 else "  ")
        oppSideStr = (" " if board[12 - index] >= 10 else "  ") + f"{RED_COLOR}{board[12 - index]}{NO_COLOR}"
        print(" " * 4 + "      |     ")
        print(userSideStr + "|" + oppSideStr)
        print(" "* 4 + " _____|_____")
    # print(" ___________")
    print("\n" + " "*10 + f"{GREEN_COLOR}{board[6]}{NO_COLOR}")  # user's bank


def printAsciiArt():
    """Prints the Mancala Capture Ascii Art"""
    print("""
  __  __                       _       
 |  \/  |                     | |      
 | \  / | __ _ _ __   ___ __ _| | __ _ 
 | |\/| |/ _` | '_ \ / __/ _` | |/ _` |
 | |  | | (_| | | | | (_| (_| | | (_| |
 |_|__|_|\__,_|_| |_|\___\__,_|_|\__,_|
  / ____|          | |                 
 | |     __ _ _ __ | |_ _   _ _ __ ___ 
 | |    / _` | '_ \| __| | | | '__/ _ \\
 | |___| (_| | |_) | |_| |_| | | |  __/
  \_____\__,_| .__/ \__|\__,_|_|  \___|
             | |                       
             |_|  
    """)


def erasePreviousLines(numLines, overrideEraseMode=False):
    """Erases the specified previous number of lines from the terminal"""
    eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
    if eraseMode:
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')


def main():
    printAsciiArt()
    printBoard(BOARD, 0)


if __name__ == '__main__':
    main()