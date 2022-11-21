# Constant values to be used across multiple files

# Text colors
GREEN_COLOR = '\033[92m'	      # green
YELLOW_COLOR = "\u001b[38;5;226m" # yellow
RED_COLOR = '\033[91m'		      # red
NO_COLOR = '\033[0m' 		      # white
BLUE_COLOR = '\033[38;5;39m'      # blue

# Terminal text erase functionality
ERASE_MODE_ON = True
CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'

# Symbols
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"
INFO_SYMBOL = f"{BLUE_COLOR}<!>{NO_COLOR}"

# Board size
BOARD_SIZE = 14  # total # pockets on each side plus the banks. Must be even
POCKETS_PER_SIDE = int(BOARD_SIZE/2 - 1)  # excludes bank pockets

# Pebble count
PEBBLES_PER_POCKET = 4
TOTAL_PEBBLES = PEBBLES_PER_POCKET * POCKETS_PER_SIDE * 2

# Bank indices
PLAYER1_BANK_INDEX = int(BOARD_SIZE/2 - 1)  # 6
PLAYER2_BANK_INDEX = int(BOARD_SIZE - 1)    # 13

# Board printing
SIDE_INDENT_STR = "          "  # default 10 spaces
PLAYER1_ARROW   = f"    {YELLOW_COLOR}-->{NO_COLOR}   "
PLAYER2_ARROW   = f"{YELLOW_COLOR}   <--{NO_COLOR}"
BOARD_OUTPUT_HEIGHT = (3 * POCKETS_PER_SIDE) + (2 * 2)  # how many lines are printed when printing the board


# Default board layout
#   __13__
# 0   |   12
# 1   |   11
# 2   |   10
# 3   |   9
# 4   |   8
# 5 __|__ 7
#     6