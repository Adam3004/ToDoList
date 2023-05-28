import csv
import os

from main.src.toDoList.task import Task
from main.src.toDoList.user import User
from main.src.game.block import GameBlock


def read_list_for_user(user: User) -> None:
    data_folder: str = os.getcwd()
    file_to_open: str = data_folder + '\\resources\\toDoLists\\user1.csv'

    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            user.list.load_task(Task(row[0], row[2], eval(row[1]), int(row[3])))


def read_game_status(list_of_blocks: list) -> str:
    data_folder: str = os.getcwd()
    file_to_open: str = data_folder + '\\resources\\toDoLists\\gameStatus.csv'

    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file)
        theme = "default"
        i: int = 0
        j: int = 0
        counter: int = 0
        list_of_blocks.append([])
        for row in csvreader:
            if counter == 16:
                theme = row[0]
            else:
                if j == 4:
                    i += 1
                    list_of_blocks.append([])
                    j = 0
                list_of_blocks[i].append(GameBlock(int(row[0])))
                j += 1
            counter += 1
    return theme
