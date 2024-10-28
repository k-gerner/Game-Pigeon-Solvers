# The super class that player objects will inherit from

from typing import List, Tuple


class GomokuPlayer:

    def __init__(self, color: str, board_dimension: int = 13, is_ai: bool = True):
        """Sets the color for this player, and indicates whether it is an AI"""
        self.color = color
        self.BOARD_DIMENSION = board_dimension
        self.is_ai = is_ai

    def get_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Returns the chosen move for a given board, in [rowIndex, columnIndex] format"""
        print("\n<!> Function 'get_move' has not been implemented.\n" +
              "The program has been terminated.\n" +
              "Please make sure that you have implemented 'get_move' from the Player super class.\n")
        exit(0)
        return -1, -1 # to satisfy the return type hint warning
