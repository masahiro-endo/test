import pyxel
import random
import actor
import UI


pyxres_name = "sample.pyxres"







class App:
    def __init__(self) -> None:
        pyxel.init(160, 120)
        pyxel.mouse(True)
        pyxel.load(pyxres_name)
        self.dealer = actor.Dealer()
        self.dealer.open_deal(8)
        behaviors = ["standard", "bouncy"]
        self.gbtns_behavior = UI.ButtonContainer(behaviors, 80, 20)
        pyxel.run(self.update, self.draw)

    def update(self):
        # 入力
        msg = self.gbtns_behavior.update()
        if msg == "standard":
            self.dealer.throw(8, 40, 60, "standard")
        elif msg == "bouncy":
            self.dealer.throw(7, 40, 80, "bouncy")
        
        # 更新
        self.dealer.update()
        
    def draw(self):
        pyxel.cls(0)
        self.dealer.draw()
        self.gbtns_behavior.draw()

App()