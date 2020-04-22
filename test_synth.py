from text_to_speach import text_to_spech

def make_yandex_tts():
    platform = "yandex"
    voice = 'oksana'
    lang = 'ru-RU'
    filename = 'petrovic3'
    dir_path = ''
    text = 'проверка синтеза речи'
    speed = 1.0
    emotion = 'neutral'
    text_to_spech( platform, voice, lang, filename, dir_path, text, emotion, speed)

def make_google_tts():
    platform = "google"
    voice = 'en-US-Standard-C'
    lang = 'en-US'
    filename = 'petrovic2'
    dir_path = ''
    text = 'hello world its me'
    pitch = 15
    text_to_spech(platform, voice, lang, filename, dir_path, text, pitch)

if __name__ == '__main__':
    make_google_tts()
    make_yandex_tts()