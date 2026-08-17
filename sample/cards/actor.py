
import appconfig as gbl
from context import *







class Card:
    def __init__(self, suit, rank, x=0, y=0):
        self.suit = suit
        self.rank = rank
        self.x = x
        self.y = y
        # self.drag = False
        self.color = SUIT_COLOR[self.suit]

    def draw(self):
        px.rect(self.x, self.y, CARD_W, CARD_H, px.COLOR_WHITE)
        px.rectb(self.x, self.y, CARD_W, CARD_H, px.COLOR_BLACK)
        px.text(self.x + 2, self.y + 2, str(self.rank), self.color)
        px.text(self.x + 7, self.y + 3, self.suit, self.color, gbl.BOF)

    def is_mouse_over(self):
        mx, my = px.mouse_x, px.mouse_y
        if (self.x <= mx <= self.x + CARD_W and
            self.y <= my <= self.y + CARD_H):
            return True
        return False




class PlayArea:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_mouse_over(self):
        mx, my = px.mouse_x, px.mouse_y
        if (self.x <= mx <= self.x + CARD_W and
            self.y <= my <= self.y + CARD_H):
            return True
        return False



