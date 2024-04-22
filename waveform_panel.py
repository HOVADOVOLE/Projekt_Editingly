from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics import Line, Color, Rectangle
from pydub import AudioSegment
import numpy as np
from kivy.core.window import Window
from file_handler import file_handler
from title_manager import title_manager
from kivy.clock import Clock
from kivy.uix.button import Button
from subtitle_handler import Subtitle_Handler
from moviepy.editor import VideoFileClip

Builder.load_file('waveform.kv')

class Waveform(BoxLayout):
    def __init__(self, **kwargs):
        super(Waveform, self).__init__(**kwargs)
        self.file_handler = file_handler()
        self.title_manager = title_manager()
        self.subtitle_handler = Subtitle_Handler()

        self.points = []
        self.audio_source = None
        self.popup_file_manager = None
        self.samples = []
        self.last_point = 0
        self.pocatek = None
        self.konec = None
        self.sections = [] # ukládá pozice začátku a konce sekce
        self.previous_win_size = None
        self.popup = None

        self.selected_sector = None

        Clock.schedule_interval(self.clock_handler, 0.1)

        self.ids.canvas_box.bind(on_touch_down=self.stisk)
        self.ids.canvas_box.bind(on_touch_up=self.pusteni)
        self.title_manager.waveform_width = self.ids.canvas_box.width

        if self.file_handler.get_source() is not None:
            source = self.file_handler.get_source()
            self.audio_source = AudioSegment.from_file(source)
            self.create_wave()
        self.ids.brightnessControl.bind(value=self.on_value)
    def on_value(self, instance, value):
        if abs(self.last_point - value) > 1:
            self.file_handler.set_posunuti_videa_state(True)
            self.file_handler.set_posunuti_videa(value)
        self.last_point = value
    def add_section(self, instance):
        # if statement kontroluje, jestli sekce již nemá vytvořenou titulku
        if not self.sections[self.selected_sector][2]:
            self.sections[self.selected_sector][2] = True
            self.title_manager.create_subtitle_section(self.pocatek, self.konec)
            self.title_manager.add_row = True
            self.subtitle_handler.add_subtitle(self.pocatek, self.konec, "ahoj")
            self.popup.dismiss()

    def delete_section(self, instance):
        self.ids.canvas_box.canvas.after.remove_group('section')
        del self.sections[self.selected_sector]
        self.title_manager.remove_row(self.selected_sector)
        self.rerender_sections()

        self.popup.dismiss()
    def render_popup(self, touch):
        x, y = touch
        content = BoxLayout(orientation='vertical')
        content.add_widget(Button(text='Přidat sekci', on_press=self.add_section))
        content.add_widget(Button(text='Vymazat sekci', on_press=self.delete_section))

        self.popup = Popup(content=content, title='Popup Menu', size_hint=(None, None), size=(200, 150))

        # Zobrazíme Popup menu na zadaných souřadnicích
        self.popup.open(pos=(x, y))
    def try_find_sector(self, mouse_position):
        for i in range(len(self.sections)):
            if self.sections[i][0] <= mouse_position[0] <= self.sections[i][1]:
                self.selected_sector = i
                self.render_popup(mouse_position)
                break # Ukončí cyklus hledání sektoru
    def stisk(self, instance, touch):
        if self.ids.canvas_box.collide_point(*touch.pos):
            # kontroluje, jestli není stisknuto pravé tlačítko myši
            if self.audio_source is not None:
                if touch.button == 'right':
                    self.try_find_sector(touch.pos)

                if touch.is_double_tap and not touch.button == 'right':
                    with self.ids.canvas_box.canvas.after:
                        Color(0, 0, 0, 1)
                        Line(points=[touch.pos[0], self.ids.canvas_box.y, touch.pos[0], self.ids.canvas_box.y + self.ids.canvas_box.height], width=4, group='pointer')
                        # posune video na tuto pozici
                        #self.file_handler.set_video_position(touch.pos[0])
                        #self.file_handler.set_posunuti_videa_state(True)

                self.pocatek = touch.pos[0]
                self.ids.brightnessControl.value = touch.pos[0]
                self.file_handler.set_video_position(touch.pos[0])

    def pusteni(self, instance, touch):
        if self.ids.canvas_box.collide_point(*touch.pos) and self.audio_source is not None:
            self.konec = touch.pos[0]
            if not self.check_prekryti() and abs(self.pocatek - self.konec) > 10:
                self.sections.append([self.pocatek, self.konec, False])
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

    def check_sections_to_create(self):
        if len(self.sections) == 0:
            return False
        for i in range(len(self.sections)):
            # Zjistí, zda se nově vytvářená sekce překrývá s existující sekcí
            if (self.sections[i][0] <= self.pocatek <= self.sections[i][1] or
                    self.sections[i][0] <= self.konec <= self.sections[i][1] or
                    (self.pocatek <= self.sections[i][0] and self.konec >= self.sections[i][1])):
                return True
        return False
    def check_prekryti(self):
        if self.pocatek is not None and self.konec is not None:
            for i in range(len(self.sections)):
                if (self.sections[i][0] <= self.pocatek <= self.sections[i][1] or
                        self.sections[i][0] <= self.konec <= self.sections[i][1] or
                        (self.pocatek <= self.sections[i][0] and self.konec >= self.sections[i][1])):
                    return True
        return False
    def draw_section(self):
        delka = abs(self.pocatek - self.konec)
        self.prohozeni()
        # cyklus zkontroluje jestli vytvářená sekce nepřekrývá s již existujícími sekcemi, a pokud ano, zak vrátí true
        if delka > 20 and self.audio_source is not None:
            self.ids.canvas_box.canvas.after.remove_group('section')
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

        self.title_manager.waveform_width = self.ids.canvas_box.width
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
    def clock_handler(self, *args):
        self.update_slider_position()
        if self.title_manager.get_remove_row():
            self.delete_section_by_table(self.title_manager.index_to_remove)
    def delete_section_by_table(self, index):
        if index is not None:
            try:
                self.ids.canvas_box.canvas.after.remove_group('section')
                del self.sections[index]
                self.title_manager.remove_row(index)
                self.rerender_sections()

                self.title_manager.remove_row_statement = False
                self.title_manager.index_to_remove = None
            except:
                return
    def update_slider_position(self, *larg):
        a = self.file_handler.get_max_value()
        self.ids.brightnessControl.max = a
        self.ids.brightnessControl.value = self.file_handler.get_video_position()

        # Kontroluje, jestli byl změnený zdroj videa
        if self.audio_source is None:
            if self.file_handler.get_source() is not None:
                source = self.file_handler.get_source()
                self.audio_source = AudioSegment.from_file(source)
                self.create_wave()
    def generate_from_generator(self, segmenty):
        self.file_handler.set_max_value(self.get_video_length(self.file_handler.get_source()))
        self.title_manager.max_video_position = self.file_handler.get_max_value()
        print("délka mého pelete", self.file_handler.get_max_value())
        self.recalculate_time_to_position(segmenty)

    def recalculate_time_to_position(self, segmenty):
        self.sections = []
        print(self.ids.canvas_box.x, self.ids.canvas_box.size)
        try:
            for segment in segmenty:
                print(segment[1], segment[2], type(segment[1]), type(segment[2]))
                #self.title_manager.create_subtitle_section(segment[1], segment[2])
                self.sections.append([self.time_to_position(segment[1]), self.time_to_position(segment[2]), False])
        except Exception as e:
            print(f"Error: {e}")
        print(self.sections)

    def time_to_position(self, time):
        start_pos = self.ids.canvas_box.x
        end_pos = self.ids.canvas_box.x + self.ids.canvas_box.width
        pozice = self.ids.canvas_box.width * time / self.file_handler.get_max_value() + start_pos
        return pozice
    def get_video_length(self, video_path):
        try:
            clip = VideoFileClip(video_path)
            duration = clip.duration
            clip.close()
            return duration
        except Exception as e:
            print(f"Error: {e}")
            return None