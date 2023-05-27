import re
from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from main.src.game.direction import Direction
from main.src.game.map import GameMap
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
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.id = 2
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.render_gameview()

    def back_todo(self):
        print("Go back to 'to do' list")

    def _keyboard_closed(self):
        print('Keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            game_map.move(Direction.UP)
        elif keycode[1] == 's':
            game_map.move(Direction.DOWN)
        elif keycode[1] == 'a':
            game_map.move(Direction.LEFT)
        elif keycode[1] == 'd':
            game_map.move(Direction.RIGHT)
        else:
            return
        self.render_gameview()

    def render_gameview(self):
        print(self.ids)
        # self.ids.grid.clear_widgets()
        # for i in range(16):
        #     self.ids.grid.add_widget(Image(source=game_map.get_pic_path(i % 4, i // 4)))


class WindowManager(ScreenManager):
    pass


class ToDo2048App(App):
    def build(self):
        return Builder.load_file("../gui/window_manager.kv")


def runGui(currUser: User):
    global game_map
    global user
    game_map = GameMap()
    user = currUser
    ToDo2048App().run()
