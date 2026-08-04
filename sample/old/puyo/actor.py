
import random
import uuid

from constant import *
import appconfig as gbl







class Puyo:

    def __init__(self, col=None):
        self.color = col if col else random.choice(PUYO_COLORS)
        self.x = COLS // 2
        self.y = 0
        self.vy = 0
        self.uuid = str(uuid.uuid4())
        self.is_moving = False

    def update(self):
        self.is_moving = True
        self.vy += GRAVITY
        self.y += self.vy
        pile = self.parent.puyopile(self.x, self.y)

        if self.y + CELL_SIZE >= HEIGHT - pile:
            self.y = HEIGHT - pile - CELL_SIZE
            self.is_moving = False
            
    def draw(self):
        px.circ(self.x, self.y, CELL_SIZE // 2, self.color)

