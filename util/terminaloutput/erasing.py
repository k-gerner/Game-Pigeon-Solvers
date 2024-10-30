# Special Characters
CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'

# To allow disabling of erase mode
ENABLED = True


def set_erase_mode(is_enabled: bool):
	"""Turns erasing on or off"""
	global ENABLED
	ENABLED = is_enabled


def erase_previous_lines(num_lines:int):
	"""Erases the specified previous number of lines from the terminal"""
	if ENABLED:
		print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(num_lines, 0), end='')


def erase(output_str:str):
	"""Erases the number of lines printed by the given string"""
	erase_previous_lines(output_str.count("\n") + 1)