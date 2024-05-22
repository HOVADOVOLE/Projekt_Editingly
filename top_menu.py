from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.contextmenu import ContextMenu
from shortcuts import ShortcutsPopup
from kivy.uix.popup import Popup
from export import Export
from import_project import ImportProject
class TopMenu(BoxLayout):
    def __init__(self, **kwargs: object):
        Builder.load_file('top_menu.kv')
        super(TopMenu, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.pos_hint = {'top': 1, 'left': 1}

        self.export = Export()
        self.import_project = ImportProject()
    def open_shortcuts(self):
        popup = Popup(title='Shortcuts', content=ShortcutsPopup().build(), size_hint=(None, None), size=(500, 400))
        popup.open()
    def save_project(self):
        self.export.save_data()
        print("Save project...")
    def open_project(self):
        self.import_project.open_import_popup()
        print("Open project...")
