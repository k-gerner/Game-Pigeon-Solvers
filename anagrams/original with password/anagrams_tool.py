# Kyle Gerner
# 2.17.2020
# Anagram Game Pigeon tool
#
#
# edit password feature before sharing
#
#

def findMatches(filename, size, verify):
	ifile = open(filename, "r")
	#ofile = open("output.txt", "w")
	letters = input("Input letters:   ")
	matches = []
	if not verify:
		sys.exit()
	if len(letters) != size:
		print("Number of letters does not match input.")
		sys.exit()
	counts = Counter(letters)
	for line in ifile:
		thisline = line.rstrip() #removes newline char
		thiscounts = Counter(thisline)
		count = 0
		for i in thiscounts:
			if i not in counts or thiscounts[i] > counts[i]:
				break
			count = count+thiscounts[i]
		if count == len(thisline):
			matches.append(thisline)

	matchesSorted = sorted(matches, key=len, reverse=True)
	printlist(matchesSorted)
	#l = len(matchesSorted)
	#for i in range(l):
	#	ofile.write(matchesSorted[l-i-1]+"\n")
	ifile.close()
	#ofile.close()


def printlist(list):
	count = 1
	for i in list:
		print(str(count) + ":  " + i)
		count = count+1

def passwordCheck(pw):
	return hashlib.sha256(pw.encode()).hexdigest() == "26c109b14ad2d3c1f67ae838ffb278b5b083f0a8626afc67d02cbd18568e5721"


from collections import Counter
import sys
import hashlib

pas = input("Whats the password? ") #victorisgay
verify = passwordCheck(pas)
if(not verify):
	print("Thats not the password.")
	sys.exit()
s = input("How many letters? (6 or 7)  ")
try:
	size = int(s)
except ValueError:
	print("Enter a valid number.")
	sys.exit()
if size == 6:
	version = input("Use old version (more words, may not be in dictionary)? (type 'y' for yes)  ")
	if version == 'y':
		findMatches("letters6.txt", 6, verify)
	else:
		findMatches("letters6_better.txt", 6, verify)
elif size == 7:
	version = input("Use old version (more words, may not be in dictionary)? (type 'y' for yes)  ")
	if version == 'y':
		findMatches("letters7.txt", 7, verify)
	else:
		findMatches("letters7_better.txt", 7, verify)
else:
	print("Invalid input. Choose 6 or 7 next time.")