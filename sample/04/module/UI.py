
import pyxel as px
import copy
from enum import Enum, IntEnum, auto

import appconfig as gbl
from module.constant import *





class WIN(Enum):
    MSG = "msg"
    MENU = "menu_stat"
    MENU_SPL = "MENU_SPL"
    SHOP = "shop"
    BTL_STS = "bt_stat"
    BTL_MSG = "bt_msg"




class Window:
    all = {}

    def __init__(self, key, x1, y1, x2, y2, texts):
        self.key = key
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.texts = texts

    def draw(self):
        x1 = self.x1 * 8
        y1 = self.y1 * 8
        x2 = self.x2 * 8
        y2 = self.y2 * 8
        px.blt(x1, y1, 0, 0, 48, 8, 8)
        px.blt(x2 - 8, y1, 0, 8, 48, 8, 8)
        px.blt(x1, y2 - 8, 0, 0, 56, 8, 8)
        px.blt(x2 - 8, y2 - 8, 0, 8, 56, 8, 8)
        x = self.x1 + 1
        while x < self.x2 - 1:
            px.blt(x * 8, y1, 0, 16, 48, 8, 8)
            px.blt(x * 8, y2 - 8, 0, 16, 56, 8, 8)
            x += 1
        y = self.y1 + 1
        while y < self.y2 - 1:
            px.blt(x1, y * 8, 0, 24, 48, 8, 8)
            px.blt(x2 - 8, y * 8, 0, 24, 56, 8, 8)
            y += 1
        px.rect(x1 + 8, y1 + 8, x2 - x1 - 16, y2 - y1 - 16, 0)
        for pos, text in enumerate(self.texts):
            if pos >= 0 and pos < (self.y2 - self.y1 - 2) // 2:
                Meth.draw_text(self.x1 + 1, self.y1 + 1 + pos * 2, text)

        if gbl.current_cursor():
            gbl.current_cursor().draw()


    # クラスメソッドは主に、コンストラクタと異なる引数を持つFactoryMethod用 
    @classmethod
    def open(cls, key, x1, y1, x2, y2, texts=[]):
        if key in cls.all:
            cls.all[key].texts = texts
        else:
            # 複製を dict 連想配列 all に保存
            cls.all[key] = cls(key, x1, y1, x2, y2, texts)
        return cls.all[key]

    @classmethod
    def close(cls):
        windows_copy = copy.deepcopy(cls.all)
        for key in windows_copy:
            del cls.all[key]
        return

    @staticmethod
    def clear():
        Window.close()

    @classmethod
    def pop(cls, key):
        del cls.all[key]

    @staticmethod
    def message(msg):
        Window.open(WIN.MSG, 0, 10, 16, 16, msg)

    @staticmethod
    def battlemessage(bt_msg):
        Window.open(WIN.BTL_STS, 8, 0, 16, 8, gbl.player_party().battle_status())
        Window.open(WIN.BTL_MSG, 0, 8, 16, 16, bt_msg)









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







class Meth:

    # 全角化
    @staticmethod
    def zen(val):
        h2z = str.maketrans(
            " 1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ /+-:*#()[]",
            "　１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ　／＋－：＊＃（）［］",
        )
        return str(val).translate(h2z)

    # テキスト描画
    @staticmethod
    def draw_text(x, y, t, clr=7):
        # global BDF
        config = gbl.global_setting()
        px.text(x * 8, y * 8 + 4, Meth.zen(t), clr, config.BDF)

    # セーブファイル名
    @staticmethod
    def get_data_file():
        return px.user_data_dir("shiromofu factory", "tinyDRPG") + "save.json"

    # ボタン取得
    @staticmethod
    def get_btn_state():
        btn = {
            BTN.UP : px.btnp(px.KEY_UP   , hold=15, repeat=3) or px.btn(px.GAMEPAD1_BUTTON_DPAD_UP),
            BTN.DWN: px.btnp(px.KEY_DOWN , hold=15, repeat=3) or px.btn(px.GAMEPAD1_BUTTON_DPAD_DOWN),
            BTN.LFT: px.btnp(px.KEY_LEFT , hold=15, repeat=3) or px.btn(px.GAMEPAD1_BUTTON_DPAD_LEFT),
            BTN.RHT: px.btnp(px.KEY_RIGHT, hold=15, repeat=3) or px.btn(px.GAMEPAD1_BUTTON_DPAD_RIGHT),
            BTN.A_Z: px.btnp(px.KEY_Z    , hold=15, repeat=3) or px.btnp(px.GAMEPAD1_BUTTON_A, 10, 2),
            BTN.B_X: px.btnp(px.KEY_X    , hold=15, repeat=3) or px.btnp(px.GAMEPAD1_BUTTON_B, 10, 2),
        }
        return btn

    # パディング左よせ
    @staticmethod
    def spacing(val, length):
        return Meth.zen(val).ljust(length)[-length:]

    # パディング右よせ
    @staticmethod
    def pad(val, length, fill=" "):
        return Meth.zen(val).rjust(length, fill)[-length:]



