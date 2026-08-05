
import pyxel as px

from constant import *
from actor import *










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
        # 「0」が最低一つ存在する行を抽出＝セルが全て「0」以外で埋まる行を除去
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

        # 盤面
        for y, row in enumerate(self.vm.board):
            for x, cell in enumerate(row):
                if cell:
                    # px.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, cell)
                    px.blt(x * CELL_SIZE, y * CELL_SIZE, 0, Brick.COLORS.index(cell) * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)


        # 次候補ブロック背後の矩形
        self.draw_round_rect(50, 1, 25, 20, 2, px.COLOR_GRAY)

        # ブロック
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
