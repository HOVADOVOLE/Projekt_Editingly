import kivy
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
        Window.maximize()
        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        layout = FloatLayout()
        layout.add_widget(Waveform())
        layout.add_widget(TopMenu())
        layout.add_widget(SidePanel())
        layout.add_widget(InteractiveTable())
        return layout

if __name__ == '__main__':
    MainApp().run()
