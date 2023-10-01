import kivy
from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
import top_menu

class MainApp(App):
    def build(self):
        #return Builder.load_file('top_menu.kv')
        return top_menu.MyApp()
    
app = MainApp()
app.run()