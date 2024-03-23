import time
import ffmpeg
from faster_whisper import WhisperModel

class Generate:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Generate, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    #input_video = "trevor.mp4"
    #input_video_name = input_video.replace(".mp4", "")

    def extract_audio(self, video):
        video_name = "temp_video"#video.replace(".mp4", "")
        extracted_audio = f"audio-{video_name}.wav"

        stream = ffmpeg.input(video)
        stream = ffmpeg.output(stream, extracted_audio)
        ffmpeg.run(stream, overwrite_output=True)

        return extracted_audio


    def transcribe(self, audio_file):
        model = WhisperModel("small")
        segments, info = model.transcribe(audio_file)
        language = info[0]
        print("Transcription language:", language)
        segments = list(segments)
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" %
                  (segment.start, segment.end, segment.text))
        return language, segments
