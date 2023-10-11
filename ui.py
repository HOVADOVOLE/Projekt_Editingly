import kivy
from kivy.app import App
from kivy.core.window import Window
from waveform_panel import Waveform
from kivy.uix.floatlayout import FloatLayout

class MainApp(App):
    def build(self):
        Window.maximize()
        layout = FloatLayout()
        layout.add_widget(Waveform())
        return layout

if __name__ == '__main__':
    MainApp().run()
