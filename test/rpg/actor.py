import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *
import random
from enum import IntEnum, Enum, auto
from typing import Any, Dict
from collections import deque

import global_value as g
from scene.scene import *




GS = 32




class BaseCharacter:

    def __init__(self):
        self.hp = 1

    def is_dead(self)->bool:
        res = False
        if self.hp < 0:
            res = True
        return res

    def __str__(self):
        return "CHARA,%s,%d,%d,%d,%d,%s" % (self.name,self.x,self.y,self.direction,self.movetype,self.message)


class Player(BaseCharacter):
    def __init__(self, name, job):
        super().__init__()
        self.name = name
        self.hp = AvatorTool.Params[job].hp
        self.mp = AvatorTool.Params[job].mp

class Enemy(BaseCharacter):
    def __init__(self, name, job):
        self.name = name
        self.hp = 10
        self.mp = 10



class BaseParty():
    # パーティーメンバーのリスト
    member = []

    def __init__(self):
        self.member = deque()

    def addMember(self, chr):
        self.member.append(chr)

    def removeMember(self, idx):
        try:
            del self.member[idx]
        except:
            raise Exception(
                "specified a member who doesn't exist.：" + str(idx))


class PlayerParty(BaseParty):

    # 追従キャラの位置・方向保存
    class History:
        def __init__(self, rect, direction):
            self.rect = rect
            self.direction = direction

    class PARTYACTION:
        ATTACK = auto()
        TALK = auto()
        RUN = auto()

    def __init__(self):
        super().__init__()

        self.avator = deque()
        self.footstamp = deque()

        if __debug__:
            print("PlayerParty : Initialized.")

    def set_footstamp(self, rect, direction):
        MAX_LEN = 10
        self.footstamp.appendleft(self.History(rect, direction))
        for i in range(len(self.footstamp) - MAX_LEN):
            self.footstamp.pop()

    def set_memberPos(self):
        for i in range(len(self.member)):
            if len(self.footstamp) > (i*5):
                history = self.footstamp[i*5]
                x = history.rect.left
                y = history.rect.top
                self.avator[i].pos = (x, y)
                self.avator[i].rect = history.rect
                self.avator[i].direction = history.direction

    def initialize(self):
        self.__init__()
        self.footstamp.clear()

    def addMember(self, chr: Player):
        if len(self.member) < 5:
            self.member.append(chr)
            self.avator.append(chr)
        else:
            raise Exception("can't add a member.")



class EnemyParty(BaseParty):

    def __init__(self):
        super().__init__()

        if __debug__:
            print("PlayerParty : Initialized.")

    def initialize(self) -> None:
        self.__init__()

    def addMember(self, chr: Enemy):
        if len(self.member) < 5:
            self.member.append(chr)
        else:
            raise Exception("can't add a member.")



TRANS_COLOR = (190,179,145)  # マップチップの透明色



class AvatorTool():

    class JOB(IntEnum):
        SWORDMAN = auto()
        WHITECAT = auto()

    class TRIBE(IntEnum):
        SLIME = auto()
        WOLF = auto()

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
    Params[TRIBE.SLIME]    = Parameter(None,10, 10)
    Params[TRIBE.WOLF]    = Parameter(None,20, 20)

    @staticmethod
    def get_charachip(job)->Any:
        res = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        # image = pygame.image.load(f"{os.path.dirname(__file__)}{AvatorTool.Params[job].filename}").convert()
        image = pygame.image.load(f"{os.path.dirname(__file__)}/{AvatorTool.Params[job].filename}").convert()

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

    def __init__(self, job):
        self.objects = []
        self.anime=[]
        self.anime = AvatorTool.get_charachip(job)

        self.imgnum = 0
        self.direction = self.LOOK.DOWN

        self.pos = 0, 0
        self.rect = Rect(self.pos[0], self.pos[1], GS, GS)
        self.spd = self.WALK.NORMAL
        
    def is_movable(self, x, y)->bool:
        res = True
        rect = Rect(x, y, self.rect.width, self.rect.height) 
        for obj in g.blocks:
            if not pygame.Rect.colliderect(rect, obj.rect):
                continue
            res = False
            break
        return res

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
                
                if self.is_movable(x, y):
                    self.pos = x, y
                    self.rect = Rect(self.pos[0], self.pos[1], GS, GS)
                    self.imgnum = (self.imgnum + 1) % self.LOOK.LENGTH
                    g.party.set_footstamp(self.rect, self.direction)
                    g.party.set_memberPos()



class Block():
    def __init__(self, rect):
        self.rect = rect

