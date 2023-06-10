import csv
import os

from main.src.game.block import GameBlock
from main.src.toDoList.user import User


def write_tasks(user: User) -> None:
    """saving user's tasks to csv file"""
    file_to_open: str = f'.\\resources\\toDoLists\\{user.name}.csv'

    with open(file_to_open, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for id in user.list.tasks:
            task = user.list.get_task(id)
            csv_writer.writerow([task.name, task.is_done, task.deadline, task.points])


def write_user(user: User) -> None:
    file_to_open: str = f'.\\resources\\toDoLists\\{user.name}.csv'

    with open(file_to_open, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([user.points])
        for id in user.list.tasks:
            task = user.list.get_task(id)
            csv_writer.writerow([task.name, task.is_done, task.deadline, task.points])


def write_game_status(list_of_blocks: list[list[GameBlock]], theme: str) -> None:
    file_to_open: str = '.\\resources\\toDoLists\\gameStatus.csv'
    """saving game status to csv file"""
    with open(file_to_open, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for inner_list in list_of_blocks:
            for block in inner_list:
                if block is None:
                    csv_writer.writerow([0])
                else:
                    csv_writer.writerow([block.number])
        csv_writer.writerow([theme])
