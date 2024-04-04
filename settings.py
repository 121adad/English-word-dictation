from json import load
import logging
from pathlib import Path


class Settings:

    def __init__(self):
        # 导入参数(定时，是否听写)
        self._json_file = None
        with open("./settings.json", "r", encoding='utf-8') as file:
            self._json_file = load(file)
        self.FONT_20 = ('等线', 20)
        self.FONT_15 = ('等线', 15)
        # type 0 美音
        self.url_audios = {
            0: 'http://dict.youdao.com/dictvoice?type=0&audio=',
            1: 'http://dict.youdao.com/dictvoice?type=1&audio=',
        }

        ROOT_PATH = r".\audios"
        self.DOWNLOADED_PATH = ROOT_PATH + '\words'
        self.VOICE_OVER_PATH = ROOT_PATH + r'\voice_over'
        self.BLOCK_NAMES = ['t1', 't2']  # 先后顺序就是阅读时的顺序
        self.PRONUNCIATION_MODE = ['America_Pronunciation', 'English_Pronunciation']
        self.TIME_TO_WAIT = 18
        self.MAX_REQUEST_COUNTS = 3

    @property
    def DICTATION(self):
        return self._json_file['dictation']

    @property
    def TIME_TO_START(self):
        return self._json_file['timing']


def singleton(cls):
    _instance = {}

    def inner(*args, **kwargs):
        if cls in _instance:
            return _instance[cls]
        obj = cls(*args, **kwargs)
        _instance[cls] = obj
        return obj

    return inner


@singleton
class Loggable:
    def __init__(self):
        self._logger = self._initialize_logger()

    def _initialize_logger(self):
        """Initialize the logger and configure it."""
        log_file_path = Path(__file__).parent / "log.log"

        # Create a logger with the name of the current class
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)

        # Create a file handler that logs messages to the specified file
        file_handler = logging.FileHandler(log_file_path, mode="w")
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter for the file handler
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        return logger

    @property
    def logger(self):
        return self._logger
