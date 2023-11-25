from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from file_handler import file_handler
from kivy.clock import Clock

class VideoPlayerApp(BoxLayout):
    def __init__(self):
        super().__init__()
        self.file_handler = file_handler()
        self.size_hint = (0.5, 0.6)
        self.pos_hint = {'right': 0.95, 'top': 0.95}
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.video = VideoPlayer(size_hint=(1, 1), state='pause', allow_fullscreen=False)
        self.video.bind(position=self.update_slider_position)
        self.add_widget(self.video)

        self.bind(pos=self.update_rectangle, size=self.update_rectangle)
        self.popup_file_manager = None

        if self.file_handler.get_source() is not None:
            self.video.source = self.file_handler.get_source()
            self.video_loaded = True
        else:
            self.video.bind(on_loaded=self.on_video_loaded)
            self.video_loaded = False
        self.video.bind(state=self.change_state)
        Clock.schedule_interval(self.check_source, 0.1) # Kontroluje jestli náhodou není video načtené z waveformu
        Clock.schedule_interval(self.check_state, 0.2) # Kontlole state videa
        Clock.schedule_interval(self.video_posun, 0.2) # Posun videa
        Clock.schedule_interval(self.check_slider_movement, 0.2)# Kontroluje jestli se neposouvá slider
    def check_slider_movement(self, *larg):
        if self.file_handler.get_posunuti_videa_state():
            self.file_handler.set_posunuti_videa_state(False)
            self.video.seek(((100 * self.file_handler.get_posunuti_videa()) / self.video.duration)/100)
    def change_state(self, *larg):
        if self.video.state == 'play':
            self.file_handler.set_video_play(True)
        else:
            self.file_handler.set_video_play(False)
    def video_posun(self, *larg):
        posun = self.file_handler.get_posun()
        # převede mi aktuální čas videa na procenta
        cas_v_procentech = (100 * self.video.position) / self.video.duration
        if posun:
            self.file_handler.set_posun(False)
            # převede mi posun na procenta
            posun_v_procentech = (100 * self.file_handler.get_cas_posun()) / self.video.duration
            self.video.seek((cas_v_procentech + posun_v_procentech) / 100)

    def update_slider_position(self, instance, value):
        self.file_handler.set_video_position(value)
        self.file_handler.set_max_value(self.video.duration)
    def update_rectangle(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
    def check_state(self, *larg):
        if self.file_handler.get_video_play():
            self.video.state = 'play'
        else:
            self.video.state = 'pause'

    def check_source(self, key, *larg):
        # Kontroluje jestli náhodou není video načtené z waveformu
        if self.video.source == "":
            if self.file_handler.get_source() is not None:
                self.video.source = self.file_handler.get_source()
                self.video_loaded = True
                self.unbind(on_touch_up=self.on_touch_up)
                Clock.unschedule(self.check_source)

    def on_touch_up(self, touch):
        if self.video.collide_point(*touch.pos) and not self.video.source:
            self.open_file_manager()

    def open_file_manager(self):
        file_chooser = FileChooserIconView(path='', filters=['*.mp3', '*.wav', '*.ogg', '*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv'])
        file_chooser.bind(on_submit=self.select_file)
        file_chooser.bind(on_cancel=self.close_file_manager)
        self.popup_file_manager = Popup(title='Vyberte video', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    def select_file(self, instance, selection, *args):
        if selection:
            self.video.source = selection[0]
            self.file_handler.set_source(selection[0])
            self.popup_file_manager.dismiss()

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()

    def on_video_loaded(self, instance, value):
        print("jsem tu")
        self.video_loaded = True
        self.unbind(on_touch_up=self.on_touch_up)
        self.update_slider_position(self.video.position)