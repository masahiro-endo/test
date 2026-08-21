
import pyxel
import math

# 迷路マップ（1=壁, 0=空間）
MAP = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

VIEW_DEPTH = 4  # 奥行き
TILE_SIZE = 16  # 壁の基準サイズ

# 奥行きごとの壁サイズ（幅, 高さ）
DEPTH_SCALE = {
    1: (80, 80),
    2: (60, 60),
    3: (40, 40),
    4: (20, 20),
}

# 奥行きごとの左右オフセット
DEPTH_OFFSET = {
    1: 70,
    2: 50,
    3: 30,
    4: 10,
}

class App:
    def __init__(self):
        self.x = 3
        self.y = 3
        self.dir = 0  # 0=上, 1=右, 2=下, 3=左
        pyxel.init(160, 120, title="Pseudo 3D Maze (Wizardry Style)")
        pyxel.run(self.update, self.draw)

    def update(self):
        # 回転
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.dir = (self.dir - 1) % 4
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.dir = (self.dir + 1) % 4

        # 前進・後退
        if pyxel.btnp(pyxel.KEY_UP):
            dx, dy = self.dir_to_vec(self.dir)
            if MAP[self.y + dy][self.x + dx] == 0:
                self.x += dx
                self.y += dy
        if pyxel.btnp(pyxel.KEY_DOWN):
            dx, dy = self.dir_to_vec(self.dir)
            if MAP[self.y - dy][self.x - dx] == 0:
                self.x -= dx
                self.y -= dy

    def dir_to_vec(self, d):
        return [(0, -1), (1, 0), (0, 1), (-1, 0)][d]

    def draw(self):
        pyxel.cls(0)
        self.draw_maze_3d()

    def draw_maze_3d(self):
        # 奥から手前に描画
        for depth in range(VIEW_DEPTH, 0, -1):
            # 中央前方
            dx, dy = self.dir_to_vec(self.dir)
            cx = self.x + dx * depth
            cy = self.y + dy * depth
            self.draw_wall_if_needed(cx, cy, depth, 0)

            # 左側
            left_dir = (self.dir - 1) % 4
            ldx, ldy = self.dir_to_vec(left_dir)
            lx = cx + ldx
            ly = cy + ldy
            self.draw_wall_if_needed(lx, ly, depth, -1)

            # 右側
            right_dir = (self.dir + 1) % 4
            rdx, rdy = self.dir_to_vec(right_dir)
            rx = cx + rdx
            ry = cy + rdy
            self.draw_wall_if_needed(rx, ry, depth, 1)

    def draw_wall_if_needed(self, tx, ty, depth, side):
        if 0 <= ty < len(MAP) and 0 <= tx < len(MAP[0]):
            if MAP[ty][tx] == 1:
                w, h = DEPTH_SCALE[depth]
                offset = DEPTH_OFFSET[depth] * side
                px = pyxel.width // 2 - w // 2 + offset
                py = pyxel.height // 2 - h // 2
                color = 8 - depth  # 奥行きで色を変える
                pyxel.rect(px, py, w, h, max(1, color))

App()


