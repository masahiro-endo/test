
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

        # if gbl.current_cursor():
        #     gbl.current_cursor().draw()


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
        Window.open(WIN.BTL_STS, 8, 0, 16, 8, Window.battle_status(gbl.player_party()))
        Window.open(WIN.BTL_MSG, 0, 8, 16, 16, bt_msg)

    @staticmethod
    def battle_status(pt):
        px.rect(0, 112 + (2*8), 128, 16 * len(pt), 0)
        for pos, pl in enumerate(pt):
            # t = f"HP{Meth.pad(pl.hp,3)} MP{Meth.pad(pl.mp,2)} {Meth.pad(pt.gold,4)}G"
            t = f"{Meth.pad(pl.name,4)} HP{Meth.pad(pl.hp,3)} MP{Meth.pad(pl.mp,2)}"
            clr = px.COLOR_WHITE if pl.is_alive() else px.COLOR_RED

            Meth.draw_text(0, 14 + 2 + pos * 1.2, t, clr)












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
            BTN.SEL: px.btnp(px.KEY_SPACE, hold=15, repeat=3) or px.btnp(px.GAMEPAD1_BUTTON_START),
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



