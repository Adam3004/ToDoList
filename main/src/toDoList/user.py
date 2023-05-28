from .toDoList import ToDoList
from main.src.game.map import GameMap
from main.src.game.constants import GameConstants

class User:
    def __init__(self, name: str):
        self.name = name
        self.list = ToDoList()
        self.game = GameMap()
        self.points: int = 0

    def add_points(self, amount: int):
        self.points += amount
        print("Points added")
    def change_theme(self, theme):
        self.game.theme = theme
        self.points -= GameConstants().themes_available[theme]

    def can_change_theme(self, theme):
        return theme in GameConstants().themes_available.keys() and not (
                    theme == self.game.theme or self.points < GameConstants().themes_available[theme])
    def add_task(self, name, date):
        self.list.add(name, date)

    def __str__(self):
        return self.name
