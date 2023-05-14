import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from  kivy.uix.image import Image
from  kivy.core.window import Window
from main.src.game.map import GameMap
from main.src.game.direction import Direction

class GameWindow(BoxLayout):
    def __init__(self):
        super(GameWindow, self).__init__()
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
        else: return
        self.render_gameview()

    def render_gameview(self):
        self.ids.grid.clear_widgets()
        for i in range (16):
            self.ids.grid.add_widget(Image(source=game_map.get_pic_path(i%4, i//4)))

class GameApp(App):
    def build(self):
        x = GameWindow()
        return x


def runGameGui():
    Builder.load_file("../gui/game_window.kv")
    global game_map
    game_map=GameMap()
    x = GameApp()
    x.run()
