from main.gui.main_window import runGui
from main.src.game.map import GameMap
from main.src.utils.reader import read_game_status
from main.src.utils.reader import read_list_for_user
from main.src.utils.writer import write_game_status
from main.src.utils.writer import write_user
from toDoList.user import User

if __name__ == '__main__':
    tmp_list = []
    theme = read_game_status(tmp_list)
    game = GameMap(theme, tmp_list)
    user1 = User("Kuba", game)
    points: int = read_list_for_user(user1)
    user1.points = points
    runGui(user1)
    write_game_status(user1.game.blocks, user1.game.theme)
    write_user(user1)
