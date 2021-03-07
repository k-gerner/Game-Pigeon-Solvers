from AvalancheBoard import AvalancheBoard
from Player import Player
from AvalancheSolver import AvalancheSolver

def inputForBoard():
    while True:
        playerVals = [int(item) for item in input("From your left to your right (or top to bottom), enter the # of pebbles in each spot on your side of the board, with a space separating each number:\n").split()]
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

def createSolver(boardVals):
    p1 = Player()
    p2 = Player()
    board = AvalancheBoard(boardVals, p1, p2, True)
    solver = AvalancheSolver(board)
    return solver

def printSequence(mode, solver, pointsGained, bestMoves):
    if mode == 1:
        solver.printBestMovesOneByOne(pointsGained, bestMoves)
    else: solver.printBestMoveStatus(pointsGained, bestMoves)

print("Welcome to Kyle's Mancala Avalanche AI! Written on 7.9.2020")
if input("Would you like to receive your moveset one at a time (as opposed to a printed list)? (y/n): ").strip() == "y":
    printMode = 1
else:
    printMode = 2
boardVals = inputForBoard()
solver = createSolver(boardVals)
print("The starting board looks like this:")
solver.board.printBoardHorizontal()
print("(if this is incorrect, restart the program and make sure the values you entered are correct)")
oldPlayerPoints = 0
oldEnemyPoints = 0
while True:
    input("Press enter to receive best move set")
    pointsGained, bestMoves = solver.findBestMove(solver.board, 0)
    printSequence(printMode, solver, pointsGained, bestMoves)
    solver.makeMovesOnMoveset(bestMoves, solver.board)
    if input("To see the board after these moves, enter \"y\": ").strip() == "y":
        solver.board.printBoardHorizontal()
    if input("Continue? (y/n):  ").strip() == "n":
        print("Thanks for playing!")
        break
    print("You will now be asked to input the new version of the board")
    oldEnemyPoints = int(input("How many points does the enemy have after that turn? ").strip())
    boardVals = inputForBoard()
    oldPlayerPoints = solver.board.p1.score
    solver = createSolver(boardVals)
    solver.board.p1.score = oldPlayerPoints
    solver.board.p2.score = oldEnemyPoints