# 3.5.2020 Kyle Gerner
# I'll explain my thought process so that if I ever come 
# back to this project then I can maybe have an idea of how
# to continue. The way that I was thinking of implementing this
# was to have a board class that has 16 letterSquare objects 
# which correspond to the letters on the board. Each letterSquare
# object has 8 fields which are the letters that are its border.
# The plan was to go one by one for each letter and recursively 
# check each branch, while marking each letter already visited
# by changing the letterSquare's "checked" field to True. This 
# became more complicated the more I thought about it. So where
# I'm at right now, I think I have the board set up with the letters 
# in the right spots. A question I have is whether or not I am getting 
# a pointer to the letterSquare objects in wordBoard when I reference them, 
# or if I am getting a copy of them. This matters because then setting the 
# checked field to True won't do anything. So anyways, given that everything
# so far works, what I need to do now is to actually search the surrounding 
# letters recursively.


import sys
from collections import Counter

class letterSquare:
	def __init__(self, letter, tl, t, tr, r, br, b, bl, l):
		self.letter = letter
		self.tl = tl
		self.t = t
		self.tr = tr
		self.r = r
		self.br = br 
		self. b = b
		self.bl = bl 
		self.l = l
		self.checked = False
		self.border = [self.tl, self.t, self.tr, self.r, self.br, self.b, self.bl, self.l]

class wordBoard:

	vowels = "aeiouy"
	consonants = "bcdfghjklmnpqrstvwxz"

	def __init__ (self, letters, matches):
		self.letters = letters
		r1 = letters[0:4]
		r2 = letters[4:8]
		r3 = letters[8:12]
		r4 = letters[12:16]
		row1, row2, row3, row4 = [], [], [], []
		l11 = letterSquare(r1[0], None, None, None, r1[1], r2[1], r2[0], None, None)
		l12 = letterSquare(r1[1], None, None, None, r1[2], r2[2], r2[1], r2[0], r1[0])
		l13 = letterSquare(r1[2], None, None, None, r1[3], r2[3], r2[2], r2[1], r1[1])
		l14 = letterSquare(r1[3], None, None, None, None, None, r2[3], r2[2], r1[2])
		l21 = letterSquare(r2[0], None, r1[0], r1[1], r2[1], r3[1], r3[0], None, None)
		l22 = letterSquare(r2[1], r1[0], r1[1], r1[2], r2[2], r3[2], r3[1], r3[0], r2[0])
		l23 = letterSquare(r2[2], r1[1], r1[2], r1[3], r2[3], r3[3], r3[2], r3[1], r2[1])
		l24 = letterSquare(r2[3], r1[2], r1[3], None, None, None, r3[3], r3[2], r2[2])
		l31 = letterSquare(r3[0], None, r2[0], r2[1], r3[1], r4[1], r4[0], None, None)
		l32 = letterSquare(r3[1], r2[0], r2[1], r2[2], r3[2], r4[2], r4[1], r4[0], r3[0])
		l33 = letterSquare(r3[2], r2[1], r2[2], r2[3], r3[3], r4[3], r4[2], r4[1], r3[1])
		l34 = letterSquare(r3[3], r2[2], r2[3], None, None, None, r4[3], r4[2], r3[2])
		l41 = letterSquare(r4[0], None, r3[0], r3[1], r4[1], None, None, None, None)
		l42 = letterSquare(r4[1], r3[0], r3[1], r3[2], r4[2], None, None, None, r4[0])
		l43 = letterSquare(r4[2], r3[1], r3[2], r3[3], r4[3], None, None, None, r4[1])
		l44 = letterSquare(r4[3], r3[2], r3[3], None, None, None, None, None, r4[2])
		self.row1 = [l11, l12, l13, l14]
		self.row2 = [l21, l22, l23, l24]
		self.row3 = [l31, l32, l33, l34]
		self.row4 = [l41, l42, l43, l44]
		self.matches = matches

	def resetBoard(self):
		for row in [self.row1, self.row2, self.row3, self.row4]:
			for let in row:
				let.checked = False

	def getSurroundingLetters(self, index, rowNum):
		if(rowNum == 0):

		elif(rowNum == 1 or rowNum == 2):

		elif(rowNum == 3):

		else:
			return;

	def findCorrespondingLetterSquare(self, letter):
		for row in [self.row1, self.row2, self.row3, self.row4]:
			for let in row:
				if let.letter == letter:
					return let
		return None

	def findMatches(self):
		for row in [self.row1, self.row2, self,row3, self.row4]:
			findMatchesRow(self, row)

	def findMatchesRow(self, row):
		for let in row:
			for bor in let.border:
				#do stuff
				#do stuff
				#do stuff
				#do stuff
				#do stuff
			resetBoard(self)





infile = open("letters7_better.txt", "r")
is4x4 = input("Is this board 4x4? (y/n) ")
if is4x4 != 'y': 
	print("Sorry, only 4x4 boards are supported at this time.")
	sys.exit()
letters = input("Type the board from left to right, top to bottom:\n")
letters = letters.rstrip()
if len(letters) != 16: 
	print("You need 16 letters.")
	sys.exit()
counts = Counter(letters)
matches = []
for line in infile:
	thisline = line.rstrip() #removes newline char
	thiscounts = Counter(thisline)
	count = 0
	for i in thiscounts:
		if i not in counts or thiscounts[i] > counts[i]:
			break
		count = count+thiscounts[i]
	if count == len(thisline):
		matches.append(thisline)

board1 = wordBoard(letters, matches)
board1.findMatches


