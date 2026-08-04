
import pyxel
import random



# ゲーム設定
WIDTH, HEIGHT = 80, 120
CELL_SIZE = 8
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
PUYO_COLORS = [8, 10, 11, 12]  # 赤, 緑, 青, 黄




class PuyoPuyo:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="PuyoPuyo Chain Demo")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.spawn_puyo()
        self.game_over = False
        self.drop_timer = 0
        self.state = "play"  # play, clear_anim, drop_anim
        self.clear_list = []
        self.anim_timer = 0
        self.chain_count = 0

    def spawn_puyo(self):
        self.puyo = [(COLS // 2, 0), (COLS // 2, 1)]
        self.color = random.choice(PUYO_COLORS)
        if any(self.field[y][x] != 0 for x, y in self.puyo):
            self.game_over = True

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        if self.state == "play":
            self.update_play()
        elif self.state == "clear_anim":
            self.update_clear_anim()
        elif self.state == "drop_anim":
            self.update_drop_anim()

    def update_play(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.move(-1)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.move(1)
        if pyxel.btnp(pyxel.KEY_UP):
            self.rotate()

        speed = 5 if pyxel.btn(pyxel.KEY_DOWN) else 20
        self.drop_timer += 1
        if self.drop_timer >= speed:
            self.drop_timer = 0
            if not self.move_down():
                self.lock_puyo()
                self.chain_count = 0
                self.check_and_clear()

    def update_clear_anim(self):
        self.anim_timer += 1
        if self.anim_timer > 10:  # 消えるまでの時間
            for x, y in self.clear_list:
                self.field[y][x] = 0
            self.state = "drop_anim"
            self.anim_timer = 0

    def update_drop_anim(self):
        # 重力処理
        for x in range(COLS):
            stack = [self.field[y][x] for y in range(ROWS) if self.field[y][x] != 0]
            for y in range(ROWS - 1, -1, -1):
                self.field[y][x] = stack.pop() if stack else 0
        # 次の連鎖判定
        self.check_and_clear()

    def move(self, dx):
        if all(0 <= x + dx < COLS and self.field[y][x + dx] == 0 for x, y in self.puyo):
            self.puyo = [(x + dx, y) for x, y in self.puyo]

    def rotate(self):
        pivot = self.puyo[0]
        other = self.puyo[1]
        ox, oy = other[0] - pivot[0], other[1] - pivot[1]
        nx, ny = -oy, ox
        new_pos = (pivot[0] + nx, pivot[1] + ny)
        if 0 <= new_pos[0] < COLS and 0 <= new_pos[1] < ROWS and self.field[new_pos[1]][new_pos[0]] == 0:
            self.puyo[1] = new_pos

    def move_down(self):
        if all(y + 1 < ROWS and self.field[y + 1][x] == 0 for x, y in self.puyo):
            self.puyo = [(x, y + 1) for x, y in self.puyo]
            return True
        return False

    def lock_puyo(self):
        for x, y in self.puyo:
            if 0 <= y < ROWS:
                self.field[y][x] = self.color

    def check_and_clear(self):
        visited = [[False] * COLS for _ in range(ROWS)]
        to_clear = []

        def dfs(x, y, color):
            stack = [(x, y)]
            group = []
            while stack:
                cx, cy = stack.pop()
                if not (0 <= cx < COLS and 0 <= cy < ROWS):
                    continue
                if visited[cy][cx] or self.field[cy][cx] != color:
                    continue
                visited[cy][cx] = True
                group.append((cx, cy))
                stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
            return group

        for y in range(ROWS):
            for x in range(COLS):
                if self.field[y][x] != 0 and not visited[y][x]:
                    group = dfs(x, y, self.field[y][x])
                    if len(group) >= 4:
                        to_clear.extend(group)

        if to_clear:
            self.clear_list = to_clear
            self.state = "clear_anim"
            self.anim_timer = 0
            self.chain_count += 1
        else:
            if self.chain_count > 0:
                print(f"{self.chain_count} 連鎖!")
            self.spawn_puyo()
            self.state = "play"

    def draw(self):
        pyxel.cls(0)
        # フィールド描画
        for y in range(ROWS):
            for x in range(COLS):
                if self.field[y][x] != 0:
                    # 消去アニメ中は点滅
                    if self.state == "clear_anim" and (x, y) in self.clear_list:
                        if self.anim_timer % 4 < 2:
                            continue
                    pyxel.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, self.field[y][x])
        # 操作中ぷよ
        if self.state == "play":
            for x, y in self.puyo:
                pyxel.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, self.color)
        # ゲームオーバー表示
        if self.game_over:
            pyxel.text(WIDTH // 2 - 16, HEIGHT // 2, "GAME OVER", 7)
            pyxel.text(WIDTH // 2 - 20, HEIGHT // 2 + 10, "Press R to Restart", 7)

        # 連鎖数表示
        if self.chain_count > 0 and self.state != "play":
            pyxel.text(2, 2, f"{self.chain_count} RENSA!", 7)

if __name__ == "__main__":
    PuyoPuyo()


