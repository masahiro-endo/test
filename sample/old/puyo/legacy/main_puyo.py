
import pyxel
import random
from collections import deque

# ゲーム設定
WIDTH, HEIGHT = 80, 120
CELL_SIZE = 8
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

PUYO_COLORS = [8, 10, 12, 14]  # 赤, 緑, 青, 黄






class PuyoPuyo:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="PuyoPuyo Clone")
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.spawn_puyo()
        self.drop_timer = 0
        self.chain_count = 0
        self.state = "play"  # play, clear, drop
        self.clear_timer = 0

    def spawn_puyo(self):
        color1 = random.choice(PUYO_COLORS)
        color2 = random.choice(PUYO_COLORS)
        self.puyo = [(COLS // 2, 0, color1), (COLS // 2, 1, color2)]
        self.rotation = 0

    def can_move(self, dx, dy, puyo_list=None):
        if puyo_list is None:
            puyo_list = self.puyo
        for x, y, _ in puyo_list:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return False
            if ny >= 0 and self.field[ny][nx] != 0:
                return False
        return True

    def rotate(self):
        cx, cy, ccol = self.puyo[0]
        ox, oy, ocol = self.puyo[1]
        dx, dy = ox - cx, oy - cy
        ndx, ndy = -dy, dx
        new_pos = [(cx, cy, ccol), (cx + ndx, cy + ndy, ocol)]
        if self.can_move(0, 0, new_pos):
            self.puyo = new_pos

    def fix_puyo(self):
        for x, y, col in self.puyo:
            if 0 <= y < ROWS:
                self.field[y][x] = col
        self.state = "clear"
        self.clear_timer = 0

    def find_groups(self):
        visited = [[False] * COLS for _ in range(ROWS)]
        groups = []
        for y in range(ROWS):
            for x in range(COLS):
                if self.field[y][x] != 0 and not visited[y][x]:
                    color = self.field[y][x]
                    # BFSで連結成分探索
                    q = deque([(x, y)])
                    group = []
                    visited[y][x] = True
                    while q:
                        cx, cy = q.popleft()
                        group.append((cx, cy))
                        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < COLS and 0 <= ny < ROWS:
                                if not visited[ny][nx] and self.field[ny][nx] == color:
                                    visited[ny][nx] = True
                                    q.append((nx, ny))
                    if len(group) >= 4:
                        groups.append(group)
        return groups

    def clear_groups(self, groups):
        for group in groups:
            for x, y in group:
                self.field[y][x] = 0

    def drop_field(self):
        for x in range(COLS):
            stack = [self.field[y][x] for y in range(ROWS) if self.field[y][x] != 0]
            for y in range(ROWS - 1, -1, -1):
                self.field[y][x] = stack.pop() if stack else 0

    def update(self):
        if self.state == "play":
            if pyxel.btnp(pyxel.KEY_LEFT) and self.can_move(-1, 0):
                self.puyo = [(x - 1, y, c) for x, y, c in self.puyo]
            if pyxel.btnp(pyxel.KEY_RIGHT) and self.can_move(1, 0):
                self.puyo = [(x + 1, y, c) for x, y, c in self.puyo]
            if pyxel.btnp(pyxel.KEY_UP):
                self.rotate()

            speed = 5 if pyxel.btn(pyxel.KEY_DOWN) else 20
            self.drop_timer += 1
            if self.drop_timer >= speed:
                self.drop_timer = 0
                if self.can_move(0, 1):
                    self.puyo = [(x, y + 1, c) for x, y, c in self.puyo]
                else:
                    self.fix_puyo()

        elif self.state == "clear":
            if self.clear_timer == 0:
                groups = self.find_groups()
                if groups:
                    self.clear_groups(groups)
                    self.chain_count += 1
                else:
                    self.chain_count = 0
                    self.spawn_puyo()
                    self.state = "play"
            self.clear_timer += 1
            if self.clear_timer > 10:
                self.state = "drop"
                self.clear_timer = 0

        elif self.state == "drop":
            self.drop_field()
            self.state = "clear"

    def draw(self):
        pyxel.cls(0)
        # フィールド
        for y in range(ROWS):
            for x in range(COLS):
                if self.field[y][x] != 0:
                    pyxel.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, self.field[y][x])
        # 操作中ぷよ
        if self.state == "play":
            for x, y, col in self.puyo:
                if y >= 0:
                    pyxel.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, col)
        # 連鎖数表示
        if self.chain_count > 0:
            pyxel.text(2, 2, f"{self.chain_count} RENSA!", 7)




if __name__ == "__main__":
    PuyoPuyo()


