# The super class that player objects will inherit from
from typing import List


class MancalaPlayer:

	def __init__(self, bankIndex, isAI: bool = True):
		"""Determines whether this player is an AI; Sets the bank indices for this player"""
		self.bankIndex = bankIndex
		self.isAI = isAI

	def getMove(self, board: List[List[int]]) -> int:
		"""Returns the chosen move for a given board, in [rowIndex, columnIndex] format"""
		print("\n<!> Function 'getMove' has not been implemented.\n" +
			  "The program has been terminated.\n" +
			  "Please make sure that you have implemented 'getMove' from the Player super class.\n")
		exit(0)
		return -1  # to satisfy the return type hint warning
