from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from waveform_panel import Waveform
from top_menu import TopMenu
from sidepanel import SidePanel
from table import InteractiveTable
from videoplayer import VideoPlayerApp
from kivy.uix.gridlayout import GridLayout



class MainApp(App):
    def build(self):
        self.title = 'Editingly - 0.0.1'

        # Základní nastavení okay
        Window.maximize()
        Window.minimum_width = 1280
        Window.minimum_height = 720
        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        # Vytvoření hlavního layoutu
        ui_box = FloatLayout()
        grid = GridLayout(cols=2, rows=1)

        left = FloatLayout()
        left.add_widget(Waveform())
        left.add_widget(InteractiveTable())
        left.add_widget(VideoPlayerApp())
        grid.add_widget(left)
        grid.add_widget(SidePanel())
        ui_box.add_widget(grid)
        ui_box.add_widget(TopMenu())
        return ui_box


if __name__ == '__main__':
    MainApp().run()