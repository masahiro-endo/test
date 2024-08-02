#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pgzrun
import math
import random
import datetime
import time
import csv

WIDTH = 1000
HEIGHT = 600  
OUTSIDE = 999
GAP = 130

now = datetime.datetime.now()
now = now.strftime("%y%m%d") # 開始日時(記録ファイル名にする)

# キャラクター情報のクラス
class Characlass:
    def __init__(self, filename, hp ,enemy):
        self.imagename = filename  # 画像ファイル名
        self.hp = hp               # ヒットポイント
        self.enemy = enemy         # 敵フラグ True

##### キャラクターの定義
charas = []
# 0:爆発
charas.append(Characlass("star.png", 1, False))
# 1:自機弾
charas.append(Characlass("mushroom_red.png",1,False))
# 2:自機
charas.append(Characlass("alien.png", 2, False))
# 3:敵弾
charas.append(Characlass("fireball.png", 1,True))
# 4:敵1
charas.append(Characlass("fly_fly1.png", 1, True))
# 5:敵2
charas.append(Characlass("fish_swim1.png", 2, True))
# 6:ボス
charas.append(Characlass("snail_walk1.png",15,True))
# 7:隕石
pipe_bottom = Actor('rock_moss_alt', anchor=('left', 'top'))

# スプライト(ゲーム背景とは別に動く画像)のクラス。Actorクラスを継承
# クラスでない記述例は、上記の7静体
class Spclass(Actor):
    def __init__(self, x, y, angle, num):
        Actor.__init__(self,charas[num].imagename,(x,y))
        self.angle = angle       # 角度
        self.hp = charas[num].hp # ヒットポイント
        self.count = 0           # カウンタ
        self.num = num           # キャラクタNo

# 爆発マークのクラス。Spclassクラスを継承
class Explosion(Spclass):
    def update(self):
        # カウント20超えると、表示を消滅する
        if self.count > 20: self.x = OUTSIDE

# 自機弾のクラス。Spclassクラスを継承
class Shot(Spclass):
    def update(self):
        # 弾の弾道や速度を決める(関数に入れて戻り値)
        self.pos = spritemove(self.pos, self.angle, 8) 
        # 敵との衝突範囲を判定
        hitbox = Rect((self.x-15, self.y-15), (30, 30))
        for sp in objects:
            if charas[sp.num].enemy==False or sp.hp==99:
                continue
            if sp.colliderect(hitbox): # アタリ判定内に入ると爆発
                objects.append(Explosion(sp.x, sp.y, 0, 0))
                self.x = OUTSIDE
                sp.hp -= 1
                break

# 自機のクラス。Spclassクラスを継承
class Player(Spclass):
    def update(self):
        # キーボードで機体を操作する。Pygame zeroではこれが可読性良い
        if keyboard.up   : self.y -= 4
        if keyboard.down : self.y += 4
        if keyboard.left : self.x -= 4
        if keyboard.right: self.x += 4
        if self.x < 35: self.x = 35
        if self.y < 35: self.y = 35
        if self.x > (WIDTH-35 ): self.x = WIDTH-35
        if self.y > (HEIGHT-35): self.y = HEIGHT-35
        if keyboard.space!=0 and (self.count % 16)==0:
            # 鉄砲音を鳴らす
            sounds.eep.play()
            # 5方向へ弾を打つ(Shot関数に代入してその戻り値)
            objects.append(Shot(self.x, self.y,  -90, 1))
            objects.append(Shot(self.x, self.y,  -60, 1))
            objects.append(Shot(self.x, self.y,  -30, 1))
            objects.append(Shot(self.x, self.y,  0, 1))
            objects.append(Shot(self.x, self.y,  30, 1))

        # 衝突判定
        hitbox = Rect((self.x-10,self.y-10), (20,20))
        for sp in objects:
            if charas[sp.num].enemy == True:
                if sp.colliderect(hitbox):
                    self.hp -= 1 # 相手のHPが減少
                    sp.hp -= 1 # 自機のHPが減少
                    sp.image = 'alien_hurt.png'
                    sp.image = 'alien.png'
                    break
            # 隕石にぶつかるとしぼう
            if sp.colliderect(pipe_bottom):
                sp.dead = True
                sp.hp -= 1 # 自機のHPが減少
                sp.image = 'alien_hurt.png'
                sp.image = 'alien.png'
                break

# 敵弾のクラス。Spclassクラスを継承
class EnemyShot(Spclass):
    def update(self):
        self.pos = spritemove(self.pos, self.angle, 4) # 弾の角度や速度
        for sp in objects:
            if sp.colliderect(pipe_bottom):
                #self.hp -= 1
                sp.hp -= 1
                break

# 敵のクラス。Spclassクラスを継承
class Enemy(Spclass):
    def update(self):
        self.x -= 2
        self.y -= int((self.count % 200) / 100) * 2  - 1 # ジグザグ移動
        
        if random.randrange(80) != 0: return # 敵の出現率
        px, py = player.pos
        rad = math.atan2(py - self.y, px - self.x) # 敵と自機の方角
        newangle = math.degrees(rad) # ラジアンから角度へ変換
        newsp = EnemyShot(self.x, self.y, newangle, 3)
        objects.append(newsp)

# ボスのクラス。Spclassクラスを継承
class Boss(Spclass):
    def update(self):
        if self.count < 100: self.y += 1
        else:
            rad = math.radians(self.count - 100)
            self.y = (HEIGHT / 2) + (math.sin(rad) * 200) # 上下に動く
        if self.count > 150 and (self.count % 5) == 0:
            newangle = (self.count * 4) % 360 # 全方向へ
            objects.append(EnemyShot(self.x, self.y, newangle, 3))

##### 関数
# 指定した角度に移動
# 引数を極座標系定義で受け取り、直行座標系へ変換する
def spritemove(pos, angle, speed):
    x, y = pos
    rad = math.radians(angle)
    x += speed  * (math.cos(rad))
    y += speed  * (math.sin(rad))
    
    return x, y

##### 初期化
def init():
    global player, objects, bosstimer
    global titlemode, gameover, stars
    global start
    
    stars = []
    for i in range(10):
        pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
        stars.append(Rect(pos,(3, 3)))

    objects = []  # スプライトのリスト
    player = Player(WIDTH * 1 / 5, HEIGHT / 2, 0, 2)
    objects.append(player)  # 自機をリストに格納
    bosstimer = 60 * 10 # ボスが出現する時間
    titlemode = True
    gameover = 0
    
    start = time.time() # スタート時刻を返す

##### ゲーム開始画面とゲームオーバー画面
def draw():
    screen.clear()

    pipe_bottom.draw() # 隕石は動き続ける
    
    for rect in stars:
        screen.draw.rect(rect, 'WHITE')
    if titlemode == True:
        screen.draw.text('Alien Shooter Game\n            by Pygame Zero', \
                         left=150,top=240,fontsize=64,color='YELLOW')
    else:
        for sp in objects:
            sp.draw()
        if gameover > 0:
            screen.draw.text("Game Over\n\n    SCORE TIME -> {0:.1f}s".format(out_time), \
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
    global bosstimer, gameover, titlemode
    global start, out_time
    
    update_pipes()
    
    if titlemode == True:
        # スペースを押すとゲーム開始
        if keyboard.space: titlemode = False
        start = time.time()
        out_time = 0
        
        return

    for i in range(len(stars)):
        stars[i].x -= (i+1)  # 星を右から左へ動かす
        if stars[i].x < 0:
            stars[i].x = WIDTH

    bosstimer -= 1
    if bosstimer==0:
        objects.append(Boss(WIDTH/2, 0, 0, 6))  # ボス出現
    elif bosstimer > 0 and random.randrange(80)==0: # 敵1出現
        y = random.randrange(WIDTH - 200) + 100
        objects.append(Enemy(y, 0, 0, 4))
    elif bosstimer > 0 and random.randrange(100)==0: # 敵2出現
        y = random.randrange(WIDTH - 200) + 100
        objects.append(Enemy(y, 0, 0, 5))
    #else:
    #    bosstimer = 60 * 1

    for sp in objects:
        sp.update()
        sp.count += 1
        if sp.hp <= 0:
            objects.append(Explosion(sp.x, sp.y, 0, 0))
            sp.x = OUTSIDE
        if sp.x<-35 or sp.x>(HEIGHT+35) or sp.y<-35 or sp.y>(WIDTH+35):
            if sp.num == 6:
                bosstimer = 60 * 10
            objects.remove(sp)  # 画面外のスプライトを消去

    if gameover == 0:
        if (player in objects) == False:
            gameover = 1
            out_time = time.time() - start # ゲームオーバーまでの時間を計算
            mylist = ['time[s]', out_time]
            with open(now + '_record_Alien_Shooter_by_Pygame_Zero.csv', 'a', encoding="utf-8") as f:
                writer = csv.writer(f, lineterminator='\n') # 改行コード
                writer.writerow(mylist) 
    else:
        gameover += 1
        if gameover > 180:
            init() # 時間を経て初期値へリセット
    print('gameover  = ' + str(gameover))
    print('bosstimer = ' + str(bosstimer))

##### イニシャライズとゲームの実行
init()
pgzrun.go()

