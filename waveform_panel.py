from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics import Line, Color, Rectangle
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
        self.last_point = 0
        self.pocatek = None
        self.konec = None
        self.sections = [] # ukládá pozice začátku a konce sekce
        self.previous_win_size = None

        Clock.schedule_interval(self.update_slider_position, 0.1)

        self.ids.canvas_box.bind(on_touch_down=self.stisk)
        self.ids.canvas_box.bind(on_touch_up=self.pusteni)

        if self.file_handler.get_source() is not None:
            source = self.file_handler.get_source()
            self.audio_source = AudioSegment.from_file(source)
            self.create_wave()
        self.ids.brightnessControl.bind(value=self.on_value)
    def on_value(self, instance, value):
        if abs(self.last_point - value) > 1:
            self.file_handler.set_posunuti_videa_state(True)
            self.file_handler.set_posunuti_videa(value)
            #self.file_handler.set_cas_posun(5)
        self.last_point = value

    def stisk(self, instance, touch):
        if self.ids.canvas_box.collide_point(*touch.pos):
            if touch.is_double_tap:
                with self.ids.canvas_box.canvas.after:
                    Color(0, 0, 0, 1)
                    Line(points=[touch.pos[0], self.ids.canvas_box.y, touch.pos[0], self.ids.canvas_box.y + self.ids.canvas_box.height], width=4)
            self.pocatek = touch.pos[0]
            self.ids.brightnessControl.value = touch.pos[0]
            self.file_handler.set_video_position(touch.pos[0])


    def pusteni(self, instance, touch):
        if self.ids.canvas_box.collide_point(*touch.pos):
            self.konec = touch.pos[0]
            self.sections.append([self.pocatek, self.konec])
            self.draw_section()

    def move_slider_backward(self):
        if self.ids.brightnessControl.value > self.ids.brightnessControl.min:
            #self.file_handler.set_video_position(self.ids.brightnessControl.value)
            self.file_handler.set_cas_posun(-5)
            self.file_handler.set_posun(True)
            #self.ids.brightnessControl.value -= 0.05 * (self.ids.brightnessControl.max - self.ids.brightnessControl.min)
    def move_slider_forward(self):
        if self.ids.brightnessControl.value < self.ids.brightnessControl.max:
            self.file_handler.set_cas_posun(5)
            self.file_handler.set_posun(True)
            #self.ids.brightnessControl.value += 0.05 * (self.ids.brightnessControl.max - self.ids.brightnessControl.min)
    def video_state(self):
        state = self.file_handler.get_video_play()
        if state:
            self.file_handler.set_video_play(False)
        else:
            self.file_handler.set_video_play(True)
    def choose_file(self):
        if self.file_handler.get_source() is None:
            self.open_file_manager()
        else:
            source = self.file_handler.get_source()
            self.audio_source = AudioSegment.from_file(source)
            self.create_wave()

    def draw_section(self):
        delka = abs(self.pocatek - self.konec)
        self.prohozeni()
        if delka > 20 and self.audio_source is not None:
            # Clear previous sections by removing the 'section' group
            #self.ids.canvas_box.canvas.after.remove_group('section')

            self.ids.canvas_box.canvas.after.add(Color(1, 0.549, 0, 1))
            self.ids.canvas_box.canvas.after.add(Line(points=[self.pocatek, self.ids.canvas_box.y, self.pocatek,
                         self.ids.canvas_box.y + self.ids.canvas_box.height], width=2, group='section'))
            self.ids.canvas_box.canvas.after.add(Color(1, 0, 0, 0.2))
            self.ids.canvas_box.canvas.after.add(Rectangle(pos=(min(self.pocatek, self.konec), self.ids.canvas_box.y),
                      size=(delka, self.ids.canvas_box.height), group='section'))
            self.ids.canvas_box.canvas.after.add(Color(1, 0.549, 0, 1))
            self.ids.canvas_box.canvas.after.add(Line(points=[self.konec, self.ids.canvas_box.y, self.konec,
                         self.ids.canvas_box.y + self.ids.canvas_box.height], width=2, group='section'))

    def prohozeni(self):
        if self.pocatek > self.konec:
            temp = self.pocatek
            self.pocatek = self.konec
            self.konec = temp

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
    def rewrite_sectors(self):
        try:
            for i in range(len(self.sections)):
                for j in range(2):
                    self.sections[i][j] = self.sections[i][j] * Window.width / self.previous_win_size
        except:
            return
    def delete_sections(self):
        try:
            if self.previous_win_size is not None and abs(self.previous_win_size - Window.width) > 2:
                self.ids.canvas_box.canvas.after.remove_group('section')
        except:
            print("Něco se nepovedlo")

    def rerender_sections(self):
        self.rewrite_sectors()

        # Clear previous sections by removing the 'section' group
        self.ids.canvas_box.canvas.after.remove_group('section')

        with self.ids.canvas_box.canvas.after:
            for i in range(len(self.sections)):
                Color(1, 0.549, 0, 1)
                Line(points=[self.sections[i][0], self.ids.canvas_box.y, self.sections[i][0],
                             self.ids.canvas_box.y + self.ids.canvas_box.height], width=2, group='section')
                Color(1, 0, 0, 0.2)
                Rectangle(pos=(min(self.sections[i][0], self.sections[i][1]), self.ids.canvas_box.y),
                          size=(abs(self.sections[i][0] - self.sections[i][1]), self.ids.canvas_box.height),
                          group='section')
                Color(1, 0.549, 0, 1)
                Line(points=[self.sections[i][1], self.ids.canvas_box.y, self.sections[i][1],
                             self.ids.canvas_box.y + self.ids.canvas_box.height], width=2, group='section')
    def update_size_of_sections(self, *args):
        self.delete_sections()
        self.rerender_sections()
    def update_wave_size(self, *args):
        if self.previous_win_size is not None and abs(self.previous_win_size - Window.width) > 2:
            self.update_size_of_sections()

        self.ids.canvas_box.canvas.clear()

        num_samples = len(self.samples)
        step = int(num_samples / self.width)
        self.points = []

        for i in range(0, num_samples, step):
            y = self.height / 2.5 + (self.samples[i] / 32768) * self.height * 0.8
            x = i * self.ids.canvas_box.width / num_samples

            self.points.extend([x, y])
        with self.ids.canvas_box.canvas:
            Color(1, 1, 1, 1)
            Line(points=self.points, close=False, width=1)

            Color(0, 0, 0, 1)
            Line(rectangle=(0, 0, self.ids.canvas_box.width, self.ids.canvas_box.height), width=2)

        self.previous_win_size = Window.width

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
                Color(1, 1, 1, 1)
                Line(points=self.points, close=False, width=1)

            try:
                self.ids.canvas_box.remove_widget(self.ids.waveform_button)
            except:
                print('Waveform button not found')

            Window.bind(on_resize=self.update_wave_size)  # zajišťuje responsivitu pro změnu velikosti okna
            Window.bind(on_maximize=self.update_wave_size)  # zajišťuje responsivitu pro maximalizaci okna
            Window.bind(on_restore=self.update_wave_size)  # zajišťuje responsivitu pro zmenšení okna
            Window.bind(size=self.update_wave_size)  # zajišťuje responsivitu pro přenos mezi monitory
            Window.bind(on_draw=self.update_wave_size)  # zajišťuje responsivitu i když vypnu okno a pak ho zase zapnu

            Window.bind(on_resize=self.update_size_of_sections)
            Window.bind(on_maximize=self.update_size_of_sections)
            Window.bind(on_restore=self.update_size_of_sections)
            Window.bind(size=self.update_size_of_sections)
            Window.bind(on_draw=self.update_size_of_sections)

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