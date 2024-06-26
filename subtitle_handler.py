import json
#import os

class Subtitle_Handler:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Subtitle_Handler, cls).__new__(cls, *args, **kwargs)
            cls._instance.subtitle_list = []
            cls._instance.posledni_od = 0
            cls._instance.posledni_do = 0
            cls._instance.path = 'subtitle_list.json'
        return cls._instance

    # přidá titulku do JSONu
    def add_subtitle(self, od, do, text):
        if text is None:
            text = ""
        self.subtitle_list.append({'start': od, 'end': do, 'text': text})
    def modify_subtitle(self, id_radku, od, do, text):
        if text is None:
            text = ""
        self.subtitle_list[id_radku] = {'start': float(od), 'end': float(do), 'text': text}
    # odebere titulku z JSONu
    def remove_subtitle(self, id_titulky):
        self.subtitle_list.pop(id_titulky)

    def return_current_subbtitle(self, cas):
        for subtitle in self.subtitle_list:
            if subtitle['start'] <= cas and subtitle['end'] >= cas:
                self.posledni_od = subtitle['start']
                self.posledni_do = subtitle['end']
                return subtitle
        return None