from pgzero.builtins import *


# プレイヤークラス（Actorクラスを継承）
class Player(Actor):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.pos = x, y
        self.isMoving = False
        self.isRunning = True
     
    def update(self):
        None
        # if not self.isRunning:
        #     self.pos = -1000, -1000
 
# プレイヤーの弾クラス
class Shot(Actor):
    def __init__(self, name, x, y, lmt):
        super().__init__(name)
        self.pos = x, y
        self.speed = 5
        self.isRunning = True
        self.limit = lmt
 
    def update(self):
        self.y -= self.speed
        if self.y < self.limit:
            self.isRunning = False
 
# 敵クラス
class Enemy(Actor):
    def __init__(self, name, x, y, lmt):
        super().__init__(name)
        self.pos = x, y
        self.speed = 2
        self.isRunning = True
        self.limit = lmt
     
    def update(self):
        # プレイヤー弾との当たり判定
        # for shot in shots:
        #     if shot.colliderect(self):
        #         self.isRunning = False
                 
        self.y += self.speed
        if self.y > self.limit:
            self.isRunning = False

