from .task import Task


class ToDoList:
    def __init__(self):
        self.tasks: list[Task] = []

    def add(self, name: str, date: str):
        task = Task(name, date)
        self.tasks.append(task)

    def __is_elem_in_list(self, elem: Task):
        return self.tasks.count(elem) > 0

    def __get_task(self, name: str):
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def remove(self, elem: Task):
        if self.__is_elem_in_list(elem):
            self.tasks.remove(elem)
            print("task was removed")
        print("task not found, so cannot be removed")

    def complete_task(self, name: str):
        task = self.__get_task(name)
        try:
            task.fulfill_task()
        except:
            print("Task not found, so cannot be completed")

    def __str__(self):
        output = ""
        for elem in self.tasks:
            output += str(elem)
            output += "\n"
        return output

