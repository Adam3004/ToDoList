import csv
import os

from main.src.toDoList.task import Task
from main.src.toDoList.user import User
from main.src.game.block import GameBlock


def read_tasks(user: User) -> None:
    """reading user's tasks from csv file"""
    file_to_open: str = f'.\\resources\\toDoLists\\{user.name}.csv'
    try:
        with open(file_to_open, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                user.list.load_task(Task(row[0], row[2], eval(row[1]), int(row[3])))
    except FileNotFoundError:
        user.list.clear()


def read_list_for_user(user: User) -> int:
    """ reading list of task for user from csv"""
    file_to_open: str = f'.\\resources\\toDoLists\\{user.name}.csv'
    i: int = 0
    points = 0
    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if i == 0:
                points = int(row[0])
                i += 1
            else:
                user.list.load_task(Task(row[0], row[2], eval(row[1]), int(row[3])))
    return points


def read_game_status(list_of_blocks: list) -> str:
    """reading game status from csv"""
    file_to_open: str = '.\\resources\\toDoLists\\gameStatus.csv'

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
                if int(row[0]) == 0:
                    list_of_blocks[i].append(None)
                else:
                    list_of_blocks[i].append(GameBlock(int(row[0])))
                j += 1
            counter += 1
    return theme
