
import appconfig as gbl
from context import *









class Meth:
    
    @staticmethod
    def _is_valid_stack(stack):
        # Check if stack is in alternating colors and descending order.
        for i in range(len(stack) - 1):
            if not Meth._can_place_column(stack[i], [stack[i+1]]):
                return False
        return True

    @staticmethod
    def _can_place_column(card, col):
        if not col:
            return True
        top = col[-1]
        return Meth._is_alternating_color(card, top) and Meth._rank_value(card) == Meth._rank_value(top) - 1

    @staticmethod
    def _can_place_homecell(card, homecell):
        if not homecell:
            return card.rank == 'A'
        top = homecell[-1]
        return card.suit == top.suit and Meth._rank_value(card) == Meth._rank_value(top) + 1

    @staticmethod
    def _is_alternating_color(c1, c2):
        red = {'♥', '♦'}
        return (c1.suit in red) != (c2.suit in red)

    @staticmethod
    def _rank_value(card):
        return RANKS.index(card.rank)

    @staticmethod
    def _find_card_at():
        # マウス位置からカードとそのカラムを探す
        for ci, col in enumerate(gbl.columns):
            for ri in reversed(range(len(col))):
                card = col[ri]
                if card.is_mouse_over():
                    return ci, ri
        return None, None

    @staticmethod
    def _get_movable_stack(ci, ri):
        # 選択したカードから下の連続ランクカードをまとめて取得
        col = gbl.columns[ci]
        stack = col[ri:]
        # 連続性チェック（降順かつ色交互）
        for i in range(len(stack) - 1):
            if RANKS.index(stack[i].rank) != RANKS.index(stack[i+1].rank) + 1:
                return [stack[0]]  # 連続していない場合は1枚だけ
            if stack[i].color == stack[i+1].color:
                return [stack[0]]
        return stack
    
    @staticmethod
    def _check_win():
        if all(len(f) == 13 for f in gbl.homecells):
            print("You win!")






