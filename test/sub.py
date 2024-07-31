from shoot import *
from pgzrun import *

# プレイヤークラス（Actorクラスを継承）
class Player(Actor):
    def __init__(self, name):
        super().__init__(name)
        self.pos = 140, 300
        self.isMoving = False
        self.isRunning = True
     
    def update(self):
        if self.isRunning == False:
            player.pos = -1000, -1000
 
# プレイヤーの弾クラス
class Shot(Actor):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.pos = x, y
        self.speed = 5
        self.isRunning = True
 
    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.isRunning = False
 
# 敵クラス
class Enemy(Actor):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.pos = x, y
        self.speed = 2
        self.isRunning = True
     
    def update(self):
        # プレイヤー弾との当たり判定
        for shot in shots:
            if shot.colliderect(self):
                self.isRunning = False
                 
        self.y += self.speed
        if self.y > HEIGHT:
            self.isRunning = False

