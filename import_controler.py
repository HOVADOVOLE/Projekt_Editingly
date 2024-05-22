import json
from subtitle_handler import Subtitle_Handler
from file_handler import file_handler
from sidepanel import SidePanel
#from title_manager import title_manager

class ImportControler():
    def __init__(self):
        self.subtitle_handler = Subtitle_Handler()
        self.file_handler = file_handler()
        #self.title_manager = title_manager()

        self.video_source = ""
        self.subtitle_list = []
        self.convert_data: list = []
    def check_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if 'video_source' not in data or 'subtitle_list' not in data:
                    print("Invalid json file")
                    return

                self.video_source = data['video_source']
                self.subtitle_list = data['subtitle_list']
                self.load_to_editor()

        except FileNotFoundError:
            print("File not found")

    def load_to_editor(self):
        self.file_handler.set_source(self.video_source)
        converted_data = [(item['text'], float(item['start']), float(item['end'])) for item in self.subtitle_list]
        #self.subtitle_handler.subtitle_list = converted_data
        SidePanel.waveform_instance.generate_from_generator(converted_data)
        print(converted_data)
        #self.title_manager.load_subtitles()
        #self.title_manager.load_video()