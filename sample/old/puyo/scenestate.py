
import pyxel as px
from enum import Enum, auto

from constant import *
import appconfig as gbl
from basestate import *
from actor import *
from method import *





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

    def enter(self):
        self.parent.chain_count = 0

    def update(self):
        if px.btnp(px.KEY_LEFT) and not Meth.is_collision(-1, 0):
            gbl.puyo = [(x - 1, y, c) for x, y, c in gbl.puyo]
            Meth.overwrite_puyoc()
        if px.btnp(px.KEY_RIGHT) and not Meth.is_collision(1, 0):
            gbl.puyo = [(x + 1, y, c) for x, y, c in gbl.puyo]
            Meth.overwrite_puyoc()
        if px.btnp(px.KEY_Z):
            self.rotate_ccw()
        if px.btnp(px.KEY_X):
            self.rotate_cw()

        speed = 5 if px.btn(px.KEY_DOWN) else 20
        self.drop_timer += 1
        if self.drop_timer >= speed:
            self.drop_timer = 0
            if not Meth.is_collision(0, 1):
                gbl.puyo = [(x, y + 1, c) for x, y, c in gbl.puyo]
                Meth.overwrite_puyoc()
            else:
                self.lock_puyo()
                self.scene.Drop()

    def draw(self):
        # for x, y, col in gbl.puyo:
        #     px.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, col)
        for puyo in gbl.puyoc:
            puyo.draw()

    def lock_puyo(self):
        for i, pu in enumerate(gbl.puyo):
            x, y, col = pu
            if 0 <= y < ROWS:
                gbl.field[y][x] = col
                gbl.board[y][x] = gbl.puyoc[i]


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
        if not Meth.is_collision(0, 0, new_pos):
            gbl.puyo = new_pos
            Meth.overwrite_puyoc()
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
                gbl.board[y][x] = None
            self.scene.Drop()

    def draw(self):
        # 消去アニメ中は点滅
        # for pos in self.parent.clear_list:
        #     x, y = pos
        #     col  = gbl.field[y][x]
        #     if self.anim_timer % 4 < 2:
        #         col = px.COLOR_BLACK
        #     px.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, col)
            
        for pos in self.parent.clear_list:
            x, y = pos
            puyo  = gbl.board[y][x]
            imgid = PUYO_COLORS.index(puyo.color)
            if self.anim_timer % 4 < 2:
                imgid = len(PUYO_COLORS)            
            px.blt(puyo.x * CELL_SIZE, puyo.fy, 0, imgid * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

            


class SceneState_Drop(BaseState):
    def __init__(self, parent):
        self.state = STATE.DROP
        self.parent = parent.parent
        self.scene = parent

    def update(self):

        # 重力処理
        for x in range(COLS):
            # １列ずつ、上から下に向かって舐めていき、
            # ゼロ以外なら、セル色をstack
            # 0  ↓  stack内部 = 4,1
            # 4 
            # 0
            # 1
            #---------------------
            stack   = [gbl.field[y][x] for y in range(ROWS) if gbl.field[y][x] != 0]
            stackbg = [gbl.board[y][x] for y in range(ROWS) if gbl.board[y][x]]
            # 底から上に向かってstackの末尾からpop()
            # stack内部 = 4,1 → 0   行末から上に向かって、stack最後尾からpop()していく。
            #                   4
            #                   1 ↑
            #----------------------
            for y in range(ROWS - 1, -1, -1):
                if stack:
                    gbl.field[y][x] = stack.pop()
                    gbl.board[y][x] = stackbg.pop()
                    if gbl.board[y][x].y != y: # debug
                        gbl.board[y][x].y = y
                else:
                    gbl.field[y][x] = 0
                    gbl.board[y][x] = None


        drop = Meth.board_is_droping()
        if drop:
            for puyo in drop:
                puyo.update()
        else:
        # 次の連鎖判定
            self.parent.check_and_clear()
            

    def draw(self):
        pass


