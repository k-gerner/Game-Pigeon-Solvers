# For dueling against external AIs
from util.terminaloutput.symbols import error, info
from importlib import import_module
import sys

AI_STRATEGY_DIR_PATH = "external.aiduel."


def _module_of_ai_strategy_file(filename):
	"""Returns the full module name of the corresponding AI strategy file"""
	return f"{AI_STRATEGY_DIR_PATH}{filename}"


def _opposing_ai_module_name():
	"""Reads the command line arguments to determine the name of module for the opposing AI"""
	try:
		index_of_flag = sys.argv.index("-d") if "-d" in sys.argv else sys.argv.index("-aiDuel")
		module = sys.argv[index_of_flag + 1].split(".py")[0]
		return module
	except (IndexError, ValueError):
		error("You need to provide the name of your AI strategy module.")
		exit(0)


def get_dueling_ai_class(player_super_class, strategy_name):
	"""Returns the imported AI Strategy class if the import is valid"""
	duel_ai_module_name = _opposing_ai_module_name()
	try:
		dueling_ai = getattr(import_module(_module_of_ai_strategy_file(duel_ai_module_name)), strategy_name)
		if not issubclass(dueling_ai, player_super_class):
			error(f"Please make sure your AI is a subclass of '{player_super_class.__name__}'")
			exit(0)
		return dueling_ai
	except ImportError:
		error(f"Please provide a valid module to import, located in {AI_STRATEGY_DIR_PATH.replace('.', '/')}")
		info("Pass the name of your Python file as a command line argument.")
		exit(0)
	except AttributeError:
		error(f"Please make sure your AI's class name is '{strategy_name}'")
		exit(0)
