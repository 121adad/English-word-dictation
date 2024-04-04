from json import load


class Settings:

    def __init__(self):
        # 导入参数(定时，是否听写)
        self._json_file = None
        with open("./settings.json", "r", encoding='utf-8') as file:
            self._json_file = load(file)
        self.FONT_20 = ('等线', 20)
        self.FONT_15 = ('等线', 15)
        # type 0 美音
        self.AMERICAN_API = 'http://dict.youdao.com/dictvoice?type=0&audio='
        self.ENGLISH_API = 'http://dict.youdao.com/dictvoice?type=1&audio='

        ROOT_PATH = r".\audios"
        self.DOWNLOADED_PATH = ROOT_PATH + '\words'
        self.VOICE_OVER_PATH = ROOT_PATH + r'\voice_over'
        self.BLOCK_NAMES = ['t1', 't2']  # 先后顺序就是阅读时的顺序
        self.PRONUNCIATION_MODE = ['America_Pronunciation', 'English_Pronunciation']
        self.TIME_TO_WAIT = 18

    @property
    def DICTATION(self):
        return self._json_file['dictation']

    @property
    def TIME_TO_START(self):
        return self._json_file['timing']
