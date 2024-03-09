import speech_recognition as sr
from moviepy.editor import *

class Generate:
    # Titulky se budou ukládat do složky, kde je video_source
    def __init__ (self, video_source, language):
        video = VideoFileClip(video_source)
        audio = video.audio
        audio.write_audiofile("temp_audio.wav")
        self.video_source = video_source
        self.language = language
        self.r = sr.Recognizer()
    def generate_subtitles(self):
        if self.video_source is not None:
            with sr.AudioFile("temp_audio.wav") as source:
                audio_data = self.r.record(source)

                try:
                    text = self.r.recognize_google_cloud(audio_data, language="en-US")
                    print("text", text)
                except sr.UnknownValueError:
                    print("Rozpoznání nebylo možné")
                except sr.RequestError as e:
                    print("Chyba při komunikaci s Google Cloud Speech-to-Text service: {0}".format(e))