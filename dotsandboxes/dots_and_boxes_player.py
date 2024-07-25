# The super class that player objects will inherit from
from typing import Tuple, Literal
from dotsandboxes.dots_and_boxes_board import DotsAndBoxesBoard

Direction = Literal['l', 'u', 'r', 'd', 'L', 'U', 'R', 'D']


class DotsAndBoxesPlayer:

	def __init__(self, player_id: int, is_ai: bool = True):
		"""Sets the player_id for this player, and indicates whether it is an AI"""
		self.player_id = player_id
		self.is_ai = is_ai

	def get_move(self, board: DotsAndBoxesBoard) -> Tuple[int, Direction]:
		"""
		Returns the chosen move for a given board.
		- The first int is which square is chosen. Zero-indexed, starting from
		  the top left and working left-to-right, top-to-bottom
		- The second int is which side is chosen. This should be one of
		  LEFT, UP, RIGHT, DOWN (0, 1, 2, 3) as specified in constants.py
		"""
		print("\n<!> Function 'getMove' has not been implemented.\n" +
			  "The program has been terminated.\n" +
			  "Please make sure that you have implemented 'getMove' from the Player super class.\n")
		exit(0)
