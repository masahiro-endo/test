
import pyxel as px
import random





CARD_WIDTH = 16
CARD_HEIGHT = 24
TABLEAU_SPACING = 8  # vertical spacing between cards in tableau
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUIT_COLOR = {"♠": 7, "♣": 7, "♥": 8, "♦": 8}
BACK_COLOR = 1






class Card:
    def __init__(self, suit, rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.face_up = face_up
        self.x = 0
        self.y = 0

    def draw(self):
        if self.face_up:
            px.rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT, 6)
            px.text(self.x + 2, self.y + 2, self.rank, SUIT_COLOR[self.suit])
            px.text(self.x + 2, self.y + 12, self.suit, SUIT_COLOR[self.suit])
        else:
            px.rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT, BACK_COLOR)

    def contains_point(self, mx, my):
        return self.x <= mx <= self.x + CARD_WIDTH and self.y <= my <= self.y + CARD_HEIGHT

    def rank_value(self):
        return RANKS.index(self.rank)


class Solitaire:
    def __init__(self):
        px.init(240, 180, title="px Solitaire")
        px.mouse(True)

        self.deck = self.create_deck()
        random.shuffle(self.deck)

        self.tableau = [[] for _ in range(7)]
        self.foundation = [[] for _ in range(4)]
        self.stock = []
        self.waste = []

        self.deal_cards()

        self.dragging_cards = []
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.source_pile = None

        self.win = False

        px.run(self.update, self.draw)

    def create_deck(self):
        return [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def deal_cards(self):
        idx = 0
        for col in range(7):
            for row in range(col + 1):
                card = self.deck[idx]
                idx += 1
                card.face_up = (row == col)
                card.x = 10 + col * (CARD_WIDTH + 4)
                card.y = 40 + row * TABLEAU_SPACING
                self.tableau[col].append(card)
        self.stock = self.deck[idx:]
        for card in self.stock:
            card.x = 10
            card.y = 10

    def update(self):
        if self.win:
            return

        mx, my = px.mouse_x, px.mouse_y

        # Click stock to deal 3 cards
        if px.btnp(px.MOUSE_BUTTON_LEFT) and not self.dragging_cards:
            if self.stock and self.stock[-1].contains_point(mx, my):
                self.deal_from_stock(3)
                return
            elif not self.stock and self.is_point_in_rect(mx, my, 10, 10, CARD_WIDTH, CARD_HEIGHT):
                self.recycle_waste()
                return

        # Pick up cards
        if px.btnp(px.MOUSE_BUTTON_LEFT):
            # Tableau
            for pile in self.tableau:
                for i, card in enumerate(pile):
                    if card.face_up and card.contains_point(mx, my):
                        self.dragging_cards = pile[i:]
                        self.source_pile = pile
                        self.drag_offset_x = mx - card.x
                        self.drag_offset_y = my - card.y
                        return
            # Waste
            if self.waste and self.waste[-1].contains_point(mx, my):
                self.dragging_cards = [self.waste[-1]]
                self.source_pile = self.waste
                self.drag_offset_x = mx - self.waste[-1].x
                self.drag_offset_y = my - self.waste[-1].y

        # Drop cards
        if px.btnr(px.MOUSE_BUTTON_LEFT) and self.dragging_cards:
            if not self.try_drop(mx, my):
                self.source_pile.extend(self.dragging_cards)
            self.dragging_cards = []
            self.source_pile = None
            self.check_win()

        # Dragging
        if self.dragging_cards:
            for j, c in enumerate(self.dragging_cards):
                c.x = mx - self.drag_offset_x
                c.y = my - self.drag_offset_y + j * TABLEAU_SPACING

    def try_drop(self, mx, my):
        moving = self.dragging_cards
        top_card = moving[0]

        # Tableau drop
        for col, pile in enumerate(self.tableau):
            if pile:
                target = pile[-1]
                if target.contains_point(mx, my) and target.face_up:
                    if self.can_stack_on_tableau(top_card, target):
                        pile.extend(moving)
                        self.flip_last_in_source()
                        return True
            else:
                # Empty tableau pile: only King allowed
                tx = 10 + col * (CARD_WIDTH + 4)
                ty = 40
                if self.is_point_in_rect(mx, my, tx, ty, CARD_WIDTH, CARD_HEIGHT):
                    if top_card.rank == "K":
                        pile.extend(moving)
                        self.flip_last_in_source()
                        return True

        # Foundation drop
        for i, pile in enumerate(self.foundation):
            x = 120 + i * (CARD_WIDTH + 4)
            y = 10
            if self.is_point_in_rect(mx, my, x, y, CARD_WIDTH, CARD_HEIGHT):
                if self.can_stack_on_foundation(top_card, pile):
                    pile.extend(moving)
                    self.flip_last_in_source()
                    return True

        return False

    def can_stack_on_tableau(self, moving_card, target_card):
        return (moving_card.rank_value() == target_card.rank_value() - 1 and
                SUIT_COLOR[moving_card.suit] != SUIT_COLOR[target_card.suit])

    def can_stack_on_foundation(self, moving_card, pile):
        if not pile:
            return moving_card.rank == "A"
        top = pile[-1]
        return (moving_card.suit == top.suit and
                moving_card.rank_value() == top.rank_value() + 1)

    def flip_last_in_source(self):
        if self.source_pile in self.tableau and self.source_pile:
            last_card = self.source_pile[-1]
            if not last_card.face_up:
                last_card.face_up = True

    def deal_from_stock(self, count):
        for _ in range(min(count, len(self.stock))):
            card = self.stock.pop()
            card.face_up = True
            card.x = 40
            card.y = 10
            self.waste.append(card)

    def is_point_in_rect(self, px, py, rx, ry, rw, rh):
        if not all(isinstance(v, (int, float)) for v in (px, py, rx, ry, rw, rh)):
            raise ValueError("All coordinates and sizes must be numbers.")
        if rw < 0 or rh < 0:
            raise ValueError("Width and height must be non-negative.")
        return rx <= px <= rx + rw and ry <= py <= ry + rh

    def check_win(self):
        try:
            for suit, pile in self.foundation:
                # Must have exactly 13 cards
                if len(pile) != 13:
                    return False
                # Must be in correct order
                expected = [(rank, suit) for rank in range(1, 14)]
                if pile != expected:
                    return False
            return True
        except Exception as e:
            print(f"Error in check_win: {e}")
            return False
        

    def draw(self):
        px.cls(0)

        # Draw stock
        if self.stock:
            px.rect(10, 10, CARD_WIDTH, CARD_HEIGHT, BACK_COLOR)
        else:
            px.rectb(10, 10, CARD_WIDTH, CARD_HEIGHT, 5)

        # Draw waste
        if self.waste:
            self.waste[-1].draw()
        else:
            px.rectb(40, 10, CARD_WIDTH, CARD_HEIGHT, 5)

        # Draw foundation
        for i in range(4):
            x = 100 + i * (CARD_WIDTH + 4)
            y = 10
            if self.foundation[i]:
                self.foundation[i][-1].draw()
            else:
                px.rectb(x, y, CARD_WIDTH, CARD_HEIGHT, 5)

        # Draw tableau
        for col, pile in enumerate(self.tableau):
            for i, card in enumerate(pile):
                card.draw()

        # Draw dragging card on top
        # if self.dragging_card:
        #     self.dragging_card.draw()
        if self.dragging_cards:
            for j, c in enumerate(self.dragging_cards):
                c.draw()





if __name__ == "__main__":
    Solitaire()




                              
