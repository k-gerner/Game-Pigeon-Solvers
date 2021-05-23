# gomoku AI BEFORE trying to implement updateValids

# Contains AI strategy and board manipulation methods

import math # for infinities
import random # for randomizing valid moves list in minimax
from functools import cmp_to_key

EMPTY, BLACK, WHITE = '.', 'X', 'O'
BLACK_HASH_ROW_NUM, WHITE_HASH_ROW_NUM = 0, 1
MAX_DEPTH = 3 # max number of moves ahead to calculate
MAX, MIN = True, False # to be used in minimax
WIN_SCORE = 1000000000 # large enough to always be the preferred outcome
MAX_NEIGHBOR_DIST = 2 # max distance from an already played piece that we want to check if open

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
		score = self.scoreBoard(board, color, self.opponentOf(color))[0]
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

		# will allow me to slightly prioritize checking the spots that are closer to 
		# other pieces by placing them in separate lists
		lists_of_valids = [] 
		for l in range(MAX_NEIGHBOR_DIST):
			lists_of_valids.append([]) 

		def findNearestNeighborDistance(row, col):
			'''Finds the closest neighbor distance. -1 if no neighbor in range'''
			if row == self.BOARD_HEIGHT//2 and col == self.BOARD_WIDTH//2:
				# if exact center spot empty, automatically make it a valid location
				return 1
			for distFromPiece in range(1, MAX_NEIGHBOR_DIST + 1):
				for i in range(-distFromPiece, distFromPiece + 1): # e.g. -1, 0, 1
					for j in range(-distFromPiece, distFromPiece + 1): # e.g. -1, 0, 1
						if i != distFromPiece and i != -distFromPiece and j != distFromPiece and j != -distFromPiece: 
							# if not in the right distance circle
							continue
						if (row + i) % self.BOARD_HEIGHT != (row + i) or (col + j) % self.BOARD_WIDTH != (col + j):
							# if outside of the board range
							continue
						if board[row + i][col + j] != EMPTY:
							# if there is a piece played here
							return distFromPiece
			return -1

		for r in range(self.BOARD_HEIGHT):
			for c in range(self.BOARD_WIDTH):
				foundOtherPieceInRange = False
				if board[r][c] == EMPTY:
					nearestNeighborDistance = findNearestNeighborDistance(r,c)
					if nearestNeighborDistance != -1:
						# append it to the correct list
						lists_of_valids[nearestNeighborDistance - 1].append([r,c])

		# shuffle the moves in each distance level
		# note this will not change the order of the distances, just the moves inside each distance level
		for l in lists_of_valids:
			random.shuffle(l)  # UNCOMMENT --------------------------------------------------------------------------------------------------------------------------------------------------------

		# combine the lists into one big list
		validLocations = [item for innerlist in lists_of_valids for item in innerlist]

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
		# elif len(self.getValidMoves(board)) == 0:
		# getting valid moves this often will slow it down too much, so can just check if an empty spot exists on the board
		for row in board:
			for spot in row:
				if spot == EMPTY:
					return False, None
		return True, None

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
		if moveRow != -1 and moveCol != -1:
			# board not filled
			self.performMove(board, moveRow, moveCol, self.AI_COLOR)
		else:
			# board filled
			self.GAME_OVER = True
		self.checkGameState(board)
		self.BOARD_STATE_DICT = {} 
		return moveRow, moveCol

	def isCoordinateInBoardRange(self, coord):
		'''Checks if the coordinate is valid on the board'''
		rowNum = coord[0]
		colNum = coord[1]
		if rowNum % self.BOARD_HEIGHT == rowNum and colNum % self.BOARD_WIDTH == colNum:
			return True
		else:
			return False


	def checkIfMoveCausedGameOver(self, board, move):
		'''
		Checks the spaces in outward directions to see if the move given caused a win
		returns the winner in [0] (BLACK, WHITE, or None if no winner)
		returns True or False in [1] whether or not the game is over
		'''
		emptySpotSeen = False
		color = board[move[0]][move[1]]
		directionVectorsList = [[1, -1], [1, 0], [1, 1], [0, 1]]
		for directionVector in directionVectorsList:
			numInARow = 1
			currCoordinatesForward = move.copy()
			currCoordinatesBackward = move.copy()
			forwardCheckStillValid = True
			backwardCheckStillValid = True
			outwardSpacesChecked = 0
			while outwardSpacesChecked < 4 and numInARow < 5 and (forwardCheckStillValid or backwardCheckStillValid):
				outwardSpacesChecked += 1
				if forwardCheckStillValid:
					# keep looking in the positive 
					currCoordinatesForward = [a + b for a, b in zip(currCoordinatesForward, directionVector)] # adds the direction vector
					if self.isCoordinateInBoardRange(currCoordinatesForward):
						currForwardSpot = board[currCoordinatesForward[0]][currCoordinatesForward[1]]
						if currForwardSpot == color:
							numInARow += 1
						else:
							if currForwardSpot == EMPTY:
								emptySpotSeen = True
							forwardCheckStillValid = False
					else:
						forwardCheckStillValid = False

				if backwardCheckStillValid:
					currCoordinatesBackward = [a - b for a, b in zip(currCoordinatesBackward, directionVector)] # subtracts the direction vector
					if self.isCoordinateInBoardRange(currCoordinatesBackward):
						currBackwardSpot = board[currCoordinatesBackward[0]][currCoordinatesBackward[1]]
						if currBackwardSpot == color:
							numInARow += 1
						else:
							if currBackwardSpot == EMPTY:
								emptySpotSeen = True
							backwardCheckStillValid = False
					else:
						backwardCheckStillValid = False
			if numInARow >= 5:
				return color, True
		# if we reach here, the move did not cause a win
		if emptySpotSeen:
			return None, False
		for row in board:
			for spot in row:
				if spot == EMPTY:
					# found an empty spot
					return None, False
		return None, True


	def minimax(self, board, depth, maxOrMin, alpha, beta, localMaxDepth):
		'''
		Recursively finds the best move for a given board
		Returns the row in [0], column in [1], and score of the board in [2]
		'''
		if depth == localMaxDepth:
			boardScores = self.scoreBoard(board, self.HUMAN_COLOR, self.AI_COLOR)
			if localMaxDepth % 2 == 0:
				# if AI's turn 1 level past max depth search level
				humanScore = boardScores[0]
				aiScore = boardScores[1] * 2
			else:
				# if human's turn 1 level past max depth search level
				humanScore = boardScores[0] * 2
				aiScore = boardScores[1]
			# NOTE: I used a multiplier above because otherwise the AI may not try to block certain moves
			# example: 	max depth 3; human gets 4 unbounded on depth 2, and AI can get 4 unbounded on depth 3
			#			in this scenario, the point values would essentially cancel out, even though the human
			#			has the clear advantage
			
			# humanScore = boardScores[0]
			# aiScore = boardScores[1]
			return None, None, aiScore - humanScore
			# return None, None, self.scoreBoard(board, self.AI_COLOR) - self.scoreBoard(board, self.HUMAN_COLOR)
		
		validMoves = self.getValidMoves(board)
		if len(validMoves) == 0:
			return -1, -1, 0
		# if localMaxDepth == 1:
		# 	print("for depth = 1, the valid moves are: %s" % str(validMoves))
		# random.shuffle(validMoves) # I now shuffle inside of getValidMoves
		if maxOrMin == MAX:
			# want to maximize this move
			# self.sortMoves(validMoves, board, 0, len(validMoves)-1, self.AI_COLOR)
			score = -math.inf
			bestMove = validMoves[0] # default best move
			# print("valid moves: "+str(validMoves))
			for move in validMoves:
				if depth == 0 and localMaxDepth == 3 and (move == [8,5]):
					abc = 0
				boardCopy = list(map(list, board)) # copies board
				self.performMove(boardCopy, move[0], move[1], self.AI_COLOR)
				dictValOfBoard = self.createZobristValueForBoardState(boardCopy)
				updatedScore = 0 # placeholder
				if dictValOfBoard in self.BOARD_STATE_DICT:
					# print("-"*70 + "  depth = %d" % localMaxDepth)
					# print("move = %s" % str(move))
					# if we've already evaluated the score of this board state
					updatedScore = self.BOARD_STATE_DICT[dictValOfBoard]
					# print("WEVE SEEN A STATE BEFORE")
					
					# _, __, updatedScore = self.minimax(boardCopy, depth + 1, MIN, alpha, beta, localMaxDepth)
					
				else:
					# print("|"*70)
					winner, gameOver = self.checkIfMoveCausedGameOver(boardCopy, move)
					if winner == self.AI_COLOR:
						updatedScore = WIN_SCORE
					elif winner == self.HUMAN_COLOR:
						updatedScore = -1 * WIN_SCORE
					else:
						# no winner
						if gameOver:
							# if board filled
							updatedScore = 0
						else:
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
				# if move == [8,4] and localMaxDepth == 3:
				# 	abc = 0
				boardCopy = list(map(list, board)) # copies board
				self.performMove(boardCopy, move[0], move[1], self.HUMAN_COLOR)
				dictValOfBoard = self.createZobristValueForBoardState(boardCopy)
				if dictValOfBoard in self.BOARD_STATE_DICT:
					updatedScore = self.BOARD_STATE_DICT[dictValOfBoard]
				else:
					winner, gameOver = self.checkIfMoveCausedGameOver(boardCopy, move)
					if winner == self.AI_COLOR:
						updatedScore = WIN_SCORE
					elif winner == self.HUMAN_COLOR:
						updatedScore = -1 * WIN_SCORE
					else:
						# no winner
						if gameOver:
							# if board filled
							updatedScore = 0
						else:
							_, __, updatedScore = self.minimax(boardCopy, depth + 1, MAX, alpha, beta, localMaxDepth)
					self.BOARD_STATE_DICT[dictValOfBoard] = updatedScore
				if updatedScore < score:
					score = updatedScore
					bestMoveForHuman = move
				beta = min(beta, score)
				if beta <= alpha:
					break # pruning
			return bestMoveForHuman[0], bestMoveForHuman[1], score

	def scoreSections(self, board, colorOfEvaluator, colorOfEnemy):
		'''Scores all the different horizontal/vertical/diagonal sections on the board'''
		evaluatorScore = 0
		enemyScore = 0
		if colorOfEvaluator == BLACK:
			evaluatorScoresDict = self.blackThreatsScores
			enemyScoresDict = self.whiteThreatsScores
		else:
			evaluatorScoresDict = self.whiteThreatsScores
			enemyScoresDict = self.blackThreatsScores

		# Check horizontal
		for c in range(self.BOARD_WIDTH - 5):
			for r in range(self.BOARD_HEIGHT):
				section6 = "".join(board[r][c:c + 6])
				section5 = section6[:-1] # first 5 spaces of section 6
				if section6 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section6]
				elif section6 in enemyScoresDict:
					enemyScore += enemyScoresDict[section6]
				if section5 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section5]
				elif section5 in enemyScoresDict:
					enemyScore += enemyScoresDict[section5]
				if c == self.BOARD_WIDTH - 6:
					# if in last section of row
					section5 = section6[1:] # check the rightmost 5 section of the row
					if section5 in evaluatorScoresDict:
						evaluatorScore += evaluatorScoresDict[section5]
					elif section5 in enemyScoresDict:
						enemyScore += enemyScoresDict[section5]

		# Check vertical
		for c in range(self.BOARD_WIDTH):
			for r in range(self.BOARD_HEIGHT - 5):
				section6 = ''
				for i in range(6):
					section6 += board[r + i][c]
				section5 = section6[:-1] # first 5 spaces of section 6
				if section6 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section6]
				elif section6 in enemyScoresDict:
					enemyScore += enemyScoresDict[section6]
				if section5 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section5]
				elif section5 in enemyScoresDict:
					enemyScore += enemyScoresDict[section5]
				if r == self.BOARD_HEIGHT - 6:
					# if in last section of col
					section5 = section6[1:] # check the bottom 5 section of the col
					if section5 in evaluatorScoresDict:
						evaluatorScore += evaluatorScoresDict[section5]
					elif section5 in enemyScoresDict:
						enemyScore += enemyScoresDict[section5]

		# Check diagonal from bottom left to top right
		for c in range(self.BOARD_WIDTH - 5):
			for r in range(self.BOARD_HEIGHT - 5):
				section6 = ''
				for i in range(6):
					section6 += board[r + i][c + i]
				section5 = section6[:-1]
				if section6 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section6]
				elif section6 in enemyScoresDict:
					enemyScore += enemyScoresDict[section6]
				if section5 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section5]
				elif section5 in enemyScoresDict:
					enemyScore += enemyScoresDict[section5]
				if c == self.BOARD_WIDTH - 6 or r == self.BOARD_HEIGHT - 6:
					# if in last section of this diagonal path
					section5 = section6[1:] # check the border section
					if section5 in evaluatorScoresDict:
						evaluatorScore += evaluatorScoresDict[section5]
					elif section5 in enemyScoresDict:
						enemyScore += enemyScoresDict[section5]
		
		# Check diagonal from bottom right to top left
		for c in range(self.BOARD_WIDTH - 5):
			for r in range(5, self.BOARD_HEIGHT):
				section6 = ''
				for i in range(6):
					section6 += board[r - i][c + i]
				section5 = section6[:-1]
				if section6 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section6]
				elif section6 in enemyScoresDict:
					enemyScore += enemyScoresDict[section6]
				if section5 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section5]
				elif section5 in enemyScoresDict:
					enemyScore += enemyScoresDict[section5]
				if c == self.BOARD_WIDTH - 6 or r == self.BOARD_HEIGHT - 1:
					# if in last section of this diagonal path
					section5 = section6[1:] # check the border section
					if section5 in evaluatorScoresDict:
						evaluatorScore += evaluatorScoresDict[section5]
					elif section5 in enemyScoresDict:
						enemyScore += enemyScoresDict[section5]

		return evaluatorScore, enemyScore

	def scorePositionWeights(self, board, colorOfEvaluator, colorOfEnemy):
		'''Scores the board based on the weights of the individual locations (center preferred)'''
		evaluatorScore = 0
		enemyScore = 0
		for row in range(self.BOARD_HEIGHT):
			for col in range(self.BOARD_WIDTH):
				currSpot = board[row][col]
				if currSpot == colorOfEvaluator:
					evaluatorScore += self.positionWeightsMatrix[row][col]
				elif currSpot == colorOfEnemy:
					enemyScore += self.positionWeightsMatrix[row][col]
		# print('score of pos weights = %d' % score)
		return evaluatorScore, enemyScore


	def scoreBoard(self, board, colorOfEvaluator, colorOfEnemy):
		'''Scores the entire board'''
		sectionsScores = self.scoreSections(board, colorOfEvaluator, colorOfEnemy)
		positionWeightScores = self.scorePositionWeights(board, colorOfEvaluator, colorOfEnemy)
		evaluatorScore = sectionsScores[0] + positionWeightScores[0]
		enemyScore = sectionsScores[1] + positionWeightScores[1]
		return evaluatorScore, enemyScore

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



