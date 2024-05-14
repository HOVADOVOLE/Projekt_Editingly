import json
from subtitle_handler import Subtitle_Handler
from file_handler import file_handler

class Export():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Export, cls).__new__(cls, *args, **kwargs)
            cls._instance.subtitle_handler = Subtitle_Handler()
            cls._instance.file_handler = file_handler()

            cls._instance.subtitle_list = []
            cls._instance.video_source = ""

        return cls._instance

    def save_data(self):
        self.video_source = self.file_handler.source
        self.subtitle_list = self.subtitle_handler.subtitle_list

        print(self.subtitle_list, self.video_source)
        #with open('export.json', 'w') as file:
        #    json.dump({'subtitle_list': self.subtitle_list, 'video_source': self.video_source}, file)