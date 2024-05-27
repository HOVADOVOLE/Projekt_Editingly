from title_manager import title_manager

class SubtitleConverter():
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SubtitleConverter, cls).__new__(cls, *args, **kwargs)
            cls._instance.title_manager = title_manager()
        return cls._instance

    def convert_to_srt(self):
        """Převede titulky do formátu srt"""

        if not self.title_manager.subtitles:
            return ''
        subtitle_list = self.title_manager.subtitles

        srt = ''
        for i in range(len(subtitle_list)):
            srt += str(i + 1) + '\n'
            srt += str(subtitle_list[i]['start']) + ' --> ' + str(subtitle_list[i]['end']) + '\n'
            srt += subtitle_list[i]['text'] + '\n\n'
        return srt
    def convert_to_xml(self):
        """Převede titulky do formátu xml"""

        if not self.title_manager.subtitles:
            return ''
        subtitle_list = self.title_manager.subtitles

        xml = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml += '<xml>\n'
        for i in range(len(subtitle_list)):
            xml += '<subtitle>\n'
            xml += '<start>' + str(subtitle_list[i]['start']) + '</start>\n'
            xml += '<end>' + str(subtitle_list[i]['end']) + '</end>\n'
            xml += '<text>' + subtitle_list[i]['text'] + '</text>\n'
            xml += '</subtitle>\n'
        xml += '</xml>'
        return xml
    def convert_to_txt(self):
        """Převede titulky do formátu txt"""

        if not self.title_manager.subtitles:
            return ''

        subtitle_list = self.title_manager.subtitles

        txt = ''
        for i in range(len(subtitle_list)):
            txt += str(i+1) + '\n'
            txt += subtitle_list[i]['text'] + '\n\n'
        return txt
    def check_json(self):
        """Zkontroluje, zda je v JSONu něco uloženo"""
        if self.title_manager.subtitles and len(self.title_manager.subtitles) > 0:
            return True
        else:
            return False