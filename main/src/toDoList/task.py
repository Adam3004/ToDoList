from datetime import datetime

class Task:
    def __init__(self, name: str, deadline):
        self.name = name
        self.is_done = False
        self.deadline = datetime.strptime(deadline, '%d/%m/%y %H:%M')
        self.points = 5

    def fulfill_task(self):
        self.is_done = True
        print(f'Task {self.name} is completed')

    def __str__(self):
        return f"Name: {self.name}, is done {self.is_done}, deadline until {self.deadline}"
