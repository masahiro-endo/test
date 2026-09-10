
import pyxel as px
import math
import random
import uuid
from enum import IntEnum, auto

import appconfig as gbl
from constant import * 
from actor.equip import Bullet 
from actor.effects import Explosion 








class Bomb:
    DURATION = 20  # 爆発表示フレーム数
    def __init__(self):
        self.active = True
        self.timer = Bomb.DURATION
        self.x = gbl.player.x - (Player.SIZE//2)
        self.y = gbl.player.y - (Player.SIZE//2)
        self.radius = 0

    def update(self):
        # ボムタイマー更新 & 敵巻き込み処理
        if self.active:
            self.timer -= 1
            self.radius = (Bomb.DURATION - self.timer) * 2
            self.check_bomb_hit()
            if self.timer <= 0:
                self.active = False

    def draw(self):
        # ボム描画
        if self.active:
            radius = (Bomb.DURATION - self.timer) * 2
            px.circ(self.x + 4, self.y, radius, 8)   # 外側
            px.circ(self.x + 4, self.y, radius // 2, 10)  # 中心光

    def is_collision(self, obj):
            dist_sq = (obj.x - self.x) ** 2 + (obj.x - self.y) ** 2
            if dist_sq <= self.radius ** 2:
                return True
            return False

    def check_bomb_hit(self):
        # """爆発範囲にいる敵を消す"""
        for e in gbl.enemies:
            if self.is_collision(e):
                e.sudden_death()
                gbl.enemies.remove(e)
                gbl.explosions.append(Explosion(e.x + (e.size//2), e.y + (e.size//2)))

        for b in gbl.enemies:
            if self.is_collision(b):
                if b in gbl.bullets:
                    gbl.bullets.remove(b)





class POW(IntEnum):
    SPD = auto()
    ATK = auto()
    BOM = auto()

class PowerUp:
    SIZE = 8
    PARAM = {
        POW.SPD: (px.COLOR_LIGHT_BLUE, 'S', px.COLOR_GREEN),
        POW.ATK: (px.COLOR_RED,        'A', px.COLOR_YELLOW),
        POW.BOM: (px.COLOR_YELLOW,     'B', px.COLOR_RED),
    }
    def __init__(self, x=None, y=None):
        self.reset(x, y)

    def reset(self, x, y):
        # ランダムな位置と速度で初期化
        self.x = x if x else random.randint(10, WIDTH - 10)
        self.y = y if y else random.randint(10, HEIGHT - 10)
        self.vx = random.choice([-0.5, 0.5])
        self.vy = random.choice([-0.5, 0.5])
        self.size = PowerUp.SIZE
        self.type = random.choice(list(POW))
        self.color, self.letter,self.letter_color = PowerUp.PARAM[self.type]
        self.active = True

    def update(self):

        if self.hit(gbl.player):
            gbl.player.levelup(self.type)
            gbl.items.remove(self)

        # 漂う動き
        self.x += self.vx
        self.y += self.vy

        # 画面端で反射
        if self.x < 0 or self.x > WIDTH - self.size:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT - self.size:
            self.vy *= -1

    def draw(self):
        px.rect(self.x, self.y, self.size, self.size, self.color)
        px.text(self.x, self.y, str(self.letter), self.letter_color)

    def hit(self, player):
        return math.hypot(self.x - player.x, self.y - player.y) < self.size - 1

    @classmethod
    def spawn(cls, dx, dy):
        gbl.items.append(cls(dx, dy))




class Player:
    SIZE = 4
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT -10
        self.size = Player.SIZE
        self.speed = 2
        self.alive = True
        self.id = uuid.uuid4()
        self.bombs = []
        self.bomb_stock = 3
        self.shot_level = 1

    def update(self):
        if not self.alive:
            return
        if px.btn(px.KEY_UP):
            self.y -= self.speed
        if px.btn(px.KEY_DOWN):
            self.y += self.speed
        if px.btn(px.KEY_LEFT):
            self.x -= self.speed
        if px.btn(px.KEY_RIGHT):
            self.x += self.speed

        if px.btnp(px.KEY_SPACE,hold=10, repeat=3):
            Bullet.fire(self, self.shot_level)
        if px.btn(px.KEY_B) and self.bomb_stock > 0:
            # 連続使用不可
            if not self.bombs:
                self.bombs.append(Bomb())
                self.bomb_stock -= 1

        self.x = max(0, min(WIDTH - Player.SIZE, self.x))
        self.y = max(0, min(HEIGHT - Player.SIZE, self.y))

        for b in self.bombs:
            b.update()
        self.bombs = [b for b in self.bombs if b.active]

    def draw(self):
        for bomb in self.bombs:
            bomb.draw()

        if self.alive:
            px.rect(self.x, self.y, Player.SIZE, Player.SIZE, 11)

    def levelup(self, type):
        if type == POW.SPD:
            self.speed += 1
        if type == POW.ATK:
            self.shot_level = 3
        if type == POW.BOM:
            self.bomb_stock += 1

