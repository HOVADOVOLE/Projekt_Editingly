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
        self.title = 'Editingly - 0.0.2'
        # Základní nastavení okay
        Window.maximize()
        Window.minimum_width = 1280
        Window.minimum_height = 720
        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        waveform = Waveform()
        table = InteractiveTable()
        video = VideoPlayerApp()
        # Vytvoření hlavního layoutu
        ui_box = FloatLayout(size_hint=(1, 1), pos_hint={'top': 1, 'left': 1})
        grid = GridLayout(cols=2, rows=1)

        left = FloatLayout()
        left.add_widget(waveform)
        left.add_widget(table)
        left.add_widget(video)
        grid.add_widget(left)
        grid.add_widget(SidePanel())
        ui_box.add_widget(grid)
        ui_box.add_widget(TopMenu())

        return ui_box

if __name__ == '__main__':
    MainApp().run()