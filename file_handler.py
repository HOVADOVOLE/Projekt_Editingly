class file_handler:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(file_handler, cls).__new__(cls, *args, **kwargs)
            cls._instance.source = None
            cls._instance.list_of_components = []
        return cls._instance

    def get_source(self):
        return self.source
    def set_source(self, source):
        self.source = source

    # Následující kód je úplně k hovnu
    def update_components(self):
        for component in self.list_of_components:
            pass # TODO update components in list_of_components
    def remove_component(self, component):
        self.list_of_components.remove(component)
    def add_component(self, component):
        self.list_of_components.append(component)