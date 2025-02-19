import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *
import random
from enum import IntEnum, Enum, auto
from typing import Any, Dict

import global_value as g
from actor import *
from scene.scene import *
from scene.scene_combat import *
from UI import *





class MapTool():

    class MAP(IntEnum):
        TOWN = 101

    class OBJECT(IntEnum):
        FOREST = auto()
        STONEFLOOR = auto()

    class Parameter:
        def __init__(self, filename):
            self.filename = filename

    Params: Dict[Enum, Any] = {
            MAP.TOWN             : Parameter,
            OBJECT.FOREST        : Parameter,
            OBJECT.STONEFLOOR    : Parameter,
    }

    Params[MAP.TOWN]             = Parameter("/data/test.map")
    Params[OBJECT.FOREST]        = Parameter("/mapchip/forest.png")
    Params[OBJECT.STONEFLOOR]    = Parameter("/mapchip/stone_floor.png")

    @staticmethod
    def loadmapchip(objno)->Any:
        image = pygame.image.load(f"{os.path.dirname(__file__)}/../{MapTool.Params[objno].filename}")
        return image

    @staticmethod
    def loadmap(mapno)->Any:
        GS = 32
        map = []
        fp = open(f"{os.path.dirname(__file__)}/../{MapTool.Params[mapno].filename}", "r")
        for line in fp:
            line = line.rstrip()  # 改行除去
            map.append(list(line))
            row = len(map)
            col = len(map[0])
        width = col * GS
        height = row * GS
        fp.close()

        # マップサーフェイスを作成
        surface = pygame.Surface((col * GS, row * GS)).convert()

        # マップからスプライトを作成
        for i in range(row):
            for j in range(col):
                if map[i][j] == 'B':
                    source = MapTool.loadmapchip(MapTool.OBJECT.FOREST)
                    g.blocks.append(Block(Rect(j * GS, i * GS, GS, GS)))
                else:
                    source = MapTool.loadmapchip(MapTool.OBJECT.STONEFLOOR)
                surface.blit(source, (j * GS, i * GS))

        g.map = map

        return surface


class FieldScene(BaseScene):

    def __init__(self):
        self.surface = MapTool.loadmap(MapTool.MAP.TOWN)

        # self.avator = Avator()
        # self.avator.pos = (GS, GS)
        for mem in g.party.member:
            mem.pos = (GS * 10, GS)

    def doEncounted(self) -> bool:
        if random.randint(0, 300) == 0:
            return True
        else:
            return False

    def trans_combatScene(self):
        g.sceneStack.appendleft(CombatScene())

    def calc_offset(self):
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        MAP_WIDTH, MAP_HEIGHT = self.surface.get_size()
        leader = g.party.member[0]

        # 画面中央の座標とプレイヤー位置の差分
        if (leader.pos[0] - (WIDTH / 2))==0:
            pass

        offsetx = leader.pos[0] + (leader.rect.width / 2) - (WIDTH / 2)
        offsety = leader.pos[1] + (leader.rect.height / 2) - (HEIGHT / 2)

        # 端ではスクロールしない
        if offsetx < 0:
            offsetx = 0 # 左端
        elif offsetx > MAP_WIDTH - WIDTH:
            offsetx = MAP_WIDTH - WIDTH # 右端

        if offsety < 0:
            offsety = 0
        elif offsety > MAP_HEIGHT - HEIGHT:
            offsety = MAP_HEIGHT- HEIGHT

        return offsetx, offsety

    def update(self):
        super().update()

        # if self.doEncounted():
        #     self.trans_combatScene()

    def draw(self, screen):
        super().draw(screen)
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        offsetx, offsety = self.calc_offset()
        # screen.surface.blit(self.surface, (0,0), (0, 0, WIDTH, HEIGHT))
        screen.surface.blit(self.surface, (0,0), (offsetx, offsety, WIDTH, HEIGHT))

        for mem in reversed(g.party.member):
            dx, dy = mem.pos
            dx -= offsetx
            dy -= offsety
            # プレイヤー描画もoffset分ずらさないと駄目な模様
            # screen.blit(mem.anime[mem.direction][mem.imgnum], mem.pos)
            screen.blit(mem.anime[mem.direction][mem.imgnum], (dx, dy))

    def handler(self, keyboard):
        super().handler(keyboard)
        leader = g.party.member[0]

        if keyboard[keys.RETURN]: 
            pass
        if keyboard[keys.DOWN]:
            leader.turn(Avator.LOOK.DOWN)
        if keyboard[keys.LEFT]:
            leader.turn(Avator.LOOK.LEFT)
        if keyboard[keys.RIGHT]:
            leader.turn(Avator.LOOK.RIGHT)
        if keyboard[keys.UP]:
            leader.turn(Avator.LOOK.UP)

        if keyboard[keys.SPACE]: 
            pass



