
import pyxel
import math

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Bouncing Deforming Circle", fps=60)

        # 円の初期位置と速度
        self.x = 80
        self.y = 60
        self.vx = 1.5
        self.vy = 1.2

        # 円の半径
        self.radius = 10

        # 変形アニメーション用
        self.deform_x = 1.0
        self.deform_y = 1.0
        self.deform_timer = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        # 位置更新
        self.x += self.vx
        self.y += self.vy

        # 壁との衝突判定
        if self.x - self.radius <= 0 or self.x + self.radius >= pyxel.width:
            self.vx *= -1
            self.start_deform(horizontal=True)

        if self.y - self.radius <= 0 or self.y + self.radius >= pyxel.height:
            self.vy *= -1
            self.start_deform(horizontal=False)

        # 変形アニメーション更新
        if self.deform_timer > 0:
            t = self.deform_timer / 10
            # 緩やかに元の形に戻す
            self.deform_x = 1.0 + (self.target_dx - 1.0) * t
            self.deform_y = 1.0 + (self.target_dy - 1.0) * t
            self.deform_timer -= 1
        else:
            self.deform_x = 1.0
            self.deform_y = 1.0

    def start_deform(self, horizontal=True):
        """衝突時に変形開始"""
        self.deform_timer = 10
        if horizontal:
            self.target_dx = 1.3
            self.target_dy = 0.7
        else:
            self.target_dx = 0.7
            self.target_dy = 1.3

    def draw(self):
        pyxel.cls(0)

        # 円を変形して描画
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            px = self.x + math.cos(rad) * self.radius * self.deform_x
            py = self.y + math.sin(rad) * self.radius * self.deform_y
            pyxel.pset(int(px), int(py), 11)

# 実行
App()

