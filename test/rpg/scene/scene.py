import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *
import os
import sys
import struct
import codecs
import control 
from enum import IntEnum, Enum, auto
from typing import Any, Dict





GS = 32


class SCENE(Enum):
    TITLE = auto()
    PROLOGUE = auto()
    DEMO = auto()
    FIELD = auto()
    BATTLE = auto()
    GAMEOVER = auto()
    WINDOW_OPEN = auto()



class BaseScene:

    # 経過時間
    tick = 0

    # stateStackへの参照
    stateStack = None

    # 描画の座標オフセット
    DRAW_OFFSET_X = 0
    DRAW_OFFSET_Y = 0


    def __init__(self):
        pass

    def update(self):
        self.tick += 1

    def draw(self, screen):
        screen.fill(Color('black'))

    def handler(self, event):
        if keyboard[keys.ESCAPE]:
            pygame.quit()
            sys.exit()

    def onEnter(self):
        # タイマーカウンタ初期化
        self.tick = 0

    def onExit(self):
        pass




