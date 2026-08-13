import pyxel
import random

WIDTH = 10
HEIGHT = 10
MINES = 15
CELL_SIZE = 8

HIDDEN = 0
REVEALED = 1
FLAGGED = 2

class Minesweeper:
    def __init__(self):
        pyxel.init(WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE, title="Retro Minesweeper")
        pyxel.load("assets_mine.pyxres")  # 画像リソース読み込み
        self.reset()
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.state = [[HIDDEN for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.game_over = False
        self.win = False

        mines = set()
        while len(mines) < MINES:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            mines.add((x, y))
        for (mx, my) in mines:
            self.board[my][mx] = -1

        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x] == -1:
                    continue
                count = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                            if self.board[ny][nx] == -1:
                                count += 1
                self.board[y][x] = count

    def reveal(self, x, y):
        if self.state[y][x] != HIDDEN:
            return
        self.state[y][x] = REVEALED
        if self.board[y][x] == 0:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                        self.reveal(nx, ny)

    def check_win(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x] != -1 and self.state[y][x] != REVEALED:
                    return False
        return True

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and not self.game_over:
            mx, my = pyxel.mouse_x // CELL_SIZE, pyxel.mouse_y // CELL_SIZE
            if 0 <= mx < WIDTH and 0 <= my < HEIGHT:
                if self.board[my][mx] == -1:
                    self.game_over = True
                else:
                    self.reveal(mx, my)
                    if self.check_win():
                        self.win = True
                        self.game_over = True

        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON) and not self.game_over:
            mx, my = pyxel.mouse_x // CELL_SIZE, pyxel.mouse_y // CELL_SIZE
            if 0 <= mx < WIDTH and 0 <= my < HEIGHT:
                if self.state[my][mx] == HIDDEN:
                    self.state[my][mx] = FLAGGED
                elif self.state[my][mx] == FLAGGED:
                    self.state[my][mx] = HIDDEN

        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

    def draw(self):
        pyxel.cls(0)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                px, py = x * CELL_SIZE, y * CELL_SIZE
                if self.state[y][x] == HIDDEN:
                    pyxel.blt(px, py, 0, 0, 0, CELL_SIZE, CELL_SIZE)  # 閉じたマス
                elif self.state[y][x] == FLAGGED:
                    pyxel.blt(px, py, 0, CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)  # 旗
                elif self.board[y][x] == -1:
                    pyxel.blt(px, py, 0, CELL_SIZE * 2, 0, CELL_SIZE, CELL_SIZE)  # 地雷
                else:
                    num = self.board[y][x]
                    if num == 0:
                        pyxel.rect(px, py, CELL_SIZE, CELL_SIZE, 7)  # 空白
                    else:
                        pyxel.blt(px, py, 0, CELL_SIZE * (2 + num), 0, CELL_SIZE, CELL_SIZE)  # 数字

        if self.game_over:
            msg = "YOU WIN!" if self.win else "GAME OVER"
            pyxel.text(5, HEIGHT * CELL_SIZE // 2, msg, 10)

Minesweeper()


