
import pyxel as px
from collections import deque
import os
import sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))

import appconfig as gbl
from constant import * 
from scenestate import * 
from actor.player import Player









class App:
    def __init__(self):
        px.init(WIDTH, HEIGHT, title="Enemy Path Array Movement")
        px.load("assets_anim.pyxres") 

        gbl.player = Player()
        gbl.enemies = []
        gbl.bullets = []
        gbl.explosions = []
        gbl.items = []
        gbl.stars = []
        gbl.obstacles = []
        gbl.score = 0
        
        gbl.stack = deque([SceneStates(self)])
        gbl.state = gbl.stack[-1]
        gbl.state.Stage1()
        px.run(self.update, self.draw)

        gbl.score = 0


    def update(self):

        gbl.stack[0].update()

        for s in gbl.stars:
            s.update()

        for o in gbl.obstacles:
            o.update()

        # ステージ初めのイントロなどで、
        # 操作を制限させるため、
        # scene 側で定義
        # gbl.player.update()scene

        for ex in gbl.explosions:
            ex.update()

        for e in gbl.enemies:
            e.update()

        for b in gbl.bullets:
            b.update()

        for i in gbl.items:
            i.update()


        gbl.obstacles = [o for o in gbl.obstacles if o.active]
        gbl.explosions = [ex for ex in gbl.explosions if not ex.is_finished()]
        gbl.enemies = [e for e in gbl.enemies if not e.is_offscreen()]
        gbl.bullets = [b for b in gbl.bullets if b.active]
        gbl.items = [i for i in gbl.items if i.active]

    def draw(self):
        px.cls(px.COLOR_BLACK)
        
        for sn in reversed(gbl.stack):
            sn.draw()

        for s in gbl.stars:
            s.draw()

        for o in gbl.obstacles:
            o.draw()

        gbl.player.draw()

        gbl.state.draw()

        for ex in gbl.explosions:
            ex.draw()

        for e in gbl.enemies:
            e.draw()

        for b in gbl.bullets:
            b.draw()

        for i in gbl.items:
            i.draw()


if __name__ == "__main__":
    App()




