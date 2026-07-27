
import pyxel as px
import math
import time
import random
from enum import Enum, Flag, IntEnum, auto

from module.constant import EFCT
from module.state.basestate import *
from module.UI import Meth















# 待機処理
# stack が空になることを防ぐための待機用
class Effect_Loading(BaseState):
    def __init__(self, parent):
        self.parent = parent

    def update(self):
        if len(self.parent.active) > 1:
            # 自身をスタックから除外する
            self.dispose()

    def dispose(self):
        dat = self.parent.active
        dlen = len(dat)
        for rev_i, task in enumerate(reversed(dat)):
            if isinstance(task, Effect_Loading):
                # reversed()すると、添字の並びが、
                # 末尾がゼロで、先頭に向かって値が増える順になる。
                # 元の基準に戻す。
                org_i = dlen - rev_i - 1
                dat.pop(org_i)




class Effect_Slash(BaseState):

    def __init__(self, parent):
        self.parent = parent
        self.view_timer = -1
        self.slash_x = 60
        self.slash_y = 60

    def __call__(self):
        self.start_slash()
        return self

    def update(self):
        if self.view_timer > 0:
            self.view_timer -= 1
        elif self.view_timer == 0:
            self.parent.active.append(EFCT.DONE)
        else:
            self.slash_x = 0
            self.slash_y = 0

    def draw(self):
        px.line(self.slash_x, self.slash_y,
                    self.slash_x - self.view_timer * 12,
                    self.slash_y - self.view_timer * 12, px.COLOR_WHITE)

    def start_slash(self, duration=5):
        self.view_timer = duration




class Effect_Shake(BaseState):

    def __init__(self, parent):
        self.parent = parent
        self.camera_x = 0
        self.camera_y = 0
        self.shake_timer = -1
        self.shake_intensity = 0

    def __call__(self):
        self.start_shake(intensity=6, duration=15)  # イベントごとに調整可能
        return self
    
    def update(self):

        # シェイク処理
        if self.shake_timer > 0:
            # ランダムでカメラを揺らす
            self.camera_x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.camera_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_timer -= 1
            self.shake_intensity = max(0, self.shake_intensity - 1)
        elif self.shake_timer == 0:
            self.parent.active.append(EFCT.DONE)
        else:
            self.camera_x = 0
            self.camera_y = 0

    def draw(self):
        px.camera(self.camera_x, self.camera_y)

    def start_shake(self, intensity=4, duration=10):
        self.shake_intensity = intensity
        self.shake_timer = duration






class Effect_Buff(BaseState):

    def __init__(self, parent):
        self.parent = parent
        self.view_timer = -1
        self.buff_x = 30
        self.buff_y = 30

    def __call__(self):
        self.start_buff()
        return self

    def update(self):
        if self.view_timer > 0:
            self.view_timer -= 1
        elif self.view_timer == 0:
            self.parent.active.append(EFCT.DONE)
        else:
            self.slash_x = 0
            self.slash_y = 0

    def draw(self):
        px.circ(self.buff_x, self.buff_y, self.view_timer * 5, px.COLOR_WHITE)

    def start_buff(self, duration=5):
        self.view_timer = duration



