
import pyxel
import random

pyxel.init(160, 120, title="パーティクルシステム")

class Snowflake:
    def __init__(self):
        self.x = random.randint(0, 160)
        self.y = random.randint(-10, 0)
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        self.y += self.speed
        if self.y > 120:
            self.y = random.randint(-10, 0)
            self.x = random.randint(0, 160)

snowflakes = [Snowflake() for _ in range(50)]

def update():
    for snowflake in snowflakes:
        snowflake.update()
    
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(1)
    for snowflake in snowflakes:
        pyxel.pset(snowflake.x, snowflake.y, 7)

pyxel.run(update, draw)


