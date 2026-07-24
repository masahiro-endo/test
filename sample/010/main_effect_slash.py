# Python
import pyxel

class RPGBattle:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel RPG Battle")
        self.attack_frame = 0
        self.attacking = False
        self.slash_x = 80
        self.slash_y = 60
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.attacking = True
            self.attack_frame = 0

        if self.attacking:
            self.attack_frame += 1
            if self.attack_frame > 5:  # エフェクト表示時間
                self.attacking = False

    def draw(self):
        pyxel.cls(0)
        # プレイヤーと敵表示
        pyxel.rect(40, 50, 16, 16, 11)  # プレイヤー
        pyxel.rect(100, 50, 16, 16, 8)  # 敵

        # 斬撃エフェクト
        if self.attacking:
            # pyxel.line(self.slash_x, self.slash_y,
            #            self.slash_x + self.attack_frame*8,
            #            self.slash_y - self.attack_frame*4, 7)  # 白線
            pyxel.line(self.slash_x, self.slash_y,
                       self.slash_x + self.attack_frame*8,
                       self.slash_y + self.attack_frame*4, 7)

RPGBattle()

