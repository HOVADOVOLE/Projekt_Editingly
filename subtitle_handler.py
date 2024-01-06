import json
#import os

class Subtitle_Handler:
    # přidá titulku do JSONu
    def __init__(self):
        self.subtitle_list = []
        self.posledni_od = 0
        self.posledni_do = 0

        self.srt_subtitles = ''
        self.path = 'subtitle_list.json'

    # přidá titulku do JSONu
    def add_subtitle(self, od, do, text):
        self.subtitle_list.append({'start': od, 'end': do, 'text': text})
        #self.srt_subtitles = self.json_to_srt()

    # odebere titulku z JSONu
    def remove_subtitle(self, id_titulky):
        self.subtitle_list.pop(id_titulky)
        #self.srt_subtitles = self.json_to_srt()

    def return_current_subbtitle(self, cas):
        # ošetření na jestli nebude žádná titulka, tak aby ne nevracelo nic
        for subtitle in self.subtitle_list:
            if subtitle['start'] <= cas and subtitle['end'] >= cas:
                self.posledni_od = subtitle['start']
                self.posledni_do = subtitle['end']
                return subtitle
        return None

    # kontroluje, jestli se má vykreslit další titulka, nebo zůstat stejná
    def is_next_subtitle(self, cas):
        if self.posledni_od <= cas and self.posledni_do >= cas:
            return False
        return True

    #Uloží všechny titulky do JSONu pro případ zavření aplikace
    # TODO - přidat ošetření na přepsání souboru
    def zapis_do_json(self):
        with open(self.path, 'w') as file:
            json.dump(self.subtitle_list, file)

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