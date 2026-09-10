
import pyxel
import random
import math

pyxel.init(160, 120, title="パーティクルエフェクト")

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

particles = []

def create_explosion(x, y):
    for _ in range(50):
        particles.append(Particle(x, y))

def update():
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        create_explosion(pyxel.mouse_x, pyxel.mouse_y)
    
    for particle in particles[:]:
        particle.update()
        if particle.life <= 0:
            particles.remove(particle)
    
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    for particle in particles:
        pyxel.pset(particle.x, particle.y, 8 + particle.life % 8)

pyxel.run(update, draw)



