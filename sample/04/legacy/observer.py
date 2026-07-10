
import pyxel as px
from abc import ABC, abstractmethod
from typing import List
import copy
from module.constant import *


class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass


class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)




class ControlDevice(Subject):

    pressed = {}

    def __init__(self):
        self.attach(UIObserver())

    @classmethod
    def get_btn_state(cls):
        push = {
            BTN.UP : px.btnp(px.KEY_UP   , hold=15, repeat=3) or px.btn(px.GAMEPAD1_BUTTON_DPAD_UP),
            BTN.DWN: px.btnp(px.KEY_DOWN , hold=15, repeat=3) or px.btn(px.GAMEPAD1_BUTTON_DPAD_DOWN),
            BTN.LFT: px.btnp(px.KEY_LEFT , hold=15, repeat=3) or px.btn(px.GAMEPAD1_BUTTON_DPAD_LEFT),
            BTN.RHT: px.btnp(px.KEY_RIGHT, hold=15, repeat=3) or px.btn(px.GAMEPAD1_BUTTON_DPAD_RIGHT),
            BTN.A_Z: px.btnp(px.KEY_Z    , hold=15, repeat=3) or px.btnp(px.GAMEPAD1_BUTTON_A, 10, 2),
            BTN.B_X: px.btnp(px.KEY_X    , hold=15, repeat=3) or px.btnp(px.GAMEPAD1_BUTTON_B, 10, 2),
        }
        for btn in push:
            if push[btn]:
                cls.notify()
                cls.pressed[btn] = btn
        return push

    @classmethod
    def close(cls):
        clone = copy.deepcopy(cls.pressed)
        for key in clone:
            del cls.pressed[clone]
        return

    @staticmethod
    def clear():
        ControlDevice.close()


class UIObserver(Observer):
    def update(self, subject):
        print(f"[UI] pressed: {subject.pressed} ")




