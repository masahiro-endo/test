
from abc import ABC, abstractmethod
from typing import List




class Observer(ABC):
    @abstractmethod
    def update(self, subject: "Subject"):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)




class Player(Subject):
    def __init__(self, name: str, hp: int):
        super().__init__()
        self.name = name
        self._hp = hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        # HPが変化したら通知
        if value != self._hp:
            self._hp = max(0, value)  # HPは0未満にならない
            print(f"[DEBUG] {self.name} HP changed to {self._hp}")
            self.notify()


class UIObserver(Observer):
    def update(self, subject: Subject):
        if isinstance(subject, Player):
            print(f"[UI] {subject.name} のHP: {subject.hp}")


class LogObserver(Observer):
    def update(self, subject: Subject):
        if isinstance(subject, Player):
            print(f"[Log] {subject.name} HPが {subject.hp} に変更されました")



