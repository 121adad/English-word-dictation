import tkinter as tk
import json
from requests import post
from fake_useragent import UserAgent
from shutil import rmtree
from requests import get
from os import path, makedirs, walk
from pygame import mixer
from settings import Settings


class DownloadUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.ua = UserAgent()
        # 创建文件夹
        self.creat_dir()
        self.font = self.settings.FONT_20
        # self.title = '单词下载器 有道词典要遭殃了'
        self.input_box = tk.Text(self, font=self.font, height=15, width=40)
        self.input_box.pack()
        self.variable_str = tk.StringVar()
        self.variable_str.set(f'{self.settings.BLOCK_NAMES[0]} or {self.settings.BLOCK_NAMES[1]}')
        self.label_prompt_entry = tk.Label(self, font=self.font, textvariable=self.variable_str)
        self.label_prompt_entry.pack()
        self.entry_box = tk.Entry(self, font=self.font)
        self.entry_box.pack()
        self.btn_download = tk.Button(self, text='download', font=self.font, command=self.download)
        self.btn_download.pack()
        self.btn_test_audio = tk.Button(self, text='test audio', font=self.settings.FONT_20, command=self.test_mp3)
        self.btn_test_audio.pack()
        self.btn_delete_audios = tk.Button(self, text='delete words', font=self.settings.FONT_20,
                                           command=self.deleteAllWords)
        self.btn_delete_audios.pack()
        self.creat_dir()
        self.mainloop()

    def mixer_init(self):
        mixer.init()
        mixer.music.load(self.settings.VOICE_OVER_PATH + "\\background.mp3")
        mixer.music.play()
        mixer.music.set_volume(0)

    def creat_dir(self):
        def _mkdir(path):
            makedirs(path)

        for name in self.settings.BLOCK_NAMES:
            for mode in range(len(self.settings.PRONUNCIATION_MODE)):
                _path = self.get_path(name, mode)
                if not path.exists(_path):
                    _mkdir(_path)

    def get_path(self, block_name: str, pronunciation_mode: int):
        return rf'{self.settings.DOWNLOADED_PATH}\{block_name}\{self.settings.PRONUNCIATION_MODE[pronunciation_mode]}'

    def get_text_box_value(self) -> str:
        return self.input_box.get('1.0', 'end')

    def get_input_box_value(self) -> str:
        return self.entry_box.get()

    def download(self):
        def _filter(text: str):
            text = text[:-1]  # 去除\n
            return text.split(',')

        def _request(_word, api: int):
            headers = {'User-Agent': self.ua.random}
            if api == 0:
                api = self.settings.ENGLISH_API
            elif api == 1:
                api = self.settings.AMERICAN_API
            try:
                _response = get(api + _word, headers)
                return _response
            except:
                self.variable_str.set(f'下载错误 真服了~c --{_word}')
                return False

        def _write_mp3(_path, _response):
            with open(_path, 'wb') as f:
                f.write(_response.content)

        # 获取用户输入的单词
        words = _filter(self.get_text_box_value())
        # 获取并判断分区
        block_name = self.get_input_box_value()
        if block_name not in self.settings.BLOCK_NAMES:
            self.variable_str.set('不存在此分区!!')
            return False
        download_root_path = self.settings.DOWNLOADED_PATH + rf"\{block_name}"
        for word in words:
            responses = [_request(word, 0), _request(word, 1)]
            for index, response in enumerate(responses):
                if response:
                    _write_mp3(download_root_path + "\\" + self.settings.PRONUNCIATION_MODE[index] + rf"\{word}.mp3",
                               response)

    def deleteAllWords(self):
        try:
            rmtree("./audios/words")
        except FileNotFoundError:
            self.variable_str.set('文件早就被删了-别瞎点烦死了')
        self.creat_dir()
        return True

    def test_mp3(self):
        self.mixer_init()

        def _loadSound(file_path):
            return mixer.Sound(file_path)

        error_files = []
        for root, dirs, files in walk(self.settings.DOWNLOADED_PATH):
            for file in files:
                _path = path.join(root, file)
                if not _loadSound(_path):
                    error_files.append(_path)
        self.variable_str.set(str(error_files))
        return error_files


class Translator:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Origin': 'https://fanyi.baidu.com',
            'Referer': 'https://fanyi.baidu.com/mtpe-individual/multimodal',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.ua.random,
            'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    def make_request(self, word: str) -> json:
        data = {
            'kw': f'{word}',
        }
        for _ in range(3):
            print(word)
            response = post('https://fanyi.baidu.com/sug', data=data, headers=self.headers)
            if response.status_code == 200:
                return response.json()['data'][0]['v']


if __name__ == '__main__':
    downloadUI = DownloadUI()
