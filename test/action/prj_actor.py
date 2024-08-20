import pygame
from pygame.locals import *
import os
import sys
import os
os.chdir(os.path.dirname(__file__))



class Python(pygame.sprite.Sprite):
    """パイソン"""
    MOVE_SPEED = 2.5    # 移動速度
    JUMP_SPEED = 6.0    # ジャンプの初速度
    GRAVITY = 0.2       # 重力加速度
    MAX_JUMP_COUNT = 2  # ジャンプ段数の回数

    def __init__(self, pos, blocks):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]  # 座標設定
        self.blocks = blocks  # 衝突判定用

        # ジャンプ回数
        self.jump_count = 0

        # 浮動小数点の位置と速度
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = 0.0
        self.fpvy = 0.0

        # 地面にいるか？
        self.on_floor = False

    def update(self):
        """スプライトの更新"""
        # キー入力取得
        pressed_keys = pygame.key.get_pressed()

        # 左右移動
        if pressed_keys[K_RIGHT]:
            self.image = self.right_image
            self.fpvx = self.MOVE_SPEED
        elif pressed_keys[K_LEFT]:
            self.image = self.left_image
            self.fpvx = -self.MOVE_SPEED
        else:
            self.fpvx = 0.0

        # ジャンプ
        if pressed_keys[K_SPACE]:
            if self.on_floor:
                self.fpvy = - self.JUMP_SPEED  # 上向きに初速度を与える
                self.on_floor = False
                self.jump_count = 1
            elif not self.prev_button and self.jump_count < self.MAX_JUMP_COUNT:
                self.fpvy = -self.JUMP_SPEED
                self.jump_count += 1

        # 速度を更新
        if not self.on_floor:
            self.fpvy += self.GRAVITY  # 下向きに重力をかける

        self.collision_x()  # X方向の衝突判定処理
        self.collision_y()  # Y方向の衝突判定処理

        # 浮動小数点の位置を整数座標に戻す
        # スプライトを動かすにはself.rectの更新が必要！
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

        # ボタンのジャンプキーの状態を記録
        self.prev_button = pressed_keys[K_SPACE]

    def collision_x(self):
        """X方向の衝突判定処理"""
        # パイソンのサイズ
        width = self.rect.width
        height = self.rect.height

        # X方向の移動先の座標と矩形を求める
        newx = self.fpx + self.fpvx
        newrect = Rect(newx, self.fpy, width, height)

        # ブロックとの衝突判定
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突するブロックあり
                if self.fpvx > 0:    # 右に移動中に衝突
                    # めり込まないように調整して速度を0に
                    self.fpx = block.rect.left - width
                    self.fpvx = 0
                elif self.fpvx < 0:  # 左に移動中に衝突
                    self.fpx = block.rect.right
                    self.fpvx = 0
                break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.fpx = newx

    def collision_y(self):
        """Y方向の衝突判定処理"""
        # パイソンのサイズ
        width = self.rect.width
        height = self.rect.height

        # Y方向の移動先の座標と矩形を求める
        newy = self.fpy + self.fpvy
        newrect = Rect(self.fpx, newy, width, height)

        # ブロックとの衝突判定
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突するブロックあり
                if self.fpvy > 0:    # 下に移動中に衝突
                    # めり込まないように調整して速度を0に
                    self.fpy = block.rect.top - height
                    self.fpvy = 0
                    # 下に移動中に衝突したなら床の上にいる
                    self.on_floor = True
                    self.jump_count = 0  # ジャンプカウントをリセット
                elif self.fpvy < 0:  # 上に移動中に衝突
                    self.fpy = block.rect.bottom
                    self.fpvy = 0
                break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.fpy = newy
                # 衝突ブロックがないなら床の上にいない
                self.on_floor = False

class Block(pygame.sprite.Sprite):
    """ブロック"""
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

