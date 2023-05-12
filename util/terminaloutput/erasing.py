# Special Characters
CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'


def erasePreviousLines(numLines):
	"""Erases the specified previous number of lines from the terminal"""
	print(f"{CURSOR_UP_ONE}{ERASE_LINE}" * max(numLines, 0), end='')
