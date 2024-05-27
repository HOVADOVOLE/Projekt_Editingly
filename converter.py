from title_manager import title_manager


class SubtitleConverter():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SubtitleConverter, cls).__new__(cls, *args, **kwargs)
            cls._instance.title_manager = title_manager()
        return cls._instance

    def convert_to_srt(self, file_name):
        """Převede titulky do formátu srt a uloží je do souboru"""
        if not self.title_manager.subtitles:
            return ''
        subtitle_list = self.title_manager.subtitles

        srt = ''
        for i, subtitle in enumerate(subtitle_list):
            index = i + 1
            start_time = self.seconds_to_srt_time(subtitle[1])
            end_time = self.seconds_to_srt_time(subtitle[2])
            srt += f"{index}\n{start_time} --> {end_time}\n{subtitle[0]}\n\n"

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(srt)
        print(f"SubRip subtitles saved to: {file_name}")
        return srt

    def convert_to_xml(self, file_name):
        """Převede titulky do formátu xml a uloží je do souboru"""
        if not self.title_manager.subtitles:
            return ''
        subtitle_list = self.title_manager.subtitles

        xml = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml += '<xml>\n'
        for i, subtitle in enumerate(subtitle_list):
            xml += '<subtitle>\n'
            xml += f'<start>{subtitle[1]}</start>\n'
            xml += f'<end>{subtitle[2]}</end>\n'
            xml += f'<text>{subtitle[0]}</text>\n'
            xml += '</subtitle>\n'
        xml += '</xml>'

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(xml)
        return xml

    def convert_to_txt(self, file_name):
        """Převede titulky do formátu txt a uloží je do souboru"""
        if not self.title_manager.subtitles:
            return ''

        subtitle_list = self.title_manager.subtitles

        txt = ''
        for i, subtitle in enumerate(subtitle_list):
            index = i + 1
            txt += f"{index}\n{subtitle[0]}\n\n"

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(txt)
        return txt

    def check_json(self):
        """Zkontroluje, zda je v JSONu něco uloženo"""
        if self.title_manager.subtitles and len(self.title_manager.subtitles) > 0:
            return True
        else:
            return False

    def seconds_to_srt_time(self, seconds):
        """Konvertuje sekundy na formát hh:mm:ss,ms pro SRT titulky"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"