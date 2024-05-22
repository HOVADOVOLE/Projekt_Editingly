import os
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.app import App

class ImportProject(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.selected_file = None  # Inicializace proměnné

        self.filechooser = FileChooserListView(filters=['*.json'], path='./')
        self.filechooser.bind(on_selection=self.selected)
        self.add_widget(self.filechooser)

        self.load_button = Button(text="Load Selected File", size_hint=(1, 0.1))
        self.load_button.bind(on_release=self.load_file)
        self.add_widget(self.load_button)

        self.result_label = Label(text="File content will be displayed here", size_hint=(1, 0.1))
        self.add_widget(self.result_label)

    def selected(self, filechooser, selection):
        print(f"Selection changed: {selection}")  # Debugovací výpis pro výběr souboru
        if selection:
            self.selected_file = selection[0]
            print(f"Selected file: {self.selected_file}")  # Pro debugging
        else:
            self.selected_file = None
            print("No file selected")  # Pro debugging

    def load_file(self, instance):
        print(f"Attempting to load file: {self.selected_file}")  # Pro debugging
        if self.selected_file and os.path.exists(self.selected_file):
            with open(self.selected_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    self.result_label.text = json.dumps(data, indent=4)
                except json.JSONDecodeError:
                    self.result_label.text = "Invalid JSON file"
        else:
            self.result_label.text = "No file selected or file does not exist"
            print("No file selected or file does not exist")  # Pro debugging

    def open_import_popup(self):
        content = ImportProject()
        self.popup = Popup(title="Import Project", content=content, size_hint=(0.9, 0.9))
        self.popup.open()