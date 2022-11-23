# Kyle Gerner
# Started 11.19.2022
# Mancala Capture, client facing
import os
import sys
import time
from constants import *
from Player import Player
from board_functions import *
from strategy import *

ERASE_MODE_ON = True
USE_REVERSED_PRINT_LAYOUT = False
BOARD = [4]*6 + [0] + [4]*6 + [0]
PLAYER1_ID = 1
PLAYER2_ID = 2


# class for the Human player
class HumanPlayer(Player):

    def __init__(self, bankIndex=6):
        super().__init__(bankIndex, isAI=False)

    def getMove(self, board):
        """Takes in the user's input and returns the index on the board for the selected move"""
        spot = input(f"It's your turn, which spot would you like to play? (1 - {POCKETS_PER_SIDE}):\t").strip().upper()
        erasePreviousLines(1)
        while True:
            if spot == 'Q':
                print("\nThanks for playing!\n")
                exit(0)
            elif spot == 'F':
                global USE_REVERSED_PRINT_LAYOUT
                USE_REVERSED_PRINT_LAYOUT = not USE_REVERSED_PRINT_LAYOUT
                erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
                printBoard(board)
                print("\n")
                spot = input(f"Board print layout changed. Which spot would you like to play? (1 - {POCKETS_PER_SIDE}):\t").strip().upper()
                erasePreviousLines(1)
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
                spot = input(f"{ERROR_SYMBOL} Please enter a number 1 - {POCKETS_PER_SIDE}:\t").strip().upper()
                erasePreviousLines(1)
            elif board[int(spot) - 1] == 0:
                spot = input(f"{ERROR_SYMBOL} That pocket is empty! Please try again:\t").strip().upper()
                erasePreviousLines(1)
            else:
                break

        return int(spot) - 1


def printBoard(board, playerId=None, move=None):
    """Prints the game board"""
    # orientation
    arrowIndex = -1
    if USE_REVERSED_PRINT_LAYOUT:
        topBankIndex = PLAYER1_BANK_INDEX
        bottomBankIndex = PLAYER2_BANK_INDEX
        leftSidePlayerId = PLAYER2_ID
        topLeftPocketIndex = POCKETS_PER_SIDE + 1  # which index is printed in the top left corner of the printed board
        leftSideColor = RED_COLOR
        rightSideColor = GREEN_COLOR
        if move is not None:
            arrowIndex = move if move > POCKETS_PER_SIDE else getIndexOfOppositeHole(move)
    else:
        topBankIndex = PLAYER2_BANK_INDEX
        bottomBankIndex = PLAYER1_BANK_INDEX
        leftSidePlayerId = PLAYER1_ID
        topLeftPocketIndex = 0
        leftSideColor = GREEN_COLOR
        rightSideColor = RED_COLOR
        if move is not None:
            arrowIndex = move if move < POCKETS_PER_SIDE else getIndexOfOppositeHole(move)

    print()
    print(SIDE_INDENT_STR + " "*5 + f"{rightSideColor}{board[topBankIndex]}{NO_COLOR}")  # top bank
    print(SIDE_INDENT_STR + "___________")
    for index in range(topLeftPocketIndex, topLeftPocketIndex + POCKETS_PER_SIDE):
        leftSideStrPrefix = SIDE_INDENT_STR  # may change to arrow
        rightSideStrSuffix = ""  # may change to arrow
        if index == arrowIndex:
            if playerId == leftSidePlayerId:
                leftSideStrPrefix = LEFT_SIDE_ARROW
            else:
                rightSideStrSuffix = RIGHT_SIDE_ARROW

        leftSideStr = leftSideStrPrefix + " "*2 \
                      + f"{leftSideColor}{board[index]}{NO_COLOR}" \
                      + (" " if board[index] >= 10 else "  ")
        rightSideStr = (" " if board[getIndexOfOppositeHole(index)] >= 10 else "  ") \
                     + f"{rightSideColor}{board[getIndexOfOppositeHole(index)]}{NO_COLOR}" \
                     + rightSideStrSuffix
        print(SIDE_INDENT_STR + "     |     ")
        print(leftSideStr + str(min(index, getIndexOfOppositeHole(index)) + 1) + rightSideStr)
        print(SIDE_INDENT_STR + "_____|_____")
    print("\n" + SIDE_INDENT_STR + " "*5 + f"{leftSideColor}{board[bottomBankIndex]}{NO_COLOR}\n")  # bottom bank


def opponentOf(playerId):
    """Gets the id opponent of the given id"""
    return PLAYER1_ID if playerId == PLAYER2_ID else PLAYER2_ID


def printAverageTimeTakenByPlayers(timeTakenPerPlayer):
    """Prints out the average time taken per move for each player"""
    userTimeTaken = round(timeTakenPerPlayer[PLAYER1_ID][1]/max(1, timeTakenPerPlayer[PLAYER1_ID][2]), 2)
    aiTimeTaken = round(timeTakenPerPlayer[PLAYER2_ID][1]/max(1, timeTakenPerPlayer[PLAYER2_ID][2]), 2)
    print("Average time taken per move:")
    print(f"{GREEN_COLOR}{timeTakenPerPlayer[PLAYER1_ID][0]}{NO_COLOR}: {userTimeTaken}s")
    print(f"{RED_COLOR}{timeTakenPerPlayer[PLAYER2_ID][0]}{NO_COLOR}: {aiTimeTaken}s")


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

    players = {                         # remove hardcode values later
        PLAYER1_ID: HumanPlayer(PLAYER1_BANK_INDEX),
        PLAYER2_ID: Strategy(PLAYER2_BANK_INDEX)
    }
    nameOfPlayer1 = "Human"
    nameOfPlayer2 = "AI"
    playerNames = {
        PLAYER1_ID: nameOfPlayer1,
        PLAYER2_ID: nameOfPlayer2
    }
    timeTakenPerPlayer = {
        PLAYER1_ID: [nameOfPlayer1, 0, 0],    # [player name, total time, num moves]
        PLAYER2_ID: [nameOfPlayer2, 0, 0]
    }

    userGoFirst = input("Would you like to go first? (y/n):\t").strip().upper()
    erasePreviousLines(1)
    if userGoFirst == "Y":
        turn = PLAYER1_ID
        print("%s will go first!" % playerNames[turn])
    else:
        turn = PLAYER2_ID
        print("%s will go first!" % playerNames[turn])

    print("Type 'q' to quit.")
    print("Type 'f' to flip the board orientation 180 degrees.")
    # print("Type 's' to save the game. [NOT YET IMPLEMENTED]")
    # print("Type 'h' to see previous moves. [NOT YET IMPLEMENTED]")

    gameOver = False
    printBoard(BOARD)
    print("\n")
    extraLinesPrinted = 2
    while not gameOver:
        nameOfCurrentPlayer = playerNames[turn]
        currentPlayer = players[turn]
        if currentPlayer.isAI:
            userInput = input(f"{nameOfCurrentPlayer}'s turn, press enter for it to play.\t").strip().upper()
            erasePreviousLines(1)
            while userInput in ['Q', 'H', 'F', 'S']:
                if userInput == 'Q':
                    # printAverageTimeTakenByPlayers()
                    print("\nThanks for playing!\n")
                    exit(0)
                elif userInput == 'H':
                    # userInput = getBoardHistoryInputFromUser(isAi=True)
                    userInput = input(f"{ERROR_SYMBOL} Board history not implemented yet. Press enter to continue:\t").strip().upper()
                    erasePreviousLines(1)
                elif userInput == 'F':
                    global USE_REVERSED_PRINT_LAYOUT
                    USE_REVERSED_PRINT_LAYOUT = not USE_REVERSED_PRINT_LAYOUT
                    erasePreviousLines(BOARD_OUTPUT_HEIGHT + 2)
                    printBoard(BOARD)
                    print("\n")
                    userInput = input(f"Board print layout changed. Press enter to continue:\t").strip().upper()
                    erasePreviousLines(1)
                else:
                    # saveGame(gameBoard, turn)
                    # userInput = input(f"Press enter for {nameOfCurrentPlayer} to play, or press 'q' to quit:\t").strip().upper()
                    # erasePreviousLines(2)
                    userInput = input(f"{ERROR_SYMBOL} Game saving not implemented yet. Please choose a move:\t").strip().upper()
                    erasePreviousLines(1)

        startTime = time.time()
        chosenMove = currentPlayer.getMove(BOARD)
        endTime = time.time()
        totalTimeTakenForMove = endTime - startTime
        timeTakenPerPlayer[turn][1] += totalTimeTakenForMove
        timeTakenPerPlayer[turn][2] += 1
        minutesTaken = int(totalTimeTakenForMove) // 60
        secondsTaken = totalTimeTakenForMove % 60
        timeTakenOutputStr = ("  (%dm " if minutesTaken > 0 else "  (") + ("%.2fs)" % secondsTaken) if currentPlayer.isAI else ""
        finalPebbleLocation = performMove(BOARD, chosenMove, currentPlayer.bankIndex)
        # BOARD_HISTORY.append([[[rowPlayed, colPlayed]], copyOfBoard(gameBoard)])
        erasePreviousLines(BOARD_OUTPUT_HEIGHT + extraLinesPrinted)
        printBoard(BOARD, turn, chosenMove)
        moveFormatted = str(min(BOARD_SIZE - 2 - chosenMove, chosenMove) + 1)
        print("%s played in spot %s%s. " % (nameOfCurrentPlayer, moveFormatted, timeTakenOutputStr), end='')
        if finalPebbleLocation != currentPlayer.bankIndex:
            print("\n")
            turn = opponentOf(turn)
        else:
            print("%s's move ended in their bank, so they get another turn.\n" % nameOfCurrentPlayer)
        extraLinesPrinted = 2
        gameOver = isBoardTerminal(BOARD)

    pushAllPebblesToBank(BOARD)
    erasePreviousLines(BOARD_OUTPUT_HEIGHT + extraLinesPrinted)
    printBoard(BOARD)
    winnerId = PLAYER1_ID if winningPlayerBankIndex(BOARD) == PLAYER1_BANK_INDEX else PLAYER2_ID
    if winnerId is None:
        print("It's a tie!\n")
    else:
        print("%s wins!\n" % playerNames[winnerId])
    printAverageTimeTakenByPlayers(timeTakenPerPlayer)


if __name__ == '__main__':
    main()