from business_logic_layer import WordDictsAllBlock
from settings import Settings
from ui import MainWindow
from timer import ObserverAbstracted, Timer


def Init(dictation):
    wordDicts = WordDictsAllBlock()
    if dictation:
        observer = Observer(wordDicts)
        timer = Timer([observer])
        timer.update()
    else:
        RunProgram(wordDicts, False)


class Observer(ObserverAbstracted):
    def __init__(self, wordDicts):
        super().__init__()
        self.wordDicts = wordDicts

    def update(self):
        RunProgram(self.wordDicts, True)


class RunProgram:
    def __init__(self, wordDicts: WordDictsAllBlock, dictation: bool):
        self.mainWindow = MainWindow(wordDicts, dictation)


if __name__ == '__main__':
    settings = Settings()
    Init(settings.DICTATION)
