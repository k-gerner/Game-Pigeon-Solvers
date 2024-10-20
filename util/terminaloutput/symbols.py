from util.terminaloutput.colors import RED_COLOR, BLUE_COLOR, YELLOW_COLOR, NO_COLOR

ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"
WARN_SYMBOL = f"{YELLOW_COLOR}<!>{NO_COLOR}"
INFO_SYMBOL = f"{BLUE_COLOR}<!>{NO_COLOR}"


def info(text):
	"""Prints an info message to the terminal."""
	print(f"{INFO_SYMBOL} {text}")


def warn(text):
	"""Prints a warning message to the terminal."""
	print(f"{WARN_SYMBOL} {text}")


def error(text):
	"""Prints an error message to the terminal."""
	print(f"{ERROR_SYMBOL} {text}")
