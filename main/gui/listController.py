from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from main.src.toDoList.user import User


class ListWindow(BoxLayout):
    user: User = None

    def play_2048(self):
        print('Play 2048')

    def view_history(self):
        print('View history')

    def add_task(self):
        print('Add task')

    def buy_item(self):
        print('Buy item')

    def add_user(self, new_user: User):
        self.user = new_user
        print(self.user)


class ListApp(App):
    def build(self):
        x = ListWindow()
        # x.add_user()
        return x


def runGui():
    Builder.load_file("../gui/list_window.kv")
    x = ListApp()
    x.run()
