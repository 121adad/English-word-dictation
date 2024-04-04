from business_logic_layer import WordDictsAllBlock
from settings import Settings
from ui import MainWindow
from timer import ObserverAbstracted, Timer


def Init(dictation) -> None:
    """
    初始化函数，根据是否进行听写来决定执行不同的逻辑。

    参数:
    dictation: 布尔值，表示是否进行听写。

    返回值:
    无
    """
    wordDicts = WordDictsAllBlock()  # 创建包含所有单词的字典

    if dictation:
        # 如果要进行听写
        observer = Observer(wordDicts)  # 创建观察者，传入单词字典
        timer = Timer([observer])  # 创建计时器，并将观察者添加到计时器中
        timer.update()  # 更新计时器
    else:
        # 如果不进行听写
        RunProgram(wordDicts, False)  # 以非听写模式运行程序


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
