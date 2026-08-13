
import pyxel as px
import random


WIDTH, HEIGHT = 160, 120
CELL_SIZE = 8
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

NUM_MINES = 30

HIDDEN = 0
REVEALED = 1
FLAGGED = 2






class ViewModel:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.grid = [[{"mine": False, "state": HIDDEN, "count": 0} for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False
        self.win = False

        # Place mines
        mines = set()
        while len(mines) < NUM_MINES:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            mines.add((x, y))
        for (mx, my) in mines:
            self.grid[my][mx]["mine"] = True

        # Count adjacent mines
        for y in range(ROWS):
            for x in range(COLS):
                if not self.grid[y][x]["mine"]:
                    self.grid[y][x]["count"] = self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x, y):
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    if self.grid[ny][nx]["mine"]:
                        count += 1
        return count

    def reveal_cell(self, x, y):
        if self.grid[y][x]["state"] != HIDDEN:
            return
        self.grid[y][x]["state"] = REVEALED
        if self.grid[y][x]["mine"]:
            self.game_over = True
            return
        if self.grid[y][x]["count"] == 0:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        self.reveal_cell(nx, ny)

    # フラグの上げ下げ
    def toggle_flag(self, x, y):
        if self.grid[y][x]["state"] == HIDDEN:
            self.grid[y][x]["state"] = FLAGGED
        elif self.grid[y][x]["state"] == FLAGGED:
            self.grid[y][x]["state"] = HIDDEN

    def check_win(self):
        for y in range(ROWS):
            for x in range(COLS):
                cell = self.grid[y][x]
                if not cell["mine"] and cell["state"] != REVEALED:
                    return False
        return True

    def update(self):
        if self.game_over or self.win:
            if px.btnp(px.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

        if px.btnp(px.MOUSE_BUTTON_LEFT):
            mx, my = px.mouse_x // CELL_SIZE, px.mouse_y // CELL_SIZE
            if 0 <= mx < COLS and 0 <= my < ROWS:
                self.reveal_cell(mx, my)
                if not self.game_over:
                    self.win = self.check_win()

        if px.btnp(px.MOUSE_BUTTON_RIGHT):
            mx, my = px.mouse_x // CELL_SIZE, px.mouse_y // CELL_SIZE
            if 0 <= mx < COLS and 0 <= my < ROWS:
                self.toggle_flag(mx, my)


class AppView:
    def __init__(self, ViewModel):
        self.vm = ViewModel

        px.init(WIDTH, HEIGHT, capture_scale=1, title="px Minesweeper")
        px.load("assets_mine.pyxres")  # Load sprites
        px.mouse(True)
        px.run(self.update, self.draw)

    def update(self):
        self.vm.update()

    def draw(self):
        px.cls(px.COLOR_BLACK)
        for y in range(ROWS):
            for x in range(COLS):
                cell = self.vm.grid[y][x]
                sx, sy = x * CELL_SIZE, y * CELL_SIZE

                if cell["state"] == HIDDEN:
                    px.blt(sx, sy, 0, 72, 0, CELL_SIZE, CELL_SIZE, 0)
                elif cell["state"] == FLAGGED:
                    px.blt(sx, sy, 0, 80, 0, CELL_SIZE, CELL_SIZE, 0)
                elif cell["mine"]:
                    px.blt(sx, sy, 0, 88, 0, CELL_SIZE, CELL_SIZE, 0)
                else:
                    px.blt(sx, sy, 0,  cell["count"] * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE, 0)

        if self.vm.game_over:
            px.text(5, ROWS * CELL_SIZE // 2, "GAME OVER - Click to restart", 8)
        elif self.vm.win:
            px.text(5, ROWS * CELL_SIZE // 2, "YOU WIN! - Click to restart", 11)




if __name__ == "__main__":
    vm = ViewModel()
    AppView(vm)


