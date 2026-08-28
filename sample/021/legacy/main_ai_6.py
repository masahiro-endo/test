





import pyxel

class Enemy:
    def __init__(self, path, speed, color):
        self.path = path
        self.speed = speed
        self.color = color
        self.current_index = 0
        self.next_index = 1
        self.progress = 0.0
        self.x, self.y = self.path[0]

    def lerp(self, a, b, t):
        """線形補間"""
        return a + (b - a) * t

    def update(self):
        # 補間進行
        self.progress += self.speed
        if self.progress >= 1.0:
            self.progress = 0.0
            self.current_index = self.next_index
            self.next_index = (self.next_index + 1) % len(self.path)

        # 現在位置を補間で計算
        x1, y1 = self.path[self.current_index]
        x2, y2 = self.path[self.next_index]
        self.x = self.lerp(x1, x2, self.progress)
        self.y = self.lerp(y1, y2, self.progress)

    def draw(self):
        pyxel.circ(self.x, self.y, 4, self.color)


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Multiple Enemies with Lerp Paths")

        # 複数の敵を定義（経路・速度・色）
        self.enemies = [
            Enemy(
                path=[(20, 20), (140, 20), (140, 100), (20, 100), (20, 20)],
                speed=0.01,
                color=8
            ),
            Enemy(
                path=[(80, 10), (150, 60), (80, 110), (10, 60), (80, 10)],
                speed=0.015,
                color=11
            ),
            Enemy(
                path=[(40, 40), (120, 40), (120, 80), (40, 80), (40, 40)],
                speed=0.008,
                color=14
            )
        ]

        pyxel.run(self.update, self.draw)

    def update(self):
        for enemy in self.enemies:
            enemy.update()

    def draw(self):
        pyxel.cls(0)

        # 経路表示（デバッグ用）
        for enemy in self.enemies:
            for px, py in enemy.path:
                pyxel.circ(px, py, 1, 5)

        # 敵描画
        for enemy in self.enemies:
            enemy.draw()

        pyxel.text(5, 5, "Multiple Lerp Path Enemies", 7)


if __name__ == "__main__":
    App()



