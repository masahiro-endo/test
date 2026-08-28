
import pyxel

def cubic_bezier(p0, p1, p2, p3, t):
    """
    3次ベジェ曲線の座標を計算
    p0: 始点 (x, y)
    p1: 制御点1
    p2: 制御点2
    p3: 終点
    t: 0.0〜1.0
    """
    x = ((1 - t) ** 3) * p0[0] + 3 * ((1 - t) ** 2) * t * p1[0] \
        + 3 * (1 - t) * (t ** 2) * p2[0] + (t ** 3) * p3[0]
    y = ((1 - t) ** 3) * p0[1] + 3 * ((1 - t) ** 2) * t * p1[1] \
        + 3 * (1 - t) * (t ** 2) * p2[1] + (t ** 3) * p3[1]
    return (x, y)

def generate_bezier_path(p0, p1, p2, p3, steps=100):
    """
    ベジェ曲線上の座標リストを生成
    steps: 分割数（多いほど滑らか）
    """
    path = []
    for i in range(steps + 1):
        t = i / steps
        path.append(cubic_bezier(p0, p1, p2, p3, t))
    return path

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Bezier Path Example")

        # 始点, 制御点1, 制御点2, 終点
        p0 = (10, 100)
        p1 = (50, 20)
        p2 = (110, 20)
        p3 = (150, 100)

        # 経路生成
        self.path = generate_bezier_path(p0, p1, p2, p3, steps=200)
        self.index = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        # 経路を進める
        if self.index < len(self.path) - 1:
            self.index += 1

    def draw(self):
        pyxel.cls(0)

        # 経路を描画
        for px, py in self.path:
            pyxel.pset(int(px), int(py), 5)

        # 現在位置を描画
        x, y = self.path[self.index]
        pyxel.circ(int(x), int(y), 2, 11)

if __name__ == "__main__":
    App()

    