
import pyxel
import random

# --- 定数 ---
SCREEN_W = 160
SCREEN_H = 120

# --- プレイヤー ---
class Player:
    def __init__(self):
        self.x = SCREEN_W // 2
        self.y = SCREEN_H - 20
        self.speed = 2
        self.power = 1  # 弾の威力レベル
        self.cooldown = 0
        self.bullets = []

    def update(self):
        # 移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(0, self.x - self.speed)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(SCREEN_W - 8, self.x + self.speed)

        # 射撃
        if self.cooldown > 0:
            self.cooldown -= 1
        if pyxel.btn(pyxel.KEY_SPACE) and self.cooldown == 0:
            self.shoot()
            self.cooldown = 10  # 発射間隔

        # 弾更新
        for b in self.bullets:
            b["y"] -= 3
        self.bullets = [b for b in self.bullets if b["y"] > -4]

    def shoot(self):
        # パワーに応じて弾数増加
        if self.power == 1:
            self.bullets.append({"x": self.x + 3, "y": self.y})
        elif self.power == 2:
            self.bullets.append({"x": self.x, "y": self.y})
            self.bullets.append({"x": self.x + 6, "y": self.y})
        else:  # power >= 3
            self.bullets.append({"x": self.x - 2, "y": self.y})
            self.bullets.append({"x": self.x + 3, "y": self.y})
            self.bullets.append({"x": self.x + 8, "y": self.y})

    def draw(self):
        pyxel.rect(self.x, self.y, 8, 8, 11)  # プレイヤー
        for b in self.bullets:
            pyxel.rect(b["x"], b["y"], 2, 4, 10)

# --- 敵 ---
class Enemy:
    def __init__(self):
        self.x = random.randint(0, SCREEN_W - 8)
        self.y = -8
        self.speed = 1
        self.alive = True

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_H:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, 8, 8, 8)

# --- パワーアップアイテム ---
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.alive = True

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_H:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x + 4, self.y + 4, 3, 14)

# --- メインゲーム ---
class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Shooting with PowerUp")
        self.player = Player()
        self.enemies = []
        self.items = []
        self.spawn_timer = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

        # 敵出現
        self.spawn_timer += 1
        if self.spawn_timer > 30:
            self.enemies.append(Enemy())
            self.spawn_timer = 0

        # 敵更新
        for e in self.enemies:
            e.update()

        # アイテム更新
        for it in self.items:
            it.update()

        # 弾と敵の当たり判定
        for b in self.player.bullets:
            for e in self.enemies:
                if e.alive and abs(b["x"] - e.x) < 6 and abs(b["y"] - e.y) < 6:
                    e.alive = False
                    # 30%の確率でパワーアップアイテム生成
                    if random.random() < 0.3:
                        self.items.append(PowerUp(e.x, e.y))

        # プレイヤーとアイテムの当たり判定
        for it in self.items:
            if abs(it.x - self.player.x) < 6 and abs(it.y - self.player.y) < 6:
                it.alive = False
                self.player.power = min(self.player.power + 1, 3)  # 最大3段階

        # 生存オブジェクトだけ残す
        self.enemies = [e for e in self.enemies if e.alive]
        self.items = [it for it in self.items if it.alive]

    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        for e in self.enemies:
            e.draw()
        for it in self.items:
            it.draw()
        pyxel.text(5, 5, f"POWER: {self.player.power}", 7)

# 実行
App()

