#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pgzrun
from pgzero.builtins import *
import random
import datetime
import time
import csv
import os
import shooter_global as g
from shooter_sub import *
os.chdir('test')


WIDTH = 1000
HEIGHT = 600  
g.OUTSIDE = 999
GAP = 130

now = datetime.datetime.now()
now = now.strftime("%y%m%d") # 開始日時(記録ファイル名にする)



##### 初期化
def init():
    # global player, objects, bosstimer
    # global titlemode, gameover, stars
    # global start
    
    g.stars = []
    for i in range(10):
        pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
        g.stars.append(Rect(pos,(3, 3)))

    g.objects = []  # スプライトのリスト
    g.player = Player(WIDTH * 1 / 5, HEIGHT / 2, 0, 2)
    g.objects.append(g.player)  # 自機をリストに格納
    g.bosstimer = 60 * 10 # ボスが出現する時間
    g.titlemode = True
    g.gameover = 0
    
    g.start = time.time() # スタート時刻を返す

##### ゲーム開始画面とゲームオーバー画面
def draw():
    screen.clear()

    pipe_bottom.draw() # 隕石は動き続ける
    
    for rect in g.stars:
        screen.draw.rect(rect, 'WHITE')
    if g.titlemode == True:
        screen.draw.text('Alien Shooter Game\n            by Pygame Zero', \
                         left=150,top=240,fontsize=64,color='YELLOW')
    else:
        for sp in g.objects:
            sp.draw()
        if g.gameover > 0:
            screen.draw.text("Game Over\n\n    SCORE TIME -> {0:.1f}s".format(g.out_time), \
                             left=200,top=240,fontsize=64,color='RED')
##### 隕石左へ消える
def reset_pipes():
    pipe_gap_y = random.randint(200, HEIGHT - 200)
    pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)
##### 隕石右から現れる
def update_pipes():
    pipe_bottom.left -= 3
    if pipe_bottom.right < 0:
        reset_pipes()

##### Pygame zeroのメイン関数とも言うべきupdata関数
# 文末当たりのpgzrun.go()実行により、この関数がループすることになる。
def update():
    
    update_pipes()
    
    if g.titlemode == True:
        # スペースを押すとゲーム開始
        if keyboard.space: 
            g.titlemode = False
            g.start = time.time()
            g.out_time = 0
        
        return

    for i in range(len(g.stars)):
        g.stars[i].x -= (i+1)  # 星を右から左へ動かす
        if g.stars[i].x < 0:
            g.stars[i].x = WIDTH

    g.bosstimer -= 1
    if g.bosstimer==0:
        g.objects.append(Boss(WIDTH/2, 0, 0, 6))  # ボス出現
    elif g.bosstimer > 0 and random.randrange(80)==0: # 敵1出現
        y = random.randrange(WIDTH - 200) + 100
        g.objects.append(Enemy(y, 0, 0, 4))
    elif g.bosstimer > 0 and random.randrange(100)==0: # 敵2出現
        y = random.randrange(WIDTH - 200) + 100
        g.objects.append(Enemy(y, 0, 0, 5))
    #else:
    #    bosstimer = 60 * 1

    for sp in g.objects:
        sp.update()
        sp.count += 1
        if sp.hp <= 0:
            g.objects.append(Explosion(sp.x, sp.y, 0, 0))
            sp.x = g.OUTSIDE
        if sp.x<-35 or sp.x>(HEIGHT+35) or sp.y<-35 or sp.y>(WIDTH+35):
            if sp.num == 6:
                g.bosstimer = 60 * 10
            g.objects.remove(sp)  # 画面外のスプライトを消去

    if g.gameover == 0:
        if (g.player in g.objects) == False:
            g.gameover = 1
            g.out_time = time.time() - g.start # ゲームオーバーまでの時間を計算
            mylist = ['time[s]', g.out_time]
            with open(now + '_record_Alien_Shooter_by_Pygame_Zero.csv', 'a', encoding="utf-8") as f:
                writer = csv.writer(f, lineterminator='\n') # 改行コード
                writer.writerow(mylist) 
    else:
        g.gameover += 1
        if g.gameover > 180:
            init() # 時間を経て初期値へリセット
    print('gameover  = ' + str(g.gameover))
    print('bosstimer = ' + str(g.bosstimer))

##### イニシャライズとゲームの実行
init()
pgzrun.go()

