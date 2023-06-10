from main.src.toDoList.task import Task
from typing import Dict, Optional


class ToDoList:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}

    def add(self, name: str, date: str) -> None:
        task = Task(name, date)
        self.tasks[task.id] = task

    def clear(self) -> None:
        self.tasks.clear()

    def load_task(self, task: Task):
        self.tasks[task.id] = task

    def __is_elem_in_list(self, elem: Task) -> bool:
        return elem.id in self.tasks

    def get_task(self, id: int) -> Optional[Task]:
        if not self.tasks.keys().__contains__(id):
            return None
        foundElem: Optional[Task] = self.tasks[id]
        if foundElem is not None:
            return foundElem
        else:
            print("Elem not found ")

    def remove(self, elem: Task) -> None:
        if self.__is_elem_in_list(elem):
            self.tasks.pop(elem)
            print("task was removed")
        print("task not found, so cannot be removed")

    def complete_task(self, id: int) -> bool:
        task = self.get_task(id)
        if task is not None:
            task.complete_task()
            return True
        else:
            print("Task not found, so cannot be completed")
            return False

    def __str__(self):
        output = ""
        for elem in self.tasks:
            output += "Dict ID: "
            output += str(elem)
            output += ", Task: ["
            output += str(self.tasks[elem])
            output += "]\n"
        return output
