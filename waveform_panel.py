from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics import Line, Color
from pydub import AudioSegment
import numpy as np


Builder.load_file('waveform.kv')

class Waveform(BoxLayout):
    def __init__(self, **kwargs):
        super(Waveform, self).__init__(**kwargs)
        self.points = []
        self.audio_source = None
        self.popup_file_manager = None

    def move_slider_backward(self):
        if self.ids.brightnessControl.value > self.ids.brightnessControl.min:
            self.ids.brightnessControl.value -= 0.05 * (self.ids.brightnessControl.max - self.ids.brightnessControl.min)

    def move_slider_forward(self):
        if self.ids.brightnessControl.value < self.ids.brightnessControl.max:
            self.ids.brightnessControl.value += 0.05 * (self.ids.brightnessControl.max - self.ids.brightnessControl.min)

    def choose_file(self):
        self.open_file_manager()

    def open_file_manager(self):
        file_chooser = FileChooserIconView(path='./', filters=['*.mp3', '*.wav', '*.ogg'])
        file_chooser.bind(on_submit=self.select_file)
        file_chooser.bind(on_cancel=self.close_file_manager)
        self.popup_file_manager = Popup(title='Choose file', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    def select_file(self, instance, selection, *args):
        if selection:
            self.audio_source = AudioSegment.from_file(selection[0])
            self.popup_file_manager.dismiss()
            self.create_wave()

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()

    def create_wave(self):
        self.points = []

        if self.audio_source:
            samples = np.array(self.audio_source.get_array_of_samples())
            num_samples = len(samples)
            step = int(num_samples / self.width)
            for i in range(0, num_samples, step):
                y = self.height / 2 + (samples[i] / 32768) * self.height / 3
                x = self.ids.waveform_button.x + i * self.ids.waveform_button.width / num_samples

                self.points.extend([x, y])

            with self.ids.canvas_box.canvas.before:
                Color(1,1,1,1)
                Line(points=self.points, close=False, pos=self.ids.waveform_button.pos, width=1, size_hint=(0.5, 1))

            self.ids.canvas_box.remove_widget(self.ids.waveform_button)