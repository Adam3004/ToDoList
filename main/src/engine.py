from toDoList.user import User
from main.gui.listController import runGui
from main.gui.gameController import runGameGui
from toDoList.toDoList import Task
from main.src.utils.reader import read_list_for_user
from main.src.utils.writer import write

if __name__ == '__main__':
    user1 = User("Kuba")
    user1.add_task("tak1", '2023-05-12 12:30:00')
    print(user1.list)
    # user1.add_task("task2", '2023-05-12 12:30:00')
    # print(user1.list)
    # user1.list.complete_task(user1.list.get_task(0).id)
    # print(user1.list)
    # print(f'Points: {user1.points}')
    read_list_for_user(user1)
    user1.add_task("task1", '2023-04-13 12:30:00')
    # print(user1.list)
    write(user1)
    runGameGui()
    print(user1.list)

