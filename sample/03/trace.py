import pyxel
import math

pyxres_name = "sample.pyxres"

WHITE = (255, 255, 255)

# ①
g = 9.8
v0 = 30
angle = 45.0
dt = 0.01
radius = 10


class diff:

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = v0*math.cos(angle*math.pi/180.0)
        self.vy = v0*math.sin(angle*math.pi/180.0)



class ball:

    def __init__(self):
        self.dv = diff()

    def update(self):

        self.dv.x = self.dv.x+self.dv.vx*dt
        self.dv.y = self.dv.y+self.dv.vy*dt
        self.dv.vx = self.dv.vx
        self.dv.vy = self.dv.vy-g*dt


    def draw(self):
        pyxel.circ(self.dv.x, self.dv.y, radius, pyxel.COLOR_ORANGE)


class App:

    def __init__(self):
        self.obj = ball()
        pyxel.init(200, 200)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.obj.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        self.obj.draw()



App()