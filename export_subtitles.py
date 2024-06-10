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
        box = BoxLayout(orientation='vertical', padding=[20, 50, 20, 20], spacing=20)

        # GridLayout for centering the elements
        layout = GridLayout(cols=1, spacing=20, size_hint=(None, None), width=400)
        layout.bind(minimum_height=layout.setter('height'))

        # Label and Spinner
        lbl_format = Label(text='Formát titulek:', size_hint=(None, None), width=150, height=44)
        self.format_spinner = Spinner(
            text='Select format',
            values=['SubRip (.srt)', 'Text file (.txt)', 'Adobe Premiere Pro (.xml)'],
            size_hint=(None, None),
            size=(170, 44)
        )

        format_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44)
        format_layout.add_widget(lbl_format)
        format_layout.add_widget(self.format_spinner)

        # Centering the format_layout
        format_container = BoxLayout(size_hint=(1, None), height=44, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        format_container.add_widget(format_layout)

        # Label and Button
        lbl_location = Label(text='Místo uložení:', size_hint=(None, None), width=150, height=44)
        btn_location = Button(text='Vybrat místo uložení', size_hint=(None, None), size=(170, 44))
        btn_location.bind(on_press=self.show_file_chooser)

        location_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44)
        location_layout.add_widget(lbl_location)
        location_layout.add_widget(btn_location)

        # Centering the location_layout
        location_container = BoxLayout(size_hint=(1, None), height=44)
        location_container.add_widget(location_layout)

        # Add horizontal layouts to the main layout
        layout.add_widget(format_container)
        layout.add_widget(location_container)

        # Add the main layout to the box
        box.add_widget(layout)

        # Create and add the submit button
        submit_button = Button(
            text='Odeslat',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5}
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

        file_label = Label(text='Název souboru:', size_hint=(None, None), width=150, height=40)
        self.file_name_input = TextInput(text='export', size_hint=(None, None), width=150, height=40)

        confirm_button = Button(text='Confirm', size_hint=(None, None), width=100, height=40)
        confirm_button.bind(on_press=lambda x: self.select_folder(file_chooser.path))

        # Layout pro popisek, textový vstup a tlačítko
        input_button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), width=350, height=40)
        input_button_layout.add_widget(file_label)
        input_button_layout.add_widget(self.file_name_input)
        input_button_layout.add_widget(confirm_button)

        # Obalový layout pro centrální zarovnání
        center_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=30)
        center_layout.add_widget(BoxLayout(size_hint=(0.25, 1)))
        center_layout.add_widget(input_button_layout)
        center_layout.add_widget(BoxLayout(size_hint=(0.25, 1)))

        # Hlavní vertikální layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(file_chooser)
        layout.add_widget(center_layout)

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