from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from converter import SubtitleConverter


class ExportSubtitles(App):
    def build(self):
        box = BoxLayout(orientation='vertical')
        layout = GridLayout(cols=2, spacing=10, size_hint=(1, 1))

        # Label and Spinner
        lbl_format = Label(text='Formát titulek:', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.format_spinner = Spinner(
            text='Select format',
            values=['SubRip (.srt)', 'Text file (.txt)', 'Adobe Premiere Pro (.xml)'],
            size_hint=(None, None),
            size=(170, 44),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        lbl_location = Label(text='Místo uložení:')
        btn_location = Button(text='Vybrat místo uložení', size_hint=(None, None), size=(170, 44))
        btn_location.bind(on_press=self.show_file_chooser)

        # Add Label and Spinner to the layout
        layout.add_widget(lbl_format)
        layout.add_widget(self.format_spinner)
        layout.add_widget(lbl_location)
        layout.add_widget(btn_location)

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

        if hasattr(self, 'selected_path') and hasattr(self, 'file_name'):
            if format == 'SubRip (.srt)':
                self.convert_to_subrip()
            elif format == 'Text file (.txt)':
                self.convert_to_txt()
            elif format == 'Adobe Premiere Pro (.xml)':
                self.convert_to_xml()
        else:
            print("Path or file name not selected")

    def show_file_chooser(self, instance):
        file_chooser = FileChooserListView(path='./', dirselect=True)

        self.file_name_input = TextInput(text='export')

        confirm_button = Button(text='Confirm')
        confirm_button.bind(on_press=lambda x: self.select_folder(file_chooser.path))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(file_chooser)
        layout.add_widget(self.file_name_input)
        layout.add_widget(confirm_button)

        self.popup_file_manager = Popup(title='Choose folder and file name', content=layout, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    def select_folder(self, path):
        self.selected_path = path
        self.file_name = self.file_name_input.text
        print(f"Selected path: {self.selected_path}, File name: {self.file_name}")
        self.popup_file_manager.dismiss()

    def convert_to_subrip(self):
        file_name = f"{self.selected_path}/{self.file_name}.srt"
        converter = SubtitleConverter()
        srt_content = converter.convert_to_srt(file_name)
        print(f"SubRip subtitles saved to: {file_name}")

    def convert_to_txt(self):
        file_name = f"{self.selected_path}/{self.file_name}.txt"
        converter = SubtitleConverter()
        txt_content = converter.convert_to_txt(file_name)
        print(f"Text subtitles saved to: {file_name}")

    def convert_to_xml(self):
        file_name = f"{self.selected_path}/{self.file_name}.xml"
        converter = SubtitleConverter()
        xml_content = converter.convert_to_xml(file_name)
        print(f"XML subtitles saved to: {file_name}")