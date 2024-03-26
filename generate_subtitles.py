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

    def split_by_words(self, segments, max_words):
        audio = []
        for segment in segments:
            segment_text = segment  # Předpokládáme, že 'segments' je seznam textových segmentů
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
        print(audio)
        return audio

    def split_by_characters(self, segments, max_characters, tolerance):
        audio = []
        for segment in segments:
            segment_text = segment.strip()
            if len(segment_text) > max_characters:
                # Rozdělení segmentu na části podle maximální délky s ohledem na tolerance pro celá slova
                current_part = ""
                words = segment_text.split()
                for word in words:
                    if len(current_part) + len(word) <= max_characters:
                        current_part += " " + word if current_part else word
                    else:
                        audio.append(current_part.strip())
                        current_part = word
                if current_part:
                    audio.append(current_part.strip())
            else:
                audio.append(segment_text)
        print(audio)
        return audio

    def split_by_limit(self, is_limited, is_by_words, text, max = 0):
        if is_limited:
            # Je omezeno pomocí počtu slov
            if is_by_words:
                self.split_by_words(text, max)
            # Je omezeno pomocí počtu charakterů
            else:
                self.split_by_characters(text, max, 7)

    def transcribe(self, audio_file, is_limited, is_by_words, max_per_subtitle):
        model = WhisperModel("small")
        segments, info = model.transcribe(audio_file)

        segments = list(segments)
        segments_text = [segment.text for segment in segments]

        self.split_by_limit(is_limited, is_by_words, segments_text, max_per_subtitle)

        return segments