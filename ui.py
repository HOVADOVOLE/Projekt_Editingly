import kivy
from kivy.app import App
from kivy.core.window import Window
from waveform_panel import Waveform
from top_menu import TopMenu
from kivy.uix.floatlayout import FloatLayout

class MainApp(App):
    def build(self):
        self.title = 'Editingly - 0.0.1'
        Window.maximize()
        layout = FloatLayout()
        layout.add_widget(Waveform())
        layout.add_widget(TopMenu())
        return layout

if __name__ == '__main__':
    MainApp().run()
