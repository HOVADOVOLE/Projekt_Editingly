import json

class Subtitle_Handler:
    # přidá titulku do JSONu
    def __init__(self):
        self.subtitle_list = []
        self.posledni_od = 0
        self.posledni_do = 0
    def add_subtitle(self, od, do, text):
        self.subtitle_list.append({'start': od, 'end': do, 'text': text})

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

    # kontroluje, jestli se má vykreslit další titulka, nebo zůstat stejná
    def is_next_subtitle(self, cas):
        if self.posledni_od <= cas and self.posledni_do >= cas:
            return False
        return True


    #Uloží všechny titulky do JSONu pro případ zavření aplikace
    # TODO - přidat ošetření na přepsání souboru
    def zapis_do_json(self, path):
        with open(path, 'w') as file:
            json.dump(self.subtitle_list, file)

    # Načte všechny titulky z JSONu pro případ znovu otevření aplikace
    def rozbal_json(self, path):
        with open(path, 'r') as file:
            self.subtitle_list = json.load(file)