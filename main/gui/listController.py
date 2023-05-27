from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window
from main.src.toDoList.user import User
import time


class ListWindow(BoxLayout):
    toPrint = StringProperty()
    txt_inpt = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListWindow, self).__init__(**kwargs)
        self.toPrint = printList(user, False)
        self.txt_inpt = ''

    def play_2048(self):
        print(f'Play 2048')

    def view_history(self):
        print(printList(user, True))

    def add_task(self):
        user.list.add("task2", "2023-04-13 12:30:00")
        self.toPrint = printList(user, False)
        print('Add task')

    def buy_item(self):
        print('Buy item')


    def check_status(self, input):
        print('text input text is: {txt}'.format(txt=input.text))




def printList(user: User, is_done: bool) -> str:
    output = ""
    for elem in user.list.tasks.values():
        if elem.is_done == is_done:
            output += "Task: "
            output += str(elem.name)
            output += "\n"
    return output


class ListApp(App):

    def build(self):
        return ListWindow()


def runGui(guser: User):
    Builder.load_file("../gui/list_window.kv")
    global user
    user = guser
    x: ListApp = ListApp()
    x.build()
    x.run()
