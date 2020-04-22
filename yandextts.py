import json
import requests
import os
from config import Config
from synthesis import TTSFactory, TTS, TTSValidator
config = Config()
basedir = os.path.abspath(os.path.dirname(__file__))


class Yandex_creator(TTSFactory):

    def __init__(self, voice, lang, filename, dir_path, text, emotion, speed):
        super(Yandex_creator, self).__init__(voice, lang, filename, dir_path, text, emotion, speed)

    def validation(self, voice, lang, filename, dir_path, text, emotion, speed):
        YandexValidator.validate_text(self, text)
        YandexValidator.validate_lang(self, lang)
        YandexValidator.validate_path(self, dir_path)
        YandexValidator.validate_filename(self, filename)

    def synhtesis(self, voice, lang, filename, dir_path, text, emotion, speed):
        iam_token = YandexTTS.authentication(self)
        synth_text = YandexTTS.execute(self, voice, lang, filename, dir_path, text, emotion, speed, iam_token)
        YandexTTS.generateWAV(synth_text, filename, dir_path)


class YandexTTS(TTS):
    def __init__(self, voice, lang, filename, dir_path, text, emotion, speed, iam_token):
        super(YandexTTS, self).__init__(voice, lang, filename, dir_path, text, emotion, speed, iam_token)

    def authentication(self):
        url = config['yandex_synth']['URL_OAUTH']
        oauth_token = config['yandex_synth']['yandexPassportOauthToken']
        params = {'yandexPassportOauthToken': oauth_token}
        response = requests.post(url, params=params)
        decode_response = response.content.decode('UTF-8')
        text = json.loads(decode_response)
        iam_token = text.get('iamToken')
        expires_iam_token = text.get('expiresAt')
        return iam_token

    def execute(self, voice, lang, filename, dir_path, text, emotion, speed, iam_token):
        id_folder = config['yandex_synth']['FOLDER_ID']
        headers = {
            'Authorization': 'Bearer ' + iam_token,
        }
        data = {
            'text': text,
            'lang': lang,
            'voice': voice,
            'emotion': emotion,
            'folderId': id_folder,
            'speed': speed,
            'format': 'lpcm',
            'sampleRateHertz': 8000,
        }

        with requests.post(url=config['yandex_synth']['URL_SYN'], headers=headers, data=data) as resp:
            if resp.status_code != 200:
                raise Exception("Request to Yandex TTS failed: code: {}, body: {}".format(resp.status_code, resp.text))
        return resp.iter_content()

        # for chunk in resp.iter_content(chunk_size=None):
        #     yield chunk



class YandexValidator(TTSValidator):

    def __init__(self, lang, text):
        super(YandexValidator, self).__init__(lang, text)

    def validate_lang(self, lang):
        if lang not in ["en-US", "ru-RU", "tr-TR"]:
            raise Exception ("Unsupported language for Yandex TTS")

    def validate_text(self, text):
        if len(text) >= 5000:
            raise Exception("Yandex TTS: incorrect text length")

