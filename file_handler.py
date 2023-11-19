class file_handler:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(file_handler, cls).__new__(cls, *args, **kwargs)
            cls._instance.source = None
            cls._instance.video_position = 0
            cls._instance.max_value = 0
        return cls._instance

    def get_source(self):
        return self.source
    def set_video_position(self, video_position):
        self.video_position = video_position
    def get_video_position(self):
        return self.video_position
    def set_source(self, source):
        self.source = source
    def get_max_value(self):
        return self.max_value
    def set_max_value(self, max_value):
        self.max_value = max_value