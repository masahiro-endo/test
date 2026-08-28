
import pyxel
import random
import math

# 画面サイズ
SCREEN_W = 160
SCREEN_H = 120

# プレイヤー設定
PLAYER_SPEED = 2

# Boids設定
ENEMY_COUNT = 15
MAX_SPEED = 1.5
NEIGHBOR_RADIUS = 20
SEPARATION_RADIUS = 8
CHASE_DISTANCE = 40  # プレイヤーがこの距離に入ると追尾

# 障害物設定
OBSTACLES = [
    {"x": 50, "y": 50, "r": 10},
    {"x": 110, "y": 70, "r": 12},
    {"x": 80, "y": 30, "r": 8}
]
OBSTACLE_AVOID_RADIUS = 15  # 回避を始める距離

class Enemy:
    def __init__(self):
        self.x = random.uniform(0, SCREEN_W)
        self.y = random.uniform(0, SCREEN_H)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.mode = "boid"  # "boid" or "chase"

    def update(self, enemies, player_x, player_y):
        # プレイヤーとの距離
        dxp = player_x - self.x
        dyp = player_y - self.y
        dist_p = math.hypot(dxp, dyp)

        # モード切り替え
        if dist_p < CHASE_DISTANCE:
            self.mode = "chase"
        else:
            self.mode = "boid"

        if self.mode == "chase":
            # プレイヤー追尾
            if dist_p != 0:
                self.vx += (dxp / dist_p) * 0.05
                self.vy += (dyp / dist_p) * 0.05
        else:
            # Boidsアルゴリズム
            align_x, align_y = 0, 0
            coh_x, coh_y = 0, 0
            sep_x, sep_y = 0, 0
            count = 0

            for other in enemies:
                if other is self:
                    continue
                dx = other.x - self.x
                dy = other.y - self.y
                dist = math.hypot(dx, dy)

                if dist < NEIGHBOR_RADIUS:
                    # 整列
                    align_x += other.vx
                    align_y += other.vy
                    # 結合
                    coh_x += other.x
                    coh_y += other.y
                    count += 1

                if dist < SEPARATION_RADIUS and dist > 0:
                    # 分離
                    sep_x -= dx / dist
                    sep_y -= dy / dist

            if count > 0:
                # 整列
                align_x /= count
                align_y /= count
                self.vx += (align_x - self.vx) * 0.05

                # 結合
                coh_x /= count
                coh_y /= count
                self.vx += (coh_x - self.x) * 0.01
                self.vy += (coh_y - self.y) * 0.01

            # 分離
            self.vx += sep_x * 0.05
            self.vy += sep_y * 0.05

        # --- 障害物回避 ---
        for obs in OBSTACLES:
            dxo = obs["x"] - self.x
            dyo = obs["y"] - self.y
            dist_o = math.hypot(dxo, dyo)
            if dist_o < OBSTACLE_AVOID_RADIUS + obs["r"]:
                # 障害物から離れる方向にベクトルを加える
                if dist_o != 0:
                    self.vx -= (dxo / dist_o) * 0.1
                    self.vy -= (dyo / dist_o) * 0.1

        # 速度制限
        speed = math.hypot(self.vx, self.vy)
        if speed > MAX_SPEED:
            self.vx = (self.vx / speed) * MAX_SPEED
            self.vy = (self.vy / speed) * MAX_SPEED

        # 位置更新
        self.x += self.vx
        self.y += self.vy

        # 画面端で反射
        if self.x < 0 or self.x > SCREEN_W:
            self.vx *= -1
        if self.y < 0 or self.y > SCREEN_H:
            self.vy *= -1

    def draw(self):
        color = 8 if self.mode == "boid" else 10  # 追尾中は緑
        pyxel.circ(self.x, self.y, 2, color)


class Game:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Pyxel Boids + Obstacle Avoidance")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.player_x = SCREEN_W // 2
        self.player_y = SCREEN_H // 2
        self.enemies = [Enemy() for _ in range(ENEMY_COUNT)]

    def update(self):
        # プレイヤー操作
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += PLAYER_SPEED

        # 画面外制限
        self.player_x = max(0, min(SCREEN_W, self.player_x))
        self.player_y = max(0, min(SCREEN_H, self.player_y))

        # 敵更新
        for enemy in self.enemies:
            enemy.update(self.enemies, self.player_x, self.player_y)
            # 衝突判定
            if math.hypot(enemy.x - self.player_x, enemy.y - self.player_y) < 4:
                pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 5, "Boids + Obstacle Avoidance", 7)
        pyxel.circ(self.player_x, self.player_y, 2, 11)  # プレイヤー
        for enemy in self.enemies:
            enemy.draw()
        # 障害物描画
        for obs in OBSTACLES:
            pyxel.circ(obs['x'], obs['y'], obs['r'], 2) 




# 実行
Game()
