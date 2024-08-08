from typing import List
import pygame
from pygame.locals import *
from pgzero.builtins import *
from enum import Enum
import global_value as g
import random
from shooter_sub import *
import time
from typing import Any, Dict


class Define:
    _subwnd: Dict[str, Any] = {
            'image': Any,
            'script': Any,
    }


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
        pass
        # if event.type == QUIT:
        #     pygame.quit()
        #     sys.exit()

        # if event.type == KEYDOWN:

        #     if event.key == K_ESCAPE:
        #         pygame.quit()
        #         sys.exit()

    def onEnter(self):
        # タイマーカウンタ初期化
        self.tick = 0

    def onExit(self):
        pass



class TitleScene(BaseScene):
    _stars = []

    def __init__(self, size: tuple):
        WIDTH, HEIGHT = size

        for i in range(10):
            pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
            self._stars.append(Rect(pos,(3, 3)))

    def update(self):
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        super().update()
        for i in range(len(self._stars)):
            self._stars[i].x-=(i+1)  # 星を右から左へ動かす
            if self._stars[i].x < 0:
                self._stars[i].x = WIDTH
                    
    def draw(self, screen):
        super().draw(screen)
        for rect in self._stars:
            screen.draw.rect(rect, 'WHITE')

        screen.draw.text('Press Enter Key\n', \
                         left=150,top=240,fontsize=64,color='YELLOW')


    def handler(self, keyboard):
        super().handler(keyboard)

        if keyboard[keys.RETURN]: 
            g.game_state = SCENE.GAME
            g.start = time.time()
            g.out_time = 0
            g.currentScene.popleft()
            g.currentScene.appendleft(FieldScene())


class PrologueScene(BaseScene):
    def __init__(self):
        pass

class DemoScene(BaseScene):
    def __init__(self):
        pass


class FieldScene(BaseScene):
    _stars = []

    def __init__(self):
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        for i in range(10):
            pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
            self._stars.append(Rect(pos,(3, 3)))

        g.objects.append(g.player)  # 自機をリストに格納


    def draw(self, screen):
        super().draw(screen)
        for rect in self._stars:
            screen.draw.rect(rect, 'WHITE')

    def update(self):
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        super().update()
        for i in range(len(self._stars)):
            self._stars[i].x-=(i+1)  # 星を右から左へ動かす
            if self._stars[i].x < 0:
                self._stars[i].x = WIDTH
                    
    def handler(self, event):
        super().handler(event)

        if event[keys.ESCAPE]: 
            g.game_state = SCENE.GAMEOVER
            g.currentScene.popleft()
            g.currentScene.appendleft(GameOverScene())


class GameOverScene(BaseScene):
    _stars = []

    def __init__(self):
        pass

    def draw(self, screen):
        super().draw(screen)

        screen.draw.text('game over\n', \
                         left=150,top=240,fontsize=64,color='YELLOW')

    def update(self):
        super().update()
                    
    def handler(self, event):
        super().handler(event)

        if keyboard[keys.ESCAPE]: 
            g.game_state = SCENE.TITLE
            g.currentScene.popleft()
            g.currentScene.appendleft(TitleScene())

