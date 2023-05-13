import sys
import os
from collections import OrderedDict
from util.terminaloutput.symbols import ERROR_SYMBOL
from util.terminaloutput.erasing import erase, erasePreviousLines
from seabattle import sea_battle_client
from anagrams import anagrams_client
from connect4 import connect4_client
from gomoku import gomoku_client
from mancalaavalanche.python import mancala_ava_client
from mancalacapture import mancala_cap_client
from othello import othello_client
from tictactoe import tictactoe_client
from wordbites import word_bites_client
from wordhunt import word_hunt_client

clients = OrderedDict([
	("anagrams", anagrams_client),
	("connect4", connect4_client),
	("gomoku", gomoku_client),
	("mancala-avalanche", mancala_ava_client),
	("mancala-capture", mancala_cap_client),
	("othello", othello_client),
	("seabattle", sea_battle_client),
	("tictactoe", tictactoe_client),
	("wordbites", word_bites_client),
	("wordhunt", word_hunt_client),
])

mode_select_str = """
[1]  Anagrams    (game=anagrams)
[2]  Connect 4   (game=connect4)
[3]  Gomoku 	 (game=gomoku)
[4]  Mancala Avalanche  (game=mancala-avalanche)
[5]  Mancala Capture    (game=mancala-capture)
[6]  Othello	 (game=othello)
[7]  Sea Battle  (game=seabattle)
[8]  Tic Tac Toe (game=tictactoe)
[9]  Word Bites  (game=wordbites)
[10] Word Hunt   (game=wordhunt)
"""
ascii_art = """
              _  __     _      _                               
             | |/ /    | |    ( )                              
             | ' /_   _| | ___|/ ___                           
             |  <| | | | |/ _ \ / __|                          
             | . \ |_| | |  __/ \__ \                          
   _____     |_|\_\__, |_|\___| |___/ _                        
  / ____|          __/ |       |  __ (_)                       
 | |  __  __ _ _ _|___/   ___  | |__) |  __ _  ___  ___  _ __  
 | | |_ |/ _` | '_ ` _ \ / _ \ |  ___/ |/ _` |/ _ \/ _ \| '_ \ 
 | |__| | (_| | | | | | |  __/ | |   | | (_| |  __/ (_) | | | |
  \_____|\__,_|_| |_| |_|\___| |_|   |_|\__, |\___|\___/|_| |_|
     / ____|     | |                  | |__/ |                 
    | (___   ___ | |_   _____ _ __ ___| |___/                  
     \___ \ / _ \| \ \ / / _ \ '__/ __| |                      
     ____) | (_) | |\ V /  __/ |  \__ \_|                      
    |_____/ \___/|_| \_/ \___|_|  |___(_) 
"""


def gamemode_specified():
	"""
	Gets the client for the gamemode specified in the command line params, or None
	"""
	for arg in sys.argv:
		if arg.startswith("game=") and arg.split("=")[1] in clients.keys():
			return clients[arg.split("=")[1]]
	return None


def get_client_from_user():
	"""
	Prompts the user for which game they would like to play. Returns the chosen client
	"""
	print("Please choose one of the options by typing the corresponding number.")
	mode = input(mode_select_str).strip()
	erasePreviousLines(1)
	while not (mode.isnumeric() and 1 <= int(mode) <= 10):
		if mode.lower() == 'q':
			exit(0)
		mode = input(f"{ERROR_SYMBOL} Please choose a valid number:  ").strip()
		erasePreviousLines(1)
	erase(mode_select_str)  # clear client list
	return list(clients.values())[int(mode) - 1]


def create_saves_directory():
	"""Creates the game saves directory if it doesn't exist"""
	if not os.path.isdir("saved_games"):
		os.makedirs("saved_games")


def create_dueling_directory():
	"""Creates the AI dueling directory if it doesn't exist"""
	if not os.path.isdir("dueling"):
		os.makedirs("dueling")


def main():
	client = gamemode_specified()
	if client is None:
		print(ascii_art)
		client = get_client_from_user()
		erase(ascii_art)  # clear ascii art
	create_saves_directory()
	create_dueling_directory()
	client.run()


if __name__ == '__main__':
	main()
