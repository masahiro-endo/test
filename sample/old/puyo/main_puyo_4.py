
import pyxel as px
import random

from constant import *
import appconfig as gbl
from scenestate import SceneStates









class ViewModel:
    def __init__(self):
        self.reset()

    def reset(self):
        gbl.field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        gbl.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        gbl.puyos = []
        self.spawn_puyo()
        self.game_over = False
        self.state = SceneStates(self)
        self.chain_count = 0
        self.clear_list = []

    def spawn_puyo(self):
        color1 = random.choice(PUYO_COLORS)
        color2 = random.choice(PUYO_COLORS)
        gbl.puyo = [(COLS // 2, 0, color1), (COLS // 2, 1, color2)]
        if self.is_collision(0, 0):
            self.game_over = True

    # 指定座標より下に、ぷよが何個存在するか
    def puyopile(self, x, y):
        stack = [gbl.field[y][x] for y in range(int(y), ROWS) if gbl.field[y][x] != 0]
        return len(stack)


    def update(self):
        if self.game_over:
            if px.btnp(px.KEY_R):
                self.reset()
            return

        self.state.update()

    def update_board(self):
        for y in range(ROWS):
            for x in range(COLS):
                if gbl.board[y][x]:
                    gbl.board[y][x].update()



    def is_collision(self, dx, dy, puyo_list=None):
        if puyo_list is None:
            puyo_list = gbl.puyo
        for x, y, _ in puyo_list:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return True
            if ny >= 0 and gbl.field[ny][nx] != 0:
                return True
        return False


    # 「同色４つ以上」グループの探索
    def find_4puyos_toclear(self):
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
        return to_clear


    def check_and_clear(self):

        to_clear = self.find_4puyos_toclear()
        if to_clear:
            self.clear_list = to_clear
            self.state.Clear()
            self.chain_count += 1
        else:
            if self.chain_count > 0:
                print(f"{self.chain_count} 連鎖!")
            move = [p for p in gbl.puyos if p.is_moving]
            if move:
                return
            self.spawn_puyo()
            self.state.Play()

    def board_is_moving(self):
        for y in range(ROWS):
            for x in range(COLS):
                if gbl.board[y][x]:
                    gbl.board[y][x].draw()



class AppView:
    def __init__(self, ViewModel):
        self.vm = ViewModel

        px.init(WIDTH, HEIGHT, title="Puyo Demo")
        self.reset()
        self.state = SceneStates(self)
        px.run(self.update, self.draw)

    def update(self):
        self.vm.update()

    def draw(self):
        px.cls(0)
        # フィールド描画
        for y in range(ROWS):
            for x in range(COLS):
                if gbl.field[y][x] != 0:
                    px.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, gbl.field[y][x])

        self.state.draw()
        self.draw_board()

        # ゲームオーバー表示
        if self.game_over:
            px.text(WIDTH // 2 - 16, HEIGHT // 2, "GAME OVER", 7)
            px.text(WIDTH // 2 - 20, HEIGHT // 2 + 10, "Press R to Restart", 7)

        # 連鎖数表示
        if self.chain_count > 0:
            px.text(2, 2, f"{self.chain_count} RENSA!", 7)

    def draw_board(self):
        for y in range(ROWS):
            for x in range(COLS):
                if gbl.board[y][x]:
                    gbl.board[y][x].draw()





if __name__ == "__main__":
    vm = ViewModel()
    AppView(vm)



