import os
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.app import App

class ImportProject(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.selected_file = None  # Inicializace proměnné

    def open_import_popup(self):
        self.file_chooser = FileChooserIconView(path='./', filters=['*.json'])  # Vytvoření file chooseru s možností vybrat pouze .json soubory
        self.file_chooser.bind(on_submit=self.select_file)
        self.file_chooser.bind(on_cancel=self.close_file_manager)
        self.popup_file_manager = Popup(title='Choose file', content=self.file_chooser, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    def select_file(self, instance, selection, *args):
        if selection:
            self.selected_file = selection[0]
            print(f"Selected file: {self.selected_file}")
            self.popup_file_manager.dismiss()

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()