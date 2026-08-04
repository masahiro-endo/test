
import pyxel as px
import random

from constant import *
import appconfig as gbl
from scenestate import SceneStates








class PuyoPuyo:
    def __init__(self):
        px.init(WIDTH, HEIGHT, title="Puyo Demo")
        self.reset()
        self.state = SceneStates(self)
        px.run(self.update, self.draw)

    def reset(self):
        gbl.field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        gbl.puyos = []
        self.spawn_puyo()
        self.game_over = False
        self.state = SceneStates(self)
        self.chain_count = 0
        self.clear_list = []

    def spawn_puyo(self):
        color1 = random.choice(PUYO_COLORS)
        color2 = random.choice(PUYO_COLORS)
        # gbl.puyo = [(COLS // 2, 0, color1), (COLS // 2, 1, color2)]
        gbl.puyo = [(COLS // 2, 0, color1), (COLS // 2, CELL_SIZE, color2)]
        if self.is_collision(0, 0):
            self.game_over = True

    def puyopile(self, x, y):
        stack = [gbl.field[y][x] for y in range(y, ROWS) if gbl.field[y][x] != 0]
        return len(stack) * CELL_SIZE


    def update(self):
        if self.game_over:
            if px.btnp(px.KEY_R):
                self.reset()
            return

        self.state.update()




    def is_collision(self, dx, dy, puyo_list=None):
        if puyo_list is None:
            puyo_list = gbl.puyo
        for x, y, _ in puyo_list:
            nx, ny = x + dx, y + dy * CELL_SIZE # yだけ * CELL_SIZE
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return True
            if ny >= 0 and gbl.field[ny][nx] != 0:
                return True
        return False


    # 「同色４つ以上」グループの探索
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
                if visited[cy][cx] or gbl.field[cy][cx] != color:
                    continue
                visited[cy][cx] = True
                group.append((cx, cy))
                stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
            return group

        for y in range(ROWS):
            for x in range(COLS):
                if gbl.field[y][x] != 0 and not visited[y][x]:
                    group = dfs(x, y, gbl.field[y][x])
                    if len(group) >= 4:
                        to_clear.extend(group)

        if to_clear:
            self.clear_list = to_clear
            self.state.Clear()
            self.chain_count += 1
        else:
            if self.chain_count > 0:
                print(f"{self.chain_count} 連鎖!")
            self.spawn_puyo()
            self.state.Play()


    def draw(self):
        px.cls(0)
        # フィールド描画
        for y in range(ROWS):
            for x in range(COLS):
                if gbl.field[y][x] != 0:
                    px.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, gbl.field[y][x])

        self.state.draw()

        # ゲームオーバー表示
        if self.game_over:
            px.text(WIDTH // 2 - 16, HEIGHT // 2, "GAME OVER", 7)
            px.text(WIDTH // 2 - 20, HEIGHT // 2 + 10, "Press R to Restart", 7)

        # 連鎖数表示
        if self.chain_count > 0:
            px.text(2, 2, f"{self.chain_count} RENSA!", 7)




if __name__ == "__main__":
    PuyoPuyo()



