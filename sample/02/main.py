import pyxel
from scene import SceneManager



class App:

    def __init__(self):
        self.mgr = SceneManager()
        pyxel.init(200, 200)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.mgr.update()

    def draw(self):
        pyxel.cls(0)
        self.mgr.draw()





App()