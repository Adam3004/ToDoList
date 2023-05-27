from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from main.src.game.direction import Direction
from  kivy.uix.image import Image
from main.src.game.map import GameMap
from main.src.toDoList.user import User
from  kivy.core.window import Window
class ListWindow(Screen):
    def view_history(self):
        print(user.list)

    def add_task(self):
        user.list.add("task2", "2023-04-13 12:30:00")
        print('Add task')

    def buy_item(self):
        print('Buy item')

class GameWindow(Screen):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.id=2
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
    game_map=GameMap()
    user = currUser
    ToDo2048App().run()


