
import pyxel as px 
import random

import appconfig as gbl
from context import *
from actor import *
from method import *








class ViewModel:

    def __init__(self):
        self.columns = [[] for _ in range(NUM_TABLEAU)]
        self.freecells = [None] * NUM_FREECELLS
        self.homecells = [[] for _ in range(NUM_HOMECELLS)]

        gbl.columns = self.columns
        gbl.homecells = self.homecells

        self.drag_stack = []
        self.drag_from = None
        self.drag_offset = (0, 0)
        self._new_game()

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
        ci, ri = Meth._find_card_at(mx, my)
        # if ci: のみでは、「0」で「偽」になる。
        if ci is not None:
            movable = Meth._get_movable_stack(ci, ri)
            self.drag_stack = movable
            self.drag_from = ("column", ci)
            self.drag_offset = (mx - movable[0].x, my - movable[0].y) 
            self.columns[ci] = self.columns[ci][:ri]


        # # ドラッグ中
        # if self.drag_stack:
        #     for i, card in enumerate(self.drag_stack):
        #         card.x = mx - self.drag_offset[0]
        #         card.y = my - self.drag_offset[1] + i * 15


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
                if len(self.drag_stack) == 1 and Meth._can_place_homecell(self.drag_stack[0], self.homecells[i]):
                    card = self.drag_stack[0]
                    self.homecells[i].append(card)
                    self.drag_stack = []
                    return

        # Drop to columns
        for ci, col in enumerate(self.columns):
            x = ci * (CARD_W + 2)
            y = 30 + len(col) * 15 # 最後尾
            if x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
                if Meth._can_place_column(self.drag_stack[0], col):
                    col.extend(self.drag_stack)
                    # # 表示位置を再設定
                    # for i, card in enumerate(col):
                    #     y = 30 + i * 15
                    #     card.x = x
                    #     card.y = y
                    self.drag_stack = []
                    return

        # If invalid drop, return to original place
        if self.drag_from:
            if self.drag_from[0] == "freecell":
                self.freecells[self.drag_from[1]] = self.drag_stack[0]
            elif self.drag_from[0] == "column":
                self.columns[self.drag_from[1]].extend(self.drag_stack)
        self.drag_stack = []



class AppView:
    def __init__(self, ViewModel):
        self.vm = ViewModel

        px.init(180, 160, title="FreeCell", fps=30)
        px.mouse(True)
        gbl.BOF = px.Font("k8x12S.bdf")
        px.run(self.update, self.draw)

    def update(self):
        self.vm.update()

    def draw(self):
        px.cls(px.COLOR_GREEN)

        # Draw freecells
        for i, fcell in enumerate(self.vm.freecells):
            x = i * (CARD_W + 4)
            y = 2
            px.rectb(x, y, CARD_W, CARD_H, px.COLOR_WHITE)
            if fcell:
                fcell.x = x
                fcell.y = y
                fcell.draw()

        # Draw homecells
        for i, hcell in enumerate(self.vm.homecells):
            x = 100 + i * (CARD_W + 4)
            y = 2
            px.rectb(x, y, CARD_W, CARD_H, px.COLOR_YELLOW)
            if hcell:
                hcell[-1].x = x
                hcell[-1].y = y
                hcell[-1].draw()

        # Draw columns
        for ci, col in enumerate(self.vm.columns):
            x = ci * (CARD_W + 2)
            for idx, card in enumerate(col):
                y = 30 + idx * 15
                card.x = x
                card.y = y
                card.draw()

        # Draw dragging stack
        if self.vm.drag_stack:
            mx, my = px.mouse_x, px.mouse_y
            for idx, card in enumerate(self.vm.drag_stack):
                card.x = mx - self.vm.drag_offset[0]
                card.y = my - self.vm.drag_offset[1] + idx * 15
                card.draw()





if __name__ == "__main__":
    vm = ViewModel()
    AppView(vm)


