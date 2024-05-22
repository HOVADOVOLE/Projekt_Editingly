import json
from subtitle_handler import Subtitle_Handler
from file_handler import file_handler
#from title_manager import title_manager

class ImportControler():
    def __init__(self):
        self.subtitle_handler = Subtitle_Handler()
        self.file_handler = file_handler()
        #self.title_manager = title_manager()

        self.video_source = ""
        self.subtitle_list = []
    def check_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if 'video_source' not in data or 'subtitle_list' not in data:
                    print("Invalid json file")
                    return

                self.video_source = data['video_source']
                self.subtitle_list = data['subtitle_list']
                print(self.video_source)
                self.load_to_editor()

        except FileNotFoundError:
            print("File not found")

    def load_to_editor(self):
        self.file_handler.set_source(self.video_source)
        self.subtitle_handler.subtitle_list = self.subtitle_list
        #self.title_manager.load_subtitles()
        #self.title_manager.load_video()