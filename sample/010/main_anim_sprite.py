
import pyxel

# ゲーム定数
PLAYER_X = 60
GROUND_Y = 100
GRAVITY = 0.5
JUMP_SPEED = -5

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Landing Animation")
        pyxel.load("assets_anim.pyxres")  # .pyxres にスプライトを格納

        self.x = PLAYER_X
        self.y = GROUND_Y
        self.vy = 0
        self.state = "idle"  # idle, jump, land
        self.frame = 0
        self.land_timer = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state == "idle":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.vy = JUMP_SPEED
                self.state = "jump"
                self.frame = 0

        elif self.state == "jump":
            self.vy += GRAVITY
            self.y += self.vy
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.state = "land"
                self.land_timer = 0
                self.frame = 0

        elif self.state == "land":
            self.land_timer += 1
            # 着地アニメーションが終わったら idle に戻す
            if self.land_timer > 10:  # 10フレーム後に idle
                self.state = "idle"
                self.frame = 0

    def draw(self):
        pyxel.cls(12)

        if self.state == "idle":
            img_u = (0, 0, 16, 16)  # idle フレーム
        elif self.state == "jump":
            img_u = (16, 0, 16, 16)  # jump フレーム
        elif self.state == "land":
            # land アニメーション（2フレーム切り替え）
            img_u = (32 + (self.land_timer // 5) * 16, 0, 16, 16)

        pyxel.blt(self.x, self.y, 0, img_u[0], img_u[1], img_u[2], img_u[3], 0)

App()
