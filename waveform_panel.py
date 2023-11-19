from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics import Line, Color
from pydub import AudioSegment
import numpy as np
from kivy.core.window import Window
from file_handler import file_handler
from kivy.clock import Clock

Builder.load_file('waveform.kv')

class Waveform(BoxLayout):
    def __init__(self, **kwargs):
        super(Waveform, self).__init__(**kwargs)
        self.file_handler = file_handler()

        self.points = []
        self.audio_source = None
        self.popup_file_manager = None
        self.samples = []

        Clock.schedule_interval(self.update_slider_position, 0.1)

        if self.file_handler.get_source() is not None:
            source = self.file_handler.get_source()
            self.audio_source = AudioSegment.from_file(source)
            self.create_wave()

    def move_slider_backward(self):
        if self.ids.brightnessControl.value > self.ids.brightnessControl.min:
            self.ids.brightnessControl.value -= 0.05 * (self.ids.brightnessControl.max - self.ids.brightnessControl.min)

    def move_slider_forward(self):
        if self.ids.brightnessControl.value < self.ids.brightnessControl.max:
            self.ids.brightnessControl.value += 0.05 * (self.ids.brightnessControl.max - self.ids.brightnessControl.min)

    def choose_file(self):
        if self.file_handler.get_source() is None:
            self.open_file_manager()
        else:
            source = self.file_handler.get_source()
            self.audio_source = AudioSegment.from_file(source)
            self.create_wave()

    def open_file_manager(self):
        file_chooser = FileChooserIconView(path='./', filters=['*.mp3', '*.wav', '*.ogg', '*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv'])
        file_chooser.bind(on_submit=self.select_file)
        file_chooser.bind(on_cancel=self.close_file_manager)
        self.popup_file_manager = Popup(title='Choose file', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    def select_file(self, instance, selection, *args):
        if selection:
            self.file_handler.set_source(selection[0])

            self.audio_source = AudioSegment.from_file(selection[0])
            self.popup_file_manager.dismiss()
            self.create_wave()

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()
    def update_wave_size(self, *args):
        num_samples = len(self.samples)
        step = int(num_samples / self.width)
        self.points = []

        for i in range(0, num_samples, step):
            y = self.height / 2.5 + (self.samples[i] / 32768) * self.height * 0.8
            x = i * self.ids.canvas_box.width / num_samples

            self.points.extend([x, y])

        self.ids.canvas_box.canvas.clear()
        with self.ids.canvas_box.canvas:
            Color(1,1,1,1)
            Line(points=self.points, close=False, width=1)
            
            Color(0,0,0,1)
            Line(rectangle=(0, 0, self.ids.canvas_box.width, self.ids.canvas_box.height), width=2)
    def check_source(self):
        pass
    def create_wave(self):
        self.points = []

        if self.audio_source:
            self.samples = np.array(self.audio_source.get_array_of_samples())
            num_samples = len(self.samples)
            step = int(num_samples / self.width)

            for i in range(0, num_samples, step):
                y = self.height / 2.5 + (self.samples[i] / 32768) * self.height * 0.8
                x = i * self.ids.canvas_box.width / num_samples

                self.points.extend([x, y])

            with self.ids.canvas_box.canvas:
                Color(1,1,1,1)
                Line(points=self.points, close=False, width=1)

            try:
                self.ids.canvas_box.remove_widget(self.ids.waveform_button)
            except:
                print('Waveform button not found')

            Window.bind(on_resize=self.update_wave_size) # zajišťuje responsivitu pro změnu velikosti okna
            Window.bind(on_maximize=self.update_wave_size) # zajišťuje responsivitu pro maximalizaci okna
            Window.bind(on_restore=self.update_wave_size) # zajišťuje responsivitu pro zmenšení okna
            Window.bind(size=self.update_wave_size) # zajišťuje responsivitu pro přenos mezi monitory
            Window.bind(on_draw=self.update_wave_size) # zajišťuje responsivitu i když vypnu okno a pak ho zase zapnu
    def update_slider_position(self, key, *larg):
        a = self.file_handler.get_max_value()
        self.ids.brightnessControl.max = a
        self.ids.brightnessControl.value = self.file_handler.get_video_position()

        # Kontroluje, jestli byl změnený zdroj videa
        if self.audio_source is None:
            if self.file_handler.get_source() is not None:
                source = self.file_handler.get_source()
                self.audio_source = AudioSegment.from_file(source)
                self.create_wave()
