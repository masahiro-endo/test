
import pyxel as px
import random

# 定数
WIDTH = 80
HEIGHT = 120
CELL_SIZE = 4
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

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

COLORS = [8, 9, 10, 11, 12, 13, 14]  # px カラーID

# 回転関数
def rotate_cw(shape):
    return [list(row) for row in zip(*shape[::-1])]

def rotate_ccw(shape):
    return [list(row) for row in zip(*shape)][::-1]

# 衝突判定
def is_collision(board, shape, x, y):
    for j, row in enumerate(shape):
        for i, cell in enumerate(row):
            if cell:
                if (x + i < 0 or x + i >= COLS or y + j >= ROWS or board[y + j][x + i]):
                    return True
    return False

# ライン消去
def clear_lines(board):
    # 「0」が最低一つ存在する行を抽出＝セルが全て「0」以外の行を除く
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board) # 消えた行数
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * COLS) # 消えた行数分を補充
    return new_board, lines_cleared

class Tetris:
    def __init__(self):
        px.init(WIDTH, HEIGHT, title="px Tetris")
        px.load("assets_tetris.pyxres")
        self.BOF = px.Font("umplus_j10r.bdf")

        self.reset()
        px.run(self.update, self.draw)

    def reset(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.spawn_block()
        self.drop_timer = 0
        self.score = 0
        self.game_over = False

    def spawn_block(self):
        self.idx = random.randrange(len(SHAPES))
        self.shape = [row[:] for row in SHAPES[self.idx]]
        self.color = COLORS[self.idx]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0
        if is_collision(self.board, self.shape, self.x, self.y):
            self.game_over = True

    def lock_block(self):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    # ロックされたら
                    # 自分の位置の盤面セルを「色番号」で上書き
                    self.board[self.y + j][self.x + i] = self.color 
        self.board, lines = clear_lines(self.board)
        self.score += lines * 100
        self.spawn_block()

    def hard_drop(self):
        """スペースキーで一気に落下"""
        while not is_collision(self.board, self.shape, self.x, self.y + 1):
            self.y += 1
        self.lock_block()

    def get_ghost_y(self):
        """ゴーストブロックのY座標を計算"""
        ghost_y = self.y
        while not is_collision(self.board, self.shape, self.x, ghost_y + 1):
            ghost_y += 1
        return ghost_y

    def update(self):
        if self.game_over:
            if px.btnp(px.KEY_R):
                self.reset()
            return

        # 左右移動
        if px.btnp(px.KEY_LEFT) and not is_collision(self.board, self.shape, self.x - 1, self.y):
            self.x -= 1
        if px.btnp(px.KEY_RIGHT) and not is_collision(self.board, self.shape, self.x + 1, self.y):
            self.x += 1

        # 回転
        if px.btnp(px.KEY_X):  # 時計回り
            new_shape = rotate_cw(self.shape)
            if not is_collision(self.board, new_shape, self.x, self.y):
                self.shape = new_shape
        if px.btnp(px.KEY_Z):  # 反時計回り
            new_shape = rotate_ccw(self.shape)
            if not is_collision(self.board, new_shape, self.x, self.y):
                self.shape = new_shape

        # 下移動
        if px.btnp(px.KEY_DOWN):
            if not is_collision(self.board, self.shape, self.x, self.y + 1):
                self.y += 1
            else:
                self.lock_block()

        # ハードドロップ
        if px.btnp(px.KEY_SPACE):
            self.hard_drop()

        # 自動落下
        self.drop_timer += 1
        if self.drop_timer > 15:
            self.drop_timer = 0
            if not is_collision(self.board, self.shape, self.x, self.y + 1):
                self.y += 1
            else:
                self.lock_block()

    def draw(self):
        px.cls(0)
        # 盤面描画
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    # px.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, cell)
                    px.blt(x * CELL_SIZE, y * CELL_SIZE, 0, COLORS.index(cell) * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

        # ゴーストブロック描画（薄い色）
        ghost_y = self.get_ghost_y()
        ghost_color = 5  # 薄い色（Pyxelの水色）
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    px.rectb((self.x + i) * CELL_SIZE, (ghost_y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE, ghost_color)

        # 現在のブロック描画
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                # 移動中のセル値は「１」
                if cell:
                    # px.rect((self.x + i) * CELL_SIZE, (self.y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE, self.color)
                    px.blt((self.x + i) * CELL_SIZE, (self.y + j) * CELL_SIZE, 0, COLORS.index(self.color) * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

        # スコア表示
        px.text(2, 2, f"SCORE: {self.score}", 7)
        if self.game_over:
            px.text(WIDTH // 2 - 15, HEIGHT // 2, "GAME OVER", 8)
            px.text(WIDTH // 2 - 20, HEIGHT // 2 + 10, "Press R to Restart", 7)

if __name__ == "__main__":
    Tetris()

