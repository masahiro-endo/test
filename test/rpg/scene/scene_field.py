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
                else:
                    source = MapTool.loadmapchip(MapTool.OBJECT.STONEFLOOR)
                surface.blit(source, (j * GS, i * GS))

        return surface


class FieldScene(BaseScene):

    def __init__(self):
        self.avator = Avator()
        self.surface = MapTool.loadmap(MapTool.MAP.TOWN)

    def doEncounted(self) -> bool:
        if random.randint(0, 300) == 0:
            return True
        else:
            return False

    def trans_combatScene(self):
        g.sceneStack.appendleft(CombatScene())


    def update(self):
        super().update()

        if self.doEncounted():
            self.trans_combatScene()

    def draw(self, screen):
        super().draw(screen)
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        screen.surface.blit(self.surface, (0,0), (0, 0, WIDTH, HEIGHT))
        screen.blit(self.avator.anime[self.avator.direction][self.avator.imgnum], self.avator.pos)

    def handler(self, keyboard):
        super().handler(keyboard)
        x, y = self.avator.pos

        if keyboard[keys.RETURN]: 
            pass
        if keyboard[keys.DOWN]:
            self.avator.turn(self.avator.LOOK.DOWN)
        if keyboard[keys.LEFT]:
            self.avator.turn(self.avator.LOOK.LEFT)
        if keyboard[keys.RIGHT]:
            self.avator.turn(self.avator.LOOK.RIGHT)
        if keyboard[keys.UP]:
            self.avator.turn(self.avator.LOOK.UP)

        if keyboard[keys.SPACE]: 
            pass



