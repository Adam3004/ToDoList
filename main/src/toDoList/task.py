from datetime import datetime
import itertools


class Task:
    # auto incrementing id for new tasks
    newid = itertools.count()

    def __init__(self, name: str, deadline, isDone: bool = False, pointsAmount: int = 5):
        self.id = next(self.newid)
        self.name = name
        self.is_done = isDone
        self.deadline = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
        self.points = pointsAmount

    def complete_task(self) -> None:
        self.is_done = True

    def __str__(self):
        return f"ID: {self.id}, name: {self.name}, is done {self.is_done}, deadline until {self.deadline}, points: {self.points}"
