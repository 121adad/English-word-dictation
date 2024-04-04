import tkinter as tk
from settings import Settings
from json import load, dump


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.title('Setting')
        self.geometry('300x300')
        self.label_time = tk.Label(self, text='时间', font=self.settings.FONT_15)
        self.label_time.pack()
        self.entry_hour = tk.Entry(self, font=self.settings.FONT_20, width=10, justify='center')
        self.entry_hour.pack()
        self.entry_minute = tk.Entry(self, font=self.settings.FONT_20, width=10, justify='center')
        self.entry_minute.pack()
        self.label_dictation = tk.Label(self, text='听力播放(0 or 1)', font=self.settings.FONT_15, width=20,
                                        justify='center')
        self.label_dictation.pack()
        self.entry_dictation = tk.Entry(self, font=self.settings.FONT_20, width=10, justify='center')
        self.entry_dictation.pack()
        self.save_button = tk.Button(self, text='save', font=self.settings.FONT_20, command=self.save)
        self.save_button.pack()
        self.str_var = tk.StringVar()
        self.prompt_label = tk.Label(self, textvariable=self.str_var, font=self.settings.FONT_15)
        self.prompt_label.pack()
        self.mainloop()

    def save(self) -> None:
        hour = self.entry_hour.get()
        minute = self.entry_minute.get()
        dictation = self.entry_dictation.get()
        try:
            if 0 <= int(hour) <= 24 and 0 <= int(minute) <= 60:
                hour = int(hour)
                minute = int(minute)
        except:
            self.str_var.set("??? what ? time ? it ? is? ???")
            return None

        with open("./settings.json", "r", encoding="utf-8") as f:
            json_data = load(f)
        json_data["timing"] = [hour, minute]
        json_data['dictation'] = bool(int(dictation))
        with open("./settings.json", "w", encoding="utf-8") as f:
            dump(json_data, f)
        print('settings has been amended')


window = Window()
