from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner  # Changed to Spinner for standard Kivy usage

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from converter import SubtitleConverter

class ExportSubtitles(App):
    def build(self):
        box = BoxLayout(orientation='vertical')
        layout = GridLayout(cols=2, spacing=10, size_hint=(1, 1))

        # Label and Spinner
        txtLabel = Label(text='Formát titulek:', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.format_spinner = Spinner(
            text='Select format',
            values=['SubRip (.srt)', 'Text file (.txt)', 'Adobe Premiere Pro (.xml)'],
            size_hint=(None, None),
            size=(250, 44),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Add Label and Spinner to the layout
        layout.add_widget(txtLabel)
        layout.add_widget(self.format_spinner)

        # Add the layout to the box
        box.add_widget(layout)

        # Create and add the submit button
        submit_button = Button(
            text='Odeslat',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Bind the button to a function
        submit_button.bind(on_press=self.on_submit)

        # Add the button to the box
        box.add_widget(submit_button)

        return box

    def on_submit(self, instance):
        format = self.format_spinner.text

        if format == 'SubRip (.srt)':
            self.convert_to_subrip()
        elif format == 'Text file (.txt)':
            self.convert_to_txt()
        elif format == 'Adobe Premiere Pro (.xml)':
            self.convert_to_xml()
    def convert_to_subrip(self):
        SubtitleConverter().convert_to_srt()
    def convert_to_xml(self):
        SubtitleConverter().convert_to_xml()
    def convert_to_txt(self):
        SubtitleConverter().convert_to_txt()