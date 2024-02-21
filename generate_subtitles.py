import autosub
import os

class Generate:
    # Titulky se budou ukládat do složky, kde je video_source
    def __init__ (self, video_source, language):
        index = video_source.rfind("/")  # Najde index posledního '/'
        nova_adresa = video_source[:index]  # Vytvoří nový řetězec od začátku až po index posledního '/'
        print(nova_adresa)  # Vypíše "C:\Users\Domča\OneDrive - SPSUL\Plocha"
        autosub.generate_subtitles(video_source, nova_adresa, language)
