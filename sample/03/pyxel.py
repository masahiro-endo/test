import pyxel


pyxres_name = "sample.pyxres"


class App:

    def __init__(self):
        pyxel.init(160, 120)
        pyxel.mouse(True)
        pyxel.load(pyxres_name)
        pyxel.run(self.update, self.draw)

    def update(self):


    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)




if __name__ == "__main__":
    App()