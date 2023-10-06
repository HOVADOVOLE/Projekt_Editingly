import kivy
from kivy.app import App
from kivy.lang import Builder

kivy.require("2.0.0")

class Table(App):
    def build(self):
        return Builder.load_file('table.kv')  # Replace with your .kv file name

if __name__ == '__main__':
    Table().run()
