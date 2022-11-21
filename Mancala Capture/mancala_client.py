# Kyle Gerner
# Started 11.19.2022
# Mancala Capture, client facing
import os
import sys
from constants import *
from Player import Player
from board_functions import *
from strategy import *

ERASE_MODE_ON = True
BOARD = [4]*6 + [0] + [4]*6 + [0]


# class for the Human player
class HumanPlayer(Player):

    def __init__(self, bankIndex=6):
        super().__init__(bankIndex, isAI=False)

    def getMove(self, board):
        """Takes in the user's input and returns the index on the board for the selected move"""
        spot = input("It's your turn, which spot would you like to play? (1 - 6):\t").strip().upper()
        erasePreviousLines(1)
        while True:
            if spot == 'Q':
                print("\nThanks for playing!\n")
                exit(0)
            elif spot == 'S':
                print("Save not yet implemented!")
                exit(0)
                # saveGame(board, self.color)
                # spot = input("Enter a coordinates for a move, or press 'q' to quit:\t").strip().upper()
                # erasePreviousLines(2)
            elif spot == 'H':
                print("History not yet implemented!")
                exit(0)
                # spot = getBoardHistoryInputFromUser(isAi=False)
            elif not spot.isdigit() or int(spot) < 1 or int(spot) > 6:
                spot = input(f"{ERROR_SYMBOL} Please enter a number 1 - 6:\t").strip().upper()
                erasePreviousLines(1)
            elif board[int(spot) - 1] == 0:
                spot = input(f"{ERROR_SYMBOL} That pocket is empty! Please try again:\t").strip().upper()
                erasePreviousLines(1)
            else:
                break

        return int(spot) - 1




def printBoard(board, turn):
    """Prints the game board"""
    print(SIDE_INDENT_STR + " "*5 + f"{RED_COLOR}{board[13]}{NO_COLOR}")  # enemy's bank
    print(SIDE_INDENT_STR + "___________")
    for index in range(6):
        userSideStr = SIDE_INDENT_STR + " "*2 + f"{GREEN_COLOR}{board[index]}{NO_COLOR}" + (" " if board[index] >= 10 else "  ")
        oppSideStr = (" " if board[12 - index] >= 10 else "  ") + f"{RED_COLOR}{board[12 - index]}{NO_COLOR}"
        print(SIDE_INDENT_STR + "     |     ")
        print(userSideStr + "|" + oppSideStr)
        print(SIDE_INDENT_STR + "_____|_____")
    print("\n" + SIDE_INDENT_STR + " "*5 + f"{GREEN_COLOR}{board[6]}{NO_COLOR}")  # user's bank


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
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(int(numLines), 0), end='')


def main():
    if "-e" in sys.argv or "-eraseModeOff" in sys.argv:
        global ERASE_MODE_ON
        ERASE_MODE_ON = False
    os.system("") # allows colored terminal to work on Windows OS
    printAsciiArt()

    print("Type 'q' to quit.")
    print("Type 's' to save the game. [NOT YET IMPLEMENTED]")
    print("Type 'h' to see previous moves. [NOT YET IMPLEMENTED]")
    print("\n")
    print("\n")

    gameOver = False

    players = [HumanPlayer(6), Strategy(13)]  # remove hardcode values later
    playerNames = ["Human", "AI"]
    printBoard(BOARD, 123456789)
    turn = 0
    while not gameOver:
        nameOfCurrentPlayer = playerNames[turn]
        currentPlayer = players[turn % 2]
        if currentPlayer.isAI:
            userInput = input(f"{nameOfCurrentPlayer}'s turn, press enter for it to play.\t").strip().upper()
            erasePreviousLines(1)
            while userInput in ['Q', 'S', 'H']:
                if userInput == 'Q':
                    # printAverageTimeTakenByPlayers()
                    print("\nThanks for playing!\n")
                    exit(0)
                elif userInput == 'H':
                    # userInput = getBoardHistoryInputFromUser(isAi=True)
                    userInput = input(f"{ERROR_SYMBOL} Board history not implemented yet. Please choose a move:\t").strip().upper()
                    erasePreviousLines(1)
                else:
                    # saveGame(gameBoard, turn)
                    # userInput = input(f"Press enter for {nameOfCurrentPlayer} to play, or press 'q' to quit:\t").strip().upper()
                    # erasePreviousLines(2)
                    userInput = input(f"{ERROR_SYMBOL} Game saving not implemented yet. Please choose a move:\t").strip().upper()
                    erasePreviousLines(1)

        # startTime = time.time()
        chosenMove = currentPlayer.getMove(BOARD)
        # endTime = time.time()
        # totalTimeTakenForMove = endTime - startTime
        # TIME_TAKEN_PER_PLAYER[turn][1] += totalTimeTakenForMove
        # TIME_TAKEN_PER_PLAYER[turn][2] += 1
        # minutesTaken = int(totalTimeTakenForMove) // 60
        # secondsTaken = totalTimeTakenForMove % 60
        # timeTakenOutputStr = ("  (%dm " if minutesTaken > 0 else "  (") + ("%.2fs)" % secondsTaken) if currentPlayer.isAI else ""
        timeTakenOutputStr = ""  # edit or remove later
        finalPebbleLocation = performMove(BOARD, chosenMove, currentPlayer.bankIndex)
        # BOARD_HISTORY.append([[[rowPlayed, colPlayed]], copyOfBoard(gameBoard)])
        erasePreviousLines(BOARD_OUTPUT_HEIGHT)
        printBoard(BOARD, 123456789)
        print("%s played in spot %d%s\n" % (nameOfCurrentPlayer, chosenMove + 1, timeTakenOutputStr))
        if finalPebbleLocation != currentPlayer.bankIndex:
            turn = (turn + 1) % 2
        else:
            print("%s's move ended in their bank, so they get another turn.\n" % nameOfCurrentPlayer)
        gameOver = isBoardTerminal(BOARD)

    pushAllPebblesToBank(BOARD)
    winner = winningPlayerBankIndex(BOARD)
    if winner is None:
        print("It's a tie!")
    else:
        print("Winner has bank index of %d!" % winner)


if __name__ == '__main__':
    main()