import pgzrun
import os
import random
from sample_shot_sub import *
os.chdir('test')


WIDTH = 320
HEIGHT = 480
TITLE = "PyGame Zero Title"
 
BACKGROUND = 50, 165, 165
shots = []
enemys = []

LIMIT_AXIS_Y_SHOT = 0
LIMIT_AXIS_Y_ENEMY = HEIGHT


player = Player("player", 140, 300)
dx, dy = 0, 0
 
def player_shot():
    shot = Shot("shot", player.x, player.y-16, LIMIT_AXIS_Y_SHOT)
    shots.append(shot)
    print("shots: {}発".format(len(shots)))
    # clock.schedule_unique(player_shot, 0.5)
 

def on_key_down(key):
    # キー入力をチェック
    if key == keys.SPACE:
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
        enemy = Enemy("enemy", x, y, LIMIT_AXIS_Y_ENEMY)
        enemys.append(enemy)
        print("enemys: {}体".format(len(enemys)))
     
    # プレイヤーのショット処理
    for shot in shots:
        if not shot.isRunning:
            shots.remove(shot)
        else:
            shot.update()
     
    # 敵の処理
    for enemy in enemys:
        for shot in shots:
            if shot.colliderect(enemy):
                shot.isRunning = False
                enemy.isRunning = False

        if not enemy.isRunning:
            enemys.remove(enemy)
        else:
            enemy.update()


        # プレイヤーとの当たり判定
        if player.colliderect(enemy):
            player.isRunning = False
 
     
    # プレイヤーの処理
    player.update()
 
    # 画面描画
    mydraw()
 
pgzrun.go()


