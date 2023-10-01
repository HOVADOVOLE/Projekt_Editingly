import kivy
from kivy.uix.button import Button
from kivy.app import App

class MainApp(App):
    def build(self):
        return Button(text='Hello World')
    
app = MainApp()
app.run()