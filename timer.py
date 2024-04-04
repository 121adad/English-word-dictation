from abc import ABC, abstractmethod
from datetime import datetime
from sys import exit
from settings import Settings
from time import sleep


class Timer:
    def __init__(self, observers):
        self.observers = observers or []
        self.settings = Settings()

    def update(self):
        i = 0
        while True:
            now = datetime.now()
            if now.hour == self.settings.TIME_TO_START[0]:
                if now.minute == self.settings.TIME_TO_START[1]:
                    self.alert()
                    break
                elif now.minute > self.settings.TIME_TO_START[1]:
                    self.beyond_time()
            else:
                self.beyond_time()

            if i % 60 == 0:
                print(f'{self.settings.TIME_TO_START[1] - datetime.now().minute}分钟后开始听写')
            i += 1
            sleep(1)

    def beyond_time(self):
        print('看看现在几点了')
        exit()

    def alert(self):
        print('alert')
        for observer in self.observers:
            observer.update()

    def append(self, observers):
        self.observers.append(observers)


class ObserverAbstracted(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        pass
