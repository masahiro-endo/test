from typing import overload

import pyxel as px
import copy
from enum import Enum, auto
import appconfig







# ウィンドウオブジェクト
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
                draw_text(self.x1 + 1, self.y1 + 1 + pos * 2, text)

    @classmethod
    def open(cls, key, x1, y1, x2, y2, texts=[]):
        if key in cls.all:
            cls.all[key].texts = texts
        else:
            cls.all[key] = cls(key, x1, y1, x2, y2, texts)
        return cls.all[key]

    @classmethod
    def close(cls):
        windows_copy = copy.deepcopy(cls.all)
        for key in windows_copy:
            del cls.all[key]
        return




# カーソル（選択肢の ▶︎）
class Cursor:

    def __init__(self, key, list_x, y, cancel_pos=None):
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
        btn = get_btn_state()

        if btn["r"] or btn["l"]:
            if self.moved:
                return
            dist = 1 if btn["r"] else -1
            self.pos = (self.pos + dist) % len(self.list_x)
            self.moved = True
        else:
            self.moved = False
        if btn["a"]:
            # px.play(3, 35)
            return self.pos
        elif btn["b"]:
            return self.cancel_pos
        return None









### ユーティリティ関数 ###


# 全角化
def zen(val):
    h2z = str.maketrans(
        " 1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ /+-:*#()[]",
        "　１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ　／＋－：＊＃（）［］",
    )
    return str(val).translate(h2z)


# テキスト描画
def draw_text(x, y, t):
    # global BDF
    config = appconfig.get_settings()
    px.text(x * 8, y * 8 + 4, zen(t), 7, config.BDF)


# セーブファイル名
def get_data_file():
    return px.user_data_dir("shiromofu factory", "tinyDRPG") + "save.json"


# ボタン取得
def get_btn_state():
    btn = {
        "u": px.btn(px.KEY_UP) or px.btn(px.GAMEPAD1_BUTTON_DPAD_UP),
        "d": px.btn(px.KEY_DOWN) or px.btn(px.GAMEPAD1_BUTTON_DPAD_DOWN),
        "l": px.btn(px.KEY_LEFT) or px.btn(px.GAMEPAD1_BUTTON_DPAD_LEFT),
        "r": px.btn(px.KEY_RIGHT) or px.btn(px.GAMEPAD1_BUTTON_DPAD_RIGHT),
        "a": px.btnp(px.KEY_Z, 10, 2) or px.btnp(px.GAMEPAD1_BUTTON_A, 10, 2),
        "b": px.btnp(px.KEY_X, 10, 2) or px.btnp(px.GAMEPAD1_BUTTON_B, 10, 2),
    }
    return btn


# パディング左よせ
def spacing(val, length):
    return zen(val).ljust(length)[-length:]


# パディング右よせ
def pad(val, length, fill=" "):
    return zen(val).rjust(length, fill)[-length:]



# 起動画面ウィンドウ生成
def welcome_show():
    message_window([" New Cont Exit", " (Zキー or Aボタン)"])
    
    self.cur = Cursor("welcome", [1, 5, 10], 12)
    # すでにデータがある場合、カーソル位置をContにあわせる
    # if self.load_data():
    #     self.cur.pos = 1
    # self.scene = "welcome"
    # self.play_bgm(1)


# メッセージ
def message_window(msg):
    Window.open("msg", 0, 10, 16, 16, msg)
    # self.wait = True

