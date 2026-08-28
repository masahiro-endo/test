
import pyxel

# ゲーム設定
SCREEN_W = 160
SCREEN_H = 120
PLAYER_W = 8
PLAYER_H = 16
GROUND_Y = SCREEN_H - PLAYER_H - 8
GRAVITY = 0.5
JUMP_VELOCITY = -5
PUNCH_RANGE = 12
MAX_HP = 5

class Player:
    def __init__(self, x, color, left_key, right_key, jump_key, punch_key):
        self.x = x
        self.y = GROUND_Y
        self.vy = 0
        self.color = color
        self.left_key = left_key
        self.right_key = right_key
        self.jump_key = jump_key
        self.punch_key = punch_key
        self.hp = MAX_HP
        self.is_punching = False
        self.punch_timer = 0

    def update(self):
        # 横移動
        if pyxel.btn(self.left_key):
            self.x -= 1
        if pyxel.btn(self.right_key):
            self.x += 1

        # ジャンプ
        if pyxel.btnp(self.jump_key) and self.y >= GROUND_Y:
            self.vy = JUMP_VELOCITY

        # 重力
        self.vy += GRAVITY
        self.y += self.vy
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vy = 0

        # パンチ
        if pyxel.btnp(self.punch_key):
            self.is_punching = True
            self.punch_timer = 5

        if self.punch_timer > 0:
            self.punch_timer -= 1
        else:
            self.is_punching = False

        # 画面外制限
        self.x = max(0, min(SCREEN_W - PLAYER_W, self.x))

    def draw(self):
        pyxel.rect(self.x, self.y, PLAYER_W, PLAYER_H, self.color)
        if self.is_punching:
            # パンチのエフェクト
            if self.color == 8:  # 赤
                px = self.x + PLAYER_W
            else:  # 青
                px = self.x - 4
            pyxel.rect(px, self.y + 4, 4, 4, 7)

class Game:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Pyxel 格闘ゲーム")
        self.p1 = Player(30, 8, pyxel.KEY_A, pyxel.KEY_D, pyxel.KEY_W, pyxel.KEY_S)
        self.p2 = Player(110, 12, pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_DOWN)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.p1.update()
        self.p2.update()

        # 当たり判定（パンチ）
        if self.p1.is_punching and abs((self.p1.x + PLAYER_W/2) - (self.p2.x + PLAYER_W/2)) < PUNCH_RANGE and abs(self.p1.y - self.p2.y) < PLAYER_H:
            self.p2.hp = max(0, self.p2.hp - 1)

        if self.p2.is_punching and abs((self.p2.x + PLAYER_W/2) - (self.p1.x + PLAYER_W/2)) < PUNCH_RANGE and abs(self.p2.y - self.p1.y) < PLAYER_H:
            self.p1.hp = max(0, self.p1.hp - 1)

    def draw(self):
        pyxel.cls(0)
        # 地面
        pyxel.rect(0, SCREEN_H - 8, SCREEN_W, 8, 3)

        # プレイヤー描画
        self.p1.draw()
        self.p2.draw()

        # HPバー
        pyxel.text(5, 5, f"P1 HP: {self.p1.hp}", 7)
        pyxel.text(SCREEN_W - 40, 5, f"P2 HP: {self.p2.hp}", 7)

        # 勝敗表示
        if self.p1.hp == 0:
            pyxel.text(SCREEN_W//2 - 20, SCREEN_H//2, "P2 WINS!", 10)
        elif self.p2.hp == 0:
            pyxel.text(SCREEN_W//2 - 20, SCREEN_H//2, "P1 WINS!", 10)

# 実行
if __name__ == "__main__":
    Game()


