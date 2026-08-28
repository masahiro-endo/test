
import pyxel
import math

# 三角形の頂点座標
A = (40, 60)
B = (120, 50)
C = (80, 110)

def circumcircle(p1, p2, p3):
    """
    三角形の3頂点から外接円の中心座標と半径を求める
    """
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3

    # 行列式の分母
    d = 2 * (x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
    if d == 0:
        raise ValueError("3点が同一直線上にあるため外接円は存在しません")

    # 中心座標 (Ux, Uy)
    ux = ((x1**2 + y1**2)*(y2 - y3) +
          (x2**2 + y2**2)*(y3 - y1) +
          (x3**2 + y3**2)*(y1 - y2)) / d

    uy = ((x1**2 + y1**2)*(x3 - x2) +
          (x2**2 + y2**2)*(x1 - x3) +
          (x3**2 + y3**2)*(x2 - x1)) / d

    # 半径
    r = math.sqrt((ux - x1)**2 + (uy - y1)**2)

    return ux, uy, r

# 外接円の計算
cx, cy, radius = circumcircle(A, B, C)

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Circumcircle of Triangle")
        pyxel.run(self.update, self.draw)

    def update(self):
        pass  # 今回は静止表示

    def draw(self):
        pyxel.cls(0)

        # 三角形の描画
        pyxel.line(A[0], A[1], B[0], B[1], 7)
        pyxel.line(B[0], B[1], C[0], C[1], 7)
        pyxel.line(C[0], C[1], A[0], A[1], 7)

        # 頂点
        for x, y in [A, B, C]:
            pyxel.circ(x, y, 2, 8)

        # 外接円
        pyxel.circb(int(cx), int(cy), int(radius), 11)

        # 中心点
        pyxel.circ(int(cx), int(cy), 2, 9)

App()




