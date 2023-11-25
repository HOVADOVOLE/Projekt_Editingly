class file_handler:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(file_handler, cls).__new__(cls, *args, **kwargs)
            cls._instance.source = None
            cls._instance.video_position = 0
            cls._instance.max_value = 0
            cls._instance.video_play = False
            cls._instance.cas_posun = 0
            cls._instance.posun = False
            cls._instance.nastav_posun = 0
            cls._instance.posunuti_videa = False
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
    def set_video_play(self, video_play):
        self.video_play = video_play
    def get_video_play(self):
        return self.video_play
    def set_cas_posun(self, cas_posun):
        self.cas_posun = cas_posun
    def get_cas_posun(self):
        return self.cas_posun
    def get_posun(self):
        return self.posun
    def set_posun(self, posun):
        self.posun = posun
    def set_posunuti_videa(self, posun):
        self.nastav_posun = posun
    def get_posunuti_videa(self):
        return self.nastav_posun
    def set_posunuti_videa_state(self, posun):
        self.posunuti_videa = posun
    def get_posunuti_videa_state(self):
        return self.posunuti_videa