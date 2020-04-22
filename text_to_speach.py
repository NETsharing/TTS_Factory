from yandextts import Yandex_creator
from googletts import Google_creator
import os

CLASSES = {
    "google": Google_creator,
    "yandex": Yandex_creator
}

def text_to_spech(platform, *args):
    if platform in CLASSES:
        synth_method = CLASSES[platform]
    try:
        synth_method(*args).validation(*args)
    except:
        raise Exception('Validation False.')
    try:
        synth_method(*args).synhtesis(*args)
    except:
        raise Exception('The TTS could not be loaded.')
    return {'message': 'Success'}


