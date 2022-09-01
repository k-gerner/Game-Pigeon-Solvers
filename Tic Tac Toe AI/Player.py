# The super class that player objects will inherit from

from typing import List

class Player:

    def __init__(self, color:str, isAI:bool=True):
        """Sets the color for this player, and indicates whether it is an AI"""
        self.color = color
        self.isAI = isAI

    def getMove(self, board:List[List[str]]) -> List[int]:
        """Returns the chosen move for a given board, in [rowIndex, columnIndex] format"""
        raise NotImplementedError("<!> Function 'getMove' has not been implemented.")
