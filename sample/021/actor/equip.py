
import pyxel as px
import math

import appconfig as gbl
from constant import * 








class Bullet:
    SIZE = 4
    def __init__(self, owner_id, x, y, dx, dy, col=px.COLOR_WHITE):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = col
        self.active = True
        self.owner_id = owner_id

    def update(self):
        self.x += self.dx
        self.y += self.dy
        # 画面外で無効化
        if self.is_offscreen():
            self.active = False

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_offscreen(self):
        # 画面外で無効化
        if (self.x < -Bullet.SIZE or self.x > WIDTH  + Bullet.SIZE or 
            self.y < -Bullet.SIZE or self.y > HEIGHT + Bullet.SIZE):
            return True
        return False


    @classmethod
    def chase_target(cls, target, actor):
            dx = target.x - actor.x
            dy = target.y - actor.y
            dist = math.sqrt(dx**2 + dy**2) or 1
            speed = 1.5
            gbl.bullets.append(cls(actor.id, 
                                   actor.x, actor.y, 
                                   dx/dist * speed, dy/dist * speed))

    @classmethod
    def fire(cls, actor, way=1):
            speed = 10
            angles = []

            if way == 1:
                angles = [90]
            if way == 3:
                angles = [90, 105, 75]
            for deg in angles:
                # gbl.bullets.append(cls(actor.id, 
                #                    actor.x + (Player.SIZE//2), actor.y + (Player.SIZE//2),
                #                     0, -speed, deg))
                angle = math.radians(deg)  # convert to radians
                dx = -speed * math.cos(angle)
                dy = -speed * math.sin(angle)
                gbl.bullets.append(cls(actor.id, 
                                   actor.x + (actor.size//2), actor.y + (actor.size//2),
                                    dx, dy))







