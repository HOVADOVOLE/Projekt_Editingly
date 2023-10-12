from kivy.app import App
from kivy.core.window import Window
from waveform_panel import Waveform
from top_menu import TopMenu
from sidepanel import SidePanel
from table import InteractiveTable
from kivy.uix.floatlayout import FloatLayout
class MainApp(App):
    def build(self):
        self.title = 'Editingly - 0.0.1'

        # Základní nastavení okna
        Window.maximize()
        Window.minimum_width = 1280
        Window.minimum_height = 720
        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        # Vytvoření hlavního layoutu
        layout = FloatLayout()

        layout.add_widget(Waveform())
        layout.add_widget(SidePanel())
        layout.add_widget(InteractiveTable())
        layout.add_widget(TopMenu())

        return layout

if __name__ == '__main__':
    MainApp().run()
