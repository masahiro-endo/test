import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *
import os
import sys
os.chdir(os.path.dirname(__file__))


class Map:
    """マップ（プレイヤーや内部のスプライトを含む）"""
    GS = 32  # グリッドサイズ

    def __init__(self, filename):
        # スプライトグループの登録
        self.all = pygame.sprite.RenderUpdates()
        self.blocks = pygame.sprite.Group()
        Python.containers = self.all
        Block.containers = self.all, self.blocks

        # プレイヤーの作成
        self.python = Python((300,200), self.blocks)

        # マップをロードしてマップ内スプライトの作成
        self.load(filename)

        # マップサーフェイスを作成
        self.surface = pygame.Surface((self.col*self.GS, self.row*self.GS)).convert()

    def draw(self):
        """マップサーフェイスにマップ内スプライトを描画"""
        self.surface.fill((0,0,0))
        self.all.draw(self.surface)

    def update(self):
        """マップ内スプライトを更新"""
        self.all.update()

    def calc_offset(self):
        """オフセットを計算"""
        offsetx = self.python.rect.topleft[0] - SCR_RECT.width/2
        offsety = self.python.rect.topleft[1] - SCR_RECT.height/2
        return offsetx, offsety

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

        # マップからスプライトを作成
        for i in range(self.row):
            for j in range(self.col):
                if map[i][j] == 'B':
                    Block((j*self.GS, i*self.GS))  # ブロック

