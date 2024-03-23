import time
import ffmpeg
from faster_whisper import WhisperModel

class Generate:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Generate, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def extract_audio(self, video):
        video_name = "temp_video"
        extracted_audio = f"audio-{video_name}.wav"

        stream = ffmpeg.input(video)
        stream = ffmpeg.output(stream, extracted_audio)
        ffmpeg.run(stream, overwrite_output=True)

        return extracted_audio
    def split_by_limit(self, is_limited, is_by_words, text):
        if is_limited:
            # Je omezeno pomocí počtu slov
            if is_by_words:
                self.split_by_words(text, 10)
            # Je omezeno pomocí počtu charakterů
            else:
                return False
    def split_by_words(self, segments, max_words):
        audio = []
        for segment in segments:
            segment_text = segment.text  # Získání textového obsahu segmentu
            words = segment_text.split()  # Rozdělení textu na slova
            splitted_text = []
            current_part = []
            word_count = 0

            for word in words:
                current_part.append(word)
                word_count += 1

                if word_count >= max_words:
                    splitted_text.append(" ".join(current_part))
                    current_part = []
                    word_count = 0

            if current_part:
                splitted_text.append(" ".join(current_part))
            audio.extend(splitted_text)  # Rozšíření seznamu audio o rozdělený segment
        #return audio
        #TODO pak mi musí vracet text (Audio proměnná)
        print("Audio", audio)

    def transcribe(self, audio_file, max_per_subtitle=10):
        model = WhisperModel("small")
        segments, info = model.transcribe(audio_file)
        language = info[0]
        print("Transcription language:", language)
        segments = list(segments)
        self.split_by_limit(True, True, segments)
        #for segment in segments:
        #    print("[%.2fs -> %.2fs] %s" %
        #          (segment.start, segment.end, segment.text))

        # Rozdělení textu na části s maximálním počtem slov na titulku
        #for segment in segments:
        #    segment.splitted_text = self.split_text(segment.text, max_words_per_subtitle)
        #    print(segment.splitted_text)

        return language, segments
