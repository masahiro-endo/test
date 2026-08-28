
import pyxel as px

import appconfig as gbl
from actor import *
from constant import * 
from scenestate import * 









class App:
    def __init__(self):
        px.init(WIDTH, HEIGHT, title="Enemy Path Array Movement")
        px.load("assets_anim.pyxres") 

        gbl.player = Player()
        gbl.enemies = []
        gbl.bullets = []
        gbl.explosions = []
        gbl.score = 0
        
        gbl.state = SceneStates(self)
        gbl.state.Stage1()
        px.run(self.update, self.draw)

        gbl.score = 0


    def update(self):

        gbl.player.update()

        for ex in gbl.explosions:
            ex.update()

        for e in gbl.enemies:
            e.update()

        gbl.state.update()

        for b in gbl.bullets:
            b.update()

        for ex in gbl.items:
            ex.items()

        gbl.explosions = [ex for ex in gbl.explosions if not ex.is_finished()]
        gbl.enemies = [e for e in gbl.enemies if not e.is_offscreen()]
        gbl.bullets = [b for b in gbl.bullets if b.active]
        gbl.items = [b for b in gbl.items if b.active]

    def draw(self):
        px.cls(0)
        
        # # 経路表示（デバッグ用）
        # for ptx, pty in self.path:
        #     px.circ(ptx, pty, 2, 5)

        gbl.player.draw()

        gbl.state.draw()

        for ex in gbl.explosions:
            ex.draw()

        for e in gbl.enemies:
            e.draw()

        for b in gbl.bullets:
            b.draw()



if __name__ == "__main__":
    App()




