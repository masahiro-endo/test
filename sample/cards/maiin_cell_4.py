
import pyxel as px 
import random

CARD_W, CARD_H = 16, 24
NUM_COLUMNS = 8
NUM_FREECELLS = 4
NUM_FOUNDATIONS = 4
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

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
        px.rect(self.x, self.y, CARD_W, CARD_H, 7)
        px.text(self.x + 3, self.y + 4, str(self.rank), SUIT_COLOR[self.suit])
        px.text(self.x + 3, self.y + 14, self.suit, SUIT_COLOR[self.suit])


class FreeCell:
    def __init__(self):
        px.init(180, 160, title="FreeCell", fps=30)
        px.mouse(True)

        self.columns = [[] for _ in range(NUM_COLUMNS)]
        self.freecells = [None] * NUM_FREECELLS
        self.foundations = [[] for _ in range(NUM_FOUNDATIONS)]

        self.drag_stack = []
        self.drag_from = None
        self.drag_offset = (0, 0)

        self._new_game()
        px.run(self.update, self.draw)

    def _new_game(self):
        deck = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(deck)
        for i, card in enumerate(deck):
            self.columns[i % NUM_COLUMNS].append(card)

    def update(self):
        if px.btnp(px.MOUSE_LEFT_BUTTON):
            self._pick_cards()
        elif px.btnr(px.MOUSE_LEFT_BUTTON):
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
        for ci, col in enumerate(self.columns):
            for idx, card in enumerate(col):
                x = ci * (CARD_W + 2)
                y = 30 + idx * 4
                if x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
                    if self._is_valid_stack(col[idx:]):
                        self.drag_stack = col[idx:]
                        self.drag_from = ("column", ci)
                        self.drag_offset = (mx - x, my - y)
                        self.columns[ci] = col[:idx]
                        return

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

        # Drop to foundation
        for i in range(NUM_FOUNDATIONS):
            x = 100 + i * (CARD_W + 4)
            y = 2
            if x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
                if len(self.drag_stack) == 1 and self._can_place_foundation(self.drag_stack[0], i):
                    self.foundations[i].append(self.drag_stack[0])
                    self.drag_stack = []
                    return

        # Drop to columns
        for ci, col in enumerate(self.columns):
            x = ci * (CARD_W + 2)
            y = 30 + len(col) * 4
            if x <= mx <= x + CARD_W and y <= my <= y + CARD_H:
                if self._can_place_column(self.drag_stack[0], col):
                    self.columns[ci].extend(self.drag_stack)
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

    def _can_place_foundation(self, card, foundation_index):
        foundation = self.foundations[foundation_index]
        if not foundation:
            return card[0] == "A"
        top = foundation[-1]
        return card[1] == top[1] and self._rank_value(card) == self._rank_value(top) + 1

    def _is_alternating_color(self, c1, c2):
        red = {"♥", "♦"}
        return (c1[1] in red) != (c2[1] in red)

    def _rank_value(self, card):
        return RANKS.index(card[0])

    def _check_win(self):
        if all(len(f) == 13 for f in self.foundations):
            print("You win!")

    def draw(self):
        px.cls(0)

        # Draw freecells
        for i, card in enumerate(self.freecells):
            x = i * (CARD_W + 4)
            y = 2
            px.rectb(x, y, CARD_W, CARD_H, 7)
            if card:
                self._draw_card(x, y, card)

        # Draw foundations
        for i, foundation in enumerate(self.foundations):
            x = 100 + i * (CARD_W + 4)
            y = 2
            px.rectb(x, y, CARD_W, CARD_H, 10)
            if foundation:
                self._draw_card(x, y, foundation[-1])

        # Draw columns
        for ci, col in enumerate(self.columns):
            x = ci * (CARD_W + 2)
            for idx, card in enumerate(col):
                y = 30 + idx * 4
                self._draw_card(x, y, card)

        # Draw dragging stack
        if self.drag_stack:
            mx, my = px.mouse_x, px.mouse_y
            for idx, card in enumerate(self.drag_stack):
                self._draw_card(
                    self.mx - self.drag_offset[0],
                    self.my - self.drag_offset[1] + idx * 4,
                    card
                )

