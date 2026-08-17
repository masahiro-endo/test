
import pyxel as px
import random

import appconfig as gbl




CARD_WIDTH = 16
CARD_HEIGHT = 24
SUITS = ['♠', '♥', '♦', '♣']
# フォントを介さないと表示できない
# SUITS = [
#         "\u2660",   # ♠
#         "\u2665",   # ♥
#         "\u2666",   # ♦
#         "\u2663",   # ♣
#         ]
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']





class Card:
    def __init__(self, suit, rank, x, y):
        self.suit = suit
        self.rank = rank
        self.x = x
        self.y = y
        self.face_up = True

    def draw(self):
        # カード背景
        px.rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT, px.COLOR_WHITE if self.face_up else px.COLOR_NAVY)
        px.rectb(self.x, self.y, CARD_WIDTH, CARD_HEIGHT, px.COLOR_BLACK)
        if self.face_up:
            col = px.COLOR_BLACK
            if any(suit in self.suit for suit in ['♥', '♦']):
                col = px.COLOR_RED
            px.text(self.x + 2, self.y + 2, f"{self.suit}{self.rank}", col, gbl.BOF)


class Solitaire:
    def __init__(self):
        px.init(160, 120, title="px Solitaire")
        px.mouse(True)
        gbl.BOF = px.Font("k8x12S.bdf")

        self.cards = self.create_deck()
        self.selected_card = None
        px.run(self.update, self.draw)

    def create_deck(self):
        deck = [Card(s, r, 10 + i * 18, 10) for i, (s, r) in enumerate(
            [(s, r) for s in SUITS for r in RANKS]
        )]
        random.shuffle(deck)
        return deck[:5]  # 簡易表示用に5枚だけ

    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT):
            mx, my = px.mouse_x, px.mouse_y
            for card in self.cards:
                if card.x <= mx <= card.x + CARD_WIDTH and card.y <= my <= card.y + CARD_HEIGHT:
                    self.selected_card = card
                    break
        if px.btn(px.MOUSE_BUTTON_LEFT) and self.selected_card:
            self.selected_card.x = px.mouse_x - CARD_WIDTH // 2
            self.selected_card.y = px.mouse_y - CARD_HEIGHT // 2
        if not px.btn(px.MOUSE_BUTTON_LEFT):
            self.selected_card = None

    def draw(self):
        px.cls(3)
        for card in self.cards:
            card.draw()

if __name__ == "__main__":
    Solitaire()

