# The super class that player objects will inherit from

from typing import List


class Connect4Player:

    def __init__(self, color: str, is_ai: bool = True):
        """Sets the color for this player, and indicates whether it is an AI"""
        self.color = color
        self.is_ai = is_ai

    def get_move(self, board: List[List[str]]) -> int:
        """Returns the chosen move for a given board, in [rowIndex, columnIndex] format"""
        print("\n<!> Function 'getMove' has not been implemented.\n"+
              "The program has been terminated.\n" +
              "Please make sure that you have implemented 'getMove' from the Player super class.\n")
        exit(0)
        return -1 # to satisfy the return type hint warning
