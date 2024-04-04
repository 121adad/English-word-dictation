from requests import get, post
from fake_useragent import UserAgent
from settings import Settings, Loggable
import json

settings = Settings()
ua = UserAgent()
loggable = Loggable()


def requestWordAudio(word: str, accent_code: int):
    headers = {'User-Agent': ua.random}
    match accent_code:
        case 0:
            url = settings.url_audios[0]
        case 1:
            url = settings.url_audios[1]
        case _:
            raise Exception('Unknown Accent Code')

    try:
        for _ in range(settings.MAX_REQUEST_COUNTS):
            _response = get(url + word, headers)
            if _response.status_code == 200:
                return _response
    except:
        loggable.logger.error(f'api--音频下载出问题{url + word}')
        return False
    return False


def requestWordTranslated(word: str) -> json:
    headers = {'User-Agent': ua.random}
    data = {
        'kw': f'{word}',
    }
    try:
        for _ in range(settings.MAX_REQUEST_COUNTS):
            response = post('https://fanyi.baidu.com/sug', data=data, headers=headers)
            if response.status_code == 200:
                return response.json()['data']
    except Exception as e:
        loggable.logger.error(f'api--翻译出问题')
        return e
    return False
