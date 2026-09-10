
import pyxel
import random

# 画面サイズ
WIDTH = 160
HEIGHT = 120

class PowerUp:
    def __init__(self):
        self.reset()

    def reset(self):
        # ランダムな位置と速度で初期化
        self.x = random.randint(10, WIDTH - 10)
        self.y = random.randint(10, HEIGHT - 10)
        self.vx = random.choice([-0.5, 0.5])
        self.vy = random.choice([-0.5, 0.5])
        self.size = 4
        self.color = 10  # 緑色

    def update(self):
        # 漂う動き
        self.x += self.vx
        self.y += self.vy

        # 画面端で反射
        if self.x < 0 or self.x > WIDTH - self.size:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT - self.size:
            self.vy *= -1

    def draw(self):
        pyxel.rect(self.x, self.y, self.size, self.size, self.color)


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Pyxel Shooting Power-Up")
        self.powerups = [PowerUp() for _ in range(3)]  # 複数漂わせる
        pyxel.run(self.update, self.draw)

    def update(self):
        # ESCキーで終了
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # パワーアップ更新
        for p in self.powerups:
            p.update()

    def draw(self):
        pyxel.cls(0)  # 背景黒
        for p in self.powerups:
            p.draw()


if __name__ == "__main__":
    App()


    