import tkinter as tk
import json
from api import requestWordAudio, requestWordTranslated
from fake_useragent import UserAgent
from shutil import rmtree
from os import path, makedirs, walk
from pygame import mixer, error
from settings import Settings


# variable_str.set(f'下载错误重试 or 去4班--{word}')


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
        self.btn_test_audio = tk.Button(self, text='test audio', font=self.settings.FONT_20,
                                        command=self.verifyAudiosIntegrity)
        self.btn_test_audio.pack()
        self.btn_delete_audios = tk.Button(self, text='delete words', font=self.settings.FONT_20,
                                           command=self.deleteAllWordFiles)
        self.btn_delete_audios.pack()
        self.creat_dir()
        self.mainloop()

    def mixer_init(self):
        mixer.init()
        mixer.music.load(self.settings.VOICE_OVER_PATH + "\\background.mp3")
        mixer.music.play()
        mixer.music.set_volume(0)
        mixer.music.unload()

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

    @staticmethod
    def saveAudioAsFile(_path, _response):
        with open(_path, 'wb') as f:
            f.write(_response.content)

    @staticmethod
    def filterEnteredWords(text: str):
        text = text[:-1]  # 去除\n
        # 将字符全部转为小写
        text = text.lower()
        # 去除空格
        text = text.replace(' ', '')

        return list(filter(lambda x: x != "", text.split(',')))

    def download(self):
        # 获取并判断分区
        block_name = self.get_input_box_value()
        if block_name not in self.settings.BLOCK_NAMES:
            self.variable_str.set('不存在此分区!!')
            return False
        # 获取用户输入的单词
        words = self.filterEnteredWords(self.get_text_box_value())
        download_root_path = self.settings.DOWNLOADED_PATH + rf"\{block_name}"
        for word in words:
            responses = [requestWordAudio(word, 0), requestWordAudio(word, 1)]
            for index, response in enumerate(responses):
                if response:
                    self.saveAudioAsFile(
                        download_root_path + "\\" + self.settings.PRONUNCIATION_MODE[index] + rf"\{word}.mp3",
                        response)

    def deleteAllWordFiles(self):
        try:
            rmtree("./audios/words")
        except FileNotFoundError:
            self.variable_str.set('文件早就被删了-别瞎点烦死了')
        self.creat_dir()
        return True

    @staticmethod
    def loadSound(filePath):
        try:
            mixer.Sound(filePath).get_length()
            return True
        except error as e:
            # 只捕获 pygame.error，认为这是与音频文件加载直接相关的异常
            print(f"无法加载音频文件: {filePath}, 错误: {e}")
            return False
        except Exception as e:
            print(f"加载音频文件时发生意外错误: {filePath}, 错误: {e}")
            return False

    def verifyAudiosIntegrity(self):
        self.mixer_init()

        error_files = []
        for root, dirs, files in walk(self.settings.DOWNLOADED_PATH):
            for file in files:
                _path = path.join(root, file)
                if not self.loadSound(_path):
                    error_files.append(_path)
        if len(error_files) < 5:
            self.variable_str.set(str(error_files))
        else:
            self.variable_str.set(str(len(error_files)))
        mixer.quit()
        return error_files


if __name__ == '__main__':
    downloadUI = DownloadUI()
