# Kyle Gerner    7.9.2020
# The class that contains the main method that runs the solver. Also contains
from mancalaavalanche.python.classes import AvalancheBoard, AvalanchePlayer, AvalancheSolver
from util.terminaloutput.colors import GREEN_COLOR, RED_COLOR, NO_COLOR
from util.terminaloutput.symbols import ERROR_SYMBOL
from util.terminaloutput.erasing import erasePreviousLines

ONE_BY_ONE = 1
ALL_AT_ONCE = 2


def input_for_board():
	"""Reads in the input for the board from the user"""
	player_values_input = input(f"""
From your left to your right (or top to bottom), enter the # of pebbles in
each spot on {GREEN_COLOR}your{NO_COLOR} side of the board, with a space separating each number:

    """).strip().split()

	while True:
		try:
			erasePreviousLines(1)
			player_vals = [int(item) for item in player_values_input]
			if len(player_vals) != 6:
				player_values_input = input(f"{ERROR_SYMBOL} There should be 6 values entered.\t").strip().split()
				continue
			break
		except ValueError:
			player_values_input = input(
				f"{ERROR_SYMBOL} There was an issue with your input. Please try again.\t").strip().split()
	erasePreviousLines(4)

	enemy_values_input = input(f"""
From your left to your right (or top to bottom), enter the # of pebbles in 
each spot on the {RED_COLOR}enemy{NO_COLOR} side of the board, with a space separating each number:

    """).strip().split()
	while True:
		erasePreviousLines(1)
		try:
			enemy_vals = [int(item) for item in enemy_values_input]
			if len(enemy_vals) != 6:
				enemy_values_input = input(f"{ERROR_SYMBOL} There should be 6 values entered.\t").strip().split()
				continue
			break
		except ValueError:
			enemy_values_input = input(
				f"{ERROR_SYMBOL} There was an issue with your input. Please try again.\t").strip().split()
	erasePreviousLines(4)
	enemy_vals.reverse()
	board_vals = player_vals + [0] + enemy_vals + [0]
	return board_vals


def create_solver(board_vals):
	"""Creates the AvalancheSolver object"""
	p1 = AvalanchePlayer()
	p2 = AvalanchePlayer()
	board = AvalancheBoard(board_vals, p1, p2, True)
	solver = AvalancheSolver(board)
	return solver


def increase_all_values_in_list_by_one(values_list):
	"""Copy a list and return that list with every value increased by one"""
	return [item + 1 for item in values_list]


def print_best_move_status(points_gained, best_moves):
	"""Prints the best moveset all at once"""
	print("\nThe max # of points you can score on this turn is %d in %d move%s." % (
		points_gained, len(best_moves), "" if points_gained == 1 else "s"))
	print("The move set is: " + ", ".join(map(str, increase_all_values_in_list_by_one(best_moves))))
	print("Note: 1 corresponds to the first (left) spot on your side, 6 corresponds to the last (right) spot")


def print_best_moves_one_by_one(points_gained, best_moves):
	"""Prints the best moveset one by one"""
	print("\nThe max # of points you can score on this turn is %d in %d move%s." % (
		points_gained, len(best_moves), "" if points_gained == 1 else "s"))
	print("Note: 1 corresponds to the first (left) spot on your side, 6 corresponds to the last (right) spot")
	print("Press enter each time to receive the next move. Press q to quit at any time.\n")
	best_move_indexes = increase_all_values_in_list_by_one(best_moves)
	count = 1
	for moveIndex in best_move_indexes:
		if input("#%d:  %d%s" % (count, moveIndex, "\n")).strip().lower() == 'q':
			print("\nThanks for using my Mancala Avalanche solver!\n")
			exit(0)
		count += 1
		erasePreviousLines(2)


def print_sequence(mode, points_gained, best_moves):
	"""Prints the player's best moves in the selected mode"""
	if mode == ONE_BY_ONE:
		print_best_moves_one_by_one(points_gained, best_moves)
	else:
		print_best_move_status(points_gained, best_moves)


def run():
	print("\nWelcome to Kyle's Mancala Avalanche AI! Written on 7.9.2020")
	if input(
			"\nWould you like to receive your move set in a printed list (as opposed to one at a time)? (y/n):\t").strip().lower() == "y":
		erasePreviousLines(1)
		print_mode = ALL_AT_ONCE
		print("Moves will be presented all at once.")
	else:
		erasePreviousLines(1)
		print_mode = ONE_BY_ONE
		print("Moves will be presented one at a time.")
	board_vals = input_for_board()
	solver = create_solver(board_vals)
	print("\nThe current board looks like this:\n")
	solver.board.print_board_horizontal()
	first_iteration = True
	while True:
		user_input = input("Press enter to receive best move set, or 'q' to quit.\t").strip().lower()
		erasePreviousLines(1)
		if user_input == 'q':
			print("Thanks for playing!")
			exit(0)
		points_gained, best_moves = solver.find_best_move(solver.board, 0)
		solver.make_moves_on_moveset(best_moves, solver.board)
		erasePreviousLines(5 if first_iteration else 11)
		solver.board.print_board_horizontal()
		print_sequence(print_mode, points_gained, best_moves)
		print("%sThat's the end of the move set.\n" % ("\n" if print_mode == ALL_AT_ONCE else ""))
		print("You will now be asked to input the new version of the board")
		old_enemy_points = input("How many points does the enemy have after their turn?\t").strip()
		erasePreviousLines(1)
		while not old_enemy_points.isdigit():
			old_enemy_points = input(f"{ERROR_SYMBOL} Please enter a number: ").strip()
			erasePreviousLines(1)
		erasePreviousLines(2)
		old_enemy_points = int(old_enemy_points)
		board_vals = input_for_board()
		old_player_points = solver.board.p1.score
		solver = create_solver(board_vals)
		solver.board.p1.score = old_player_points
		solver.board.p2.score = old_enemy_points
		first_iteration = False
