from abc import ABC, abstractmethod
from os.path import dirname, exists, isdir, join
import wave

class TTSFactory(ABC):

    def __init__(self, voice, lang, filename, dir_path, text, emotion='neutral', speed=1, pitch=0):
        super(TTSFactory, self).__init__()
        self.text = text
        self.lang = lang
        self.voice = voice
        self.filename = filename
        self.dir_path = dir_path
        self.emotion = emotion
        self.speed = speed
        self.pitch = pitch


    @abstractmethod
    def validation(self):
        pass


    @abstractmethod
    def synhtesis(self):
        pass

class TTSValidator(ABC):

    def __init__(self):
        pass

    def validate(self):
        self.validate_path()
        self.validate_filename()
        self.validate_lang()
        self.validate_connection()
        self.validate_text()

    def validate_filename(self, filename):
        if (filename and filename.endswith('.wav')):
            raise Exception( "name must not be in .wav format!")


    def validate_path(self, dir_path):
        if not (exists(dir_path) and isdir(dir_path)):
            raise Exception("dir_path %s is not valid!")

    @abstractmethod
    def validate_lang(self, lang):
        pass

    @abstractmethod
    def validate_connection(self, tts):
        pass

    @abstractmethod
    def validate_text(self, text):
        pass

    @abstractmethod
    def validate_voice(self, voice):
        pass


class TTS(ABC):

    def __init__(self, voice, platform, lang, filename, dir_path, text):
        super(TTS, self).__init__()
        pass


    @abstractmethod
    def authentication(self):
        pass

    @abstractmethod
    def execute(self, *args):
        pass

    @staticmethod
    def generateWAV(synth_text, filename, dir_path):
        try:
            with wave.open(dir_path + filename + '.wav', "wb") as f:
                f.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
                for audio_content in synth_text:
                    f.writeframes(audio_content)
        except Exception as e:
            raise Exception("Wave file does not exist")
