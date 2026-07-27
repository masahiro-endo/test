
import pyxel as px
import copy
from enum import Enum, IntEnum, auto

import appconfig as gbl
from module.constant import *









class TITLE_SEL(IntEnum):
    Cancel = -1 # 先頭に戻る
    New = 0
    Continue = auto()
    Exit = auto()

class MENU_SEL(IntEnum):
    Cancel = -1
    Save = 0
    Spells = auto()
    Close = auto()

class SPELL_SEL(IntEnum):
    Cancel = -1

class BATTLE_SEL(IntEnum):
    Cancel = -1
    Attack = 0
    Spell = auto()
    Run = auto()

class SHOP_SEL(IntEnum):
    Cancel = -1
    HP = 0
    MP = auto()
    STR = auto()
    AGI = auto()



class CSR(Enum):
    WELCOME = "welcome"
    MENU = "menu"
    SPELLS = "spells"
    SHOP = "shop"
    BOSS1 = "boss1"
    BOSS2 = "boss2"
    BOSS3 = "boss3"
    BTL_CMD = "bt_command"
    BTL_SPL = "bt_spells"
    



# カーソル（選択肢の ▶︎）
class Cursor:

    def __init__(self, key, list_x, y, cancel_pos=None):
        gbl.current_cursor = self
        self.key = key
        self.list_x = list_x
        self.y = y
        self.pos = 0
        self.cancel_pos = cancel_pos
        self.moved = False

    def draw(self):
        x = self.list_x[self.pos]
        px.blt(x * 8, self.y * 8, 0, 32, 48, 8, 8)

    def update(self):
        push = Meth.get_btn_state()

        if push[BTN.RHT] or push[BTN.LFT]:
            if self.moved:
                return
            dist = 1 if push[BTN.RHT] else -1
            self.pos = (self.pos + dist) % len(self.list_x)
            self.moved = True
        else:
            self.moved = False
        if push[BTN.A_Z]:
            # px.play(3, 35)
            return self.pos
        elif push[BTN.B_X]:
            return self.cancel_pos
        return None

    def dispose(self):
        gbl.current_cursor = None
        del self







