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



