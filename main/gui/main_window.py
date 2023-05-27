from kivy.config import Config
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from main.src.game.direction import Direction
from main.src.game.map import GameMap
from main.src.toDoList.user import User
from kivy.properties import StringProperty, ObjectProperty
import time

class ListWindow(Screen):
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

    def check_status(self, name, date, warning):
        print(f'text input text is: {name.text}, date {date.text}')
        if len(name.text) == 0:
            warning.text = 'Name field cannot be empty'
        elif len(date.text) == 0:
            warning.text = 'Wrong data format! \nyyyy-mm-dd hh:mm:ss'
        else:
            warning.text = ''


def printList(user: User, is_done: bool) -> str:
    output = ""
    for elem in user.list.tasks.values():
        if elem.is_done == is_done:
            output += "Task: "
            output += str(elem.name)
            output += "\n"
    return output


class GameWindow(Screen):
    info=StringProperty('use w, s, a, d to play')
    instructions=StringProperty('Beat 2048 to win!')
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_kv_post(self, base_widget):
        self.render_gameview()

    def _keyboard_closed(self):
        print('Keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not (user.game.won() or user.game.lost()):
            if keycode[1] == 'w':
                user.game.move(Direction.UP)
            elif keycode[1] == 's':
                user.game.move(Direction.DOWN)
            elif keycode[1] == 'a':
                user.game.move(Direction.LEFT)
            elif keycode[1] == 'd':
                user.game.move(Direction.RIGHT)
            else:
                return
            self.render_gameview()
        if user.game.won():
            self.instructions='CONGRATULATIONS! You won!!!'
            self.info = ''
        elif user.game.lost():
            self.instructions='You have lost :(( Try again'
            self.info = ''

    def new_game(self):
        self.instructions = 'Beat 2048 to win!'
        self.info = 'use w, s, a, d to play'
        user.game.new_game()
        self.render_gameview()

    def render_gameview(self):
        self.ids.grid.clear_widgets()
        for i in range(16):
            self.ids.grid.add_widget(Image(source=user.game.get_pic_path(i % 4, i // 4)))

class WindowManager(ScreenManager):
    pass

class ToDo2048App(App):
    def build(self):
        return Builder.load_file("../gui/window_manager.kv")


def runGui(currUser: User):
    global user
    user = currUser
    ToDo2048App().run()
