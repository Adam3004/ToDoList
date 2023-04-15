import csv
import os
from main.src.toDoList.user import User
from main.src.toDoList.task import Task


def write(user: User) -> None:
    data_folder: str = os.getcwd()
    file_to_open: str = data_folder + '\\resources\\toDoLists\\user1.csv'

    with open(file_to_open, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for id in user.list.tasks:
            task = user.list.get_task(id)
            csv_writer.writerow([task.name, task.is_done, task.deadline, task.points])
