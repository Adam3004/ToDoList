from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from main.src.toDoList.user import User


class ListWindow(BoxLayout):
    
    def __init__(self):
        super(ListWindow, self).__init__()

    def play_2048(self):
        print(f'Play 2048')

    def view_history(self):
        print(user.list)

    def add_task(self):
        user.list.add("task2", "2023-04-13 12:30:00")
        print('Add task')

    def buy_item(self):
        print('Buy item')



class ListApp(App):
    x = None
    def build(self):
        self.x = ListWindow()
        return self.x

    def getX(self):
        return self.x


def runGui(guser: User):
    Builder.load_file("../gui/list_window.kv")
    global user
    user = guser
    x:ListApp = ListApp()
    x.build()
    x.run()
