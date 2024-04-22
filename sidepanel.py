'''
Side panel: a panel widget that attach to a side of the screen
'''

__all__ = ('SidePanel', )

from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import partial
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import *
from kivy.core.window import Window
from kivy.app import App
from waveform_panel import Waveform
from videoplayer import VideoPlayerApp
from table import InteractiveTable
from file_handler import file_handler
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
#from generate_subtitle_popup import GenerateSubtitlePopup
from dropdown import ComboBox
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from generate_subtitles import Generate
from title_manager import title_manager
from subtitle_handler import Subtitle_Handler

class SidePanel(Widget):
    '''A panel widget that attach to a side of the screen
    (similar to gnome-panel for linux user).

    :Parameters:
        `align` : str, default to 'center'
            Alignement on the side. Can be one of
            'left', 'right', 'top', 'bottom', 'center', 'middle'.
            For information, left-bottom, center-middle, right-top have the
            same meaning.
        `corner` : Widget object, default to None
            Corner object to use for pulling in/out the layout. If None
            is provided, the default will be a Button() with appropriate
            text label (depend of side)
        `corner_size` : int, default to 30
            Size of the corner, can be the width or height, it depend of side.
        `duration` : float, default to 0.5
            Animation duration for pull in/out
        `hide` : bool, default to True
            If true, the widget will be hide by default, otherwise,
            the panel is showed
        `layout` : AbstractLayout object, default to None
            Layout to use inside corner widget. If None is provided,
            the default will be a BoxLayout() with default parameters
        `side` : str, default to 'left'
            Side to attach the widget. Can be one of
            'left', 'right', 'top', 'bottom'.
    '''
    def __init__(self, **kwargs):
        kwargs.setdefault('hide', True)

        super(SidePanel, self).__init__(**kwargs)

        self.side        = kwargs.get('side', 'left')
        self.align       = kwargs.get('align', 'center')
        self.corner_size = kwargs.get('corner_size', 30)
        self.duration    = kwargs.get('duration', .5)
        self.relIndex    = kwargs.get('relative', 0)
        layout           = kwargs.get('layout', None)
        corner           = kwargs.get('corner', None)

        assert(self.side in ('bottom', 'top', 'left', 'right'))
        assert(self.align in ('bottom', 'top', 'left', 'right', 'middle', 'center'))

        if layout is None:
            from kivy.uix.boxlayout import BoxLayout
            layout = BoxLayout()
        self.layout = layout
        super(SidePanel, self).add_widget(layout)

        if corner is None:
            if self.side == 'right':
                label = '<'
            elif self.side == 'left':
                label = '>'
            elif self.side == 'top':
                label = 'v'
            elif self.side == 'bottom':
                label = '^'
            self.corner = Button(text=label)
        else:
            self.corner = Button()
            self.corner.texture = corner.texture
            self.corner.texture_size = corner.texture_size
            self.corner.size = corner.texture_size[0]+6, corner.texture_size[1]+6
            self.corner_size = None
        
        if corner:
          super(SidePanel, self).add_widget(self.corner)
        self.corner.bind(on_press = self._corner_on_press)

        self.initial_pos = self.pos
        self.need_reposition = True

        if kwargs.get('hide'):
            self.visible = False
            self.hide()
            
        Clock.schedule_once(self.update, .1)
    
    def add_widget(self, widget):
        self.layout.add_widget(widget)
        self.update()

    def remove_widget(self, widget):
        self.layout.remove_widget(widget)
        self.update()

    def _corner_on_press(self, *largs):
        if self.visible:
            self.hide()
        else:
            self.show()
        return True

    def _get_position_for(self, visible):
        # get position for a specific state (visible or not visible)
        w = self.get_parent_window()
        if not w:
            return

        side = self.side
        x = self.layout.x
        y = self.layout.y
        
        if visible:
            if side == 'right':
                x = w.width - self.layout.width 
            elif side == 'top':
                y = w.height - self.layout.height
            elif side == 'left':
                x = 0
            elif side == 'bottom':
                y = 0
        else:
            if side == 'left':
                x, y = (-self.layout.width, y)
            elif side == 'right':
                x, y = (w.width, y)
            elif side == 'top':
                x, y = (x, w.height)
            elif side == 'bottom':
                x, y = (x, -self.layout.height)
        return x, y

    def _get_corner_position_for(self, visible):
        # adjust size + configure position
        w = self.get_parent_window()
        if not w:
            return

        side = self.side
        align = self.align
        
        cw, ch = self.corner.size
        dx, dy = self._get_position_for(visible)
        if side in ('left', 'right'):
            if self.corner_size is not None:
                self.corner.size = (self.corner_size, self.layout.height)
            if align in ('bottom', 'left'):
                cy = ly = 0
            elif align in ('top', 'right'):
                ly = w.height - self.layout.height
                cy = w.height - ch
            elif align in ('center', 'middle'):
                ly = w.center[1] - self.layout.height / 2.
                cy = w.center[1] - ch / 2.
            self.layout.y = ly
        elif side in ('top', 'bottom'):
            if self.corner_size is not None:
                self.corner.size = (self.layout.width, self.corner_size)
            if align in ('bottom', 'left'):
                cx = lx = 0
            elif align in ('top', 'right'):
                lx = w.width - self.layout.width
                cx = w.width - cw
            elif align in ('center', 'middle'):
                lx = w.center[0] - self.layout.width / 2.
                cx = w.center[0] - cw / 2.
            self.layout.x = lx
        if side == 'left':
            cx = dx + self.layout.width
            cy = cy + self.corner.height * self.relIndex
        elif side == 'right':
            cx = dx - self.corner.width
            cy = cy + self.corner.height * self.relIndex
        elif side == 'top':
            cy = dy - self.corner.height
        elif side == 'bottom':
            cy = dy + self.layout.height
        return cx,cy
    
    def show(self, *largs):
        dpos = self._get_position_for(visible=True)
        cpos = self._get_corner_position_for(visible=True)
        
        # bring to front on activation
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(self)
        self.visible = True
        
        Animation(d=self.duration, t='out_cubic', pos=dpos).start(self.layout)
        Animation(d=self.duration, t='out_cubic', pos=cpos).start(self.corner)

    def _on_animation_complete_hide(self, *largs):
        self.visible = False

    def hide(self, *largs):
        dpos = self._get_position_for(visible=False)
        cpos = self._get_corner_position_for(visible=False)
        if dpos is None:
            return
        anim = Animation(d=self.duration, t='out_cubic', pos=dpos)
        anim.bind(on_complete=self._on_animation_complete_hide)
        anim.start(self.layout)
        Animation(d=self.duration, t='out_cubic', pos=cpos).start(self.corner)

    def place(self, noop=None):
        self.need_reposition = True
        self.update(noop)
        
    def update(self, noop=None):
        w = self.get_parent_window()
        side = self.side
        align = self.align

        # first execution, need to place layout in the good size
        if self.need_reposition:
            dpos = self._get_position_for(self.visible)
            if dpos is not None:
              self.layout.pos = dpos
              self.corner.pos = self._get_corner_position_for(self.visible)
              self.need_reposition = False
              if self.visible:
                self.show()
              else:
                self.hide()
            else:
              return
                      
    def on_move(self, x, y):
        self.initial_pos = x, y
        self.layout.pos  = x, y

    def on_touch_down(self, touch):
        if self.corner.on_touch_down(touch):
            return True
        return super(SidePanel, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.corner.on_touch_move(touch):
            return True
        return super(SidePanel, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.corner.on_touch_up(touch):
            return True
        return super(SidePanel, self).on_touch_up(touch)

class SidePanel(BoxLayout):
    waveform_instance = Waveform()
    def __init__(self, left_layout, **kwargs):
        Builder.load_file('sidepanel.kv')
        super().__init__(**kwargs)

        self.video_source = None
        self.left_layout = left_layout
        self.size_hint = (None, 0.97)
        self.width = 90
        self.pos_hint = {"right": 1, "bottom": 1}
        self.title_manager = title_manager()
        self.subtitle_handler = Subtitle_Handler()

        self.visible = False # určuje, jestli je sidepanel otevřený, a nebo zavřený

        # Funkcionalita pro zobrazení waveform panelu
        self.waveform_visible = True
        #self.waveform_instance = Waveform()
        self.left_layout.add_widget(SidePanel.waveform_instance)

        # Funkcionalita pro zobrazení video přehrávače
        self.videoplayer_visible = True
        self.videoplayer_instance = VideoPlayerApp()
        self.left_layout.add_widget(self.videoplayer_instance)

        # Funkcionalita pro zobrazení tabulky
        self.table_visible = True
        self.table_instance = InteractiveTable()
        self.left_layout.add_widget(self.table_instance)

    def show(self):
        anim = Animation(width=260, duration=0.15)
        anim.start(self)
        self.visible = True

    def hide(self):
        anim = Animation(width=90, duration=0.15)
        anim.start(self)
        self.visible = False

    # Funkce na tlačítkách
    def toggle_panel(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def show_popup(self):
        layout = GenerateSubtitlePopup()
        print(layout.height)
        popup = Popup(title='Generate subtitles', content=layout, size_hint=(None, None), size=(600, 400), auto_dismiss=True)
        popup.open()
    def new_project(self):
        print("New project")
    def open_project(self):
        print("Open project")
    def save_project(self):
        print("Save project")
    def generate_subtitles(self):
        self.show_popup()
    def toggle_table(self):
        if self.table_visible:
            self.left_layout.remove_widget(self.table_instance)
            self.table_instance = None
            self.table_visible = False
        else:
            self.table_instance = InteractiveTable()
            self.left_layout.add_widget(self.table_instance)
            self.table_visible = True
    def toggle_video(self):
        if self.videoplayer_visible:
            self.videoplayer_instance.video.state = 'pause'
            self.left_layout.remove_widget(self.videoplayer_instance)
            self.videoplayer_instance = None
            self.videoplayer_visible = False
        else:
            self.videoplayer_instance = VideoPlayerApp()
            self.left_layout.add_widget(self.videoplayer_instance)
            self.videoplayer_visible = True
    def toggle_waveform(self):
        if self.waveform_visible:
            self.left_layout.remove_widget(SidePanel.waveform_instance)
            SidePanel.waveform_instance = None
            self.waveform_visible = False
        else:
            SidePanel.waveform_instance = Waveform()
            self.left_layout.add_widget(SidePanel.waveform_instance)
            self.waveform_visible = True

    def help(self):
        print("Help")

class GenerateSubtitlePopup(FloatLayout):
    def __init__(self):
        super().__init__()
        self.generate = Generate()
        self.file_handler = file_handler()
        self.size_hint = (1, 1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.size = (400, 400)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.atributes = {}
        self.subtitle_handler = Subtitle_Handler()
        #self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        main_grid = GridLayout(cols=1, rows=3, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        grid = GridLayout(cols=2, rows=4, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        #grid.add_widget(Label(text='Language of audio:', size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        #self.language_combobox = ComboBox(options=['English', 'Czech', 'Russian'], size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        #grid.add_widget(self.language_combobox)

        grid.add_widget(Label(text='Format of subtitles:', size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.format_combobox = ComboBox(options=['SubRip (.srt)', 'Text file (.txt)', 'Adobe Premiere Pro (.xml)'], size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        grid.add_widget(self.format_combobox)

        grid.add_widget(Label(text='Audio / Video file:', size_hint=(1, 0.1), pos_hint={'top': 1}))
        file_button = Button(text='Choose file', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        file_button.bind(on_press=self.on_button_file)
        grid.add_widget(file_button)

        grid.add_widget(Label(text='Limits:', size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.limits = CheckBox(size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, active=False)
        self.limits.bind(active=partial(self.on_limit_checkbox_active))
        grid.add_widget(self.limits)

        #-----------------------------------------------------------------------

        grid_two = GridLayout(cols=3, rows=2, size_hint=(1, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        grid_two.add_widget(Label(text='Max. number of characters:', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.numOfCharsLimit = TextInput(hint_text='', multiline=False, size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, disabled=True)
        self.checkOfCharsLimit = CheckBox(size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, disabled=True, group='charsLimits')
        self.checkOfCharsLimit.bind(active=partial(self.on_limit_select))
        grid_two.add_widget(self.numOfCharsLimit)
        grid_two.add_widget(self.checkOfCharsLimit)

        grid_two.add_widget(Label(text='Max. number of words:', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.numOfWordsLimit = TextInput(hint_text='', multiline=False, size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, disabled=True)
        self.checkOfWordsLimit = CheckBox(size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, disabled=True, group='wordsLimits')
        self.checkOfWordsLimit.bind(active=partial(self.on_limit_select))
        grid_two.add_widget(self.numOfWordsLimit)
        grid_two.add_widget(self.checkOfWordsLimit)

        main_grid.add_widget(grid)
        main_grid.add_widget(grid_two)
        flex = FloatLayout(size_hint=(1, None), pos_hint={'center_x': 0.5, 'bottom': 0.95})
        generate = Button(text='Generate', size=(100, 50), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.45})

        generate.bind(on_press=self.on_generate_submit)
        flex.add_widget(generate)

        main_grid.add_widget(flex)
        self.add_widget(main_grid)
    def on_button_file(self, instance):
        self.open_file_manager()

    def on_select_file(self, instance, selection, *args):
        if selection:
            self.video_source = selection[0]
            self.popup_file_manager.dismiss()
            print(self.video_source)
    def open_file_manager(self):
        file_chooser = FileChooserIconView(path='', filters=['*.mp3', '*.wav', '*.ogg', '*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv'])
        file_chooser.bind(on_submit=self.on_select_file)
        file_chooser.bind(on_cancel=self.close_file_manager)
        self.popup_file_manager = Popup(title='Vyberte video', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()
    def close_file_manager(self, instance):
        self.popup_file_manager.dismiss()

    '''Kontroluje, jestli je zaškrtnutý checkbox pro aktivování limitů'''
    def on_limit_checkbox_active(self, checkbox, value):
        if value:
            self.numOfCharsLimit.disabled = False
            self.checkOfCharsLimit.disabled = False
            self.numOfWordsLimit.disabled = False
            self.checkOfWordsLimit.disabled = False
        else:
            self.checkOfCharsLimit.active = False
            self.checkOfWordsLimit.active = False

            self.numOfCharsLimit.disabled = True
            self.checkOfCharsLimit.disabled = True
            self.numOfWordsLimit.disabled = True
            self.checkOfWordsLimit.disabled = True
    def on_limit_select(self, checkbox, value):
        if value:
            if checkbox.group == 'charsLimits':
                self.checkOfWordsLimit.disabled = True
                self.numOfWordsLimit.disabled = True
            elif checkbox.group == 'wordsLimits':
                self.checkOfCharsLimit.disabled = True
                self.numOfCharsLimit.disabled = True
        else:
            self.checkOfCharsLimit.disabled = False
            self.numOfCharsLimit.disabled = False
            self.checkOfWordsLimit.disabled = False
            self.numOfWordsLimit.disabled = False
    def get_attributes(self):
        if self.format_combobox.select != '':
            # self.language_combobox.select != ''
            #self.atributes['language'] = self.language_combobox.select
            self.atributes['format'] = self.format_combobox.select
            self.atributes['video_source'] = self.video_source
            self.atributes['is_limited'] = self.limits.active
    def parse_inputs_to_num(self):
        if self.limits.active:
            try:
                if self.checkOfCharsLimit.active:
                    self.atributes['chars_limit'] = int(self.numOfCharsLimit.text)
                elif self.checkOfWordsLimit.active:
                    self.atributes['words_limit'] = int(self.numOfWordsLimit.text)
            except ValueError:
                print("Neplatný vstup")
    def on_generate_submit(self, instance):
        self.atributes = {}
        self.get_attributes()
        self.parse_inputs_to_num()
        print(self.atributes)
        self.file_handler.set_source(self.atributes['video_source'])

        extracted_audio = self.generate.extract_audio(rf"{self.atributes['video_source']}")

        self.segments = []

        if self.atributes['is_limited']:
            if 'chars_limit' in self.atributes:
                self.segments = self.generate.transcribe(extracted_audio, True, False, self.atributes['chars_limit'])
            else:
                self.segments = self.generate.transcribe(extracted_audio, True, True, self.atributes['words_limit'])
        else:
            self.segments = self.generate.transcribe(extracted_audio, False, False, 0)

        SidePanel.waveform_instance.generate_from_generator(self.segments)

    def convert_to_subtitle_list(self):
        subtitles = []
        for segment in self.segments:
            subtitles.append({'start': segment[1], 'end': segment[2], 'text': segment[0]})
        self.subtitle_handler.subtitle_list = subtitles