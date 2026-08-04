
import pyxel as px
from enum import Enum, auto

from constant import *
import appconfig as gbl
from basestate import *
from actor import *






class STATE(Enum):
    PLAY = auto()
    CLEAR = auto()
    DROP = auto()







class SceneStates(BaseContext):
    def __init__(self, parent):
        self.parent = parent
        self.table = {
            STATE.PLAY  : SceneState_Play(self),
            STATE.CLEAR : SceneState_Clear(self),
            STATE.DROP  : SceneState_Drop(self),
        }
        self.changeState(STATE.PLAY)

    def update(self):
        self.currentState.update()
    def draw(self):
        self.currentState.draw()

    def Play(self):
        self.changeState(STATE.PLAY)
    def Clear(self):
        self.changeState(STATE.CLEAR)
    def Drop(self):
        self.changeState(STATE.DROP)









class SceneState_Play(BaseState):
    def __init__(self, parent):
        self.state = STATE.PLAY
        self.parent = parent.parent
        self.scene = parent
        self.drop_timer = 0

    def update(self):
        if px.btnp(px.KEY_LEFT) and not self.parent.is_collision(-1, 0):
            gbl.puyo = [(x - 1, y, c) for x, y, c in gbl.puyo]
        if px.btnp(px.KEY_RIGHT) and not self.parent.is_collision(1, 0):
            gbl.puyo = [(x + 1, y, c) for x, y, c in gbl.puyo]
        if px.btnp(px.KEY_Z):
            self.rotate_ccw()
        if px.btnp(px.KEY_X):
            self.rotate_cw()

        speed = 5 if px.btn(px.KEY_DOWN) else 20
        self.drop_timer += 1
        if self.drop_timer >= speed:
            self.drop_timer = 0
            if not self.parent.is_collision(0, 1):
                gbl.puyo = [(x, y + 1, c) for x, y, c in gbl.puyo]
            else:
                self.lock_puyo()
                self.scene.Drop()

    def draw(self):
        for x, y, col in gbl.puyo:
            px.rect(x * CELL_SIZE, y, CELL_SIZE, CELL_SIZE, col)


    def lock_puyo(self):
        for x, y, col in gbl.puyo:
            if 0 <= y < ROWS:
                gbl.field[y][x] = col
                gbl.puyos.append(Puyo(col))


    #反時計回り
    def rotate_ccw(self, ccw=True):
        cx, cy, ccol = gbl.puyo[0] #pivot
        ox, oy, ocol = gbl.puyo[1] #other
        dx, dy = ox - cx, oy - cy
        if ccw:
            ndx, ndy = dy, -dx
        else:
            ndx, ndy = -dy, dx
        new_pos = [(cx, cy, ccol), (cx + ndx, cy + ndy, ocol)] #pivotの座標は変わってない。
        if not self.parent.is_collision(0, 0, new_pos):
            gbl.puyo = new_pos
    #時計回り
    def rotate_cw(self):
        self.rotate_ccw(False)







class SceneState_Clear(BaseState):
    def __init__(self, parent):
        self.state = STATE.CLEAR
        self.parent = parent.parent
        self.scene = parent
        self.anim_timer = 0

    def enter(self):
        self.anim_timer = 0

    def update(self):
        self.anim_timer += 1
        if self.anim_timer > 10:  # 消えるまでの時間
            for x, y in self.parent.clear_list:
                gbl.field[y][x] = 0
            self.scene.Drop()

    def draw(self):
        # 消去アニメ中は点滅
        for pos in self.parent.clear_list:
            x, y = pos
            col  = gbl.field[y][x]
            if self.anim_timer % 4 < 2:
                col = px.COLOR_BLACK
            px.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, col)
            

            


class SceneState_Drop(BaseState):
    def __init__(self, parent):
        self.state = STATE.DROP
        self.parent = parent.parent
        self.scene = parent

    def update(self):
        for puyo in [p for p in gbl.puyos if p.is_moving]:
            puyo.update()

        # 重力処理
        for x in range(COLS):
            # １列ずつ、上から下に向かって舐めていき、
            # ゼロ以外なら、セル色をstack
            # 0  ↓  stack内部 = 4,1
            # 4 
            # 0
            # 1
            #---------------------
            stack = [gbl.field[y][x] for y in range(ROWS) if gbl.field[y][x] != 0]
            # 底から上に向かってstackの末尾からpop()
            # stack内部 = 4,1 → 0   行末から上に向かって、stack最後尾からpop()していく。
            #                   4
            #                   1 ↑
            #----------------------
            for y in range(ROWS - 1, -1, -1):
                if stack:
                    gbl.field[y][x] = stack.pop()
                else:
                    gbl.field[y][x] = 0

        # 次の連鎖判定
        self.parent.check_and_clear()

    def update_drop_anim_gravity(board):
        for col in range(COLS):
            # 下から順に空白を探し、上のぷよを落とす
            for row in range(ROWS - 1, -1, -1):
                if not board[row][col]:
                    # 上方向にぷよを探す
                    for above in range(row - 1, -1, -1):
                        if board[above][col]:
                            board[row][col] = board[above][col]
                            board[above][col] = None
                            break

    def draw(self):
        for puyo in [p for p in gbl.puyos if p.is_moving]:
            puyo.draw()



