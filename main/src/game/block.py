class GameBlock:
    def __init__(self, number: int =2):
        self.number = number

    def __str__(self):
        return f"[{self.number}]"

    def add(self, to_add: "GameBlock"):
        """adding two blocks together"""
        self.number += to_add.number

    def can_add(self, block: "GameBlock"):
        """checking if two blocks can be added (2048 conditions)"""
        return block is not None and self.number == block.number

    def path_sufix(self):
        """getting picture path sufix"""
        if self.number > 2048: return "_uk"
        return f"_{self.number}"
