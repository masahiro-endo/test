
import pyxel as px
import random

from constant import *









class Brick:
    # ブロック定義（2Dリスト）
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[0, 1, 0], [1, 1, 1]],  # T
        [[1, 0, 0], [1, 1, 1]],  # J
        [[0, 0, 1], [1, 1, 1]],  # L
        [[1, 1, 0], [0, 1, 1]],  # S
        [[0, 1, 1], [1, 1, 0]]   # Z
    ]
    # px カラーID ブロック定義順
    COLORS = [
        px.COLOR_LIGHT_BLUE, 
        px.COLOR_YELLOW,
        px.COLOR_PURPLE,
        px.COLOR_DARK_BLUE,
        px.COLOR_ORANGE,
        px.COLOR_GREEN,
        px.COLOR_RED
        ] 

    def __init__(self, parent):
        self.parent = parent
        self.board = parent.board
        self.idx   = random.randrange(len(Brick.SHAPES))
        self.shape = [row[:] for row in Brick.SHAPES[self.idx]]
        self.color = Brick.COLORS[self.idx]
        self.x = random.randrange(len(Brick.SHAPES))
        self.y = 0
        self.drop_timer = 0

    def active(self):
        self.x = random.randrange(len(Brick.SHAPES))
        self.y = 0

    def next_circle(self):
        self.x = 11
        self.y = 1

    def update(self):
        # 左右移動
        # 現在位置よりも＋１、未来の進行位置で判定
        if px.btnp(px.KEY_LEFT, hold=3, repeat=3) and not self.is_collision(self.board, x=-1):
            self.x -= 1
        if px.btnp(px.KEY_RIGHT, hold=3, repeat=3) and not self.is_collision(self.board, x=1):
            self.x += 1

        # 回転
        if px.btnp(px.KEY_X, hold=3, repeat=3):  # 時計回り
            new_shape = self.rotate_cw()
            if not self.is_collision(self.board):
                self.shape = new_shape
        if px.btnp(px.KEY_Z, hold=3, repeat=3):  # 反時計回り
            new_shape = self.rotate_ccw()
            if not self.is_collision(self.board):
                self.shape = new_shape

        # 下移動
        if px.btnp(px.KEY_DOWN, hold=3, repeat=3):
            if not self.is_collision(self.board, y=1):
                self.y += 1
            else:
                self.lock_brick()

        # ハードドロップ
        if px.btnp(px.KEY_SPACE):
            self.hard_drop()

        # 自動落下
        self.drop_timer += 1
        if self.drop_timer > 10:
            self.drop_timer = 0
            if not self.is_collision(self.board, y=1):
                self.y += 1
            else:
                self.lock_brick()

    def draw(self):
        # 現在のブロック描画
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                # 移動中のセル値は「１」
                if cell:
                    # px.rect((self.x + i) * CELL_SIZE, (self.y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE, self.color)
                    px.blt((self.x + i) * CELL_SIZE, (self.y + j) * CELL_SIZE, 0, Brick.COLORS.index(self.color) * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

    def draw_ghost(self):
        # ゴーストブロック描画（薄い色）
        ghost_y = self.get_ghost_y()
        ghost_color = px.COLOR_GRAY
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    px.rectb((self.x + i) * CELL_SIZE, (ghost_y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE, ghost_color)


    # 回転関数
    def rotate_cw(self):
        return [list(row) for row in zip(*self.shape[::-1])]

    def rotate_ccw(self):
        return [list(row) for row in zip(*self.shape)][::-1]

    # 衝突判定
    def is_collision(self, board, **kwargs):
        x = kwargs.get('x', 0) 
        y = kwargs.get('y', 0) 
        return self.is_base_collision(board, self.x + x, self.y + y)
    def is_base_collision(self, board, x, y):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    if (x + i < 0 or x + i >= COLS or y + j >= ROWS or board[y + j][x + i]):
                        return True
        return False

    def lock_brick(self):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    # ロックされたら
                    # 自分の位置の盤面セルを「色番号」で上書き
                    self.board[self.y + j][self.x + i] = self.color 
        self.parent.board, lines = self.parent.clear_lines()
        self.parent.score += lines * 100
        self.parent.bricks.pop(0) #「操作対象」を消す
        self.parent.spawn_brick()


    def hard_drop(self):
        # スペースキーで一気に落下
        while not self.is_collision(self.board, y=1):
            self.y += 1
        self.lock_brick()

    def get_ghost_y(self):
        # ゴーストブロックのY座標を計算
        ghost_y = self.y
        while not self.is_base_collision(self.board, self.x, ghost_y + 1):
            ghost_y += 1
        return ghost_y





