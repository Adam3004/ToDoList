from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

class GameWindow(BoxLayout):
    def back_todo(self):
        print("Go back to 'to do' list")

class GameApp(App):
    def build(self):
        x = GameWindow()
        return x


def runGui():
    Builder.load_file("../gui/game_window.kv")
    x = GameApp()
    x.run()


Builder.load_file("../gui/game_window.kv")
x = GameApp()
x.run()