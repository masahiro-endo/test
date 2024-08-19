import pgzrun
from pgzero.builtins import *
from collections import deque
import os
import sys
import global_value as g
from proj_sub import *
from proj_scene import *
from proj_control import *
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))




class Game:
    class Setting:
        class DisplayResolution():
            VGA = (640, 480)
            SVGA = (800, 600)
            XGA = (1024, 768)
        
        def is_dispay_area(pos: tuple) -> bool:
            x, y = pos
            if (0 < x < WIDTH) and (0 < y < HEIGHT):
                return True
            return False

    def init():

        g.objects = []  # スプライトのリスト
        g.playerRemain = 2 # 残機
        g.player = None
        g.bosstimer = 60 * 10 # ボスが出現する時間
        g.game_state = SCENE.TITLE

        g.sceneStack = deque()
        g.sceneStack.appendleft(TitleScene(Game.Setting.DisplayResolution.SVGA))
        
        g.OUTSIDE = -9999


WIDTH, HEIGHT = Game.Setting.DisplayResolution.SVGA






##### ゲーム開始画面とゲームオーバー画面
def draw():
    screen.clear()

    for scene in reversed(g.sceneStack):
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
    
    for scene in reversed(g.sceneStack):
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

    elif g.game_state==SCENE.WINDOW_OPEN:
        pass
        return
    else:
        pass

    g.bosstimer -= 1

    for sp in reversed(g.objects):
        sp.update()
        sp.count+=1

        if sp.hp<=0:
            g.objects.append(Explosion(sp.x, sp.y, 0, CHARA.EXPLOSION))
            g.objects.remove(sp)  # 耐久値ゼロのスプライトを消去
            continue
        
        if not Game.Setting.is_dispay_area(sp.pos):
            g.objects.remove(sp)  # 画面外のスプライトを消去
            continue

    if player_isDead():
        if player_isRemain():
            g.sceneStack[0].playerReveal(WIDTH, HEIGHT)
            return

        trans_gameOver()


    print('bosstimer = ' + str(g.bosstimer))






##### イニシャライズとゲームの実行
Game.init()
pgzrun.go()

