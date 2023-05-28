class GameBlock:
    def __init__(self, number=2):
        self.number=number

    def __str__(self):
        return f"[{self.number}]"

    def add(self, to_add):
        self.number+=to_add.number

    def can_add(self, block):
        return block is not None and self.number==block.number

    def path_sufix(self):
        if self.number>2048: return "_uk"
        return f"_{self.number}"