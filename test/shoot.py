import pgzrun
import os
import random
from shoot_sub import *
os.chdir('test')


WIDTH = 320
HEIGHT = 480
TITLE = "PyGame Zero Title"
 
BACKGROUND = 50, 165, 165
shots = []
enemys = []




player = Player("player")
dx, dy = 0, 0
 
def player_shot():
    shot = Shot("shot", player.x, player.y-16)
    shots.append(shot)
    print("shots: {}発".format(len(shots)))
    clock.schedule_unique(player_shot, 0.5)
 
player_shot()
 
def on_mouse_down(pos):
    global dx, dy
    player.isMoving = True
    x, y = pos
    dx = player.x - x
    dy = player.y - y
 
def on_mouse_up():
    player.isMoving = False
 
def on_mouse_move(pos):
    if player.isMoving:
        x, y = pos
        player.x = dx + x
        player.y = dy + y 
 
def mydraw():
    screen.fill(BACKGROUND)
    player.draw()
    for shot in shots:
        shot.draw()
    for enemy in enemys:
        enemy.draw()
 
def update():
    # 敵の発生
    if random.randint(1, 100) == 1:
        x = random.randint(0, WIDTH)
        y = 0
        enemy = Enemy("enemy", x, y)
        enemys.append(enemy)
        print("enemys: {}体".format(len(enemys)))
     
    # プレイヤーのショット処理
    for shot in shots:
        if shot.isRunning == False:
            shots.remove(shot)
        else:
            shot.update()
     
    # 敵の処理
    for enemy in enemys:
        # プレイヤーとの当たり判定
        if player.colliderect(enemy):
            player.isRunning = False
 
        if enemy.isRunning == False:
            enemys.remove(enemy)
        else:
            enemy.update()
     
    # プレイヤーの処理
    player.update()
 
    # 画面描画
    mydraw()
 
pgzrun.go()


