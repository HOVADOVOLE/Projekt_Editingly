from kivy.app import App
from kivy.lang import Builder
from kivy_garden.contextmenu import ContextMenu, ContextMenuTextItem, ContextMenuDivider

class MyApp(App):
    def build(self):
        self.title = 'Editingly - 0.0.1'
        #return Builder.load_string(kv)
        return Builder.load_file('top_menu.kv')

if __name__ == '__main__':
    MyApp().run()