import tkinter as tk
from business_logic_layer import WordDictsAllBlock
from threading import Thread
from tkinter import ttk
from tkinter.ttk import Treeview
from pygame import mixer
from settings import Settings


class MainWindow(tk.Tk):
    def __init__(self, word_dicts, dictation=False):
        super().__init__()
        self.settings = Settings()
        self.title("Listening and Writing")
        self.window_size = (self.winfo_screenwidth(), self.winfo_screenheight())
        self.geometry(f"{self.window_size[0]}x{self.window_size[1]}")
        self.adaptive_value = 80
        self.btn_start = tk.Button(self, text="Start", command=self.start_listening, font=self.settings.FONT_20)
        self.btn_start.place(x=self.window_size[0] // 2, y=self.window_size[1] - self.adaptive_value)
        self.btn_stop = tk.Button(self, text="Stop", command=self.stop_audio, font=self.settings.FONT_20)
        self.btn_stop.place(x=self.window_size[0] // 2 + 100, y=self.window_size[1] - self.adaptive_value)
        self.btn_table = tk.Button(self, text="Show", command=self.show_table, font=self.settings.FONT_20)
        self.btn_table.place(x=self.window_size[0] // 2 - 100, y=self.window_size[1] - self.adaptive_value)

        ''' type:WordDictsAllBlock '''
        self.audio_player = word_dicts
        if dictation:
            self.start_listening()
        self.table1 = TreeView(self, word_dicts, self.window_size[0] // 2, self.settings.BLOCK_NAMES[0])
        self.table2 = TreeView(self, word_dicts, self.window_size[0] // 2, self.settings.BLOCK_NAMES[1])
        self.mainloop()

    def stop_audio(self):
        pass

    def show_table(self):
        self.table1.pack()
        self.table2.pack()

    def start_listening(self):
        Thread(target=self.audio_player.start_listening).start()


class TreeView:
    def __init__(self, window: MainWindow, wordDicts: WordDictsAllBlock, table_width: int, block_name: str):
        self.settings = Settings()
        self.wordDicts = wordDicts.word_dicts
        self.columns = [self.settings.BLOCK_NAMES[0],
                        self.settings.BLOCK_NAMES[0] + '_translated',
                        ]
        self.tree = Treeview(window, height=10, selectmode="none", columns=self.columns)
        self.tree.heading(self.columns[0], text=self.settings.BLOCK_NAMES[0])
        self.tree.heading(self.columns[1], text=self.settings.BLOCK_NAMES[1])
        self.tree.column('#0', width=0, minwidth=0)
        self.tree.column(self.columns[0], width=table_width // 2 - 300, minwidth=table_width // 2 - 300)
        self.tree.column(self.columns[1], width=table_width // 2 + 300, minwidth=table_width // 2 + 300)
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=90)
        self.tree.config = 'Treeview'
        self.insert_data_into_table(block_name)
        self.set_tree_font()

    def insert_data_into_table(self, block_name: str) -> None:
        for block, words in self.wordDicts.items():
            if block != block_name: continue
            for name, word in words.items():
                print(word)
                self.tree.insert('', 'end', values=(word.word, word.translated_word))

    def set_tree_font(self):
        """设置tree字体"""
        items = self.tree.get_children()  # 获取所有的单元格
        for item in items:
            self.tree.item(item, tags='oddrow')  # 对每一个单元格命名
            self.tree.tag_configure('oddrow', font=self.settings.FONT_20)  # 设定treeview里字体格式font=ft
        self.tree.update()  # 更新tree

    def pack(self):
        self.tree.pack(side='left')


def init():
    settings = Settings()
    mixer.init()
    mixer.music.load(settings.VOICE_OVER_PATH + r'\background.mp3')
    mixer.music.play()
    mixer.music.set_volume(0)


if __name__ == "__main__":
    MainWindow(WordDictsAllBlock(), False)
