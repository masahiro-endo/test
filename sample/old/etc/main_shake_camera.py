# -*- coding: utf-8 -*-
# Python
import pyxel
import random

class RPGGame:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel RPG Screen Shake Example")
        self.camera_x = 0
        self.camera_y = 0
        self.shake_timer = 0
        self.shake_intensity = 0
        pyxel.run(self.update, self.draw)

    def start_shake(self, intensity=4, duration=10):
        """画面シェイクを開始する関数"""
        self.shake_intensity = intensity
        self.shake_timer = duration

    def update(self):
        # 入力例：スペースキーで画面シェイクをトリガー
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.start_shake(intensity=6, duration=15)  # イベントごとに調整可能

        # シェイク処理
        if self.shake_timer > 0:
            # ランダムでカメラを揺らす
            self.camera_x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.camera_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_timer -= 1
            self.shake_intensity = max(0, self.shake_intensity - 1)
        else:
            self.camera_x = 0
            self.camera_y = 0

    def draw(self):
        pyxel.cls(0)
        pyxel.camera(self.camera_x, self.camera_y)

        # 背景を描画
        pyxel.rect(0, 0, 160, 120, 7)

        # サンプルイベントオブジェクト（赤い正方形）
        pyxel.rect(70, 50, 20, 20, 8)

# ゲーム開始
RPGGame()

