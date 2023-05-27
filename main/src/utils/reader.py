import csv
import os

from main.src.toDoList.task import Task
from main.src.toDoList.user import User


def read_list_for_user(user: User) -> None:
    data_folder: str = os.getcwd()
    file_to_open: str = data_folder + '\\resources\\toDoLists\\user1.csv'

    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            user.list.load_task(Task(row[0], row[2], eval(row[1]), int(row[3])))
