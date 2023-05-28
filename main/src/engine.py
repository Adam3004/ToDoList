from main.gui.main_window import runGui
from main.src.utils.reader import read_list_for_user
from main.src.utils.reader import read_game_status
from main.src.utils.writer import write_user
from main.src.utils.writer import write_game_status
from main.src.game.map import GameMap
from toDoList.user import User

from main.src.game.block import GameBlock

if __name__ == '__main__':
    l = []
    theme = read_game_status(l)
    game = GameMap(theme, l)
    user1 = User("Kuba", game)
    read_list_for_user(user1)
    runGui(user1)
    print(user1.list)
    write_game_status(user1.game.blocks, user1.game.theme)
    write_user(user1)
