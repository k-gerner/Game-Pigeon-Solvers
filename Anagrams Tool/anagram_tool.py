# Kyle Gerner
# 2.17.2020 (revamped 3.5.2021)
# Anagrams Game Pigeon tool

from functools import cmp_to_key

englishWords = set()
wordStarts = set()
foundWords = set()

INPUT_FILENAME = "letters7.txt"

RED_COLOR = '\033[91m'
NO_COLOR = '\033[0m'
ERROR_SYMBOL = f"{RED_COLOR}<!>{NO_COLOR}"

def findWords(letters, currStr=""):
	"""Finds all the words that can be made with the given letters. Populates the foundWords set"""
	if len(currStr) >= 3 and currStr not in wordStarts:
		return
	if currStr in englishWords:
		foundWords.add(currStr)
	if len(letters) == 0:
		return
	for i in range(len(letters)):
		findWords(letters[:i] + letters[i+1:], currStr + letters[i])

def wordCompare(a, b):
	"""The comparison function used for sorting words. Sorts by length, then alphabetically"""
	if len(a) < len(b):
		return 1
	elif len(a) == len(b):
		return -1 if a < b else 1
	return -1

def printFoundWords(words):
	"""Prints the valid words that were found, according to user input"""
	count = 1
	print("\n%d word%s found.\n" % (len(words), '' if len(words) == 1 else 's'))
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
			wordsLeft = len(words) - count + 1
			if wordsLeft > 1:
				grammar = "final %d words" % wordsLeft
			else:
				grammar = "final word"
		cmd = input("Press enter for %s, or 'q' to quit, or 'a' for all:\t" % grammar).rstrip()

def populateWordSets(numLetters):
	"""Fills the sets that will contain words we can search for"""
	try :
		inputFile = open(INPUT_FILENAME, 'r')
		for word in inputFile:
			strippedWord = word.rstrip() #removes newline char
			if len(strippedWord) > numLetters:
				continue
			englishWords.add(strippedWord)
			# add each word start to the set of word starts
			for i in range(3, len(strippedWord) + 1):
				wordStarts.add(strippedWord[:i])
		inputFile.close()
	except FileNotFoundError:
		print(f"\n{ERROR_SYMBOL} Could not open the file. Please make sure %s is in the current directory, and run this file from inside the current directory.\n" % INPUT_FILENAME)
		exit(0)

def main():
	# initial setup
	print("Welcome to Kyle's Anagrams Solver Tool!\n")
	numLetters = input("How many letters are on the board? (6 or 7):\t").strip()
	if numLetters.isnumeric() and (int(numLetters) == 6 or int(numLetters) == 7):
		numLetters = int(numLetters)
	else:
		print(f"{ERROR_SYMBOL} Invalid input. Using default value of 6 instead.")
		numLetters = 6
	populateWordSets(numLetters)

	# read in user input
	letters = input("Enter the letters on the board, with no spaces in between:  ").strip()
	while len(letters) != numLetters:
		print(f"{ERROR_SYMBOL} The number of letters did not match the specified max length. Try again.\n")
		letters = input("Enter the letters on the board, with no spaces in between:\t").rstrip()

	# call function to find words
	findWords(letters)
	word_cmp_key = cmp_to_key(wordCompare)
	validWords = sorted(list(foundWords), key=word_cmp_key)
	if len(validWords) == 0:
		print(f"{ERROR_SYMBOL} There were no valid words for the board.")
	else:
		printFoundWords(validWords)
	print("Thanks for using my Anagrams Solver Tool!\n")


if __name__ == '__main__':
	main()