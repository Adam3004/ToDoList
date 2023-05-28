from main.src.game.block import GameBlock
from random import sample
from main.src.game.direction import Direction

class GameMap:
    def __init__(self, theme="default", blocks=None):
        self.theme=theme
        self.empty_fields=0
        self.max_val = -1
        self.blocks=blocks
        if blocks is None:
            self.new_game()
        else:
            for i in range(4):
                for j in range(4):
                    if blocks[i][j] is None:
                        self.empty_fields+=1
                    else:
                        self.max_val=max(self.max_val, blocks[i][j].number)

    def new_game(self):
        self.blocks = [[None for _ in range(4)] for i in range(4)]
        self.empty_fields = 16
        self.get_random_init2()
        self.max_val = 2

    def place (self, x,y):
        self.blocks[x][y] = GameBlock()
        self.empty_fields-=1

    def get_random_init2(self):
        init1, init2=sample(range(0,16), 2)
        self.place(init1 // 4,init1 % 4)
        self.place(init2 // 4, init2 % 4)

    def __str__(self):
        st=""
        for i in range(4):
            for j in range (4):
                a=self.blocks[i][j]
                if a is None:
                    a="[#]"
                st=st+str(a)
            st=st+"\n"
        return st

    def merge(self, main: (int, int), to_marge: (int,int)):
        x1,y1=main
        x2,y2=to_marge
        self.blocks[x1][y1].add(self.blocks[x2][y2])
        self.max_val=max(self.max_val, self.blocks[x1][y1].number)
        self.blocks[x2][y2]=None
        self.empty_fields+=1

    def won(self):
        return self.max_val>=2048

    def lost(self):
        if self.empty_fields!=0: return False
        for x in range(4):
            for y in range(4):
                if self.can_make_move(x,y):
                    return False
        return True

    def can_make_move(self, x, y):
        if x - 1 >= 0 and self.blocks[x][y] == self.blocks[x - 1][y]:
            return True
        elif x + 1 < 4 and self.blocks[x][y] == self.blocks[x + 1][y]:
            return True
        elif y - 1 >= 0 and self.blocks[x][y] == self.blocks[x][y - 1]:
            return True
        elif y + 1 < 4 and self.blocks[x][y] == self.blocks[x][y + 1]:
            return True
        return False

    def is_empty(self, r, c):
        return self.blocks[r][c] is None

    def get_random(self):
        if self.lost(): return
        empty=[]
        for x in range(4):
            for y in range (4):
                if self.is_empty(x,y): empty.append((x,y))
        x,y=sample(empty,1)[0]
        self.place(x,y)

    def move(self, direction: Direction):
        def transpose():
            new=[[self.blocks[c][r] for c in range (4)] for r in range (4)]
            self.blocks=new
        def change_order():
            new = [[self.blocks[3-r][c] for c in range(4)] for r in range(4)]
            self.blocks = new
        def make_move_up():
            moved=False
            to_add = [0 for _ in range(4)]
            for r in range(1, 4):
                for c in range(4):
                    if self.blocks[r][c] is not None:
                        if not self.blocks[r][c].can_add(self.blocks[to_add[c]][c]):
                            to_add[c] = r
                        else:
                            self.merge((to_add[c], c), (r, c))
                            to_add[c] = r
                            moved=True
            to_move = [0 for _ in range(4)]
            for r in range(4):
                for c in range(4):
                    if self.blocks[r][c] is not None:
                        if to_move[c]!=r:
                            self.blocks[to_move[c]][c] = self.blocks[r][c]
                            self.blocks[r][c] = None
                            moved=True
                        to_move[c] += 1
            return moved

        moved=False
        if direction==Direction.UP:
            moved=make_move_up()
        elif direction == Direction.DOWN:
            change_order()
            moved=make_move_up()
            change_order()
        elif direction == Direction.LEFT:
            transpose()
            moved=make_move_up()
            transpose()
        else:
            transpose()
            change_order()
            moved=make_move_up()
            change_order()
            transpose()
        if moved: self.get_random()

    def change_theme(self, new_theme):
        self.theme=new_theme

    def get_pic_path(self, x, y):
        if self.is_empty(y,x):
            return "../../main/gui/resources/themes/"+self.theme+"/"+self.theme+'empty.png'
        else:
            return "../../main/gui/resources/themes/"+self.theme+"/"+self.theme+self.blocks[y][x].path_sufix()+'.png'


