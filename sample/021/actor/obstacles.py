
import pyxel as px
import math
import random
import uuid
from enum import IntEnum, auto

import appconfig as gbl
from constant import * 







class Star:
    SIZE = 1
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH - Star.SIZE)
        self.y = random.randint(0, HEIGHT - Star.SIZE)
        self.speed = random.choice([0.5, 1, 1.5]) # 初速
        self.color = random.choice([5, 6, 7])

        self.vy = self.speed
        self.target_rate = 1   # 最終速度 現在速度に対する率
        self.target_vy = 0
        self.change_speed(self.target_rate)
        self.df_rate = 0.03 # 最終速度に至るまでの変化率

    def update(self):
        # if px.frame_count % 200 == 0:
        #     self.change_speed(5 if self.target_rate == 1 else 1)

        df = (max(self.vy, self.target_vy) - min(self.vy, self.target_vy)) * self.df_rate
        self.vy += df if self.vy < self.target_vy else -df

        # 位置更新
        self.y += self.vy

        if self.is_offscreen():
            self.x = random.randint(0, WIDTH - Star.SIZE)
            self.y = -Star.SIZE

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_offscreen(self):
        if (self.x < -Star.SIZE or self.x > WIDTH  + Star.SIZE or 
            self.y < -Star.SIZE or self.y > HEIGHT + Star.SIZE):
            return True
        return False

    def change_speed(self, rate):
        self.target_rate = rate
        self.target_vy = self.speed * (self.target_rate)

    @classmethod
    def spawn(cls):
        pass



class Terrain:
    # """上下の壁や障害物をスクロールさせる"""
    def __init__(self):
        self.segments = []
        self.generate_initial()

    def generate_initial(self):
        # 初期地形を生成
        for x in range(WIDTH // 8 + 2):
            self.segments.append(self.random_segment())

    def random_segment(self):
        # 上下の壁の高さをランダム生成
        top_height = random.randint(0, 20)
        bottom_height = random.randint(0, 20)
        return (top_height, bottom_height)

    def update(self):
        # 左にスクロール
        if px.frame_count % 8 == 0:  # スクロール速度
            self.segments.pop(0)
            self.segments.append(self.random_segment())

    def draw(self):
        for i, (top, bottom) in enumerate(self.segments):
            x = i * 8
            if top > 0:
                px.rect(x, 0, 8, top, 3)  # 上の壁
            if bottom > 0:
                px.rect(x, HEIGHT - bottom, 8, bottom, 3)  # 下の壁

    def check_collision(self, px, py, pw, ph):
        for i, (top, bottom) in enumerate(self.segments):
            x = i * 8
            if x < px + pw and x + 8 > px:
                if py < top or py + ph > HEIGHT - bottom:
                    return True
        return False


class Debris():
    SIZE = 8
    def __init__(self, dx, dy):
        self.x = random.randint(-Debris.SIZE, WIDTH)
        self.y = random.randint(-Debris.SIZE, HEIGHT - Debris.SIZE)
        self.dx = dx
        self.dy = dy
        self.speed = random.choice([0.5, 1, 1.5]) # 初速
        self.color = random.choice([5, 6, 7])
        self.craters =  []
        for _ in range(5):
            crater = (
                random.randint(0, Debris.SIZE),
                random.randint(0, Debris.SIZE)
            )
            self.craters.append(crater)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        # 画面外で無効化
        if self.is_offscreen():
            self.active = False

    def draw(self):
        px.rect(self.x, self.y, Debris.SIZE, Debris.SIZE, px.COLOR_BROWN)
        for c in self.craters:
            dx, dy = c
            px.pset(self.x + dx, self.y + dy, px.COLOR_BLACK)

    def is_offscreen(self):
        if (self.x < -Debris.SIZE or self.x > WIDTH  + Debris.SIZE or 
            self.y < -Debris.SIZE or self.y > HEIGHT + Debris.SIZE):
            return True
        return False

    @classmethod
    def spawn(cls):
        speed = random.randrange(10, 20, 1)
        deg = random.randrange(105, 75, 1)
        angle = math.radians(deg)  # convert to radians
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        gbl.obstacles.append(cls(dx, dy))




