
import pyxel as px
import math
import random
import uuid
from enum import IntEnum, auto

import appconfig as gbl
from constant import * 







class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0  # 爆発の経過フレーム

    def update(self):
        self.timer += 1

    def draw(self):
        # 爆発を円で簡易表現（本来はスプライトでもOK）
        px.circ(self.x, self.y, self.timer, 8 + self.timer % 8)

    def is_finished(self):
        return self.timer > 10  # 爆発終了条件




class Sparks_spread:
    def __init__(self, x, y, angle, speed, life, color):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = life
        self.color = color
        self.timer = 0  # 爆発の経過フレーム

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.timer += 1

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_finished(self):
        return self.timer > self.life

    @classmethod
    def spawn(cls, cnt,  actor):
        for _ in range(cnt):  # パーティクル数
            #angle = random.uniform(0, math.tau)  # 0〜2π
            angle = random.uniform(-math.tau*(1/8), -math.tau*(3/8))  # 0〜2π
            speed = random.uniform(1.0, 2.0)
            life = random.randint(10, 20)
            color = random.choice([8, 9, 10])  # 赤系
            dx = actor.x + (actor.size//2)
            dy = actor.y + (actor.size//2)
            gbl.explosions.append(cls(dx, dy, angle, speed, life, color))



class Sparks_parabola:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-4, -2)
        self.life = random.randint(10, 30)  # 寿命フレーム
        self.color = random.choice([px.COLOR_YELLOW, px.COLOR_ORANGE, px.COLOR_RED])
        self.timer = 0  # 爆発の経過フレーム

    def update(self):
        # 重力加速度
        self.vy += 0.2
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_finished(self):
        return self.life <= 0

    @classmethod
    def spawn(cls, cnt,  actor):
        for _ in range(cnt):  # パーティクル数
            radius = actor.size//2
            dx = actor.x + radius + random.randint(-radius, radius)
            dy = actor.y + radius + random.randint(-radius, radius)
            gbl.explosions.append(cls(dx, dy))






