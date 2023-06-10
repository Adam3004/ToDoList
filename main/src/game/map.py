from main.src.game.block import GameBlock
from random import sample
from main.src.game.direction import Direction


def render_gamestatus(saved_status):
    first = 0
    blocks_1d = []
    for i, char in enumerate(saved_status):
        if char == "$":
            if i - first == 0:
                blocks_1d.append(None)
            else:
                blocks_1d.append(GameBlock(int(saved_status[first:i])))
            first = i + 1
    if len(blocks_1d) != 16:
        raise Exception("couldn't render gamestatus")
    return [[blocks_1d[j * 4 + i] for i in range(4)] for j in range(4)]


def save_gamestatus(blocks):
    status = ""
    for row in blocks:
        for block in row:
            if block is not None:
                status = status + str(block.number)
            status = status + "$"
    return status


class GameMap:
    """This class implements game 2048"""

    def __init__(self, theme: str = "default", blocks=None):
        self.theme = theme
        self.empty_fields = 0
        self.max_val = -1
        self.blocks = blocks
        if blocks is None:
            self.new_game()
        else:
            for row in blocks:
                for block in row:
                    if block is None:
                        self.empty_fields += 1
                    else:
                        self.max_val = max(self.max_val, block.number)

    def __str__(self):
        """this function was used to play in terminal"""
        st = ""
        for i in range(4):
            for j in range(4):
                a = self.blocks[i][j]
                if a is None:
                    a = "[#]"
                st = st + str(a)
            st = st + "\n"
        return st

    def new_game(self):
        """called when new game button is clicked"""
        self.blocks = [[None for _ in range(4)] for i in range(4)]
        self.empty_fields = 16
        self.get_random_init2()
        self.max_val = 2

    def place(self, x: int, y: int):
        """placing new block on map"""
        self.blocks[x][y] = GameBlock()
        self.empty_fields -= 1

    def get_random_init2(self):
        """placing 2 initial blocks on radom places"""
        init1, init2 = sample(range(0, 16), 2)
        self.place(init1 // 4, init1 % 4)
        self.place(init2 // 4, init2 % 4)

    def merge(self, main: (int, int), to_marge: (int, int)):
        """merging to blocks into one, #e assume those blocks can be merged (conditions are satisfied)"""
        x1, y1 = main
        x2, y2 = to_marge
        self.blocks[x1][y1].add(self.blocks[x2][y2])
        self.max_val = max(self.max_val, self.blocks[x1][y1].number)
        self.blocks[x2][y2] = None
        self.empty_fields += 1

    def won(self):
        """checking if the game has been won already"""
        return self.max_val >= 2048

    def lost(self):
        """checking if the game has been lost already"""
        if self.empty_fields != 0: return False
        for x in range(4):
            for y in range(4):
                if self.can_make_move(x, y):
                    return False
        return True

    def can_make_move(self, x: int, y: int):
        """checking if there can be made a move from the certain block"""
        if (x - 1 >= 0 and self.blocks[x][y].number == self.blocks[x - 1][y].number) or (
                x + 1 < 4 and self.blocks[x][y].number == self.blocks[x + 1][y].number) or (
                y - 1 >= 0 and self.blocks[x][y].number == self.blocks[x][y - 1].number) or (
                y + 1 < 4 and self.blocks[x][y].number == self.blocks[x][y + 1].number):
            return True
        return False

    def is_empty(self, r: int, c: int):
        """checking if the field is empty"""
        return self.blocks[r][c] is None

    def get_random(self):
        """placing new block on random field"""
        if self.lost(): return
        empty = []
        for x in range(4):
            for y in range(4):
                if self.is_empty(x, y): empty.append((x, y))
        x, y = sample(empty, 1)[0]
        self.place(x, y)

    def move(self, direction: Direction):
        """"making a move up, down, right or left"""

        def transpose():
            new = [[self.blocks[c][r] for c in range(4)] for r in range(4)]
            self.blocks = new

        def change_order():
            new = [[self.blocks[3 - r][c] for c in range(4)] for r in range(4)]
            self.blocks = new

        def make_move_up():
            moved = False
            to_add = [0 for _ in range(4)]
            for r in range(1, 4):
                for c in range(4):
                    if self.blocks[r][c] is not None:
                        if not self.blocks[r][c].can_add(self.blocks[to_add[c]][c]):
                            to_add[c] = r
                        else:
                            self.merge((to_add[c], c), (r, c))
                            to_add[c] = r
                            moved = True
            to_move = [0 for _ in range(4)]
            for r in range(4):
                for c in range(4):
                    if self.blocks[r][c] is not None:
                        if to_move[c] != r:
                            self.blocks[to_move[c]][c] = self.blocks[r][c]
                            self.blocks[r][c] = None
                            moved = True
                        to_move[c] += 1
            return moved

        moved = False
        if direction == Direction.UP:
            moved = make_move_up()
        elif direction == Direction.DOWN:
            change_order()
            moved = make_move_up()
            change_order()
        elif direction == Direction.LEFT:
            transpose()
            moved = make_move_up()
            transpose()
        else:
            transpose()
            change_order()
            moved = make_move_up()
            change_order()
            transpose()
        if moved: self.get_random()

    def change_theme(self, new_theme: str):
        """changing game theme"""
        self.theme = new_theme

    def get_pic_path(self, x: int, y: int):
        """getting a picture path of the block on certain field"""
        if self.is_empty(y, x):
            return "../../main/gui/resources/themes/" + self.theme + "/" + self.theme + 'empty.png'
        else:
            return "../../main/gui/resources/themes/" + self.theme + "/" + self.theme + self.blocks[y][
                x].path_sufix() + '.png'
