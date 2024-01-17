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
        self.subtitle_list.append({'start': od, 'end': do, 'text': "text"})
    def modify_subtitle(self, id_radku, od, do, text):
        if text is None:
            text = ""
        self.subtitle_list[id_radku] = {'start': float(od), 'end': float(do), 'text': text}
    # odebere titulku z JSONu
    def remove_subtitle(self, id_titulky):
        self.subtitle_list.pop(id_titulky)

    def return_current_subbtitle(self, cas):
        # ošetření na jestli nebude žádná titulka, tak aby ne nevracelo nic
        for subtitle in self.subtitle_list:
            if subtitle['start'] <= cas and subtitle['end'] >= cas:
                self.posledni_od = subtitle['start']
                self.posledni_do = subtitle['end']
                return subtitle
        return None

    #Uloží všechny titulky do JSONu pro případ zavření aplikace
    # TODO - přidat ošetření na přepsání souboru
    def zapis_do_json(self):
        with open(self.path, 'w') as file:
            json.dump(self.subtitle_list, file)
    def print_json(self):
        return self.subtitle_list
    # Načte všechny titulky z JSONu pro případ znovu otevření aplikace
    def rozbal_json(self):
        with open(self.path, 'r') as file:
            self.subtitle_list = json.load(file)

    #def json_to_srt(self):
    #    srt = ''
    #    for i in range(len(self.subtitle_list)):
    #        srt += str(i+1) + '\n'
    #        srt += self.subtitle_list[i]['start'] + ' --> ' + self.subtitle_list[i]['end'] + '\n'
    #        srt += self.subtitle_list[i]['text'] + '\n\n'
    #    return srt