
import math
import pyxel







# 円軌道の座標リストを作成する関数
def generate_circle_path(cx, cy, radius, steps):
    """
    cx, cy : 円の中心座標
    radius : 半径
    steps  : 分割数（多いほど滑らか）
    return : [(x1, y1), (x2, y2), ...]
    """
    path = []
    for i in range(steps):
        angle = (2 * math.pi / steps) * i
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        path.append((x, y))
    return path


# Pyxel ゲームクラス
class App:
    def __init__(self):
        pyxel.init(160, 120, title="Enemy Circle Path")
        self.enemy_path = generate_circle_path(80, 60, 30, 60)  # 中心(80,60)、半径30、60分割
        self.enemy_index = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        # 敵の座標を順番に進める
        self.enemy_index = (self.enemy_index + 1) % len(self.enemy_path)

    def draw(self):
        pyxel.cls(0)
        # 円軌道のガイド表示
        for x, y in self.enemy_path:
            pyxel.pset(int(x), int(y), 5)
        # 敵の描画
        ex, ey = self.enemy_path[self.enemy_index]
        pyxel.circ(int(ex), int(ey), 3, 8)


if __name__ == "__main__":
    App()




