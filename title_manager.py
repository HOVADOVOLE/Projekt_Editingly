class title_manager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(title_manager, cls).__new__(cls, *args, **kwargs)
            cls._instance.start_time = None
            cls._instance.end_time = None
            cls._instance.text = None
            cls._instance.row_index = None
            cls._instance.add_row = False
        return cls._instance
    def create_subtitle_section(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.text = "text"

        self.add_row = True
    def get_add_row(self):
        return self.add_row