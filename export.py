import json
import os
from subtitle_handler import Subtitle_Handler
from file_handler import file_handler
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class Export():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Export, cls).__new__(cls, *args, **kwargs)
            cls._instance.subtitle_handler = Subtitle_Handler()
            cls._instance.file_handler = file_handler()

            cls._instance.subtitle_list = []
            cls._instance.video_source = ""
            cls._instance.popup_file_manager = None

            cls._instance.has_path = False
            cls._instance.path = ''
            cls._instance.file_name = ''

        return cls._instance

    def save_data(self):
        self.video_source = self.file_handler.source
        self.subtitle_list = self.subtitle_handler.subtitle_list

        if not self.has_path or not self.file_name:
            self.show_file_chooser()
        else:
            if not self.file_name.endswith('.json'):
                self.file_name += '.json'  # Přidání koncovky .json, pokud ji uživatel nezadá
            export_path = os.path.join(self.path, self.file_name)
            os.makedirs(os.path.dirname(export_path), exist_ok=True)  # Vytvoření adresáře, pokud neexistuje
            with open(export_path, 'w') as file:
                json.dump({'subtitle_list': self.subtitle_list, 'video_source': self.video_source}, file)
            self.popup_file_manager.dismiss()  # Zavření dialogového okna po uložení

    def show_file_chooser(self):
        file_chooser = FileChooserListView(path='./')

        file_name_input = TextInput(text='export')
        file_name_input.bind(text=self.set_file_name)  # Váže textový vstup na metodu set_file_name

        confirm_button = Button(text='Confirm')
        confirm_button.bind(on_press=lambda instance: self.select_folder(file_chooser.path))  # Předání cesty z file_chooseru do metody select_folder

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(file_chooser)
        layout.add_widget(file_name_input)
        layout.add_widget(confirm_button)

        self.popup_file_manager = Popup(title='Choose folder and file name', content=layout, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    def select_folder(self, path):
        self.path = path
        self.has_path = True
        self.save_data()

    def set_file_name(self, instance, text):
        self.file_name = text

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()
