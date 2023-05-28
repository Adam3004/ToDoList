from main.gui.main_window import runGui
from main.src.utils.reader import read_list_for_user
from main.src.utils.writer import write
from toDoList.user import User

if __name__ == '__main__':
    user1 = User("Kuba")
    read_list_for_user(user1)
    runGui(user1)
    print(user1.list)
    write(user1)
