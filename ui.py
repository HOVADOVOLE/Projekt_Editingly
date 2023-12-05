from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from top_menu import TopMenu
from sidepanel import SidePanel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')



class MainApp(MDApp):
    def build(self):
        self.title = 'Editingly - 0.0.2'

        # Základní nastavení okna
        Window.maximize()
        Window.minimum_width = 1280
        Window.minimum_height = 720
        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        # Vytvoření hlavního layoutu
        ui_box = FloatLayout(size_hint=(1, 1), pos_hint={'top': 1, 'left': 1})
        grid = GridLayout(cols=2, rows=1)

        left = RelativeLayout()
        grid.add_widget(left)
        grid.add_widget(SidePanel(left))

        ui_box.add_widget(grid)
        ui_box.add_widget(TopMenu())

        return ui_box

if __name__ == '__main__':
    MainApp().run()