class Task:
    def __init__(self, name, deadline):
        self.name = name
        self.is_done = False
        self.deadline = deadline


    def __str__(self):
        return f"Name: {self.name}, is done {self.is_done}, deadline until {self.deadline}"