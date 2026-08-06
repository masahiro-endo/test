
import random
import uuid

from constant import *
from method import *








class Puyo:

    def __init__(self, parent, puyo=None):
        self.parent = parent
        self.color = random.choice(PUYO_COLORS)
        self.x = COLS // 2
        self.y_b = 0 # borad上の座標
        if puyo:
            x, y, col = puyo
            self.x, self.y_b, self.color = x, y, col
        # borad配列の位置番号の他に、落下描画用の変数を用意
        self.fy = self.y_b * CELL_SIZE
        self.vy = 0
        self.uuid = str(uuid.uuid4())
        self.is_droping = False

    def update(self):
        self.vy += GRAVITY
        self.fy += self.vy

        ptop = (self.y_b * CELL_SIZE)
        if self.fy >= ptop:
            self.fy = ptop
            self.is_droping = False


    def draw(self):
        # px.rect(self.x * CELL_SIZE, self.fy, CELL_SIZE, CELL_SIZE, self.color)
        px.blt(self.x * CELL_SIZE, self.fy, 0, PUYO_COLORS.index(self.color) * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)


    # 内部変数「_y」と、プロパティ名「y」を
    # 一致させてしまうと無限再帰
    @property
    def y(self):
        return self.y_b
    @y.setter
    def y(self, value):
        if value != self.y_b:
            self.y_b = value
            self.is_droping = True

