# Contains AI strategy and board manipulation methods

import math # for infinities
import random # for randomizing valid moves list in minimax
from functools import cmp_to_key

EMPTY, BLACK, WHITE = '.', 'X', 'O'
BLACK_HASH_ROW_NUM, WHITE_HASH_ROW_NUM = 0, 1
MAX_DEPTH = 2 # max number of moves ahead to calculate
MAX, MIN = True, False # to be used in minimax
WIN_SCORE = 1000000000 # large enough to always be the preferred outcome

# class for the A.I.
class Strategy(object):

	def __init__(self, boardDimension, humanColor):
		'''Initializes the board attributes'''
		print("THIS PRINT IS IN INIT. CURRENT MAX DEPTH = %d%s" % (MAX_DEPTH, '--------'*80))
		self.GAME_OVER = False
		self.HUMAN_COLOR = humanColor
		self.AI_COLOR = self.opponentOf(humanColor)
		self.BOARD_WIDTH = boardDimension 
		self.BOARD_HEIGHT = boardDimension 
		# RANDOM_HASH_TABLE will be used for Zobrist Hashing.
		# Table has DIM * DIM * 2 entries, with each being a random number that will 
		# represent a number for if a certain piece is played in a certain position 
		# on the board. This will be used for XORing in the Zobrist Hashing.
		self.RANDOM_HASH_TABLE = self.createHashTable(boardDimension)
		# BOARD_STATE_DICT will be a map that maps board-state hashes to a list containing
		# important information about the board at that board-state
		# NOTE this transposition table will be cleared between different depth searches.
		# This is because I'm not quite sure how to know which boards to not explore if the 
		# depth increases. This should still help with pruning, but not as much as it would 
		# otherwise.
		self.BOARD_STATE_DICT = {} 
		self.createThreatSequencesDictionary()
		self.createBoardPositionWeights(boardDimension)

	def createThreatSequencesDictionary(self):
		'''Creates the dictionaries that will help score board sections'''
		self.blackThreatsScores = {
			'.XXXX.' : 10000,	# 4 double open, next move guaranteed win
			'.XXXX'  : 100,		# 4 single open
			'XXXX.'	 : 100, 	# 4 single open
			'X.XXX'	 : 90,		# 1-3 single open
			'XX.XX'	 : 85,		# 2-2 single open
			'XXX.X'	 : 90,		# 1-3 single open
			'.XXX.'	 : 30,		# 3 double open
			'OXXXX.' : 80,		# 4 single open
			'.XXXXO' : 80,		# 4 single open
			'.X.XX.' : 25,		# broken 3
			'.XX.X.' : 25		# broken 3
		}
		self.whiteThreatsScores = {
			'.OOOO.' : 10000,	# 4 double open, next move guaranteed win
			'.OOOO'  : 100,		# 4 single open
			'OOOO.'	 : 100, 	# 4 single open
			'O.OOO'	 : 90,		# 1-3 single open
			'OO.OO'	 : 85,		# 2-2 single open
			'OOO.O'	 : 90,		# 1-3 single open
			'.OOO.'	 : 30,		# 3 double open
			'XOOOO.' : 80,		# 4 single open
			'.OOOOX' : 80,		# 4 single open
			'.O.OO.' : 25,		# broken 3
			'.OO.O.' : 25		# broken 3
		}

	def createBoardPositionWeights(self, dim):
		'''
		Create the position weights matrix for a board of dimension `dim`
		Center weighted heavier
		'''
		self.positionWeightsMatrix = []
		for i in range(dim):
			self.positionWeightsMatrix.append([0]*dim) # create dim x dim matrix of 0s
		centerIndex = dim//2
		for i in range(dim//2):
			for row in range(centerIndex - i, centerIndex + i + 1):
				for col in range(centerIndex - i, centerIndex + i + 1):
					self.positionWeightsMatrix[row][col] += 3

	def createHashTable(self, dimension):
		'''Fills a 2 by dimension board with random 64 bit integers'''
		table = [] # 2D
		for color in range(2):
			colorLocationList = []
			for boardPos in range(dimension * dimension):
				colorLocationList.append(random.getrandbits(64))
			table.append(colorLocationList)
		return table

	def createZobristValueForBoardState(self, board):
		'''Creates the Zobrist Hashing value for a boardstate'''
		totalXOR = 0
		for row in range(self.BOARD_HEIGHT):
			for col in range(self.BOARD_WIDTH):
				piece = board[row][col]
				if piece != EMPTY:
					hash_row = BLACK_HASH_ROW_NUM if piece == BLACK else WHITE_HASH_ROW_NUM
					hash_val = self.RANDOM_HASH_TABLE[hash_row][row*self.BOARD_WIDTH + col]
					totalXOR = totalXOR ^ hash_val # ^ = XOR operator
					# print("totalXOR = %s\thash_val = %s" % (str(totalXOR), str(hash_val)))
		# print("totalXOR = %d" % totalXOR)
		return totalXOR

	def opponentOf(self, color):
		'''Get the opposing color'''
		return WHITE if color == BLACK else BLACK

	def checkGameState(self, board):
		'''Sets the GAME_OVER var to True if there is a winner'''
		if self.isTerminal(board)[0]: 
		 	self.GAME_OVER = True

	def evaluateScoreFromMove(self, board, move, color):
		'''Checks the score of the board for `color` if `move` is played on `board`'''
		self.performMove(board, move[0], move[1], color)
		score = self.scoreBoard(board, color)
		self.performMove(board, move[0], move[1], EMPTY) # undo the move
		return score

	def partition(self, movesList, board, low, high, color):
		'''Places every element greater than pivot to the left, less than pivot to the right'''
		i = low-1
		pivot = self.evaluateScoreFromMove(board, movesList[high], color)     # pivot
		for j in range(low, high):
		    if self.evaluateScoreFromMove(board, movesList[j], color) > pivot:
		        i = i+1
		        movesList[i], movesList[j] = movesList[j], movesList[i]

		movesList[i+1], movesList[high] = movesList[high], movesList[i+1]
		return i+1

	def sortMoves(self, movesList, board, low, high, color):
		'''Sorts the list of moves via Quick Sort'''
		if len(movesList) == 1:
		    return movesList
		if low < high:
		    partition_index = self.partition(movesList, board, low, high, color)

		    self.sortMoves(movesList, board, low, partition_index-1, color)
		    self.sortMoves(movesList, board, partition_index+1, high, color)

	def isValidMove(self, board, row, col):
		'''Checks if the spot is available'''
		return board[row][col] == EMPTY

	def getValidMoves(self, board):
		'''Returns a list of valid moves (moves in the center area or near other pieces)'''
		validLocations = []
		h = self.BOARD_HEIGHT
		w = self.BOARD_WIDTH
		max_dist_from_neighbor = 2 # max distance from an already played piece that we want to check
		# for r in range(len(board)):
		# 	for c in range(len(board)):
		# 		if self.isValidMove(board, r, c):
		# 			validLocations.append([r, c])

		# will allow me to slightly prioritize checking the spots that are closer to 
		# other pieces by placing them in separate lists
		# lists_of_valids = [[]] * (max_dist_from_neighbor + 1) 

		def spotIsNearOtherPieces(row, col):
			# if row in range(h//2 - h//4, h//2 + h//4 + 1) and col in range(w//2 - w//4, w//2 + w//4 + 1):
			# 	# if in middle section of board
			# 	# lists_of_valids[-1].append([row, col])
			# 	return True
			if row == h//2 and col == w//2 and board[row][col] == EMPTY:
				# if exact center spot empty
				# lists_of_valids[-1].append([row, col])
				return True
			for r2 in range(max(0, row - max_dist_from_neighbor), min(h, row + max_dist_from_neighbor + 1)):
				for c2 in range(max(0, col - max_dist_from_neighbor), min(w, col + max_dist_from_neighbor + 1)):
					if board[r2][c2] != EMPTY:
						# if there is a piece within `max_dist_from_neighbor` spots from this square
						# dist_from_neighbor = max(abs(r2-row), abs(c2-col))
						# lists_of_valids[dist_from_neighbor].append([row, col])
						return True
			return False

		for r in range(self.BOARD_HEIGHT):
			for c in range(self.BOARD_WIDTH):
				foundOtherPieceInRange = False
				if board[r][c] == EMPTY:
					if spotIsNearOtherPieces(r,c):
						validLocations.append([r,c])

		return validLocations
		# combined_list = [item for sublist in lists_of_valids for item in sublist]
		# return combined_list

	def performMove(self, board, row, col, color):
		'''Performs a given move on the board'''
		board[row][col] = color

	def isTerminal(self, board):
		'''
		Checks if the current board state is Game Over
		Returns a tuple, with [0] being the True or False value
		[1] being the winning color (None if neither color wins)
		'''
		winner = self.findWinner(board)
		if winner != None:
			return True, winner
		elif len(self.getValidMoves(board)) == 0:
			return True, None
		else:
			return False, None

	def findWinner(self, board):
		'''
		Checks if there is a winner
		returns the color of the winner if there is one, otherwise None
		'''
		# Check horizontal
		for row in board:
			for col in range(self.BOARD_WIDTH - 4):
				if row[col] == row[col+1] == row[col+2] == row[col+3] == row[col+4] != EMPTY:
					return row[col]

		# Check vertical
		for c in range(self.BOARD_WIDTH):
			for r in range(self.BOARD_HEIGHT - 4):
				if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == board[r+4][c] != EMPTY:
					return board[r][c]

		# Check diagonal from bottom left to top right
		for c in range(self.BOARD_WIDTH - 4):
			for r in range(self.BOARD_HEIGHT - 4):
				if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == board[r+4][c+4]!= EMPTY:
					return board[r][c]

		# Check diagonal from bottom right to top left
		for c in range(self.BOARD_WIDTH - 4):
			for r in range(4, self.BOARD_HEIGHT):
				if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == board[r-4][c+4] != EMPTY:
					return board[r][c]

		return None

	def playBestMove(self, board):
		'''Calculates and performs the best move for the AI for the given board'''
		x = input("It's the AI's turn, press enter for it to play.\t").strip().lower()
		if x == 'q':
			print("\nThanks for playing!\n")
			exit(0)
		moveRow, moveCol, score = -123, -123, -123 # placeholders
		for i in range(1, MAX_DEPTH + 1): # iterative deepening
			# this will prioritize game winning movesets that occur with less total moves
			moveRow, moveCol, score = self.minimax(board, 0, MAX, -math.inf, math.inf, i)
			self.BOARD_STATE_DICT.clear() # clear the dict after every depth increase
			# ^ ideally I shouldn't do this, but I don't know how to implement it otherwise yet
			if score >= WIN_SCORE:
				break
		print("score for move: %d" % score)
		self.performMove(board, moveRow, moveCol, self.AI_COLOR)
		self.checkGameState(board)
		self.BOARD_STATE_DICT = {} 
		return moveRow, moveCol

	def minimax(self, board, depth, maxOrMin, alpha, beta, localMaxDepth):
		'''
		Recursively finds the best move for a given board
		Returns the row in [0], column in [1], and score of the board in [2]
		'''
		validMoves = self.getValidMoves(board)
		# if localMaxDepth == 1:
		# 	print("valid moves: %s" % str(validMoves))
		gameOver, winner = self.isTerminal(board)
		if gameOver:
			if winner == self.AI_COLOR:
				return None, None, WIN_SCORE
			elif winner == self.HUMAN_COLOR:
				return None, None, -1 * WIN_SCORE
			else:
				# no winner
				return None, None, 0
		if depth == localMaxDepth:
			return None, None, self.scoreBoard(board, self.AI_COLOR) - self.scoreBoard(board, self.HUMAN_COLOR)
		
		# random.shuffle(validMoves)
		if maxOrMin == MAX:
			# want to maximize this move
			# self.sortMoves(validMoves, board, 0, len(validMoves)-1, self.AI_COLOR)
			score = -math.inf
			bestMove = validMoves[0] # default best move
			# print("valid moves: "+str(validMoves))
			for move in validMoves:
				
				boardCopy = list(map(list, board)) # copies board
				self.performMove(boardCopy, move[0], move[1], self.AI_COLOR)
				dictValOfBoard = self.createZobristValueForBoardState(boardCopy)
				updatedScore = 0 # placeholder
				if dictValOfBoard in self.BOARD_STATE_DICT:
					# print("-"*70 + "  depth = %d" % localMaxDepth)
					# print("move = %s" % str(move))
					# if we've already evaluated the score of this board state
					updatedScore = self.BOARD_STATE_DICT[dictValOfBoard]
					
					# _, __, updatedScore = self.minimax(boardCopy, depth + 1, MIN, alpha, beta, localMaxDepth)
					
				else:
					# print("|"*70)
					_, __, updatedScore = self.minimax(boardCopy, depth + 1, MIN, alpha, beta, localMaxDepth)
					self.BOARD_STATE_DICT[dictValOfBoard] = updatedScore
				# if move == [6, 6]:
				# 	print("score for G7 = %d\tweightMatrix for G7 = %d" % (updatedScore, self.positionWeightsMatrix[6][6]))
				if updatedScore > score:
					score = updatedScore
					bestMove = move
				alpha = max(alpha, score)
				# if depth == 0:
				# 	print("Score for slot %d = %d. Max depth = %d" % (move, updatedScore, localMaxDepth))
				if alpha >= beta:
					break # pruning
			return bestMove[0], bestMove[1], score
		else:
			# want to minimize this move
			# self.sortMoves(validMoves, board, 0, len(validMoves)-1, self.HUMAN_COLOR)
			score = math.inf
			bestMoveForHuman = validMoves[0]
			for move in validMoves:
				boardCopy = list(map(list, board)) # copies board
				self.performMove(boardCopy, move[0], move[1], self.HUMAN_COLOR)
				_, __, updatedScore = self.minimax(boardCopy, depth + 1, MAX, alpha, beta, localMaxDepth)
				if updatedScore < score:
					score = updatedScore
					bestMoveForHuman = move
				beta = min(beta, score)
				if beta <= alpha:
					break # pruning
			return bestMoveForHuman[0], bestMoveForHuman[1], score

	def scoreSections(self, board, color):
		'''Scores all the different horizontal/vertical/diagonal sections on the board'''
		score = 0
		scoresDict = self.blackThreatsScores if color == BLACK else self.whiteThreatsScores

		# Check horizontal
		for c in range(self.BOARD_WIDTH - 5):
			for r in range(self.BOARD_HEIGHT):
				section6 = "".join(board[r][c:c + 6])
				section5 = section6[:-1] # first 5 spaces of section 6
				if section6 in scoresDict:
					score += scoresDict[section6]
				if section5 in scoresDict:
					score += scoresDict[section5]
				if c == self.BOARD_WIDTH - 6:
					# if in last section of row
					section5 = section6[1:] # check the rightmost 5 section of the row
					if section5 in scoresDict:
						score += scoresDict[section5]

		# Check vertical
		for c in range(self.BOARD_WIDTH):
			for r in range(self.BOARD_HEIGHT - 5):
				section6 = ''
				for i in range(6):
					section6 += board[r + i][c]
				section5 = section6[:-1] # first 5 spaces of section 6
				if section6 in scoresDict:
					score += scoresDict[section6]
				if section5 in scoresDict:
					score += scoresDict[section5]
				if r == self.BOARD_HEIGHT - 6:
					# if in last section of col
					section5 = section6[1:] # check the bottom 5 section of the col
					if section5 in scoresDict:
						score += scoresDict[section5]

		# Check diagonal from bottom left to top right
		for c in range(self.BOARD_WIDTH - 5):
			for r in range(self.BOARD_HEIGHT - 5):
				section6 = ''
				for i in range(6):
					section6 += board[r + i][c + i]
				section5 = section6[:-1]
				if section6 in scoresDict:
					score += scoresDict[section6]
				if section5 in scoresDict:
					score += scoresDict[section5]
				if c == self.BOARD_WIDTH - 6 or r == self.BOARD_HEIGHT - 6:
					# if in last section of this diagonal path
					section5 = section6[1:] # check the border section
					if section5 in scoresDict:
						score += scoresDict[section5]
		
		# Check diagonal from bottom right to top left
		for c in range(self.BOARD_WIDTH - 5):
			for r in range(5, self.BOARD_HEIGHT):
				section6 = ''
				for i in range(6):
					section6 += board[r - i][c + i]
				section5 = section6[:-1]
				if section6 in scoresDict:
					score += scoresDict[section6]
				if section5 in scoresDict:
					score += scoresDict[section5]
				if c == self.BOARD_WIDTH - 6 or r == self.BOARD_HEIGHT - 1:
					# if in last section of this diagonal path
					section5 = section6[1:] # check the border section
					if section5 in scoresDict:
						score += scoresDict[section5]

		return score

	def scorePositionWeights(self, board, color):
		'''Scores the board based on the weights of the individual locations (center preferred)'''
		score = 0
		for row in range(self.BOARD_HEIGHT):
			for col in range(self.BOARD_WIDTH):
				if board[row][col] == color:
					score += self.positionWeightsMatrix[row][col]
		# print('score of pos weights = %d' % score)
		return score


	def scoreBoard(self, board, color):
		'''Scores the entire board'''
		return self.scoreSections(board, color) + self.scorePositionWeights(board, color)
		
		# Give a slight bonus to pieces in the middle area
		# for r in range(self.BOARD_WIDTH//4, self.BOARD_WIDTH - self.BOARD_WIDTH//4):
		# 	for c in range(self.BOARD_HEIGHT//4, self.BOARD_HEIGHT - self.BOARD_HEIGHT//4):
		# 		if board[r][c] == color:
		# 			score += 2

		# Give another bonus for piece in the center
		# if board[self.BOARD_WIDTH//2][self.BOARD_HEIGHT//2] == color:
		# 	score += 4

	# def longestSequenceOfPiece(self, section, color):
	# 	'''Finds the longest consecutive sub-sequence of a piece in a section'''
	# 	maxStreak = 0
	# 	streak = 0
	# 	for spot in section:
	# 		if spot == color:
	# 			streak += 1
	# 			maxStreak = max(maxStreak, streak)
	# 		else:
	# 			streak = 0
	# 	return maxStreak

	# def scoreSection(self, section, color):
	# 	'''Looks at the given length 5 section and scores it'''
	# 	opponentColor = self.opponentOf(color)
	# 	numMyColor = section.count(color)
	# 	numOppColor = section.count(opponentColor)
	# 	numEmpty = section.count(EMPTY)

	# 	if numMyColor == 5:
	# 		return WIN_SCORE
	# 	elif numMyColor == 4:
	# 		if numEmpty == 1:
	# 			return 30 * self.longestSequenceOfPiece(section, color)
	# 		else:
	# 			return 35
	# 	elif numMyColor == 3 and numEmpty == 2:
	# 		if section[0] == section[4] == EMPTY:
	# 			# if unbounded on both sides
	# 			return 20 * self.longestSequenceOfPiece(section, color)
	# 		else:
	# 			return 17
	# 	elif numMyColor == 2 and numEmpty == 3:
	# 		return 5 * self.longestSequenceOfPiece(section, color)
	# 	elif numOppColor == 4:
	# 		if numEmpty == 1:
	# 			return -30 * self.longestSequenceOfPiece(section, opponentColor)
	# 		else:
	# 			return -35
	# 	elif numOppColor == 3 and numEmpty == 2:
	# 		if section[0] == section[4] == EMPTY:
	# 			return -20 * self.longestSequenceOfPiece(section, opponentColor)
	# 		else:
	# 			return -17
	# 	elif numOppColor == 2 and numEmpty == 3:
	# 		return -5 * self.longestSequenceOfPiece(section, opponentColor)
	# 	else:
	# 		return 0

	# def scoreBoard(self, board, color):
	# 	'''Scores the entire board'''
	# 	score = 0

	# 	# Give a slight bonus to pieces in the middle area
	# 	for r in range(self.BOARD_WIDTH//4, self.BOARD_WIDTH - self.BOARD_WIDTH//4):
	# 		for c in range(self.BOARD_HEIGHT//4, self.BOARD_HEIGHT - self.BOARD_HEIGHT//4):
	# 			if board[r][c] == color:
	# 				score += 2

	# 	# Give another bonus for piece in the center
	# 	if board[self.BOARD_WIDTH//2][self.BOARD_HEIGHT//2] == color:
	# 		score += 4

	# 	# Check horizontal
	# 	for c in range(self.BOARD_WIDTH - 4):
	# 		for r in range(self.BOARD_HEIGHT):
	# 			score += self.scoreSection(board[r][c:c + 5], color)
				

	# 	# Check vertical
	# 	for c in range(self.BOARD_WIDTH):
	# 		for r in range(self.BOARD_HEIGHT - 4):
	# 			section = []
	# 			for i in range(5):
	# 				section.append(board[r + i][c])
	# 			score += self.scoreSection(section, color)

	# 	# Check diagonal from bottom left to top right
	# 	for c in range(self.BOARD_WIDTH - 4):
	# 		for r in range(self.BOARD_HEIGHT - 4):
	# 			section = []
	# 			for i in range(5):
	# 				section.append(board[r + i][c + i])
	# 			score += self.scoreSection(section, color)
		
	# 	# Check diagonal from bottom right to top left
	# 	for c in range(self.BOARD_WIDTH - 4):
	# 		for r in range(4, self.BOARD_HEIGHT):
	# 			section = []
	# 			for i in range(5):
	# 				section.append(board[r - i][c + i])
	# 			score += self.scoreSection(section, color)

	# 	return score



