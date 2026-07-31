
import pyxel as px
import random
import copy


# 定数
WIDTH = 80
HEIGHT = 120
CELL_SIZE = 4
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE




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
        self.x = 13
        self.y = 1

    def update(self):
        # 左右移動
        # 現在位置よりも＋１、未来の進行位置で判定
        if px.btnp(px.KEY_LEFT) and not self.is_collision(self.board, x=-1):
            self.x -= 1
        if px.btnp(px.KEY_RIGHT) and not self.is_collision(self.board, x=1):
            self.x += 1

        # 回転
        if px.btnp(px.KEY_X):  # 時計回り
            new_shape = self.rotate_cw()
            if not self.is_collision(self.board):
                self.shape = new_shape
        if px.btnp(px.KEY_Z):  # 反時計回り
            new_shape = self.rotate_ccw()
            if not self.is_collision(self.board):
                self.shape = new_shape

        # 下移動
        if px.btnp(px.KEY_DOWN):
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
        self.parent.bricks.pop(0)
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






class ViewModel:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.score = 0
        self.game_over = False
        self.bricks = []
        self.spawn_brick()

    def spawn_brick(self):
        # 「操作対象」「次の候補」の二つを生成
        while len(self.bricks) < 2:
            self.bricks.append(Brick(self))

        self.bricks[1].next_circle()
        self.bricks[0].active()
        if self.bricks[0].is_collision(self.board):
            self.game_over = True

    def update(self):
        if self.is_gameover():
            if px.btnp(px.KEY_R):
                self.reset()
            return

        self.bricks[0].update()

    # ライン消去
    def clear_lines(self):
        # 「0」が最低一つ存在する行を抽出＝セルが全て「0」以外の行を除く
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = ROWS - len(new_board) # 消えた行数
        for _ in range(lines_cleared):
            new_board.insert(0, [0] * COLS) # 消えた行数分を補充
        return new_board, lines_cleared

    def is_gameover(self):
        return self.game_over




class AppView:
    def __init__(self, ViewModel):
        self.vm = ViewModel

        px.init(WIDTH, HEIGHT, title="px Tetris")
        px.load("assets_tetris.pyxres")
        self.BOF = px.Font("umplus_j10r.bdf")

        px.run(self.update, self.draw)

    def update(self):
        self.vm.update()

    def draw(self):
        px.cls(0)
        # 盤面描画
        for y, row in enumerate(self.vm.board):
            for x, cell in enumerate(row):
                if cell:
                    # px.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, cell)
                    px.blt(x * CELL_SIZE, y * CELL_SIZE, 0, Brick.COLORS.index(cell) * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

        self.draw_round_rect(50, 1, 20, 20, 2, px.COLOR_GRAY)

        for brk in self.vm.bricks:
            brk.draw()
        self.vm.bricks[0].draw_ghost()


        # スコア表示
        px.text(2, 2, f"SCORE: {self.vm.score}", px.COLOR_WHITE)
        if self.vm.is_gameover():
            px.text(WIDTH // 2 - 15, HEIGHT // 2, "GAME OVER", px.COLOR_RED)
            px.text(WIDTH // 2 - 20, HEIGHT // 2 + 10, "Press R to Restart", px.COLOR_WHITE)


    def draw_round_rect(self, x, y, w, h, r, col):
        # 角丸四角形を描画する
        # x, y : 左上座標
        # w, h : 幅・高さ
        # r    : 角の半径
        # col  : 色番号
        # 中央の長方形
        px.rect(x + r, y, w - 2 * r, h, col)
        px.rect(x, y + r, w, h - 2 * r, col)

        # 4つの角を円で描く
        px.circ(x + r, y + r, r, col)                 # 左上
        px.circ(x + w - r - 1, y + r, r, col)         # 右上
        px.circ(x + r, y + h - r - 1, r, col)         # 左下
        px.circ(x + w - r - 1, y + h - r - 1, r, col) # 右下


if __name__ == "__main__":
    vm = ViewModel()
    AppView(vm)
