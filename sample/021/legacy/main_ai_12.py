
import pyxel
import math
import random

WIDTH, HEIGHT = 160, 120

class Enemy:
    def __init__(self, x, y, pattern, player_ref):
        self.x = x
        self.y = y
        self.pattern = pattern
        self.t = 0
        self.player_ref = player_ref
        self.angle = random.uniform(0, math.pi * 2)  # spiral用

    def update(self):
        self.t += 1

        if self.pattern == "straight":
            self.y += 1

        elif self.pattern == "zigzag":
            self.y += 0.8
            self.x += math.sin(self.t * 0.15) * 2

        elif self.pattern == "circle":
            self.y += 0.5
            self.x += math.cos(self.t * 0.1) * 2

        elif self.pattern == "spiral":
            self.angle += 0.1
            radius = 2 + self.t * 0.05
            self.x += math.cos(self.angle) * radius * 0.1
            self.y += math.sin(self.angle) * radius * 0.1 + 0.5

        elif self.pattern == "homing":
            dx = self.player_ref.x - self.x
            dy = self.player_ref.y - self.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                self.x += dx / dist * 0.8
                self.y += dy / dist * 0.8

    def draw(self):
        pyxel.circ(self.x, self.y, 3, 8)

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 10

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + 2, WIDTH)

    def draw(self):
        pyxel.tri(self.x, self.y,
                  self.x - 4, self.y + 6,
                  self.x + 4, self.y + 6, 11)

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Pyxel Complex Enemy Patterns")
        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

        # 敵生成
        self.spawn_timer += 1
        if self.spawn_timer > 30:
            pattern = random.choice(["straight", "zigzag", "circle", "spiral", "homing"])
            self.enemies.append(Enemy(random.randint(10, WIDTH - 10), 0, pattern, self.player))
            self.spawn_timer = 0

        # 敵更新
        for e in self.enemies:
            e.update()

        # 画面外削除
        self.enemies = [e for e in self.enemies if 0 <= e.x <= WIDTH and 0 <= e.y <= HEIGHT + 10]

    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        for e in self.enemies:
            e.draw()

App()



