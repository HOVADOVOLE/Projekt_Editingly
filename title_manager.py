class title_manager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(title_manager, cls).__new__(cls, *args, **kwargs)
            cls._instance.start_time = None
            cls._instance.end_time = None
            cls._instance.video_position = 0
            cls._instance.waveform_width = 0
            cls._instance.text = None
            cls._instance.row_index = None
            cls._instance.add_row = False
            cls._instance.remove_row_statement = False
            cls._instance.index_to_remove = 0
            cls._instance.max_video_position = 0
        return cls._instance
    def create_subtitle_section(self, start_time, end_time):
        #self.start_time = self.waveform_width / start_time
        #self.end_time = self.waveform_width / end_time
        #todo někde upravit aby se nastavila max_video_position páč teď je na 0
        self.start_time = self.waveform_width / self.max_video_position * start_time
        self.end_time = self.waveform_width / self.max_video_position * end_time
        print(self.start_time, self.end_time)
        #self.text = "text"
#
        #self.add_row = True
    def get_add_row(self):
        return self.add_row
    def get_remove_row(self):
        return self.remove_row_statement
    #HACK Musí být vytvořeny 2 stejné funkce, protože by se jinak hádali, možná na to kouknout, jak by se to dalo vylepšit
    def remove_row(self, index):
        self.remove_row_statement = True
        self.index_to_remove = index
    def remove_section(self, index):
        self.remove_row_statement = True
        self.index_to_remove = index
