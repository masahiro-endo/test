
import pyxel
import math
import random

# 定数
SCREEN_W = 160
SCREEN_H = 120
ENEMY_WAIT_MIN = 30   # 停滞時間の最小フレーム
ENEMY_WAIT_MAX = 90   # 停滞時間の最大フレーム
ENEMY_SPEED = 1.0
SPAWN_INTERVAL = 60   # 敵出現間隔（フレーム）

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.wait_time = random.randint(ENEMY_WAIT_MIN, ENEMY_WAIT_MAX)
        self.state = "wait"  # "wait" → "escape" → "gone"

    def update(self, player_x, player_y):
        self.timer += 1

        if self.state == "wait":
            if self.timer >= self.wait_time:
                self.state = "escape"

        elif self.state == "escape":
            # プレイヤーから離れる方向に移動
            dx = self.x - player_x
            dy = self.y - player_y
            dist = math.sqrt(dx**2 + dy**2) or 1
            self.x += (dx / dist) * ENEMY_SPEED
            self.y += (dy / dist) * ENEMY_SPEED

            # 画面外に出たら消える
            if self.x < -10 or self.x > SCREEN_W + 10 or self.y < -10 or self.y > SCREEN_H + 10:
                self.state = "gone"

    def draw(self):
        if self.state != "gone":
            color = 8 if self.state == "wait" else 2  # 待機中は青、逃走中は赤
            pyxel.rect(self.x, self.y, 8, 8, color)

class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Multiple Enemies Wait & Escape")
        self.player_x = SCREEN_W // 2
        self.player_y = SCREEN_H // 2
        self.enemies = []
        self.spawn_timer = 0
        pyxel.run(self.update, self.draw)

    def spawn_enemy(self):
        # 画面の端からランダムに出現
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = random.randint(0, SCREEN_W), 0
        elif side == "bottom":
            x, y = random.randint(0, SCREEN_W), SCREEN_H - 8
        elif side == "left":
            x, y = 0, random.randint(0, SCREEN_H)
        else:  # right
            x, y = SCREEN_W - 8, random.randint(0, SCREEN_H)

        self.enemies.append(Enemy(x, y))

    def update(self):
        # プレイヤー移動（矢印キー）
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 1
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += 1

        # 敵の出現管理
        self.spawn_timer += 1
        if self.spawn_timer >= SPAWN_INTERVAL:
            self.spawn_enemy()
            self.spawn_timer = 0

        # 敵の更新
        for enemy in self.enemies:
            enemy.update(self.player_x, self.player_y)

        # 消えた敵を削除
        self.enemies = [e for e in self.enemies if e.state != "gone"]

    def draw(self):
        pyxel.cls(0)
        # プレイヤー
        pyxel.rect(self.player_x, self.player_y, 8, 8, 11)  # 黄色
        # 敵
        for enemy in self.enemies:
            enemy.draw()

# 実行
App()



