
import random

import appconfig as gbl
from actor.effects import *



class Meth:
    
    @staticmethod
    def detect_collision():
        # 衝突判定
        for e in gbl.enemies:
            for b in gbl.bullets:
                if e.hit(b):
                    e.hp -= 1
                    if b in gbl.bullets:
                        gbl.bullets.remove(b)
                    if e.is_dead():
                        if e in gbl.enemies:
                            if e.item:
                                e.item.spawn(e.x, e.y)
                            gbl.enemies.remove(e)
                            gbl.explosions.append(Explosion(b.x, b.y))
                    else:
                        Sparks_spread.spawn(random.randint(1, 3), e)
                    break




