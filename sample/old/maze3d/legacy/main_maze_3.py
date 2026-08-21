
import pyxel

# 迷宮マップ（1=壁, 0=通路）
MAP = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

# プレイヤー初期位置と向き
player_x = 3
player_y = 3
player_dir = 0  # 0=北, 1=東, 2=南, 3=西

# 奥行きごとの壁サイズ設定
# depth: 1=手前, 2=中間, 3=奥
DEPTH_CONFIG = {
    1: {"front": (64, 128, 32), "side": (64, 32, 32)},
    2: {"front": (32, 64, 16),  "side": (32, 16, 16)},
    3: {"front": (16, 32, 8),   "side": (16, 8, 8)},
}

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Full Pseudo 3D Maze")
        self.make_textures()
        pyxel.run(self.update, self.draw)

    def make_textures(self):
        """
        壁テクスチャをPyxelのイメージバンクに描く
        """
        img = pyxel.image(0)
        img.cls(0)

        # 正面壁テクスチャ（灰色）
        img.rect(0, 0, 128, 64, 8)
        img.rectb(0, 0, 128, 64, 7)

        # 側面壁テクスチャ（暗い灰色）
        img.rect(128, 0, 32, 64, 5)
        img.rectb(128, 0, 32, 64, 7)

    def update(self):
        global player_x, player_y, player_dir

        # 回転
        if pyxel.btnp(pyxel.KEY_LEFT):
            player_dir = (player_dir - 1) % 4
        if pyxel.btnp(pyxel.KEY_RIGHT):
            player_dir = (player_dir + 1) % 4

        # 前進
        if pyxel.btnp(pyxel.KEY_UP):
            dx, dy = self.dir_to_vec(player_dir)
            if MAP[player_y + dy][player_x + dx] == 0:
                player_x += dx
                player_y += dy

        # 後退
        if pyxel.btnp(pyxel.KEY_DOWN):
            dx, dy = self.dir_to_vec(player_dir)
            if MAP[player_y - dy][player_x - dx] == 0:
                player_x -= dx
                player_y -= dy

    def draw(self):
        pyxel.cls(0)
        self.draw_maze_view()
        self.draw_minimap()

    def draw_maze_view(self):
        """
        奥から手前に、正面・左右の壁を描画
        """
        for depth in range(3, 0, -1):  # 奥から手前
            cfg = DEPTH_CONFIG[depth]
            dx, dy = self.dir_to_vec(player_dir)

            # 正面のマス
            fx = player_x + dx * depth
            fy = player_y + dy * depth
            if self.is_wall(fx, fy):
                w, W, y_off = cfg["front"]
                x = (pyxel.width - W) // 2
                pyxel.blt(x, y_off, 0, 0, 0, W, w)
                continue  # 壁があれば奥は見えない

            # 左右のマス
            left_dx, left_dy = self.dir_to_vec((player_dir - 1) % 4)
            right_dx, right_dy = self.dir_to_vec((player_dir + 1) % 4)

            # 左の壁
            lx = fx + left_dx
            ly = fy + left_dy
            if self.is_wall(lx, ly):
                h, w, y_off = cfg["side"]
                pyxel.blt(0, y_off, 0, 128, 0, w, h)

            # 右の壁
            rx = fx + right_dx
            ry = fy + right_dy
            if self.is_wall(rx, ry):
                h, w, y_off = cfg["side"]
                pyxel.blt(pyxel.width - w, y_off, 0, 128, 0, w, h)

    def draw_minimap(self):
        """
        左上にミニマップを描画
        """
        for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
                color = 7 if cell == 1 else 0
                pyxel.pset(x, y, color)
        pyxel.pset(player_x, player_y, 11)

    @staticmethod
    def dir_to_vec(d):
        return [(0, -1), (1, 0), (0, 1), (-1, 0)][d]

    @staticmethod
    def is_wall(x, y):
        return MAP[y][x] == 1

App()

