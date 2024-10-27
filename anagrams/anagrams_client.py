# Kyle Gerner
# 2.17.2020 (revamped 3.5.2021)
# Anagrams Game Pigeon tool

from functools import cmp_to_key
from util.terminaloutput.symbols import error, warn, ERROR_SYMBOL
from util.terminaloutput.erasing import erasePreviousLines

english_words = set()
word_starts = set()
found_words = set()

INPUT_FILEPATH = "anagrams/letters7.txt"


def find_words(remaining_letters, curr_str=""):
	"""Finds all the words that can be made with the given letters. Populates the found_words set"""
	if len(curr_str) >= 3 and curr_str not in word_starts:
		return
	if curr_str in english_words:
		found_words.add(curr_str)
	if len(remaining_letters) == 0:
		return
	for i in range(len(remaining_letters)):
		find_words(remaining_letters[:i] + remaining_letters[i+1:], curr_str + remaining_letters[i])


def compare_words(a, b):
	"""The comparison function used for sorting words. Sorts by length, then alphabetically"""
	if len(a) < len(b):
		return 1
	elif len(a) == len(b):
		return -1 if a < b else 1
	return -1


def print_found_words(words):
	"""Prints the valid words that were found, according to user input"""
	count = 1
	print("\n%d %s found.\n" % (len(words), 'word' if len(words) == 1 else 'words'))
	cmd = ''
	while cmd != 'q':
		if cmd == 'a':
			while count <= len(words):
				print("%d.\t%s" % (count, words[count - 1]))
				count += 1
			print()
			return
		for i in range(10):
			print("%d.\t%s" % (count, words[count - 1]))
			count += 1
			if count - 1 == len(words):
				# if reached the end of the list
				print("\nNo more words. ", end='')
				return
		if count + 8 < len(words):
			grammar = "next 10 words"
		else:
			words_remaining = len(words) - count + 1
			if words_remaining > 1:
				grammar = "final %d words" % words_remaining
			else:
				grammar = "final word"
		cmd = input("Press enter for %s, or 'q' to quit, or 'a' for all remaining words:\t" % grammar).strip().lower()
		erasePreviousLines(11)


def populate_word_sets(num_letters):
	"""Fills the sets that will contain words we can search for"""
	try:
		input_file = open(INPUT_FILEPATH, 'r')
		for word in input_file:
			stripped_word = word.rstrip()  # removes newline char
			if len(stripped_word) > num_letters:
				continue
			english_words.add(stripped_word)
			# add each word start to the set of word starts
			for i in range(3, len(stripped_word) + 1):
				word_starts.add(stripped_word[:i])
		input_file.close()
	except FileNotFoundError:
		err_text = f"Could not open the words file. Please make sure {INPUT_FILEPATH.split('/')[-1]} is in the Anagrams directory.\n"
		print()
		error(err_text)
		exit(0)


def run():
	# initial setup
	print("\nWelcome to Kyle's Anagrams Solver Tool!\n")
	num_letters = input("How many letters are on the board? (6 or 7):\t").strip()
	if num_letters.isdigit() and int(num_letters) in {6, 7}:
		num_letters = int(num_letters)
	else:
		erasePreviousLines(1)
		warn("Invalid input. Using default value of 6.")
		num_letters = 6
	populate_word_sets(num_letters)

	# read in user input
	letters = input("Enter the letters on the board, with no spaces in between:  ").strip().lower()
	while len(letters) != num_letters:
		erasePreviousLines(1)
		letters = input(f"{ERROR_SYMBOL} The number of letters did not match the specified max length. Try again:\t").strip().lower()
	erasePreviousLines(1)
	print("The letters are: %s" % " ".join(letters.upper()))

	# call function to find words
	find_words(letters)
	word_cmp_key = cmp_to_key(compare_words)
	valid_words = sorted(list(found_words), key=word_cmp_key)
	if len(valid_words) == 0:
		error("There were no valid words for the board.")
	else:
		print_found_words(valid_words)
	print("Thanks for using my Anagrams Solver Tool!\n")
