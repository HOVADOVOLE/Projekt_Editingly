import json
import os
from subtitle_handler import Subtitle_Handler
from file_handler import file_handler
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

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

        return cls._instance

    def save_data(self):
        self.video_source = self.file_handler.source
        self.subtitle_list = self.subtitle_handler.subtitle_list

        if not self.has_path:
            self.show_file_chooser()
            self.save()
        else:
            self.save()
    def save(self):
        export_path = os.path.join(self.path, 'export.json')
        with open(export_path, 'w') as file:
            json.dump({'subtitle_list': self.subtitle_list, 'video_source': self.video_source}, file)

    def show_file_chooser(self):
        file_chooser = FileChooserListView(path='./')
        confirm_button = Button(text='Confirm')
        confirm_button.bind(on_press=lambda instance: self.select_folder(file_chooser.path))  # Předání cesty z file_chooseru do metody select_folder

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(file_chooser)
        layout.add_widget(confirm_button)

        self.popup_file_manager = Popup(title='Choose folder', content=layout, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    def select_folder(self, path):  # Přidání parametru path
        self.path = path
        self.has_path = True
        self.popup_file_manager.dismiss()

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()