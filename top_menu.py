from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.contextmenu import ContextMenu


class TopMenu(BoxLayout):
    def __init__(self, **kwargs: object) -> object:
        Builder.load_file('top_menu.kv')
        super(TopMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.pos_hint = {'top': 1, 'left': 1}
