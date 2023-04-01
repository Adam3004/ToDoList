from .list import ToDoList


class User:
    def __init__(self, name: str):
        self.name = name
        self.list = ToDoList()
        self.points: int = 0

    def add_points(self, amount: int):
        self.points += amount
        print("Points added")

    def __str__(self):
        return self.name
