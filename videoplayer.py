from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

class VideoPlayerApp(BoxLayout):
    def __init__(self):
        super().__init__()
        self.size_hint = (0.5, 0.6)
        self.pos_hint = {'right': 0.95, 'top': 0.95}
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.video = VideoPlayer(size_hint=(1, 1), state='pause')
        self.add_widget(self.video)

        self.bind(pos=self.update_rectangle, size=self.update_rectangle)
        self.popup_file_manager = None

        self.video.bind(on_loaded=self.on_video_loaded)
        self.video_loaded = False

    # Zajistí, že se černý obdélník přizpůsobí velikosti videa
    def update_rectangle(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    # Pokud je video načtené, tak se při kliknutí na video otevře File Manager
    def on_touch_up(self, touch):
        if self.video.collide_point(*touch.pos) and not self.video_loaded and not self.video.source:
            self.open_file_manager()

    # Otevření File Manageru
    def open_file_manager(self):
        file_chooser = FileChooserIconView(path='.', filters=['*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv'])
        file_chooser.bind(on_submit=self.select_file)
        file_chooser.bind(on_cancel=self.close_file_manager)
        self.popup_file_manager = Popup(title='Vyberte video', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    # Filemanager se zavře po výběru souboru
    def select_file(self, instance, selection, *args):
        if selection:
            self.video.source = selection[0]
            self.popup_file_manager.dismiss()

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()

    # Zajistí, že se File Manager otevře pouze pokud přehrávač nemá source
    def on_video_loaded(self, instance, value):
        self.video_loaded = True
        self.unbind(on_touch_up=self.on_touch_up)