from os import walk, path
from data_access_layer import Translator
from settings import Settings
from time import sleep
from pygame import mixer


class PromptAudios:
    mixer.init()
    path_voice_over = "audios/voice_over/"
    prompt_one_minute_audio = mixer.Sound(path_voice_over + "prompt_one_minute.mp3")
    prompt_interval_audio = mixer.Sound(path_voice_over + "interval.mp3")
    prompt_ready_to_3500_audio = mixer.Sound(path_voice_over + "ready_to_3500.mp3")
    prompt_ready_to_xk_audio = mixer.Sound(path_voice_over + "ready_to_xk.mp3")
    prompt_end_audio = mixer.Sound(path_voice_over + "end_audio.mp3")

    mixer.music.load(path_voice_over + "background.mp3")
    mixer.music.set_volume(0)
    mixer.music.play()


class WordDictsAllBlock:
    class _Word:
        def __init__(self, English_word=None, translated_word=None, Eng_audio_path=None, Amer_audio_path=None):
            self.word = English_word
            self.Eng_audio = Eng_audio_path
            self.Amer_audio = Amer_audio_path
            self.translated_word = translated_word

    def __init__(self):
        self.settings = Settings()
        self.prompt_audios = PromptAudios()
        self.translator = Translator()
        self.word_dicts = self.audio_dict()

    def audio_dict(self) -> dict:
        _word_dicts = {}
        for block in self.settings.BLOCK_NAMES:
            _word_dicts[block] = self.word_dict(block)
        return _word_dicts

    def word_dict(self, block) -> dict:
        _path = self.settings.DOWNLOADED_PATH + rf'\{block}'
        _word_dict = {}

        for root, dirs, files in walk(_path):
            cur_accent = root.split("\\")[-1]
            if cur_accent not in self.settings.PRONUNCIATION_MODE:
                continue
            for word in files:
                word, suffix = word.split('.')[0], word.split('.')[1]
                node = _word_dict.get(word)
                if node is None:
                    _word_dict[word] = self._Word(English_word=word)
                    _word_dict[word].Amer_audio = mixer.Sound(path.join(root, word) + "." + suffix)
                else:
                    node.Eng_audio = mixer.Sound(path.join(root, word) + "." + suffix)
        for word, node in _word_dict.items():
            translated = self.translator.make_request(word)
            node.translated_word = translated

        return _word_dict

    def start_listening(self):
        # 播放开头提示音频
        self.prompt_audios.prompt_one_minute_audio.play()
        sleep(15)
        for index, word_list in enumerate(self.word_dicts.values()):
            match index:
                case 0:
                    self.prompt_audios.prompt_ready_to_3500_audio.play()
                    sleep(5)
                case 1:
                    self.prompt_audios.prompt_ready_to_xk_audio.play()
                    sleep(15)
            for word in word_list.values():
                self.prompt_audios.prompt_interval_audio.play()
                sleep(2)
                word.Amer_audio.play()
                sleep(self.settings.TIME_TO_WAIT // 2)
                word.Eng_audio.play()
                sleep(self.settings.TIME_TO_WAIT // 2)
