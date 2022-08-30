# Kyle Gerner    7.9.2020
# The class that contains the main method that runs the solver. Also contains  
from AvalancheBoard import AvalancheBoard
from Player import Player
from AvalancheSolver import AvalancheSolver

ONE_BY_ONE = 1
ALL_AT_ONCE = 2

# reads in the input for the board from the user
def inputForBoard():
    while True:
        try:
            playerVals = [int(item) for item in input("From your left to your right (or top to bottom), enter the # of pebbles in each spot on your side of the board, with a space separating each number:\n").split()]
        except ValueError:
            print("There was an issue with your input. Please try again.")
            continue
        if len(playerVals) != 6:
            print("There should be 6 values entered")
            continue
        break
    while True:
        enemyVals = [int(item) for item in input("From your left to your right (or top to bottom), enter the # of pebbles in each spot on the enemy side of the board, with a space separating each number:\n").split()]
        if len(enemyVals) != 6:
            print("There should be 6 values entered")
            continue
        break
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

# prints the player's best moves in the selected mode
def printSequence(mode, solver, pointsGained, bestMoves):
    if mode == ONE_BY_ONE:
        solver.printBestMovesOneByOne(pointsGained, bestMoves)
    else: solver.printBestMoveStatus(pointsGained, bestMoves)

# main method
def main():
    print("\nWelcome to Kyle's Mancala Avalanche AI! Written on 7.9.2020")
    if input("\nWould you like to receive your moveset one at a time (as opposed to a printed list)? (y/n): ").strip() == "y":
        printMode = ONE_BY_ONE
        print("Moves will be presented one at a time.\n")
    else:
        printMode = ALL_AT_ONCE
        print("Moves will be presented all at once.\n")
    boardVals = inputForBoard()
    solver = createSolver(boardVals)
    print("\nThe starting board looks like this:\n")
    solver.board.printBoardHorizontal()
    print("(if this is incorrect, restart the program and make sure the values you entered are correct)")
    oldPlayerPoints = 0
    oldEnemyPoints = 0
    while True:
        input("Press enter to receive best move set")
        pointsGained, bestMoves = solver.findBestMove(solver.board, 0)
        printSequence(printMode, solver, pointsGained, bestMoves)
        solver.makeMovesOnMoveset(bestMoves, solver.board)
        print("\nThat's the end of the move set.\n")
        if input("To see the board after these moves, enter \"y\": ").strip().lower() == "y":
            solver.board.printBoardHorizontal()
        if input("If you would not like to continue to the next turn, type 'q':  ").strip().lower() == "q":
            print("Thanks for playing!")
            break
        print("You will now be asked to input the new version of the board")
        oldEnemyPoints = input("How many points does the enemy have after that turn? ").strip()
        while not oldEnemyPoints.isdigit():
            oldEnemyPoints = input("Please enter a number: ").strip()
        oldEnemyPoints = int(oldEnemyPoints)
        boardVals = inputForBoard()
        oldPlayerPoints = solver.board.p1.score
        solver = createSolver(boardVals)
        solver.board.p1.score = oldPlayerPoints
        solver.board.p2.score = oldEnemyPoints


if __name__ == '__main__':
    main()