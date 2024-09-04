import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *
import random
from enum import IntEnum, Enum, auto
from typing import Any, Dict

import global_value as g
from scene.scene import *




GS = 32




class Character:

    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def __str__(self):
        return "CHARA,%s,%d,%d,%d,%d,%s" % (self.name,self.x,self.y,self.direction,self.movetype,self.message)


class Player(Character):
    def __init__(self, name, job):
        self.name = name
        self.hp = AvatorTool.Params[job].hp
        self.mp = AvatorTool.Params[job].mp

    def update(self):
        pass

class Enemy(Character):
    def __init__(self):
        super().__init__()



class Party(object):
    # パーティーメンバーのリスト
    memberList = []

    def __init__(self):
        self.memberList = []

    def addMember(self, chr: Character) -> None:
        self.memberList.append(chr)

    def removeMember(self, idx: int) -> None:
        try:
            del self.memberList[idx]
        except:
            raise Exception(
                "specified a member who doesn't exist.：" + str(idx))


class PlayerParty(Party):

    def __init__(self):
        super().__init__()

        if __debug__:
            print("PlayerParty : Initialized.")

    def initialize(self) -> None:
        self.__init__()

    def addMember(self, chr: Player) -> None:
        if len(self.memberList) < 5:
            self.memberList.append(chr)
        else:
            raise Exception("can't add a member.")



class EnemyParty(Party):

    def __init__(self):
        super().__init__()

        if __debug__:
            print("PlayerParty : Initialized.")

    def initialize(self) -> None:
        self.__init__()

    def addMember(self, chr: Enemy) -> None:
        if len(self.memberList) < 5:
            self.memberList.append(chr)
        else:
            raise Exception("can't add a member.")



TRANS_COLOR = (190,179,145)  # マップチップの透明色



class AvatorTool():

    class JOB(IntEnum):
        SWORDMAN = auto()
        WHITECAT = auto()

    class Parameter:
        def __init__(self, filename, hp, mp):
            self.filename = filename
            self.hp = hp
            self.mp = mp

    Params: Dict[Enum, Any] = {
            JOB.SWORDMAN    : Parameter,
            JOB.WHITECAT    : Parameter,
    }

    Params[JOB.SWORDMAN]    = Parameter("/images/swordman_male.png",50, 10)
    Params[JOB.WHITECAT]    = Parameter("/images/white_cat.png",999, 999)

    @staticmethod
    def get_charachip(job)->Any:
        res = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        # image = pygame.image.load(f"{os.path.dirname(__file__)}{AvatorTool.Params[job].filename}").convert()
        image = pygame.image.load(f"{os.path.dirname(__file__)}/../{AvatorTool.Params[job].filename}").convert()

        for y in range(4):
            for x in range(4):
                res[y][x] = image.subsurface(Rect(x * GS, y * GS, GS, GS))
                res[y][x].set_colorkey(TRANS_COLOR, RLEACCEL)
    
        return res



class Avator():
    class LOOK(IntEnum):
        DOWN = 0
        LEFT = 1
        RIGHT = 2
        UP = 3
        LENGTH = 4

    class WALK(IntEnum):
        NORMAL = 5

    def __init__(self):

        self.objects = []
        self.anime=[]
        self.anime = AvatorTool.get_charachip(AvatorTool.JOB.WHITECAT)

        self.imgnum = 0
        self.direction = self.LOOK.DOWN

        self.pos = 0, 0
        self.spd = self.WALK.NORmAL
        
    def turn(self, direction):
            if not self.direction==direction:
                self.direction = direction
                self.imgno = 0
            else:
                x, y = self.pos
                if self.direction==self.LOOK.UP:
                    y -= self.spd
                if self.direction==self.LOOK.DOWN:
                    y += self.spd
                if self.direction==self.LOOK.LEFT:
                    x -= self.spd
                if self.direction==self.LOOK.RIGHT:
                    x += self.spd
                self.pos = x, y
                self.imgnum = (self.imgnum + 1) % self.LOOK.LENGTH
