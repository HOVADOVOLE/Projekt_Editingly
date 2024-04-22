import time
import ffmpeg
from faster_whisper import WhisperModel
from concurrent.futures import ThreadPoolExecutor
#from file_handler import file_handler

class Generate:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Generate, cls).__new__(cls, *args, **kwargs)
            #cls.file_handler = file_handler()
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
            segment_text = segment[0]
            segment_start = segment[1]
            segment_end = segment[2]
            words = segment_text.split()
            time_per_word = (segment_end - segment_start) / len(words)
            splitted_text = []
            current_part = []
            current_time = segment_start
            word_count = 0

            for word in words:
                current_part.append(word)
                word_count += 1

                if word_count >= max_words:
                    end_time = current_time + time_per_word * max_words
                    splitted_text.append((" ".join(current_part), current_time, end_time))
                    current_part = []
                    word_count = 0
                    current_time = end_time

            if current_part:
                end_time = segment_end
                splitted_text.append((" ".join(current_part), current_time, end_time))

            audio.extend(splitted_text)

        return audio



    def split_by_characters(self, segments, max_characters, tolerance):
        audio = []
        for segment in segments:
            segment_text = segment[0].strip()  # přístup k textu segmentu
            segment_start = segment[1]  # přístup k začátku segmentu
            segment_end = segment[2]  # přístup ke konci segmentu
            if len(segment_text) > max_characters:
                # Rozdělení segmentu na části podle maximální délky s ohledem na tolerance pro celá slova
                current_part = ""
                current_length = 0
                current_start = segment_start
                words = segment_text.split()
                for word in words:
                    word_length = len(word)
                    if current_length + word_length + len(current_part) <= max_characters + tolerance:
                        current_part += " " + word if current_part else word
                        current_length += word_length
                    else:
                        audio.append((current_part.strip(), current_start, current_end))
                        current_part = word
                        current_length = word_length
                        current_start = current_end
                    current_end = current_start + (len(current_part) / len(segment_text)) * (segment_end - segment_start)

                if current_part:
                    audio.append((current_part.strip(), current_start, segment_end))
            else:
                audio.append((segment_text, segment_start, segment_end))
        return audio




    def split_by_limit(self, is_limited, is_by_words, text, max = 0):
        if is_limited:
            # Je omezeno pomocí počtu slov
            if is_by_words:
                return self.split_by_words(text, max)
            # Je omezeno pomocí počtu charakterů
            else:
                return self.split_by_characters(text, max, 7)
        return text

    def transcribe(self, audio_file, is_limited, is_by_words, max_per_subtitle):
        model = WhisperModel("small")
        segments, info = model.transcribe(audio_file)

        segments = list(segments)
        segments_text = [(segment.text, segment.start, segment.end) for segment in segments]


        with ThreadPoolExecutor() as executor:
            executor.max_workers = 1
            future = executor.submit(self.split_by_limit, is_limited, is_by_words, segments_text, max_per_subtitle)
            result = future.result()

        return result