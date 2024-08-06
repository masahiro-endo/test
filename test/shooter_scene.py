from collections import deque
from typing import List
import pygame
from pygame.locals import *
import sys
from enum import Enum
import global_value as g



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

    def draw(self, screen: pygame.Surface):
        screen.fill(Color('black'))

    def handler(self, event):

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    def onEnter(self):
        # タイマーカウンタ初期化
        self.tick = 0

    def onExit(self):
        pass



class TitleScene(BaseScene):

    def __init__(self):
        pass

    def update(self):
        super().update()
                    
    def draw(self, screen):
        super().draw(screen)

    def handler(self, event):
        super().handler(event)

        if event.type == KEYDOWN:
            
            if event.key == K_SPACE:
                g.currentScene.popleft()
                g.currentScene.appendleft(FieldScene())



class FieldScene(BaseScene):
    def __init__(self):
        pass

    def update(self):
        super().update()
                    
    def draw(self, screen):
        super().draw(screen)

    def handler(self, event):
        super().handler(event)



