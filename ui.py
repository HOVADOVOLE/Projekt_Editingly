from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from waveform_panel import Waveform
from top_menu import TopMenu
from sidepanel import SidePanel
from table import InteractiveTable
from videoplayer import VideoPlayerApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

class MainApp(App):
    def build(self):
        self.title = 'Editingly - 0.0.1'

        # Základní nastavení okna
        Window.maximize()
        Window.minimum_width = 1280
        Window.minimum_height = 720
        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        # Vytvoření hlavního layoutu
        uiBox = FloatLayout()
        wholeGrid = GridLayout(cols=1, rows=2)
        panel = BoxLayout(orientation="horizontal", size_hint=(1, 0.031))
        panel.add_widget(TopMenu())

        bottomGrid = GridLayout(cols=2, rows=2)
        left = FloatLayout()

        left.add_widget(Waveform())
        left.add_widget(InteractiveTable())
        left.add_widget(VideoPlayerApp())

        bottomGrid.add_widget(left)
        bottomGrid.add_widget(SidePanel())

        wholeGrid.add_widget(panel)
        wholeGrid.add_widget(bottomGrid)
        uiBox.add_widget(wholeGrid)
        return uiBox

if __name__ == '__main__':
    MainApp().run()