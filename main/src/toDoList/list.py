class ToDoList:
    def __init__(self):
        self.tasks = []

    def add(self, elem):
        self.tasks.append(elem)

    def __is_elem_in_list(self, elem):
        return self.tasks.count(elem) > 0

    def remove(self, elem):
        if self.__is_elem_in_list(elem):
            self.tasks.remove(elem)


    def __str__(self):
        return str(self.tasks)


if __name__ == '__main__':
    test = ToDoList()
    test.add(2)
    print(test)


