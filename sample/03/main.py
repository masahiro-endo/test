import pyxel
from actor import GameMaster


pyxres_name = "sample.pyxres"


class App:

    def __init__(self):        
        pyxel.init(160, 120)
        pyxel.mouse(True)
        pyxel.load(pyxres_name)

        self.gm = GameMaster()
        self.gm.grab_dice(5)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.gm.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        self.gm.draw()


App()