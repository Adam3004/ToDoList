from .toDoList import ToDoList
from main.src.game.map import GameMap
from main.src.game.constants import GameConstants
from datetime import datetime


class User:
    def __init__(self, name: str, game: GameMap = None, points: int = 0):
        self.name = name
        self.list = ToDoList()
        if game is None:
            self.game = GameMap()
        else:
            self.game = game
        self.points: int = points

    def add_points(self, amount: int):
        self.points += amount

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

    def have_deadlines(self) -> bool:
        for elem in self.list.tasks.values():
            if not elem.is_done and datetime.now() > elem.deadline:
                return True
        return False
