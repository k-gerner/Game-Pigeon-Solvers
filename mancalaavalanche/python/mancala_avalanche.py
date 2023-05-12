# Kyle Gerner    7.9.2020
# The class that contains the main method that runs the solver. Also contains
from mancalaavalanche.python.classes import AvalancheBoard, Player, AvalancheSolver
import os
import sys

ONE_BY_ONE = 1
ALL_AT_ONCE = 2

GREEN_COLOR = '\033[92m'
RED_COLOR = '\033[91m'
NO_COLOR = '\033[0m'
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"

CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'
ERASE_MODE_ON = True

# reads in the input for the board from the user
def inputForBoard():
    playerValuesInput = input(f"""
From your left to your right (or top to bottom), enter the # of pebbles in
each spot on {GREEN_COLOR}your{NO_COLOR} side of the board, with a space separating each number:

    """).strip().split()

    while True:
        try:
            erasePreviousLines(1)
            playerVals = [int(item) for item in playerValuesInput]
            if len(playerVals) != 6:
                playerValuesInput = input(f"{ERROR_SYMBOL} There should be 6 values entered.\t").strip().split()
                continue
            break
        except ValueError:
            playerValuesInput = input(f"{ERROR_SYMBOL} There was an issue with your input. Please try again.\t").strip().split()
    erasePreviousLines(4)

    enemyValuesInput = input(f"""
From your left to your right (or top to bottom), enter the # of pebbles in 
each spot on the {RED_COLOR}enemy{NO_COLOR} side of the board, with a space separating each number:

    """).strip().split()
    while True:
        erasePreviousLines(1)
        try:
            enemyVals = [int(item) for item in enemyValuesInput]
            if len(enemyVals) != 6:
                enemyValuesInput = input(f"{ERROR_SYMBOL} There should be 6 values entered.\t").strip().split()
                continue
            break
        except ValueError:
            enemyValuesInput = input(f"{ERROR_SYMBOL} There was an issue with your input. Please try again.\t").strip().split()
    erasePreviousLines(4)
    enemyVals.reverse()
    boardVals = playerVals + [0] + enemyVals + [0]
    return boardVals

# creates the AvalancheSolver object
def createSolver(boardVals):
    p1 = Player()
    p2 = Player()
    board = AvalancheBoard(boardVals, p1, p2, True)
    solver = AvalancheSolver(board)
    return solver

# copy a list and return that list with every value increased by one
def increaseAllValuesInListByOne(l):
    returnList = l.copy()
    for i in range(0, len(l)):
        returnList[i] += 1
    return returnList

# prints the best moveset all at once
def printBestMoveStatus(pointsGained, bestMoves):
    print("\nThe max # of points you can score on this turn is %d in %d move%s." % (pointsGained, len(bestMoves), "" if pointsGained == 1 else "s"))
    print("The move set is: " + ", ".join(map(str, increaseAllValuesInListByOne(bestMoves))))
    print("Note: 1 corresponds to the first (left) spot on your side, 6 corresponds to the last (right) spot")

# print the best moveset one by one
def printBestMovesOneByOne(pointsGained, bestMoves):
    print("\nThe max # of points you can score on this turn is %d in %d move%s." % (pointsGained, len(bestMoves), "" if pointsGained == 1 else "s"))
    print("Note: 1 corresponds to the first (left) spot on your side, 6 corresponds to the last (right) spot")
    print("Press enter each time to receive the next move. Press q to quit at any time.\n")
    bestMoveIndexes = increaseAllValuesInListByOne(bestMoves)
    count = 1
    for moveIndex in bestMoveIndexes:
        if input("#%d:  %d%s" % (count, moveIndex, "\n" if ERASE_MODE_ON else "")).strip().lower() == 'q':
            print("\nThanks for using my Mancala Avalanche solver!\n")
            exit(0)
        count += 1
        erasePreviousLines(2)


# prints the player's best moves in the selected mode
def printSequence(mode, solver, pointsGained, bestMoves):
    if mode == ONE_BY_ONE:
        printBestMovesOneByOne(pointsGained, bestMoves)
    else: printBestMoveStatus(pointsGained, bestMoves)

def erasePreviousLines(numLines, overrideEraseMode=False):
    """Erases the specified previous number of lines from the terminal"""
    eraseMode = ERASE_MODE_ON if not overrideEraseMode else (not ERASE_MODE_ON)
    if eraseMode:
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')

# main method
def main():
    os.system("") # allows output text coloring for Windows OS
    if len(sys.argv) == 2 and sys.argv[1] in ["-e", "-eraseModeOff"]:
        global ERASE_MODE_ON
        ERASE_MODE_ON = False
    print("\nWelcome to Kyle's Mancala Avalanche AI! Written on 7.9.2020")
    if input("\nWould you like to receive your move set in a printed list (as opposed to one at a time)? (y/n):\t").strip().lower() == "y":
        erasePreviousLines(1)
        printMode = ALL_AT_ONCE
        print("Moves will be presented all at once.")
    else:
        erasePreviousLines(1)
        printMode = ONE_BY_ONE
        print("Moves will be presented one at a time.")
    boardVals = inputForBoard()
    solver = createSolver(boardVals)
    print("\nThe current board looks like this:\n")
    solver.board.printBoardHorizontal()
    firstIteration = True
    while True:
        userInput = input("Press enter to receive best move set, or 'q' to quit.\t").strip().lower()
        erasePreviousLines(1)
        if userInput == 'q':
            print("Thanks for playing!")
            exit(0)
        pointsGained, bestMoves = solver.findBestMove(solver.board, 0)
        solver.makeMovesOnMoveset(bestMoves, solver.board)
        erasePreviousLines(5 if firstIteration else 11)
        solver.board.printBoardHorizontal()
        printSequence(printMode, solver, pointsGained, bestMoves)
        print("%sThat's the end of the move set.\n" % ("\n" if printMode == ALL_AT_ONCE else ""))
        print("You will now be asked to input the new version of the board")
        oldEnemyPoints = input("How many points does the enemy have after their turn?\t").strip()
        erasePreviousLines(1)
        while not oldEnemyPoints.isdigit():
            oldEnemyPoints = input(f"{ERROR_SYMBOL} Please enter a number: ").strip()
            erasePreviousLines(1)
        erasePreviousLines(2)
        oldEnemyPoints = int(oldEnemyPoints)
        boardVals = inputForBoard()
        oldPlayerPoints = solver.board.p1.score
        solver = createSolver(boardVals)
        solver.board.p1.score = oldPlayerPoints
        solver.board.p2.score = oldEnemyPoints
        firstIteration = False


if __name__ == '__main__':
    main()