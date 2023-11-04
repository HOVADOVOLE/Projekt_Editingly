from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

class Waveform(BoxLayout):
    def __init__(self, **kwargs: object) -> object:
        self.size_hint = (1, 0.3)
        Builder.load_file('waveform.kv')
        super(Waveform, self).__init__(**kwargs)
        self.orientation = 'vertical'

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
            #self.video.source = selection[0]
            print(selection[0])
            self.popup_file_manager.dismiss()

    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()

    def on_video_loaded(self, instance, value):
        #self.video_loaded = True
        self.unbind(on_touch_up=self.on_touch_up)
        self.update_slider_position(self.video.position, self.video.duration)