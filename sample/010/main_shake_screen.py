# language: python
import pyxel
import random

class RPGGame:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel RPG Shake Example")
        self.shake_duration = 0  # 振動の残りフレーム数
        self.shake_magnitude = 0  # 振動の強さ（ピクセル）
        self.screen_offset = (0, 0)  # 描画オフセット
        pyxel.run(self.update, self.draw)

    def start_shake(self, duration=10, magnitude=5):
        """画面振動を開始する"""
        self.shake_duration = duration
        self.shake_magnitude = magnitude

    def update(self):
        # 振動処理
        if self.shake_duration > 0:
            # ランダムなオフセットを生成
            self.screen_offset = (
                random.randint(-self.shake_magnitude, self.shake_magnitude),
                random.randint(-self.shake_magnitude, self.shake_magnitude)
            )
            self.shake_duration -= 1
            self.shake_magnitude = max(0, self.shake_magnitude - 1)
        else:
            self.screen_offset = (0, 0)

        # ここにゲームの更新処理を記述
        if pyxel.btnp(pyxel.KEY_SPACE):
            # スペースキー押下で画面振動開始（例）
            self.start_shake(duration=15, magnitude=4)

    def draw(self):
        pyxel.cls(0)
        # 描画位置にオフセットを加えて表示
        offset_x, offset_y = self.screen_offset
        pyxel.rect(50 + offset_x, 50 + offset_y, 60, 20, 11)  # サンプルキャラクタ
        pyxel.text(55 + offset_x, 55 + offset_y, "Shake!", pyxel.frame_count % 16)

# ゲーム起動
RPGGame()

