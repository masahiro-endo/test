#!/usr/bin/env python
import pygame
from pygame.locals import *
import pgzrun
from pgzero.builtins import *
from collections import deque
import global_value as g
from prj_scene import *
import sys
import os
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))



class Game:
    class Setting:
        class DisplayResolution():
            VGA = (640, 480)
            SVGA = (800, 600)
            XGA = (1024, 768)
        
        def is_dispay_area(pos: tuple) -> bool:
            x, y = pos
            if (0 < x < WIDTH) and (0 < y < HEIGHT):
                return True
            return False

    def init():

        g.objects = []  # スプライトのリスト
        g.player = None
        g.game_state = SCENE.TITLE

        g.sceneStack = deque()
        g.sceneStack.appendleft(TitleScene(Game.Setting.DisplayResolution.VGA))
        


WIDTH, HEIGHT = Game.Setting.DisplayResolution.VGA






def draw():
    screen.clear()

    for scene in reversed(g.sceneStack):
        if scene is None:
            continue
        scene.draw(screen)
    
    if g.game_state==SCENE.TITLE:
        pass
    else:
        for sp in g.objects:
            sp.draw()




def update():
    
    for scene in reversed(g.sceneStack):
        if scene is None:
            continue
        scene.update()
        scene.handler(keyboard)

    if g.game_state==SCENE.TITLE:
        pass        
        return

    elif g.game_state==SCENE.GAMEOVER:
        pass
        return

    else:
        pass

    for sp in reversed(g.objects):
        sp.update()

        if not Game.Setting.is_dispay_area(sp.pos):
            g.objects.remove(sp)  # 画面外のスプライトを消去
            continue



Game.init()
pgzrun.go()





SCR_RECT = Rect(0, 0, 640, 480)

class PyAction:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("マップスクロール")

        # 画像のロード
        Python.left_image = load_image("python.png", -1)                     # 左向き
        Python.right_image = pygame.transform.flip(Python.left_image, 1, 0)  # 右向き
        Block.image = load_image("block.png", -1)

        # マップのロード
        self.map = Map("data/test.map")

        # メインループ
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def update(self):
        self.map.update()

    def draw(self, screen):
        self.map.draw()

        # オフセッとに基づいてマップの一部を画面に描画
        offsetx, offsety = self.map.calc_offset()

        # 端ではスクロールしない
        if offsetx < 0:
            offsetx = 0
        elif offsetx > self.map.width - SCR_RECT.width:
            offsetx = self.map.width - SCR_RECT.width

        if offsety < 0:
            offsety = 0
        elif offsety > self.map.height - SCR_RECT.height:
            offsety = self.map.height - SCR_RECT.height

        # マップの一部を画面に描画
        screen.blit(self.map.surface, (0,0), (offsetx, offsety, SCR_RECT.width, SCR_RECT.height))


