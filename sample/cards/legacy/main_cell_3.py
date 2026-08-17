
import pyxel
import random

CARD_W, CARD_H = 16, 24
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = list(range(1, 14))  # 1(A)〜13(K)

# カードの色（黒:♠♣, 赤:♥♦）
SUIT_COLOR = {"♠": 0, "♣": 0, "♥": 8, "♦": 8}


class Card:
    def __init__(self, suit, rank, x=0, y=0):
        self.suit = suit
        self.rank = rank
        self.x = x
        self.y = y
        self.drag = False

    def draw(self):
        pyxel.rect(self.x, self.y, CARD_W, CARD_H, 7)
        pyxel.text(self.x + 3, self.y + 4, str(self.rank), SUIT_COLOR[self.suit])
        pyxel.text(self.x + 3, self.y + 14, self.suit, SUIT_COLOR[self.suit])


class FreeCell:
    def __init__(self):
        pyxel.init(200, 160, title="FreeCell")
        pyxel.mouse(True)

        self.freecells = [None] * 4
        self.homecells = [[] for _ in range(4)]
        self.tableau = [[] for _ in range(8)]

        self.selected_card = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.setup_game()
        pyxel.run(self.update, self.draw)

    def setup_game(self):
        # 52枚のカード生成
        deck = [Card(s, r) for s in SUITS for r in RANKS]
        random.shuffle(deck)

        # 8列に配る
        for i, card in enumerate(deck):
            col = i % 8
            self.tableau[col].append(card)
            card.x = 10 + col * 22
            card.y = 40 + (len(self.tableau[col]) - 1) * 6

    def can_move_to_tableau(self, card, col):
        if not self.tableau[col]:
            return True
        top = self.tableau[col][-1]
        # 色が異なり、ランクが1小さい
        return SUIT_COLOR[card.suit] != SUIT_COLOR[top.suit] and card.rank == top.rank - 1

    def can_move_to_home(self, card, home_index):
        home = self.homecells[home_index]
        if not home:
            return card.rank == 1
        top = home[-1]
        return card.suit == top.suit and card.rank == top.rank + 1

    def update(self):
        # クリック開始
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for col in range(8):
                if self.tableau[col]:
                    top_card = self.tableau[col][-1]
                    if (top_card.x <= pyxel.mouse_x <= top_card.x + CARD_W and
                            top_card.y <= pyxel.mouse_y <= top_card.y + CARD_H):
                        self.selected_card = top_card
                        self.drag_offset_x = pyxel.mouse_x - top_card.x
                        self.drag_offset_y = pyxel.mouse_y - top_card.y
                        self.tableau[col].pop()
                        break

            # フリーセルから選択
            for i, cell in enumerate(self.freecells):
                if cell:
                    if (cell.x <= pyxel.mouse_x <= cell.x + CARD_W and
                            cell.y <= pyxel.mouse_y <= cell.y + CARD_H):
                        self.selected_card = cell
                        self.drag_offset_x = pyxel.mouse_x - cell.x
                        self.drag_offset_y = pyxel.mouse_y - cell.y
                        self.freecells[i] = None
                        break

        # ドラッグ中
        if self.selected_card:
            self.selected_card.x = pyxel.mouse_x - self.drag_offset_x
            self.selected_card.y = pyxel.mouse_y - self.drag_offset_y

        # ドロップ
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.selected_card:
            placed = False

            # テーブルに置く
            for col in range(8):
                if (10 + col * 22 <= pyxel.mouse_x <= 10 + col * 22 + CARD_W and
                        40 <= pyxel.mouse_y <= 140):
                    if self.can_move_to_tableau(self.selected_card, col):
                        self.tableau[col].append(self.selected_card)
                        placed = True
                    break

            # フリーセルに置く
            if not placed:
                for i in range(4):
                    fx = 10 + i * 22
                    fy = 10
                    if (fx <= pyxel.mouse_x <= fx + CARD_W and
                            fy <= pyxel.mouse_y <= fy + CARD_H):
                        if self.freecells[i] is None:
                            self.freecells[i] = self.selected_card
                            self.freecells[i].x = fx
                            self.freecells[i].y = fy
                            placed = True
                        break

            # ホームセルに置く
            if not placed:
                for i in range(4):
                    hx = 120 + i * 22
                    hy = 10
                    if (hx <= pyxel.mouse_x <= hx + CARD_W and
                            hy <= pyxel.mouse_y <= hy + CARD_H):
                        if self.can_move_to_home(self.selected_card, i):
                            self.homecells[i].append(self.selected_card)
                            self.selected_card.x = hx
                            self.selected_card.y = hy
                            placed = True
                        break

            # 置けなかったら元に戻す（適当にテーブルの一番左へ）
            if not placed:
                self.tableau[0].append(self.selected_card)

            self.selected_card = None

    def draw(self):
        pyxel.cls(3)

        # フリーセル枠
        for i in range(4):
            pyxel.rectb(10 + i * 22, 10, CARD_W, CARD_H, 7)
            if self.freecells[i]:
                self.freecells[i].draw()

        # ホームセル枠
        for i in range(4):
            pyxel.rectb(120 + i * 22, 10, CARD_W, CARD_H, 7)
            if self.homecells[i]:
                self.homecells[i][-1].draw()

        # テーブル
        for col in range(8):
            for idx, card in enumerate(self.tableau[col]):
                card.x = 10 + col * 22
                card.y = 40 + idx * 10
                card.draw()
        
        if self.selected_card:
            for idx, card in enumerate(self.selected_card):
                card.draw()



if __name__ == "__main__":
    FreeCell()


