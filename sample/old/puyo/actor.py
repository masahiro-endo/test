
import random
import uuid

from constant import *
import appconfig as gbl







class Puyo:

    def __init__(self, parent, puyo=None):
        self.parent = parent
        self.color = random.choice(PUYO_COLORS)
        self.x = COLS // 2
        self.y = 0
        if puyo:
            x, y, col = puyo
            self.x, self.y, self.color = x, y, col
        # フィールド配列の位置番号の他に、落下描画用の変数を用意
        self.fy = self.y * CELL_SIZE
        self.vy = 0
        self.uuid = str(uuid.uuid4())
        self.is_moving = False

    def update(self):
        self.is_moving = True
        self.vy += GRAVITY
        self.fy += self.vy
        pile = self.parent.puyopile(self.x, self.fy // CELL_SIZE) * CELL_SIZE

        if self.fy + CELL_SIZE >= HEIGHT - pile:
            self.fy = HEIGHT - pile
            self.is_moving = False
            
    def draw(self):
        # rad = CELL_SIZE // 2
        # px.circ(self.x * CELL_SIZE + rad, self.y + rad, rad, self.color)
        px.rect(self.x * CELL_SIZE, self.fy, CELL_SIZE, CELL_SIZE, self.color)

