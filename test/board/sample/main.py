import asyncio
import sys

import pygame
from pygame.locals import *


class Player:
    def __init__(self):
        self.px = 120
        self.py = 500

    def update(self, screen, T):
        pygame.draw.rect(screen, (255, 0, 0), Rect(self.px, self.py, 50, 50), 1)  # ■
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.px -= 5  # 横方向
                elif event.key == K_RIGHT:
                    self.px += 5  # 横方向
                elif event.key == K_SPACE:
                    if T.isFire == False:
                        T.isFire = True
                        T.y = self.py
                        T.x = self.px + 25


class UFO:
    def __init__(self, x):
        self.ux = x
        self.uy = x
        self.uw = 20
        self.uh = 20
        self.uvx = 3
        self.uvy = 2
        self.uhp = 100

    def update(self, screen, T):
        self.ux = self.ux + self.uvx
        self.uy = self.uy + self.uvy
        if self.ux > 700 or self.ux < 0:
            self.uvx *= -1
        if self.uy > 600 or self.uy < 0:
            self.uvy *= -1
        # 当たり判定
        if (self.ux <= T.x <= self.ux + self.uw) and (
            self.uy <= T.y <= self.uy + self.uh
        ):
            self.uhp = 0
            T.isFire = False
        if self.uhp > 0:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                Rect(self.ux, self.uy, self.uw, self.uh),
            )  # ■


class Tama:
    def __init__(self):
        # プレイヤの初期設定
        self.x = 120
        self.y = 500
        self.vy = -5
        self.isFire = False

    def update(self, screen):
        print("isFile", self.isFire, "self.x=", self.x, "self.y=", self.y)
        # タマの処理と描画
        if self.isFire:
            self.y += self.vy
            if self.y < -10:
                self.isFire = False
            pygame.draw.circle(screen, (10, 10, 10), (self.x, self.y), 5)  # ●


async def main():
    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode((800, 600))  # 800*600の画面
    T1 = Tama()
    P1 = Player()
    Us = []
    ck = pygame.time.Clock()
    for i in range(10):
        Us.append(UFO(i * 50))
    while True:
        ck.tick(60)  # 1秒間で60フレーム
        screen.fill((255, 255, 255))  # 背景を白
        T1.update(screen)
        P1.update(screen, T1)
        for U in Us:
            U.update(screen, T1)
        pygame.display.update()  # 画面更新
        await asyncio.sleep(0)


# if __name__ == "__main__":
# main()
# asyncio.run(main())

asyncio.run(main())
