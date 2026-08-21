
import pyxel as px
import random

import appconfig as gbl
from context import * 
from map import *






STAR_COLORS = [px.COLOR_WHITE, 
               px.COLOR_ORANGE, 
               px.COLOR_BROWN, 
               px.COLOR_DARK_BLUE]


class Perticle:
    def __init__(self):
        self.x = random.randint(0, SCR_SIZE_MAZE)
        self.y = random.randint(0, SCR_SIZE_MAZE // 4) #描画位置を上部に絞る
        self.color = random.choice(STAR_COLORS)
        self.magnitude = random.randint(0, len(STAR_COLORS) - 1)

    def update(self):
        pass        

    def draw(self):
        # if self.magnitude == 0:
        #     px.circ(self.x + DRAW_OFFSET_X, self.y + DRAW_OFFSET_Y, 1, self.color)
        # else:
        px.pset(self.x + DRAW_OFFSET_X, self.y + DRAW_OFFSET_Y, self.color)


# 各方角ごとに星を作成
STAR_COUNT = 20
stars = [[None for _ in range(4)] for _ in range(STAR_COUNT)]
for y in range(STAR_COUNT):
    for x in range(4):
        stars[y][x] = Perticle()





class PlayerParty:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = DIRECTION_SOUTH

    def update(self):
        # 上：前進する
        if px.btnp(px.KEY_UP):
            # 前が壁であるかチェック
            if not gbl._map[self.y + VY[self.direction]][self.x + VX[self.direction]] == MAPTILE.WALL:
                self.x = self.x + VX[self.direction]
                self.y = self.y + VY[self.direction]

        # 右：右回転する
        if px.btnp(px.KEY_RIGHT):
            self.direction = self.direction + 1
            if self.direction > DIRECTION_WEST:
                self.direction = DIRECTION_NORTH
        
        # 左：左回転する
        if px.btnp(px.KEY_LEFT):
            self.direction = self.direction - 1
            if self.direction < DIRECTION_NORTH:
                self.direction = DIRECTION_WEST

    def draw(self):
        # self.__drawPlayer(0,  1, 0, 0, 0, 0)
        # self.__drawPlayer(1, 34, 0, 0, 0, 0)
        # self.__drawPlayer(2, 88, 0, 0, 0, 0)
        # self.__drawPlayer(3,100, 0, 0, 0, 0)
        pass

    def __drawPlayer(self, number, head, helm, body, weapon, shield):

        px.blt( 12, (number * 20) +  2, 1,  (head % 32) * 8,  int(head / 32) * 8,  8,  8, 0) # 頭
        px.blt( 12, (number * 20) + 10, 1,  32, 32,  8, 16, 0) # 体
        px.blt(  4, (number * 20) +  2, 1,   0, 48,  8, 16, 0) # 武器
        px.rect( 24, (number * 20) + 12, 16, 3,  5)
        px.rect( 24, (number * 20) + 15, 30, 1,  6)



