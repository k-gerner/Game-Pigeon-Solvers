# Kyle Gerner
# Started 7.28.24
# Contains AI strategy and board manipulation methods

from dotsandboxes.dots_and_boxes_player import DotsAndBoxesPlayer
from constants import LEFT, UP, RIGHT, DOWN


class DotsAndBoxesStrategy(DotsAndBoxesPlayer):

	def __init__(self, player_id):
		super().__init__(player_id, is_ai=True)

	def get_moves(self, board):
		pass
