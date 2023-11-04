from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

class FileImporter():
    soubor = None
    def __init__(self, soubor):
        self.soubor = soubor
    def open_file_manager(self):
        file_chooser = None
        if self.soubor == 'video':
            file_chooser = FileChooserIconView(path='./', filters=['*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv'])
            print(file_chooser)
        elif self.soubor == 'audio':
            file_chooser = FileChooserIconView(path='./', filters=['*.mp3', '*.wav', '*.ogg'])
        else:
            print("chyba")
            return None

        file_chooser.bind(on_submit=self.select_file)
        file_chooser.bind(on_cancel=self.close_file_manager)

        self.popup_file_manager = Popup(title='Choose file', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

        return self.soubor

    def select_file(self, instance, selection, *args):
        print("select_file")
        if selection:
            self.soubor = selection[0]
            self.popup_file_manager.dismiss()
        else:
             self.soubor = None
    def close_file_manager(self, instance):
        print("dissmiss")
        self.popup_file_manager.dismiss()
