
import pyxel as px 
import random

import appconfig as gbl





CARD_W, CARD_H = 16, 24
NUM_TABLEAU = 8
NUM_FREECELLS = 4
NUM_HOMECELLS = 4
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUIT_COLOR = {'♠': px.COLOR_BLACK,
              '♣': px.COLOR_BLACK,
              '♥': px.COLOR_RED,
              '♦': px.COLOR_RED,
              }




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


class FreeCell:
    def __init__(self):
        px.init(180, 160, title="FreeCell", fps=30)
        px.mouse(True)
        gbl.BOF = px.Font("k8x12S.bdf")

        self.columns = [[] for _ in range(NUM_TABLEAU)]
        self.freecells = [None] * NUM_FREECELLS
        self.homecells = [[] for _ in range(NUM_HOMECELLS)]

        self.drag_stack = []
        self.drag_from = None
        self.drag_offset = (0, 0)

        self._new_game()
        px.run(self.update, self.draw)

    def _new_game(self):
        deck = [Card(s, r) for s in SUITS for r in RANKS]
        random.shuffle(deck)
        for ci, card in enumerate(deck):
            col = ci % NUM_TABLEAU
            self.columns[col].append(card)
            card.x = col * (CARD_W + 2)
            card.y = 30 + (len(self.columns[col]) - 1) * 15


    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT):
            self._pick_cards()
        elif px.btnr(px.MOUSE_BUTTON_LEFT):
            self._drop_cards()


    def _find_card_at(self, mx, my):
        # マウス位置からカードとそのカラムを探す
        for ci, col in enumerate(self.columns):
            for ri in reversed(range(len(col))):
                c = col[ri]
                if (c.x <= mx <= c.x + CARD_W and
                    c.y <= my <= c.y + CARD_H):
                    return ci, ri
        return None, None

    def _get_movable_stack(self, ci, ri):
        # 選択したカードから下の連続ランクカードをまとめて取得
        col = self.columns[ci]
        stack = col[ri:]
        # 連続性チェック（降順かつ色交互）
        for i in range(len(stack) - 1):
            if RANKS.index(stack[i].rank) != RANKS.index(stack[i+1].rank) + 1:
                return [stack[0]]  # 連続していない場合は1枚だけ
            if stack[i].color == stack[i+1].color:
                return [stack[0]]
        return stack
    
    def _pick_cards(self):
        mx, my = px.mouse_x, px.mouse_y

        # Check freecells
        for i, card in enumerate(self.freecells):
            x = i * (CARD_W + 4)
            y = 2
            if card and x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
                self.drag_stack = [card]
                self.drag_from = ("freecell", i)
                self.drag_offset = (mx - x, my - y)
                self.freecells[i] = None
                return

        # Check columns
        ci, ri = self._find_card_at(mx, my)
        if ci:
            movable = self._get_movable_stack(ci, ri)
            self.drag_stack = movable
            self.drag_from = ("column", ci)
            self.drag_offset = (mx - movable[0].x, my - movable[0].y) 
            self.columns[ci] = self.columns[ci][:ri]

        # for ci, col in enumerate(self.columns):
        #     for idx, card in enumerate(col):
        #         # 座標は、描画した初期位置と合わせる
        #         x = ci * (CARD_W + 2)
        #         y = 30 + idx * 15
        #         if x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
        #             if self._is_valid_stack(col[idx:]):
        #                 self.drag_stack = col[idx:]
        #                 self.drag_from = ("column", ci)
        #                 self.drag_offset = (mx - x, my - y)
        #                 self.columns[ci] = col[:idx]
        #                 return

        # ドラッグ中
        if self.drag_stack:
            for i, card in enumerate(self.drag_stack):
                card.x = mx - self.drag_offset[0]
                card.y = my - self.drag_offset[1]


    def _drop_cards(self):
        if not self.drag_stack:
            return
        mx, my = px.mouse_x, px.mouse_y

        # Drop to freecell
        for i in range(NUM_FREECELLS):
            x = i * (CARD_W + 4)
            y = 2
            if not self.freecells[i] and x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
                if len(self.drag_stack) == 1:
                    self.freecells[i] = self.drag_stack[0]
                    self.drag_stack = []
                    return

        # Drop to homecell
        for i in range(NUM_HOMECELLS):
            x = 100 + i * (CARD_W + 4)
            y = 2
            if x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
                if len(self.drag_stack) == 1 and self._can_place_homecell(self.drag_stack[0], i):
                    card = self.drag_stack[0]
                    self.homecells[i].append(card)
                    self.drag_stack = []
                    return

        # Drop to columns
        for ci, col in enumerate(self.columns):
            x = ci * (CARD_W + 2)
            y = 30 + len(col) * 15
            if x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
                if self._can_place_column(self.drag_stack[0], col):
                    for i, card in enumerate(self.drag_stack):
                        # appendを用いることで、yを都度刷新する
                        y = 30 + len(col) * 15
                        card.x = x
                        card.y = y
                        col.append(card)
                    # self.columns[ci].extend(self.drag_stack)
                    self.drag_stack = []
                    return

        # If invalid drop, return to original place
        if self.drag_from:
            if self.drag_from[0] == "freecell":
                self.freecells[self.drag_from[1]] = self.drag_stack[0]
            elif self.drag_from[0] == "column":
                self.columns[self.drag_from[1]].extend(self.drag_stack)
        self.drag_stack = []


    def _is_valid_stack(self, stack):
        """Check if stack is in alternating colors and descending order."""
        for i in range(len(stack) - 1):
            if not self._can_place_column(stack[i], [stack[i+1]]):
                return False
        return True

    def _can_place_column(self, card, col):
        if not col:
            return True
        top = col[-1]
        return self._is_alternating_color(card, top) and self._rank_value(card) == self._rank_value(top) - 1

    def _can_place_homecell(self, card, homecell_index):
        homecell = self.homecells[homecell_index]
        if not homecell:
            return card.rank == "A"
        top = homecell[-1]
        return card.suit == top.suit and self._rank_value(card) == self._rank_value(top) + 1

    def _is_alternating_color(self, c1, c2):
        red = {"♥", "♦"}
        return (c1.suit in red) != (c2.suit in red)

    def _rank_value(self, card):
        return RANKS.index(card.rank)

    def _check_win(self):
        if all(len(f) == 13 for f in self.homecells):
            print("You win!")

    def draw(self):
        px.cls(px.COLOR_GREEN)

        # Draw freecells
        for i, fcell in enumerate(self.freecells):
            x = i * (CARD_W + 4)
            y = 2
            px.rectb(x, y, CARD_W, CARD_H, px.COLOR_WHITE)
            if fcell:
                fcell.x = x
                fcell.y = y
                fcell.draw()

        # Draw homecells
        for i, hcell in enumerate(self.homecells):
            x = 100 + i * (CARD_W + 4)
            y = 2
            px.rectb(x, y, CARD_W, CARD_H, px.COLOR_YELLOW)
            if hcell:
                hcell[-1].x = x
                hcell[-1].y = y
                hcell[-1].draw()

        # Draw columns
        for ci, col in enumerate(self.columns):
            x = ci * (CARD_W + 2)
            for idx, card in enumerate(col):
                y = 30 + idx * 15
                card.x = x
                card.y = y
                card.draw()

        # Draw dragging stack
        if self.drag_stack:
            mx, my = px.mouse_x, px.mouse_y
            for idx, card in enumerate(self.drag_stack):
                card.x = mx - self.drag_offset[0]
                card.y = my - self.drag_offset[1] + idx * 4
                card.draw()





if __name__ == "__main__":
    FreeCell()


