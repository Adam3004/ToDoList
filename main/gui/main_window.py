import re
from datetime import datetime

from kivy.config import Config

Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from main.src.game.direction import Direction
from main.src.toDoList.user import User
from main.src.game.constants import GameConstants
from kivy.properties import StringProperty, ObjectProperty
from kivy.properties import StringProperty

from main.src.game.direction import Direction
from main.src.toDoList.user import User


def check_date(date: str) -> bool:
    x = re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-5][0-9]:[0-5][0-9]$", date)
    if x:
        splited = date.split("-")
        if int(splited[1]) <= 12:
            splited = splited[2].split(" ")
            if int(splited[0]) <= 31:
                splited = splited[0].split(":")
                if int(splited[0]) <= 24:
                    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S') > datetime.now()
    return False

class ListWindow(Screen):
    toPrint = StringProperty()

    def __init__(self, **kwargs):
        super(ListWindow, self).__init__(**kwargs)
        self.toPrint = printList(user, False)

    def play_2048(self):
        print(f'Play 2048')

    def view_history(self):
        print(printList(user, True))

    def add_task(self, name: str, date: str):
        user.list.add(name, date)
        self.toPrint = printList(user, False)
        print('Add task')

    def buy_item(self):
        print('Buy item')

    def complete_task(self, task_id, task_not_found):
        if int(task_id.text) < 0 or not user.list.complete_task(int(task_id.text)):
            task_not_found.text = 'task not found'
        else:
            task_not_found.text = ''
            self.toPrint = printList(user, False)

    def check_status(self, name, date, warning):
        if len(name.text) == 0:
            warning.text = 'Name field cannot be empty'
        elif len(date.text) == 0 or not check_date(date.text):
            warning.text = 'Wrong data format! \nyyyy-mm-dd hh:mm:ss'
        else:
            print(f'text input text is: {name.text}, date {date.text}')
            warning.text = ''
            self.add_task(name.text, date.text)


def printList(user: User, is_done: bool) -> str:
    output = ""
    for elem in user.list.tasks.values():
        if elem.is_done == is_done:
            output += "Task: "
            output += str(elem.name)
            output += "\n"
    return output


def canPlay(user: User) -> bool:
    for elem in user.list.tasks.values():
        if not elem.is_done:
            return False
    return True


class GameWindow(Screen):
    info=StringProperty('use w, s, a, d to play')
    instructions=StringProperty('Beat 2048 to win!')
    points_cost = StringProperty(str(GameConstants().theme_cost))
    points_cnt = StringProperty("0")
    theme_to_change="default"
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_kv_post(self, base_widget):
        self.render_gameview()
        self.ids.spinner_id.values=GameConstants().themes_available
        self.update_points()

    def on_enter(self):
        self.update_points()

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
    def spinner_clicked(self, value):
        self.ids.spinner_id.text = value
        self.update_change_theme_button(value)

    def update_points(self):
        self.points_cnt = str(user.points)

    def update_change_theme_button(self, theme):
        if not user.can_change_theme(theme):
            self.ids.change_button.background_color=(0.078, 0.106, 0.169,1)
        else:
            self.ids.change_button.background_color = (0.208, 0.373, 0.616, 1)
    def change_theme(self):
        theme=self.ids.spinner_id.text
        if user.can_change_theme(theme):
            user.change_theme(theme)
        self.update_points()
        self.update_change_theme_button(theme)
        self.render_gameview()

class WindowManager(ScreenManager):
    pass

class ToDo2048App(App):
    def build(self):
        return Builder.load_file("../gui/window_manager.kv")


def runGui(currUser: User):
    global user
    user = currUser
    ToDo2048App().run()
