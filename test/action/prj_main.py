#!/usr/bin/env python
import pygame
from pygame.locals import *
import os
import sys
import os
os.chdir(os.path.dirname(__file__))



SCR_RECT = Rect(0, 0, 640, 480)

class PyAction:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("マップスクロール")

        # 画像のロード
        Python.left_image = load_image("python.png", -1)                     # 左向き
        Python.right_image = pygame.transform.flip(Python.left_image, 1, 0)  # 右向き
        Block.image = load_image("block.png", -1)

        # マップのロード
        self.map = Map("data/test.map")

        # メインループ
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def update(self):
        self.map.update()

    def draw(self, screen):
        self.map.draw()

        # オフセッとに基づいてマップの一部を画面に描画
        offsetx, offsety = self.map.calc_offset()

        # 端ではスクロールしない
        if offsetx < 0:
            offsetx = 0
        elif offsetx > self.map.width - SCR_RECT.width:
            offsetx = self.map.width - SCR_RECT.width

        if offsety < 0:
            offsety = 0
        elif offsety > self.map.height - SCR_RECT.height:
            offsety = self.map.height - SCR_RECT.height

        # マップの一部を画面に描画
        screen.blit(self.map.surface, (0,0), (offsetx, offsety, SCR_RECT.width, SCR_RECT.height))

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()




if __name__ == "__main__":
    PyAction()
