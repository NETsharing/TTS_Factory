import json
import requests
import os
from config import Config
from synthesis import TTSFactory, TTS, TTSValidator
from google.cloud import texttospeech

config = Config()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['google_synth']['BASEDIR'] + '/creds/86a317cb419b.json'



class Google_creator(TTSFactory):

    def __init__(self, voice, lang, filename, dir_path, text, pitch):
        super(Google_creator, self).__init__(voice, lang, filename, dir_path, text, pitch)

    def validation(self, voice, lang, filename, dir_path, text, pitch):
        GoogleTTSValidator.validate_text(self,text)
        GoogleTTSValidator.validate_lang(self, lang)
        GoogleTTSValidator.validate_path(self, dir_path)
        GoogleTTSValidator.validate_filename(self, filename)

    def synhtesis(self, voice, lang, filename, dir_path, text, pitch):
        GoogleTTS.authentication(self)
        synth_text = GoogleTTS.execute(self, voice, lang, filename, dir_path, text, pitch)
        GoogleTTS.generateWAV(self, synth_text, filename, dir_path)


class GoogleTTS(TTS):
    def __init__(self, voice, lang, filename, dir_path, text, pitch):
        super(GoogleTTS, self).__init__(voice, lang, filename, dir_path, text, pitch)

    def authentication(self):
        pass

    def execute(self, voice, lang, filename, dir_path, text, pitch):
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.types.SynthesisInput(text=text)

        voice = texttospeech.types.VoiceSelectionParams(
            language_code=lang,
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL,
        name=voice)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16, pitch=pitch, sample_rate_hertz=8000)
        try:
            response = client.synthesize_speech(input_text, voice, audio_config)
        except:
            raise Exception('Google response False.')

        client.transport.channel.close()
        response.audio_content
        return response.audio_content

    def generateWAV(self, synth_text, filename, dir_path):
        with open(dir_path + filename + '.wav', "wb") as f:
            f.write(synth_text)


class GoogleTTSValidator(TTSValidator):
    def __init__(self, lang, tts):
        super(GoogleTTSValidator, self).__init__(lang, tts)

    def validate_lang(self, lang):
        texttospeech.types.ListVoicesRequest(language_code=lang)

    def validate_text(self, text):
        if len(text) >= 5000:
            raise Exception("Google TTS: incorrect text length")



