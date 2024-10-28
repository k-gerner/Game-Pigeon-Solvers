# The super class that player objects will inherit from
from typing import List


class MancalaPlayer:

	def __init__(self, bank_index, is_ai: bool = True):
		"""Determines whether this player is an AI; Sets the bank indices for this player"""
		self.bankIndex = bank_index
		self.is_ai = is_ai

	def get_move(self, board: List[int]) -> int:
		"""Returns the chosen move for a given board, in [rowIndex, columnIndex] format"""
		print("\n<!> Function 'get_move' has not been implemented.\n" +
			  "The program has been terminated.\n" +
			  "Please make sure that you have implemented 'get_move' from the Player super class.\n")
		exit(0)
		return -1  # to satisfy the return type hint warning
