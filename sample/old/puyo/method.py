
import appconfig as gbl
from constant import *








class Meth:
    
    @staticmethod
    def overwrite_puyoc():
            for i, pu in enumerate(gbl.puyo):
                x, y, col = pu
                gbl.puyoc[i].x = x
                gbl.puyoc[i].y = y
                gbl.puyoc[i].fy = y * CELL_SIZE
                gbl.puyoc[i].color = col

    @staticmethod
    def board_is_droping():
        drop = []
        for x in range(COLS):
            stack = [gbl.board[y][x] for y in range(ROWS) if gbl.board[y][x]]
            drop.extend([puyo for puyo in stack if puyo.is_droping])
        return drop

    @staticmethod
    def is_collision(dx, dy, puyo_list=None):
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
    @staticmethod
    def find_4puyos_toclear():
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
