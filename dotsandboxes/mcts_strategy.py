# Dots and Boxes AI using Monte Carlo Tree Search
from collections import defaultdict

wi / ni + c * sqrt(t) / ni


# wi = number of wins after the i-th move
# ni = number of simulations after the i-th move
# c = exploration parameter (theoretically equal to √2)
# t = total number of simulations for the parent node

# EXPANSION:
# When it can no longer apply UCT to find the successor node,
# it expands the game tree by appending all possible states
# from the leaf node.

# SIMULATION:
# After Expansion, the algorithm picks a child node arbitrarily,
# and it simulates entire game from selected node until it
# reaches the resulting state of the game. If nodes are picked
# randomly during the play out, it is called light play out.
# You can also opt for heavy play out by writing quality
# heuristics or evaluation functions.


class MonteCarloTreeSearchNode:
	def __init__(self, state, parent=None, parent_action=None):
		self.state = state  # board state
		self.parent = parent
		self.parent_action = parent_action
		self.children = []  # all possible actions from the current node
		self._number_of_visits = 0
		self._results = defaultdict(int)
		self._results[1] = 0
		self._results[-1] = 0
		self._untried_actions = self.untried_actions()
		return

	def untried_actions(self):
		self._untried_actions = self.state.get_legal_actions()
		return self._untried_actions

	def net_score(self):
		wins = self._results[1]
		losses = self._results[-1]
		return wins - losses

	def expand(self):
		action = self._untried_actions.pop()
		next_state = self.state.move(action)
		child_node = MonteCarloTreeSearchNode(
			next_state, parent=self, parent_action=action)

		self.children.append(child_node)
		return child_node

	def is_terminal_node(self):
		return self.state.is_game_over()

	def rollout(self):
		current_rollout_state = self.state

		while not current_rollout_state.is_game_over():
			possible_moves = current_rollout_state.get_legal_actions()

			action = self.rollout_policy(possible_moves)
			current_rollout_state = current_rollout_state.move(action)
		return current_rollout_state.game_result()

	def backpropagate(self, result):
		self._number_of_visits += 1.
		self._results[result] += 1.
		if self.parent:
			self.parent.backpropagate(result)

	def is_fully_expanded(self):
		return len(self._untried_actions) == 0

	def best_child(self, c_param=0.1):

		choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
		return self.children[np.argmax(choices_weights)]

	def rollout_policy(self, possible_moves):
		return possible_moves[np.random.randint(len(possible_moves))]

	def _tree_policy(self):

		current_node = self
		while not current_node.is_terminal_node():

			if not current_node.is_fully_expanded():
				return current_node.expand()
			else:
				current_node = current_node.best_child()
		return current_node

	def best_action(self):
		simulation_no = 100

		for i in range(simulation_no):
			v = self._tree_policy()
			reward = v.rollout()
			v.backpropagate(reward)

		return self.best_child(c_param=0.)

	def get_legal_actions(self):
		"""
		Modify according to your game or
		needs. Constructs a list of all
		possible actions from current state.
		Returns a list.
		"""

	def is_game_over(self):
		"""
		Modify according to your game or
		needs. It is the game over condition
		and depends on your game. Returns
		true or false
		"""

	def game_result(self):
		"""
		Modify according to your game or
		needs. Returns 1 or 0 or -1 depending
		on your state corresponding to win,
		tie or a loss.
		"""

	def move(self, action):
		"""
		Modify according to your game or
		needs. Changes the state of your
		board with a new value. For a normal
		Tic Tac Toe game, it can be a 3 by 3
		array with all the elements of array
		being 0 initially. 0 means the board
		position is empty. If you place x in
		row 2 column 3, then it would be some
		thing like board[2][3] = 1, where 1
		represents that x is placed. Returns
		the new state after making a move.
		"""

	# def main():
	# 	root = MonteCarloTreeSearchNode(state=initial_state)
	# 	selected_node = root.best_action()
	# 	return
