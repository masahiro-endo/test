# 【design pattern】 Observer
#
#
from abc import ABC, abstractmethod
from typing import List



# --- Observer インターフェース ---
class Observer(ABC):
    @abstractmethod
    def update(self, subject: "Subject"):
        pass


# --- Subject 基底クラス ---
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


# --- 具体的な Subject: プレイヤー ---
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


# --- 具体的な Observer: UI ---
class UIObserver(Observer):
    def update(self, subject: Subject):
        if isinstance(subject, Player):
            print(f"[UI] {subject.name} のHP: {subject.hp}")


# --- 具体的な Observer: サウンド ---
class SoundObserver(Observer):
    def update(self, subject: Subject):
        if isinstance(subject, Player):
            if subject.hp <= 0:
                print("[Sound] プレイヤー死亡音を再生")
            else:
                print("[Sound] ダメージ音を再生")


# --- 具体的な Observer: ログ ---
class LogObserver(Observer):
    def update(self, subject: Subject):
        if isinstance(subject, Player):
            print(f"[Log] {subject.name} HPが {subject.hp} に変更されました")


# --- 利用例 ---
if __name__ == "__main__":
    # プレイヤー作成
    player = Player("勇者", 100)

    # オブザーバー登録
    player.attach(UIObserver())
    player.attach(SoundObserver())
    player.attach(LogObserver())

    # HP変化イベント
    player.hp -= 20
    player.hp -= 50
    player.hp -= 40  # 0以下になり死亡


