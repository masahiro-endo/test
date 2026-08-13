# Image Bank 0:
# Tile size: 16x16
# At coordinates (0,0) → hidden cell sprite
# (16,0) → revealed empty cell
# (32,0) → flag
# (48,0) → mine
# (0,16) to (128,16) → numbers 1–8 (each 16×16)
# Save as minesweeper.pyxres.

import pyxel
import random

GRID_W = 10
GRID_H = 10
NUM_MINES = 15
CELL_SIZE = 16

HIDDEN = 0
REVEALED = 1
FLAGGED = 2

class Minesweeper:
    def __init__(self):
        pyxel.init(GRID_W * CELL_SIZE, GRID_H * CELL_SIZE, title="Pyxel Minesweeper")
        pyxel.load("minesweeper.pyxres")  # Load sprites
        pyxel.mouse(True)

        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.grid = [[{"mine": False, "state": HIDDEN, "count": 0} for _ in range(GRID_W)] for _ in range(GRID_H)]
        self.game_over = False
        self.win = False

        # Place mines
        mines = set()
        while len(mines) < NUM_MINES:
            x = random.randint(0, GRID_W - 1)
            y = random.randint(0, GRID_H - 1)
            mines.add((x, y))
        for (mx, my) in mines:
            self.grid[my][mx]["mine"] = True

        # Count adjacent mines
        for y in range(GRID_H):
            for x in range(GRID_W):
                if not self.grid[y][x]["mine"]:
                    self.grid[y][x]["count"] = self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x, y):
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
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
                    if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
                        self.reveal_cell(nx, ny)

    def toggle_flag(self, x, y):
        if self.grid[y][x]["state"] == HIDDEN:
            self.grid[y][x]["state"] = FLAGGED
        elif self.grid[y][x]["state"] == FLAGGED:
            self.grid[y][x]["state"] = HIDDEN

    def check_win(self):
        for y in range(GRID_H):
            for x in range(GRID_W):
                cell = self.grid[y][x]
                if not cell["mine"] and cell["state"] != REVEALED:
                    return False
        return True

    def update(self):
        if self.game_over or self.win:
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                self.reset_game()
            return

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            mx, my = pyxel.mouse_x // CELL_SIZE, pyxel.mouse_y // CELL_SIZE
            if 0 <= mx < GRID_W and 0 <= my < GRID_H:
                self.reveal_cell(mx, my)
                if not self.game_over:
                    self.win = self.check_win()

        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
            mx, my = pyxel.mouse_x // CELL_SIZE, pyxel.mouse_y // CELL_SIZE
            if 0 <= mx < GRID_W and 0 <= my < GRID_H:
                self.toggle_flag(mx, my)

    def draw(self):
        pyxel.cls(0)
        for y in range(GRID_H):
            for x in range(GRID_W):
                cell = self.grid[y][x]
                px, py = x * CELL_SIZE, y * CELL_SIZE

                if cell["state"] == HIDDEN:
                    pyxel.blt(px, py, 0, 0, 0, CELL_SIZE, CELL_SIZE, 0)
                elif cell["state"] == FLAGGED:
                    pyxel.blt(px, py, 0, 32, 0, CELL_SIZE, CELL_SIZE, 0)
                elif cell["mine"]:
                    pyxel.blt(px, py, 0, 48, 0, CELL_SIZE, CELL_SIZE, 0)
                else:
                    pyxel.blt(px, py, 0, 16, 0, CELL_SIZE, CELL_SIZE, 0)
                    if cell["count"] > 0:
                        pyxel.blt(px, py, 0, (cell["count"] - 1) * 16, 16, CELL_SIZE, CELL_SIZE, 0)

        if self.game_over:
            pyxel.text(5, GRID_H * CELL_SIZE // 2, "GAME OVER - Click to restart", 8)
        elif self.win:
            pyxel.text(5, GRID_H * CELL_SIZE // 2, "YOU WIN! - Click to restart", 11)

if __name__ == "__main__":
    Minesweeper()


