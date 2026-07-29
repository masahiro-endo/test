
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



class BaseEffect(BaseState):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.view_timer = -1
        self.x = 30
        self.y = 30

    def __call__(self):
        self.start_effect()
        return self

    def update(self):
        super().update()

        if self.view_timer > 0:
            self.view_timer -= 1
        elif self.view_timer == 0:
            self.parent.active.append(EFCT.DONE)
        else:
            self.x = 0
            self.y = 0

    def draw(self):
        super().draw()

    def start_effect(self, duration=5):
        self.view_timer = duration



class Effect_Slash(BaseEffect):

    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        super().update()

    def draw(self):
        super().draw()
        px.line(self.x, self.y,
                    self.x - self.view_timer * 12,
                    self.y - self.view_timer * 12, px.COLOR_WHITE)

    def start_effect(self, duration=5):

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






class Effect_Buff(BaseEffect):

    class Snowflake:
        def __init__(self):
            self.x = random.randint(-60, 60)
            self.y = random.randint(-60, 60)
            self.speed = random.uniform(0.5, 3.5)

        def update(self):
            self.y += self.speed
            if self.y > 120:
                self.y = random.randint(-50, 50)
                self.x = random.randint(-50, 50)

        def draw(self):
            px.circ(self.x, self.y, 1, px.COLOR_GREEN)

    def __init__(self, parent):
        super().__init__(parent)
        self.particles = []

    def update(self):
        super().update()
        for ptc in self.particles[:]:
            ptc.update()

    def draw(self):
        super().draw()
        for ptc in self.particles:
            ptc.draw()

    def start_effect(self, duration=10):
        super().start_effect(duration)
        self.particles = [Effect_Buff.Snowflake() for _ in range(50)]




class Effect_Explode(BaseEffect):

    class Particle:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.life = 10
            # 視覚的に収束しているように見えるため、
            # 反転させ、拡散しているように見せる
            self.radius = self.life

        def update(self):
            self.life -= 2
        def draw(self):
            px.circ(self.x, self.y, (self.radius - self.life) * 5, px.COLOR_RED)

    def __init__(self, parent):
        super().__init__(parent)
        self.particles = []

    def __call__(self):
        self.start_effect()
        return self

    def update(self):
        super().update()
        if random.random() < 0.5:
            self.create_particle()
        
        for ptc in self.particles[:]:
            ptc.update()
            if ptc.life <= 0:
                self.particles.remove(ptc)

    def draw(self):
        super().draw()
        for ptc in self.particles:
            ptc.draw()

    def start_effect(self, duration=10):
        super().start_effect(duration)
        self.create_particle()

    def create_particle(self):
        x = self.x + random.randint(-50, 50)
        y = self.y + random.randint(-50, 50)
        self.particles.append(Effect_Explode.Particle(x, y))

