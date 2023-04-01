from toDoList.user import User


if __name__ == '__main__':
    user1 = User("Kuba")
    user1.list.add("tak1", '12/04/23 12:30')
    print(user1.list)
    user1.list.add("task2", '10/05/24 17:25')
    user1.list.complete_task("tak1")
    print(user1.list)
