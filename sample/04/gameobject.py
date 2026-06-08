import math
import random
import pyxel

# ゲームオブジェクト
class GameObject:
    def __init__(self):
        self.exists = False
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.size = 6
        self.hp = 1
    def init(self, x, y, deg, speed):
        self.x, self.y = x, y
        rad = math.radians(deg)
        self.set_speed(rad, speed)
    def set_position(self, x, y):
        self.x, self.y = x, y
    def move(self):
        self.x += self.vx
        self.y += self.vy
    def set_speed(self, rad, speed):
        self.vx, self.vy = speed * math.cos(rad), speed * -math.sin(rad)
    def draw_self(self, palette):
        r2 = self.size/2
        pyxel.rect(self.x-r2, self.y-r2, self.x+r2, self.y+r2, palette)
    def is_outside(self):
        r2 = self.size/2
        return self.x < -r2 or self.y < -r2 or self.x > pyxel.width+r2 or self.y > pyxel.height+r2
    def clip_screen(self):
        r2 = self.size/2
        self.x = r2 if self.x < r2 else self.x
        self.y = r2 if self.y < r2 else self.y
        self.x = pyxel.width-r2 if self.x > pyxel.width-r2 else self.x
        self.y = pyxel.height-r2 if self.y > pyxel.height-r2 else self.y
    def update(self):
        self.move()
        if self.is_outside():
            self.exists = False
    def dead(self):
        pass
    def hurt(self, val=1):
        if self.exists == False:
            return
        self.hp -= val
        if self.hp <= 0:
            self.exists = False
            self.dead()

# ゲームオブジェクト管理
class GameObjectManager:
    def __init__(self, num, obj):
        self.pool = []
        for i in range(0, num):
            self.pool.append(obj())
    def count_exists(self):
        cnt = 0
        for obj in self.pool:
            if obj.exists == True:
                cnt += 1
        return cnt

    def add(self):
        for obj in self.pool:
            if obj.exists == False:
                obj.exists = True
                return obj
        return None
    def update(self):
        for obj in self.pool:
            if obj.exists:
                obj.update()
    def draw(self):
        for obj in self.pool:
            if obj.exists:
                obj.draw()
    def vanish(self):
        for obj in self.pool:
            if obj.exists:
                obj.hurt(999)

