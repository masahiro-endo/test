#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pgzrun
from pgzero.builtins import *
from collections import deque
import random
import datetime
import time
import os
import global_value as g
from shooter_sub import *
from shooter_scene import *
os.chdir('test')


class Setting:
    class DisplayResolution():
        VGA = (640, 480)
        SVGA = (800, 600)
        XGA = (1024, 768)
    
    def is_dispay_area(pos) -> bool:
        x, y = pos
        if (0 < x < WIDTH) and (0 < y < HEIGHT):
            return True
        return False

WIDTH, HEIGHT = Setting.DisplayResolution.SVGA
g.OUTSIDE = -9999
GAP = 130

now = datetime.datetime.now()
now = now.strftime("%y%m%d") # 開始日時(記録ファイル名にする)



##### 初期化
def init():

    g.objects = []  # スプライトのリスト
    g.player = Player(WIDTH * 1 / WIDTH, HEIGHT / 2, 0, CHARA.PLAYER)
    g.bosstimer = 60 * 10 # ボスが出現する時間
    g.gameover = 0
    g.game_state = SCENE.TITLE

    g.currentScene = deque()
    g.currentScene.appendleft(TitleScene(Setting.DisplayResolution.SVGA))

    
    g.start = time.time() # スタート時刻を返す

##### ゲーム開始画面とゲームオーバー画面
def draw():
    screen.clear()

    for scene in reversed(g.currentScene):
        if scene is None:
            continue
        scene.draw(screen)
    
    if g.game_state==SCENE.TITLE:
        pass
    else:
        for sp in g.objects:
            sp.draw()


##### Pygame zeroのメイン関数とも言うべきupdata関数
# 文末当たりのpgzrun.go()実行により、この関数がループすることになる。
def update():
    
    for scene in reversed(g.currentScene):
        if scene is None:
            continue
        scene.update()
        scene.handler(keyboard)

    if g.game_state==SCENE.TITLE:
        pass        
        return

    elif g.game_state==SCENE.GAMEOVER:
        pass
        return

    g.bosstimer -= 1
    if g.bosstimer==0:
        pass
        # g.objects.append(Boss(WIDTH/2, 0, 0, CHARA.ENEMY_BOSS))  # ボス出現
    elif g.bosstimer > 0 and random.randrange(80)==0: # 敵1出現
        y = random.randrange(HEIGHT - 200) + 100
        # g.objects.append(Enemy(WIDTH, y, 0, CHARA.ENEMY_1))
    elif g.bosstimer > 0 and random.randrange(100)==0: # 敵2出現
        y = random.randrange(HEIGHT - 200) + 100
        # g.objects.append(Enemy(WIDTH, y, 0, CHARA.ENEMY_2))
    elif random.randrange(200)==0: # デブリ出現
        y = random.randrange(1, HEIGHT, 10)
        rad = random.randrange(-60, 60, 1)
        g.objects.append(Debris(WIDTH, y, rad, CHARA.DEBRIS))
    else:
        pass

    for sp in reversed(g.objects):
        sp.update()
        sp.count += 1

        if sp.hp <= 0:
            g.objects.append(Explosion(sp.x, sp.y, 0, CHARA.EXPLOSION))
            g.objects.remove(sp)  # 耐久値ゼロのスプライトを消去
            continue
        
        if not Setting.is_dispay_area(sp.pos):
            g.objects.remove(sp)  # 画面外のスプライトを消去
            continue

    if not (g.player in g.objects):
        g.scene = SCENE.GAMEOVER
        g.out_time = time.time() - g.start # ゲームオーバーまでの時間を計算

        g.currentScene.popleft()
        g.currentScene.appendleft(GameOverScene())
    
    print('bosstimer = ' + str(g.bosstimer))


##### イニシャライズとゲームの実行
init()
pgzrun.go()

