from .toDoList import ToDoList
from main.src.game.map import GameMap

class User:
    def __init__(self, name: str):
        self.name = name
        self.list = ToDoList()
        self.game = GameMap()
        self.points: int = 0

    def add_points(self, amount: int):
        self.points += amount
        print("Points added")

    def add_task(self, name, date):
        self.list.add(name, date)

    def __str__(self):
        return self.name
