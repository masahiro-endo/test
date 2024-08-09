import pygame
from pygame.locals import *
from pgzero.builtins import *
from enum import Enum
import global_value as g
import random
from shooter_sub import *
from shooter_UI import *
import time
from typing import Any, Dict



class SCENE(Enum):
    TITLE = auto()
    PROLOGUE = auto()
    DEMO = auto()
    FIELD = auto()
    BATTLE = auto()
    GAMEOVER = auto()




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
            g.game_state = SCENE.FIELD
            g.start = time.time()
            g.out_time = 0
            g.sceneStack.popleft()
            g.sceneStack.appendleft(FieldScene())


class PrologueScene(BaseScene):
    def __init__(self):
        pass

class DemoScene(BaseScene):
    def __init__(self):
        pass


class FieldScene(BaseScene):
    _stars = []

    def enemyEncount(self, WIDTH, HEIGHT ):
        
        if g.bosstimer==0:
            pass
            # g.objects.append(Boss(WIDTH/2, 0, 0, CHARA.ENEMY_BOSS))  # ボス出現
        elif g.bosstimer > 0 and random.randrange(80)==0: # 敵1出現
            y = random.randrange(HEIGHT - 200) + 100
            g.objects.append(Enemy(WIDTH, y, 0, CHARA.ENEMY_1))
        
        elif g.bosstimer > 0 and random.randrange(100)==0: # 敵2出現
            y = random.randrange(HEIGHT - 200) + 100
            # g.objects.append(Enemy(WIDTH, y, 0, CHARA.ENEMY_2))
        
        elif random.randrange(200)==0: # デブリ出現
            y = random.randrange(1, HEIGHT, 10)
            rad = random.randrange(-60, 60, 1)
            # g.objects.append(Debris(WIDTH, y, rad, CHARA.DEBRIS))
        
        else:
            pass

    def playerReveal(self, WIDTH, HEIGHT ):
        g.player = Player(WIDTH * 1 / WIDTH, HEIGHT / 2, 0, CHARA.PLAYER)
        g.objects.append(g.player)  # 自機をリストに格納


    def __init__(self):
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        for i in range(10):
            pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
            self._stars.append(Rect(pos,(3, 3)))

        self.playerReveal(WIDTH, HEIGHT)


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
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        super().handler(event)
        self.enemyEncount(WIDTH, HEIGHT)

        if event[keys.ESCAPE]: 
            g.game_state = SCENE.GAMEOVER
            g.currentScene.popleft()
            g.currentScene.appendleft(GameOverScene())

        if event[keys.S]: 
            g.termStack.appendleft(CaptionWindow(Rect( (0, 450), (600, 150) ), 'caption window'))


class BattleScene(BaseScene):
    def __init__(self):
        pass


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

