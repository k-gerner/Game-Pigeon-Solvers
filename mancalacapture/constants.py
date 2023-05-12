from util.terminaloutput.colors import YELLOW_COLOR, NO_COLOR
# Constant values to be used across multiple files

# Terminal text erase functionality
ERASE_MODE_ON = True

# Board size
POCKETS_PER_SIDE = 6  # excludes bank pockets
BOARD_SIZE = (POCKETS_PER_SIDE * 2) + 2  # total # pockets on each side plus the banks

# Pebble count
STARTING_PEBBLES_PER_POCKET = 4
TOTAL_PEBBLES = STARTING_PEBBLES_PER_POCKET * POCKETS_PER_SIDE * 2

# Bank indices
PLAYER1_BANK_INDEX = int(BOARD_SIZE/2 - 1)  # 6
PLAYER2_BANK_INDEX = int(BOARD_SIZE - 1)    # 13

# Board printing
SIDE_INDENT_STR = "          "  # default 10 spaces
LEFT_SIDE_ARROW   = f"    {YELLOW_COLOR}-->{NO_COLOR}   "
RIGHT_SIDE_ARROW   = f"{YELLOW_COLOR}   <--{NO_COLOR}"
BOARD_OUTPUT_HEIGHT = 3 * (POCKETS_PER_SIDE + 2)  # how many lines are printed when printing the board


# Default board layout
#   __13__
# 0   |   12
# 1   |   11
# 2   |   10
# 3   |   9
# 4   |   8
# 5 __|__ 7
#     6
