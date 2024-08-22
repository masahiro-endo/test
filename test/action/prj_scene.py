from pgzero.builtins import *
import pygame
from pygame.locals import *
from prj_actor import *
from enum import Enum
import global_value as g
import random
from typing import Any, Dict
from prj_actor import *
import os
os.chdir(os.path.dirname(__file__))



class FLOOR(Enum):
    MAP_1 = auto()
    BLOCK = auto()

class Parameter:
    def __init__(self, filename):
        self.filename = filename  # ファイル名

class SInfo:
    Params: Dict[Enum, Any] = {
            FLOOR.MAP_1    : Parameter,
            FLOOR.BLOCK    : Parameter,
    }

SInfo.Params[FLOOR.MAP_1]     = Parameter(os.path.abspath("./data/test.map"))
SInfo.Params[FLOOR.BLOCK]     = Parameter(os.path.abspath("./images/block.png"))



class Map:
    """マップ（プレイヤーや内部のスプライトを含む）"""
    GS = 32  # グリッドサイズ

    def __init__(self, filename):
        self.blocks = []

        # マップをロードしてマップ内スプライトの作成
        self.load(filename)

        # マップサーフェイスを作成
        # self.surface = pygame.Surface((self.col*self.GS, self.row*self.GS)).convert()

    def draw(self, screen):
        for sp in self.blocks:
            sp.draw()

    def update(self):
        for sp in self.blocks:
            sp.update()

    def load(self, filename):
        """マップをロードしてスプライトを作成"""
        map = []
        fp = open(filename, "r")
        for line in fp:
            line = line.rstrip()  # 改行除去
            map.append(list(line))
            self.row = len(map)
            self.col = len(map[0])
        self.width = self.col * self.GS
        self.height = self.row * self.GS
        fp.close()

        # マップサーフェイスを作成
        self.surface = pygame.Surface((self.col*self.GS, self.row*self.GS)).convert()
        source = pygame.image.load(SInfo.Params[FLOOR.BLOCK].filename)

        # マップからスプライトを作成
        for i in range(self.row):
            for j in range(self.col):
                if map[i][j] == 'B':
                    self.surface.blit(source, (j*self.GS, i*self.GS))
                    pygame.draw.rect(self.surface, pygame.Color('red'),Rect(j*self.GS, i*self.GS,self.GS, self.GS))
                    self.blocks.append(Block(j*self.GS, i*self.GS, SInfo.Params[FLOOR.BLOCK].filename))



class SCENE(Enum):
    TITLE = auto()
    PROLOGUE = auto()
    DEMO = auto()
    FLOOR_1 = auto()
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

    def draw(self, screen: pygame.Surface):
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



class TitleScene(BaseScene):

    def __init__(self, size: tuple):
        WIDTH, HEIGHT = size

        self._stars = []

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
            g.game_state = SCENE.FLOOR_1
            g.sceneStack.popleft()
            g.sceneStack.appendleft(Floor01_Scene(SInfo.Params[FLOOR.MAP_1].filename))


class Floor01_Scene(BaseScene):

    def __init__(self, path):
        self.map = Map(path)
        
        self.player = Player(300, 200, AInfo.charas[CHARA.PLAYER].imagename, self.map.blocks)
        # self.playerReveal(300, 200, "python.png", self.map.blocks)


    def playerReveal(self, WIDTH, HEIGHT, imgname, blocks):
        g.player = Player(WIDTH * 1 / WIDTH, HEIGHT / 2, imgname, blocks)
        g.objects.append(g.player)  # 自機をリストに格納

    def calc_offset(self):
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        """オフセットを計算"""
        offsetx = self.player.rect.topleft[0] - (WIDTH / 2)
        offsety = self.player.rect.topleft[1] - (HEIGHT / 2)
        return offsetx, offsety


    def draw(self, screen):
        super().draw(screen)

        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        # オフセッとに基づいてマップの一部を画面に描画
        offsetx, offsety = self.calc_offset()

        # 端ではスクロールしない
        if offsetx < 0:
            offsetx = 0
        elif offsetx > self.map.width - WIDTH:
            offsetx = self.map.width - WIDTH

        if offsety < 0:
            offsety = 0
        elif offsety > self.map.height - HEIGHT:
            offsety = self.map.height - HEIGHT

        # マップの一部を画面に描画
        # screen.blit(self.map.surface, (0,0), (offsetx, offsety, WIDTH, HEIGHT))
        # self.map.surface = screen.surface.copy()
        screen.surface.blit(self.map.surface, (0,0), (offsetx, offsety, WIDTH, HEIGHT))

        for sp in self.map.blocks:
            sp.x = sp.prevx - offsetx
            sp.y = sp.prevy - offsety
            sp.rect = Rect(sp.x, sp.y, sp.width, sp.height)


        self.map.draw(screen)
        self.player.draw()


    def update(self):
        super().update()

        self.map.update()
        self.player.update()

    def handler(self, event):
        super().handler(event)






