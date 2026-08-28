
import pyxel
import random

# 定数
SCREEN_W = 160
SCREEN_H = 120
BOMB_DURATION = 20  # 爆発表示フレーム数
ENEMY_COUNT = 5

class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Shooting with Bomb & Enemies")
        self.player_x = SCREEN_W // 2
        self.player_y = SCREEN_H - 20

        # ボム関連
        self.bomb_active = False
        self.bomb_timer = 0
        self.bomb_x = 0
        self.bomb_y = 0

        # 敵リスト（x, y）
        self.enemies = []
        self.spawn_enemies()

        self.score = 0
        pyxel.run(self.update, self.draw)

    def spawn_enemies(self):
        """敵をランダム配置"""
        self.enemies.clear()
        for _ in range(ENEMY_COUNT):
            x = random.randint(0, SCREEN_W - 8)
            y = random.randint(10, SCREEN_H // 2)
            self.enemies.append([x, y])

    def update(self):
        # プレイヤー移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, SCREEN_W - 8)

        # ボム発射（スペースキー）
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.bomb_active:
            self.bomb_active = True
            self.bomb_timer = BOMB_DURATION
            self.bomb_x = self.player_x
            self.bomb_y = self.player_y - 8

        # ボムタイマー更新 & 敵巻き込み処理
        if self.bomb_active:
            self.bomb_timer -= 1
            radius = (BOMB_DURATION - self.bomb_timer) * 2
            self.check_bomb_hit(radius)
            if self.bomb_timer <= 0:
                self.bomb_active = False

        # 敵が全滅したら再出現
        if not self.enemies:
            self.spawn_enemies()

    def check_bomb_hit(self, radius):
        """爆発範囲にいる敵を消す"""
        new_enemies = []
        for ex, ey in self.enemies:
            dist_sq = (ex - self.bomb_x) ** 2 + (ey - self.bomb_y) ** 2
            if dist_sq <= radius ** 2:
                self.score += 100  # スコア加算
            else:
                new_enemies.append([ex, ey])
        self.enemies = new_enemies

    def draw(self):
        pyxel.cls(0)

        # プレイヤー
        pyxel.rect(self.player_x, self.player_y, 8, 8, 11)

        # 敵
        for ex, ey in self.enemies:
            pyxel.rect(ex, ey, 8, 8, 8)

        # ボム描画
        if self.bomb_active:
            radius = (BOMB_DURATION - self.bomb_timer) * 2
            pyxel.circ(self.bomb_x + 4, self.bomb_y, radius, 8)   # 外側
            pyxel.circ(self.bomb_x + 4, self.bomb_y, radius // 2, 10)  # 中心光

        # UI
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(5, 15, "SPACE: Bomb", 7)

# 実行
App()


