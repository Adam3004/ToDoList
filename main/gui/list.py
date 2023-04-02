from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

class ListWindow(BoxLayout):
    def play_2048(self):
        print('Play 2048')

    def view_history(self):
        print('View history')

    def add_task(self):
        print('Add task')

    def buy_item(self):
        print('Buy item')

class ListApp(App):
    def build(self):
        return ListWindow()

if __name__ == "__main__":
    Builder.load_file("list_window.kv")
    ListApp().run()