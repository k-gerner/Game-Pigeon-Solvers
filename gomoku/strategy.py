# Contains AI strategy and board manipulation methods

import math # for infinities
import random # for randomizing valid moves list in minimax
import sys # for better progress bar formatting
from Player import Player # super class

#### DO NOT MODIFY ####
EMPTY, BLACK, WHITE = '.', 'X', 'O'
BLACK_HASH_ROW_NUM, WHITE_HASH_ROW_NUM = 0, 1
MAX, MIN = True, False # to be used in minimax
WIN_SCORE = 1000000000 # large enough to always be the preferred outcome
#######################
####### MODIFY ########
MAX_NEIGHBOR_DIST = 2 # max distance from an already played piece that we want to check if open
MAX_NUM_MOVES_TO_EVALUATE = 15 # most moves we want to evaluate at once for any given board
MAX_DEPTH = 6 # max number of moves ahead to calculate
#######################

# class for the A.I.
class GomokuStrategy(Player):

	def __init__(self, color, boardDimension=13):
		"""Initializes the board attributes"""
		super().__init__(color, boardDimension)
		self.GAME_OVER = False
		self.AI_COLOR = color
		self.HUMAN_COLOR = opponentOf(color)
		# RANDOM_HASH_TABLE will be used for Zobrist Hashing.
		# Table has DIM * DIM * 2 entries, with each being a random number that will 
		# represent a number for if a certain piece is played in a certain position 
		# on the board. This will be used for XORing in the Zobrist Hashing.
		self.RANDOM_HASH_TABLE = self.createHashTable(boardDimension)
		# BOARD_STATE_DICT will be a map that maps board-state hashes to a list containing
		# important information about the board at that board-state (the score)
		# NOTE this transposition table will be cleared between different depth searches.
		# Maintaining the transposition table between different depth searches could help prune
		# even further, but it would require me to define some minimum score that determines whether
		# or not it would be worth it to search this path at a deeper depth
		self.BOARD_STATE_DICT = {} 
		self.createThreatSequencesDictionary()
		self.createBoardPositionWeights(boardDimension)

	def createThreatSequencesDictionary(self):
		"""Creates the dictionaries that will help score board sections"""
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
		"""
		Create the position weights matrix for a board of dimension `dim`
		Center weighted heavier
		"""
		self.positionWeightsMatrix = []
		for i in range(dim):
			self.positionWeightsMatrix.append([0]*dim) # create dim x dim matrix of 0s
		centerIndex = dim//2
		for i in range(dim//2):
			for row in range(centerIndex - i, centerIndex + i + 1):
				for col in range(centerIndex - i, centerIndex + i + 1):
					self.positionWeightsMatrix[row][col] += 3

	def createHashTable(self, dimension):
		"""Fills a 2 by dimension board with random 64 bit integers"""
		table = [] # 2D
		for color in range(2):
			colorLocationList = []
			for boardPos in range(dimension * dimension):
				colorLocationList.append(random.getrandbits(64))
			table.append(colorLocationList)
		return table

	def createZobristValueForNewMove(self, move, color, prevZobristValue):
		"""Gives an updated Zobrist value for a board after a new move is played"""
		row, col = move
		hash_row = BLACK_HASH_ROW_NUM if color == BLACK else WHITE_HASH_ROW_NUM
		hash_val = self.RANDOM_HASH_TABLE[hash_row][row*self.BOARD_DIMENSION + col]
		return prevZobristValue ^ hash_val # ^ = XOR operator

	def checkGameState(self, board):
		"""Sets the GAME_OVER var to True if there is a winner"""
		if self.isTerminal(board)[0]:
			self.GAME_OVER = True

	def isTerminal(self, board):
		"""
		Checks if the current board state is Game Over
		Returns a tuple, with [0] being the True or False value
		[1] being the winning color (None if neither color wins)
		"""
		winner = self.findWinner(board)
		if winner is not None:
			return True, winner
		
		for row in board:
			for spot in row:
				if spot == EMPTY:
					return False, None

		return True, None

	def findWinner(self, board):
		"""
		Checks if there is a winner
		returns the color of the winner if there is one, otherwise None
		"""
		# Check horizontal
		for row in board:
			for col in range(self.BOARD_DIMENSION - 4):
				if row[col] == row[col+1] == row[col+2] == row[col+3] == row[col+4] != EMPTY:
					return row[col]

		# Check vertical
		for c in range(self.BOARD_DIMENSION):
			for r in range(self.BOARD_DIMENSION - 4):
				if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == board[r+4][c] != EMPTY:
					return board[r][c]

		# Check diagonal from top left to bottom right
		for c in range(self.BOARD_DIMENSION - 4):
			for r in range(self.BOARD_DIMENSION - 4):
				if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == board[r+4][c+4]!= EMPTY:
					return board[r][c]

		# Check diagonal from top right to bottom left
		for c in range(self.BOARD_DIMENSION - 4):
			for r in range(4, self.BOARD_DIMENSION):
				if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == board[r-4][c+4] != EMPTY:
					return board[r][c]

		return None

	def isCoordinateInBoardRange(self, coord):
		"""Checks if the coordinate is valid on the board"""
		rowNum = coord[0]
		colNum = coord[1]
		if rowNum % self.BOARD_DIMENSION == rowNum and colNum % self.BOARD_DIMENSION == colNum:
			return True
		else:
			return False

	def checkIfMoveCausedGameOver(self, board, move):
		"""
		Checks the spaces in outward directions to see if the move given caused a win
		returns the winner in [0] (BLACK, WHITE, or None if no winner)
		returns True or False in [1] whether or not the game is over
		"""
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
					# keep looking in the forward direction
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

	def getValidMoves(self, board):
		"""Returns a list of valid moves (moves in the center area or near other pieces)"""

		# Will allow me to slightly prioritize checking the spots that are closer to 
		# other pieces by placing them in separate lists
		lists_of_valids = [] 
		for l in range(MAX_NEIGHBOR_DIST):
			lists_of_valids.append([]) 

		emptiesFoundSoFar = set() # used to make sure we don't double-count empty spots

		# locate all the spots with pieces
		filledLocations = []
		for r in range(self.BOARD_DIMENSION):
			for c in range(self.BOARD_DIMENSION):
				if board[r][c] != EMPTY:
					filledLocations.append([r,c])


		def locateEmptyNearSpots(filledCoord, distFromPiece):
			"""Finds all the empty spots near this coordinate and adds them to the list of valid spots"""
			row, col = filledCoord
			for i in range(-distFromPiece, distFromPiece + 1): # e.g. -1, 0, 1
				for j in range(-distFromPiece, distFromPiece + 1): # e.g. -1, 0, 1
					if i != distFromPiece and i != -distFromPiece and j != distFromPiece and j != -distFromPiece: 
						# if not in the right distance circle
						continue
					curr_row, curr_col = row + i, col + j
					if not self.isCoordinateInBoardRange((curr_row, curr_col)):
						# if outside the board range
						continue
					neighborSpot = board[curr_row][curr_col]
					neighborCoordAsTuple = (curr_row, curr_col)
					if neighborSpot == EMPTY and neighborCoordAsTuple not in emptiesFoundSoFar:
						# if there is an empty spot here and we haven't validated it yet
						emptiesFoundSoFar.add(neighborCoordAsTuple)
						lists_of_valids[distFromPiece - 1].append([curr_row, curr_col])

		# check each distance level around each filled piece
		for distFromPiece in range(1, MAX_NEIGHBOR_DIST + 1):
			for filledCoord in filledLocations:
				locateEmptyNearSpots(filledCoord, distFromPiece)

		# shuffle the moves in each distance level
		# note this will not change the order of the distances, just the moves inside each distance level
		for l in lists_of_valids:
			random.shuffle(l) 

		# combine the lists into one big list
		validLocations = [item for innerlist in lists_of_valids for item in innerlist]

		if len(validLocations) == 0 and board[self.BOARD_DIMENSION//2][self.BOARD_DIMENSION//2] == EMPTY:
			# If there are no valid moves evaluated (due to no pieces played yet), but the center is open
			# This will occur when the AI is black and has the first move
			return [[self.BOARD_DIMENSION//2, self.BOARD_DIMENSION//2]]

		# return the best locations from all the valid locations
		return self.findBestValidMoves(validLocations, board)

	def findBestValidMoves(self, validMoves, board):
		"""Takes in all the spaces that were deemed valid and selects the ones that have the most potential"""
		if len(validMoves) <= MAX_NUM_MOVES_TO_EVALUATE:
			# no need to decrease quantity
			return validMoves

		def sectionContainsThreats(pieceColor, sectionString):
			"""
			Evaluates each length 5 and length 6 section of spots in the board for threats
			Returns True or False depending on whether a threat was found
			"""
			threatDictionary = self.blackThreatsScores if pieceColor == BLACK else self.whiteThreatsScores
			if len(sectionString) == 5:
				# if the section is only 5 spaces
				if sectionString in threatDictionary:
					return True
				return False
			for i in range(len(sectionString) - 5):
				section6 = sectionString[i:i+6]
				section5 = section6[:-1]
				if section6 in threatDictionary:
					return True
				if section5 in threatDictionary:
					return True
				if i == len(sectionString) - 6:
					# if at the last 6-piece section, we want to check the final 5 spots as well
					section5 = section6[1:]
					if section5 in threatDictionary:
						threatMultiplier = 2
						return True
			return False


		movesWithScores = [] # each element in the form:  [moveX, moveY], score 

		directionVectorsList = [[1, -1], [1, 0], [1, 1], [0, 1]]
		for move in validMoves:
			moveScore = 0
			for directionVector in directionVectorsList:
				forwardScore, backwardScore = 0, 0
				if self.isCoordinateInBoardRange([move[0] + directionVector[0], move[1] + directionVector[1]]):
					forwardCheckStillValid = True
					forwardPieceColor = board[move[0] + directionVector[0]][move[1] + directionVector[1]] # looks at first piece in forward direction
				else:
					forwardCheckStillValid = False
					forwardPieceColor = None

				if self.isCoordinateInBoardRange([move[0] - directionVector[0], move[1] - directionVector[1]]):
					backwardCheckStillValid = True
					backwardPieceColor = board[move[0] - directionVector[0]][move[1] - directionVector[1]] # looks at first piece in backward direction
				else:
					backwardCheckStillValid = False
					backwardPieceColor = None

				numForwardPlayerPieces, numBackwardPlayerPieces = 0, 0 # number of the piece we have seen in a direction
				currCoordinatesForward, currCoordinatesBackward = move.copy(), move.copy()
				outwardSpacesChecked = 0
				forwardDistanceReached, backwardDistanceReached = 0, 0 # how many spots until a block
				numForwardEmptiesBeforePiece, numBackwardEmptiesBeforePiece = 0, 0 # number of empty spots before seeing a player piece
				forwardDirectionStr, backwardDirectionStr = '', '' # string representations of the board in each direction
				
				# now will look at most 4 spaces forward in the forward and backward direction and evaluate them
				while outwardSpacesChecked < 4 and (forwardCheckStillValid or backwardCheckStillValid):
					outwardSpacesChecked += 1
					if forwardCheckStillValid:
						# keep looking in the forward direction
						currCoordinatesForward = [a + b for a, b in zip(currCoordinatesForward, directionVector)] # adds the direction vector
						if self.isCoordinateInBoardRange(currCoordinatesForward):
							currPiece = board[currCoordinatesForward[0]][currCoordinatesForward[1]]
							
							if forwardPieceColor == EMPTY:
								# if we have not found a player piece yet
								forwardDirectionStr += currPiece
								forwardDistanceReached += 1
								if currPiece == EMPTY:
									numForwardEmptiesBeforePiece += 1
								else:
									# if the current spot we are looking at is the first player piece we have seen
									forwardPieceColor = currPiece
									numForwardPlayerPieces += 1
									forwardScore += (5 - outwardSpacesChecked)

							elif forwardPieceColor == currPiece:
								# current piece is the player piece that we are searching for
								forwardDirectionStr += currPiece
								forwardDistanceReached += 1
								numForwardPlayerPieces += 1
								forwardScore += (5 - outwardSpacesChecked) * (2 ** (2 * (numForwardPlayerPieces - 1)))

							else:
								# the current spot does not contain the piece we are searching for
								if currPiece == EMPTY:
									forwardDirectionStr += currPiece
									forwardDistanceReached += 1
									forwardScore += (5 - outwardSpacesChecked)
								else:
									# if we have found the opposing color to the piece we are searching for
									forwardCheckStillValid = False
						else:
							forwardCheckStillValid = False

					if backwardCheckStillValid:
						# keep looking in the backward direction
						currCoordinatesBackward = [a - b for a, b in zip(currCoordinatesBackward, directionVector)] # subtracts the direction vector
						if self.isCoordinateInBoardRange(currCoordinatesBackward):
							currPiece = board[currCoordinatesBackward[0]][currCoordinatesBackward[1]]
							
							if backwardPieceColor == EMPTY:
								# if we have not found a player piece yet
								backwardDirectionStr += currPiece
								backwardDistanceReached += 1
								if currPiece == EMPTY:
									numBackwardEmptiesBeforePiece += 1
								else:
									# if the current spot we are looking at is the first player piece we have seen
									backwardPieceColor = currPiece
									numBackwardPlayerPieces += 1
									backwardScore += (5 - outwardSpacesChecked)

							elif backwardPieceColor == currPiece:
								# current piece is the player piece that we are searching for
								backwardDirectionStr += currPiece
								backwardDistanceReached += 1
								numBackwardPlayerPieces += 1
								backwardScore += (5 - outwardSpacesChecked) * (2 ** (2 * (numBackwardPlayerPieces - 1)))

							else:
								# the current spot does not contain the piece we are searching for
								if currPiece == EMPTY:
									backwardDirectionStr += currPiece
									backwardDistanceReached += 1
									backwardScore += (5 - outwardSpacesChecked)
								else:
									# if we have found the opposing color to the piece we are searching for
									backwardCheckStillValid = False
						else:
							backwardCheckStillValid = False

				directionVectorScore = forwardScore + backwardScore
				if forwardPieceColor == backwardPieceColor:
					# if the closest piece in each direction was the same color
					if forwardDistanceReached + 1 + backwardDistanceReached < 5:
						# if there is less than a 5 piece section here
						directionVectorScore = 0
					else:
						threatMultiplier = 1
						if forwardPieceColor != EMPTY and forwardPieceColor is not None:
							# if we actually found a piece 
							fullSectionString = backwardDirectionStr + forwardPieceColor + forwardDirectionStr # add in the imaginary piece to see if a threat is produced
							if sectionContainsThreats(forwardPieceColor, fullSectionString):
								threatMultiplier = 2

						directionVectorScore += max(forwardScore, backwardScore) * threatMultiplier
				else:
					# if the closest piece in each direction were different colors
					if forwardDistanceReached + 1 + numBackwardEmptiesBeforePiece < 5 and backwardDistanceReached + 1 + numForwardEmptiesBeforePiece < 5:
						# if there is less than a 5 piece section here
						directionVectorScore = 0
					else:
						threatMultiplier = 1

						if opponentOf(forwardPieceColor) == backwardPieceColor and forwardPieceColor is not None and backwardPieceColor is not None:
							# if the pieces in each direction are opposing colors (i.e. neither are empty or out of bounds)
							if numBackwardEmptiesBeforePiece == 0:
								# if the first spot in the backward direction is a player piece
							 	forwardSectionStr = forwardPieceColor + forwardDirectionStr
							else:
								# if the first spot in the backward direction is empty, we want to add an empty
								# spot to the front of this, since threats may have 0 or 1 spaces at the start/end
								forwardSectionStr = "." + forwardPieceColor + forwardDirectionStr
							if numForwardEmptiesBeforePiece == 0:
								# if the first spot in the forward direction is a player piece
							 	backwardSectionStr = backwardPieceColor + backwardDirectionStr
							else:
								# if the first spot in the forward direction is empty, we want to add an empty
								# spot to the front of this, since threats may have 0 or 1 spaces at the start/end
								backwardSectionStr = "." + backwardPieceColor + backwardDirectionStr

							if sectionContainsThreats(forwardPieceColor, forwardSectionStr) or sectionContainsThreats(backwardPieceColor, backwardSectionStr):
								threatMultiplier = 2


						else:
							# one of the directions is all empty spaces, and the other contains at least one player piece
							# OR one of the directions is out of bounds
							if forwardPieceColor is None:
								# if the forward direction is out of bounds
								totalSectionStr = backwardPieceColor + backwardDirectionStr
								evaluatingPieceColor = backwardPieceColor
							elif backwardPieceColor is None:
								# if the backward direction is out of bounds
								totalSectionStr = forwardPieceColor + forwardDirectionStr
								evaluatingPieceColor = forwardPieceColor
							else:
								if forwardPieceColor == EMPTY:
									# if the forward direction is all the empties
									totalSectionStr = "." + backwardPieceColor + backwardDirectionStr
									evaluatingPieceColor = backwardPieceColor
								else:
									# if the backward direction is all the empties
									totalSectionStr = "." + forwardPieceColor + forwardDirectionStr
									evaluatingPieceColor = forwardPieceColor
							
							if sectionContainsThreats(evaluatingPieceColor, totalSectionStr):
								threatMultiplier = 2

						directionVectorScore += max(forwardScore, backwardScore) * threatMultiplier

				moveScore += directionVectorScore
			movesWithScores.append([move, moveScore])

		movesWithScores.sort(key = lambda x: -x[1]) # sort in descending order by evaluated score
		highestEvaluatedMoves = []
		for i in range(MAX_NUM_MOVES_TO_EVALUATE):
			highestEvaluatedMoves.append(movesWithScores[i][0])

		return highestEvaluatedMoves

	def getMove(self, board):
		"""Calculates the best move for the AI for the given board"""
		moveRow, moveCol, score = -123, -123, -123 # placeholders
		for i in range(1, MAX_DEPTH + 1): # iterative deepening
			# this will prioritize game winning move sets that occur with less total moves
			moveRow, moveCol, score = self.minimax(board, 0, MAX, -math.inf, math.inf, i, 0)
			self.BOARD_STATE_DICT.clear() # clear the dict after every depth increase
			if score >= WIN_SCORE:
				break
		return moveRow, moveCol

	def minimax(self, board, depth, maxOrMin, alpha, beta, localMaxDepth, zobristValueForBoard):
		"""
		Recursively finds the best move for a given board
		Returns the row in [0], column in [1], and score of the board in [2]
		"""
		if depth == localMaxDepth:
			playerWithTurnAfterMaxDepth = self.AI_COLOR if localMaxDepth % 2 == 0 else self.HUMAN_COLOR
			boardScores = self.scoreBoard(board, self.HUMAN_COLOR, self.AI_COLOR, playerWithTurnAfterMaxDepth)
			humanScore = boardScores[0]
			aiScore = boardScores[1]
			return None, None, aiScore - humanScore
		
		validMoves = self.getValidMoves(board)
		if len(validMoves) == 0:
			return -1, -1, 0
		if depth == 0 and len(validMoves) == 1:
			return validMoves[0][0], validMoves[0][1], 0
		if maxOrMin == MAX:
			# want to maximize this move
			score = -math.inf
			bestMove = validMoves[0] # default best move
			if depth == 0:
				# on the top level of search, printing progress bar
				percentComplete = 0
				movesChecked = 0
				barCompleteMultiplier = 0
				print('\r[%s%s] %d%% (%d/%d moves checked) @ maxDepth = %d' % ("="*barCompleteMultiplier, "-"*(25-barCompleteMultiplier), percentComplete, movesChecked, len(validMoves), localMaxDepth), end = "")

			for move in validMoves:
				if depth == 0:
					# print progress bar
					percentComplete = int((movesChecked/len(validMoves))*100)
					barCompleteMultiplier = percentComplete // 4
					print('\r[%s%s] %d%% (%d/%d moves checked) @ maxDepth = %d' % ("="*barCompleteMultiplier, "-"*(25-barCompleteMultiplier), percentComplete, movesChecked, len(validMoves), localMaxDepth), end = "")
					movesChecked += 1

				boardCopy = copyOfBoard(board)#list(map(list, board)) # copies board
				performMove(boardCopy, move[0], move[1], self.AI_COLOR)
				newZobristValue = self.createZobristValueForNewMove(move, self.AI_COLOR, zobristValueForBoard)
				if depth >= 2 and newZobristValue in self.BOARD_STATE_DICT:
					# if we've already evaluated the score of this board state
					# no chance of repeat boards until at least depth = 2
					updatedScore = self.BOARD_STATE_DICT[newZobristValue]
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
							_, __, updatedScore = self.minimax(boardCopy, depth + 1, MIN, alpha, beta, localMaxDepth, newZobristValue)
					if depth >= 2:
						self.BOARD_STATE_DICT[newZobristValue] = updatedScore
				if updatedScore > score:
					score = updatedScore
					bestMove = move
				alpha = max(alpha, score)
				if alpha >= beta:
					break # pruning
			if depth == 0:
				# clear progress bar print-out
				sys.stdout.write('\033[2K\033[1G')
			return bestMove[0], bestMove[1], score
		else: 
			# maxOrMin == MIN
			# want to minimize this move
			score = math.inf
			bestMoveForHuman = validMoves[0]
			for move in validMoves:
				boardCopy = copyOfBoard(board) # copies board
				performMove(boardCopy, move[0], move[1], self.HUMAN_COLOR)
				newZobristValue = self.createZobristValueForNewMove(move, self.HUMAN_COLOR, zobristValueForBoard)
				if depth >= 2 and newZobristValue in self.BOARD_STATE_DICT:
					updatedScore = self.BOARD_STATE_DICT[newZobristValue]
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
							_, __, updatedScore = self.minimax(boardCopy, depth + 1, MAX, alpha, beta, localMaxDepth, newZobristValue)
					if depth >= 2:
						self.BOARD_STATE_DICT[newZobristValue] = updatedScore
				if updatedScore < score:
					score = updatedScore
					bestMoveForHuman = move
				beta = min(beta, score)
				if beta <= alpha:
					break # pruning
			return bestMoveForHuman[0], bestMoveForHuman[1], score

	def scoreSections(self, board, colorOfEvaluator, colorOfEnemy, playerWithTurnAfterMaxDepth):
		"""Scores all the different horizontal/vertical/diagonal sections on the board"""
		evaluatorScore = 0
		enemyScore = 0
		evaluatorTrapIndicators = [0, 0, 0, 0]
		enemyTrapIndicators = [0, 0, 0, 0]
		if colorOfEvaluator == BLACK:
			evaluatorScoresDict = self.blackThreatsScores
			enemyScoresDict = self.whiteThreatsScores
		else:
			evaluatorScoresDict = self.whiteThreatsScores
			enemyScoresDict = self.blackThreatsScores

		# Check horizontal
		for c in range(self.BOARD_DIMENSION - 5):
			for r in range(self.BOARD_DIMENSION):
				section6 = "".join(board[r][c:c + 6])
				section5 = section6[:-1] # first 5 spaces of section 6
				if section6 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section6]
					evaluatorTrapIndicators[0] = 1
				elif section6 in enemyScoresDict:
					enemyScore += enemyScoresDict[section6]
					enemyTrapIndicators[0] = 1
				if section5 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section5]
					evaluatorTrapIndicators[0] = 1
				elif section5 in enemyScoresDict:
					enemyScore += enemyScoresDict[section5]
					enemyTrapIndicators[0] = 1
				if c == self.BOARD_DIMENSION - 6:
					# if in last section of row
					section5 = section6[1:] # check the rightmost 5 section of the row
					if section5 in evaluatorScoresDict:
						evaluatorScore += evaluatorScoresDict[section5]
						evaluatorTrapIndicators[0] = 1
					elif section5 in enemyScoresDict:
						enemyScore += enemyScoresDict[section5]
						enemyTrapIndicators[0] = 1

		# Check vertical
		for c in range(self.BOARD_DIMENSION):
			for r in range(self.BOARD_DIMENSION - 5):
				section6 = ''
				for i in range(6):
					section6 += board[r + i][c]
				section5 = section6[:-1] # first 5 spaces of section 6
				if section6 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section6]
					evaluatorTrapIndicators[1] = 1
				elif section6 in enemyScoresDict:
					enemyScore += enemyScoresDict[section6]
					enemyTrapIndicators[1] = 1
				if section5 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section5]
					evaluatorTrapIndicators[1] = 1
				elif section5 in enemyScoresDict:
					enemyScore += enemyScoresDict[section5]
					enemyTrapIndicators[1] = 1
				if r == self.BOARD_DIMENSION - 6:
					# if in last section of col
					section5 = section6[1:] # check the bottom 5 section of the col
					if section5 in evaluatorScoresDict:
						evaluatorScore += evaluatorScoresDict[section5]
						evaluatorTrapIndicators[1] = 1
					elif section5 in enemyScoresDict:
						enemyScore += enemyScoresDict[section5]
						enemyTrapIndicators[1] = 1

		# Check diagonal from top left to bottom right
		for c in range(self.BOARD_DIMENSION - 5):
			for r in range(self.BOARD_DIMENSION - 5):
				section6 = ''
				for i in range(6):
					section6 += board[r + i][c + i]
				section5 = section6[:-1]
				if section6 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section6]
					evaluatorTrapIndicators[2] = 1
				elif section6 in enemyScoresDict:
					enemyScore += enemyScoresDict[section6]
					enemyTrapIndicators[2] = 1
				if section5 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section5]
					evaluatorTrapIndicators[2] = 1
				elif section5 in enemyScoresDict:
					enemyScore += enemyScoresDict[section5]
					enemyTrapIndicators[2] = 1
				if c == self.BOARD_DIMENSION - 6 or r == self.BOARD_DIMENSION - 6:
					# if in last section of this diagonal path
					section5 = section6[1:] # check the border section
					if section5 in evaluatorScoresDict:
						evaluatorScore += evaluatorScoresDict[section5]
						evaluatorTrapIndicators[2] = 1
					elif section5 in enemyScoresDict:
						enemyScore += enemyScoresDict[section5]
						enemyTrapIndicators[2] = 1
		
		# Check diagonal from top right to bottom left
		for c in range(self.BOARD_DIMENSION - 5):
			for r in range(5, self.BOARD_DIMENSION):
				section6 = ''
				for i in range(6):
					section6 += board[r - i][c + i]
				section5 = section6[:-1]
				if section6 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section6]
					evaluatorTrapIndicators[3] = 1
				elif section6 in enemyScoresDict:
					enemyScore += enemyScoresDict[section6]
					enemyTrapIndicators[3] = 1
				if section5 in evaluatorScoresDict:
					evaluatorScore += evaluatorScoresDict[section5]
					evaluatorTrapIndicators[3] = 1
				elif section5 in enemyScoresDict:
					enemyScore += enemyScoresDict[section5]
					enemyTrapIndicators[3] = 1
				if c == self.BOARD_DIMENSION - 6 or r == 0:
					# if in last section of this diagonal path
					section5 = section6[1:] # check the border section
					if section5 in evaluatorScoresDict:
						evaluatorScore += evaluatorScoresDict[section5]
						evaluatorTrapIndicators[3] = 1
					elif section5 in enemyScoresDict:
						enemyScore += enemyScoresDict[section5]
						enemyTrapIndicators[3] = 1

		# manually check the remaining unchecked length-5 corner sections 
		topLeft, topRight, bottomRight, bottomLeft = '', '', '', ''
		for i in range(5):
			topLeft += board[4-i][i]
			topRight += board[i][self.BOARD_DIMENSION - (5-i)]
			bottomRight += board[self.BOARD_DIMENSION - i - 1][self.BOARD_DIMENSION - (5-i)]
			bottomLeft += board[self.BOARD_DIMENSION - (5-i)][i]
		cornerCounter = 1
		for section in [topLeft, topRight, bottomRight, bottomLeft]:
			if section in evaluatorScoresDict:
				if section.count(colorOfEvaluator) == 4:
					# since a 3-piece-trap is not actually a trap in this section
					evaluatorScore += evaluatorScoresDict[section]
					evaluatorTrapIndicators[cornerCounter%2 + 2] = 1
				else:
					evaluatorScore += (evaluatorScoresDict[section] // 2) # 3 piece 'traps' aren't as valuable here
			elif section in enemyScoresDict:
				if section.count(colorOfEnemy) == 4:
					# since a 3-piece-trap is not actually a trap in this section
					enemyScore += enemyScoresDict[section]
					enemyTrapIndicators[cornerCounter%2 + 2] = 1
				else:
					enemyScore += (enemyScoresDict[section] // 2) # 3 piece 'traps' aren't as valuable here
			cornerCounter += 1


		numberOfEvaluatorTraps = sum(evaluatorTrapIndicators)
		numberOfEnemyTraps = sum(enemyTrapIndicators)

		# if traps found in multiple directions, weight this very heavily
		if numberOfEvaluatorTraps > 1:
			evaluatorScore *= 4
		if numberOfEnemyTraps > 1:
			enemyScore *= 4

		# if the player who is set to play next has trap sequences worth more, they will probably win, so give a big bonus
		if playerWithTurnAfterMaxDepth == colorOfEvaluator and numberOfEvaluatorTraps >= 1:
			evaluatorScore *= 4
			if evaluatorScore > enemyScore:
				return 25 * evaluatorScore, enemyScore
		elif playerWithTurnAfterMaxDepth == colorOfEnemy and numberOfEnemyTraps >= 1:
			enemyScore *= 4
			if enemyScore > evaluatorScore:
				return evaluatorScore, 25 * enemyScore

		# if both players have traps, check which player has the BETTER trap(s)
		if numberOfEvaluatorTraps >= 1 and numberOfEnemyTraps >= 1:
			if evaluatorScore > enemyScore:
				evaluatorScore *= 5
			elif enemyScore > evaluatorScore:
				enemyScore *= 5

		return evaluatorScore, enemyScore

	def scorePositionWeights(self, board, colorOfEvaluator, colorOfEnemy):
		"""Scores the board based on the weights of the individual locations (center preferred)"""
		evaluatorScore = 0
		enemyScore = 0
		for row in range(self.BOARD_DIMENSION):
			for col in range(self.BOARD_DIMENSION):
				currSpot = board[row][col]
				if currSpot == colorOfEvaluator:
					evaluatorScore += self.positionWeightsMatrix[row][col]
				elif currSpot == colorOfEnemy:
					enemyScore += self.positionWeightsMatrix[row][col]
		return evaluatorScore, enemyScore

	def scoreBoard(self, board, colorOfEvaluator, colorOfEnemy, playerWithTurnAfterMaxDepth):
		"""
		Scores the entire board by looking at each section of spots,
		as well as the individual piece positions
		"""
		sectionsScores = self.scoreSections(board, colorOfEvaluator, colorOfEnemy, playerWithTurnAfterMaxDepth)
		positionWeightScores = self.scorePositionWeights(board, colorOfEvaluator, colorOfEnemy)
		evaluatorScore = sectionsScores[0] + positionWeightScores[0]
		enemyScore = sectionsScores[1] + positionWeightScores[1]
		return evaluatorScore, enemyScore




def opponentOf(color):
	"""Get the opposing color"""
	return WHITE if color == BLACK else BLACK

def performMove(board, row, col, color):
	"""Performs a given move on the board"""
	board[row][col] = color

def copyOfBoard(board):
	"""Returns a copy of the given board"""
	return list(map(list, board))