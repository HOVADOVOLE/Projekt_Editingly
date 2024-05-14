from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from file_handler import file_handler
from kivy.clock import Clock
from kivy.uix.label import Label
from subtitle_handler import Subtitle_Handler
from title_manager import title_manager
import json
class VideoPlayerApp(BoxLayout):
    def __init__(self):
        super().__init__()
        self.file_handler = file_handler()
        self.size_hint = (0.5, 0.6)
        self.pos_hint = {'right': 0.95, 'top': 0.95}
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.title_manager = title_manager()
        self.subtitle_handler = Subtitle_Handler()

        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.video = VideoPlayer(size_hint=(1, 1), state='pause', allow_fullscreen=False)
        self.video.bind(position=self.update_slider_position)

        self.subtitle_widget = SubtitleWidget()

        self.add_widget(self.video)
        self.add_widget(self.subtitle_widget)

        self.bind(pos=self.update_rectangle, size=self.update_rectangle)
        self.popup_file_manager = None

        if self.file_handler.get_source() is not None:
            self.video.source = self.file_handler.get_source()
            self.video_loaded = True
        else:
            self.video.bind(on_loaded=self.on_video_loaded)
            self.video_loaded = False

        self.video.bind(state=self.change_state)
        Clock.schedule_interval(self.clock_handler, 0.2)

    def clock_handler(self, *larg):
        self.check_subtitle_change() # Kontroluje jestli se nemá změnit titulka
        self.check_source() # Kontroluje jestli náhodou není video načtené z waveformu
        self.check_state() # Kontlole state videa
        self.video_posun() # Posun videa
        self.check_slider_movement() # Kontroluje jestli se neposouvá slider
    def check_subtitle_change(self, *larg):
        #print(self.subtitle_handler.print_json())
        subtitle = self.subtitle_handler.return_current_subbtitle(self.video.position)
        if subtitle is not None:
            self.subtitle_widget.text = subtitle['text']
        else:
            self.subtitle_widget.text = ""
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

        self.title_manager.video_position = self.video.position
        self.title_manager.max_video_position = self.video.duration

    def check_source(self, *larg):
        # Kontroluje jestli náhodou není video načtené z waveformu
        if self.video.source == "":
            if self.file_handler.get_source() is not None:
                self.video.source = self.file_handler.get_source()
                self.video_loaded = True
                self.title_manager.max_video_position = self.video.duration
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
            self.title_manager.max_video_position = self.video.duration
            self.popup_file_manager.dismiss()

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()

    def on_video_loaded(self, instance, value):
        self.video_loaded = True
        self.unbind(on_touch_up=self.on_touch_up)
        self.update_slider_position(self.video.position)

class SubtitleWidget(Label):
    def __init__(self, **kwargs):
        super(SubtitleWidget, self).__init__(**kwargs)
        self.color = (1, 1, 0, 1)
        self.size_hint = (0.5, 0.1)
        self.pos_hint = {"center_x": 0.5, 'top': 0.85}
        self.font_size = 30
        self.color = (1, 1, 1, 1)
        self.size_hint_x = 0.6
        self.halign = 'center'
        self.valign = 'middle'
        self.text = ""
        self.bind(pos=self.update_rectangle, size=self.update_rectangle)

        with self.canvas:
            Color(1, 1, 1, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size, group='subtitle')
    def update_subtitle(self, text):
        self.canvas.remove_group('subtitle')
        if text is not None or text is not "":
            with self.canvas:
                Color(1, 1, 1, 0.5)
                Rectangle(pos=self.pos, size=self.size, group='subtitle')
        self.text = text
    def update_rectangle(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size