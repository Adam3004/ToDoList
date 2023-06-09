import re
from kivy.config import Config
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty
from main.src.game.constants import GameConstants
from main.src.game.direction import Direction
from main.src.toDoList.user import User
from main.src.login.login import LoginHandler, LoginException, RegistrationException

Config.set('graphics', 'resizable', '0')


class LoginWindow(Screen):
    warning = StringProperty()

    def __init__(self, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        self.warning = ""
        self.handler = LoginHandler()

    def on_leave(self) -> None:
        self.handler.disconnect()

    def login(self, login, password) -> None:
        try:
            global user
            user = self.handler.log(login.text, password.text)
            self.warning = ""
            self.manager.current = 'list'
        except LoginException as e:
            self.warning = str(e)

    def register(self, login, password) -> None:
        try:
            self.handler.register(login.text, password.text)
            self.warning = "Sucessfully registered!"
        except RegistrationException as e:
            self.warning = str(e)


class ListWindow(Screen):
    toPrint: str = StringProperty()
    userPoints: str = StringProperty()
    history: str = StringProperty()
    header: str = StringProperty()

    def __init__(self, **kwargs):
        super(ListWindow, self).__init__(**kwargs)
        Window.bind(on_request_close=save_and_exit)

    def on_enter(self) -> None:
        self.userPoints: str = str(user.points)
        self.toPrint: str = printList(user, False)
        self.taskStatus: bool = False
        self.userPoints: str = str(user.points)
        self.history: str = "HISTORY"
        self.header: str = "Your to do list"

    def view_history(self) -> None:
        self.taskStatus = not self.taskStatus
        self.toPrint = printList(user, self.taskStatus)
        if self.history == "HISTORY":
            self.history = "TO DO LIST"
            self.header = "Your completed tasks"
        else:
            self.history = "HISTORY"
            self.header = "Your to do list"

    def add_task(self, name: str, date: str) -> None:
        user.list.add(name, date)
        self.taskStatus = False
        self.toPrint = printList(user, self.taskStatus)
        self.history = "HISTORY"
        self.header = "Your to do list"

    def complete_task(self, task_id, task_not_found) -> None:
        if len(task_id.text) == 0:
            task_not_found.text = 'task id field cannot be empty'
        elif not task_id.text.isdigit():
            task_not_found.text = 'id must be a number'
        elif int(task_id.text) < 0 or not user.list.get_task(int(task_id.text)):
            task_not_found.text = 'task not found'
        elif user.list.get_task(int(task_id.text)).is_done:
            task_not_found.text = 'Task is already done'
        else:
            user.list.complete_task(int(task_id.text))
            task_not_found.text = ''
            self.taskStatus = True
            self.toPrint = printList(user, self.taskStatus)
            user.add_points(user.list.get_task(int(task_id.text)).points)
            self.userPoints: str = str(user.points)
            self.history = "TO DO LIST"
            self.header = "Your completed tasks"

    def prepare_task(self, name, date, warning) -> None:
        def check_date(date: str) -> bool:
            x = re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-5][0-9]:[0-5][0-9]$", date)
            if x:
                splited = date.split("-")
                if int(splited[1]) <= 12:
                    splited = splited[2].split(" ")
                    if int(splited[0]) <= 31:
                        splited = splited[1].split(":")
                        if int(splited[0]) <= 24:
                            return True
            return False

        if len(name.text) == 0:
            warning.text = 'Name field cannot be empty'
        elif len(date.text) == 0 or not check_date(date.text):
            warning.text = 'Wrong data format! \nyyyy-mm-dd hh:mm:ss'
        elif datetime.strptime(date.text, '%Y-%m-%d %H:%M:%S') < datetime.now():
            warning.text = 'Deadline cannot be in the past'
        else:
            warning.text = ''
            self.add_task(name.text, date.text)


def printList(user: User, is_done: bool) -> str:
    output = ""
    for elem in user.list.tasks.values():
        if elem.is_done == is_done:
            output += f'[{elem.id}] {elem.name}, {elem.deadline}\n'
    return output


class GameWindow(Screen):
    info = StringProperty()
    instructions = StringProperty()
    points_cost = StringProperty("0")
    points_cnt = StringProperty("0")
    theme_to_change = "default"

    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        Window.bind(on_request_close=save_and_exit)

    def on_kv_post(self, base_widget) -> None:
        # self.render_gameview()
        self.ids.spinner_id.values = GameConstants().themes_available.keys()
        # self.update_points()

    def on_enter(self) -> None:
        self.update_points()
        self.render_gameview()
        self.update_change_theme_button(self.ids.spinner_id.text)
        Window.bind(on_key_down=self._on_keyboard_down)
        if user.have_deadlines():
            self.instructions = 'Complete tasks before!'
            self.info = ''
        else:
            self.instructions = 'Beat 2048 to win!'
            self.info = 'use w, s, a, d to play'

    def on_leave(self) -> None:
        Window.unbind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, window, key, scancode, keycode, modifiers) -> None:
        if not user.have_deadlines():
            if not (user.game.won() or user.game.lost()):
                if keycode == 'w':
                    user.game.move(Direction.UP)
                elif keycode == 's':
                    user.game.move(Direction.DOWN)
                elif keycode == 'a':
                    user.game.move(Direction.LEFT)
                elif keycode == 'd':
                    user.game.move(Direction.RIGHT)
                else:
                    return
                self.render_gameview()
            if user.game.won():
                self.instructions = 'CONGRATULATIONS! You won!!!'
                self.info = ''
            elif user.game.lost():
                self.instructions = 'You have lost :(( Try again'
                self.info = ''
        else:
            self.instructions = 'Complete tasks before!'

    def new_game(self) -> None:
        self.instructions = 'Beat 2048 to win!'
        self.info = 'use w, s, a, d to play'
        user.game.new_game()
        self.render_gameview()

    def render_gameview(self) -> None:
        self.ids.grid.clear_widgets()
        for i in range(16):
            self.ids.grid.add_widget(Image(source=user.game.get_pic_path(i % 4, i // 4)))

    def spinner_clicked(self, value) -> None:
        self.ids.spinner_id.text = value
        self.update_change_theme_button(value)
        self.points_cost = str(GameConstants().themes_available[value])

    def update_points(self) -> None:
        self.points_cnt = str(user.points)

    def update_change_theme_button(self, theme) -> None:
        button = self.ids.change_button
        if not user.can_change_theme(theme):
            button.background_color = (0.024, 0.024, 0.106, 1)
            button.strikethrough = True
        else:
            button.background_color = (0.184, 0.192, 0.376, 1)
            button.strikethrough = False

    def change_theme(self) -> None:
        theme = self.ids.spinner_id.text
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


def save_and_exit(*args):
    LoginHandler().save(user)
    return False


def runGui():
    global user
    user = None
    ToDo2048App().run()
