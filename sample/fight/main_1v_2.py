
import pyxel
import math

# 画面サイズ
SCREEN_W = 160
SCREEN_H = 120

# キャラ設定
MOVE_SPEED = 2
JUMP_SPEED = 4
GRAVITY = 0.3
ATTACK_DURATION = 10
ATTACK_RANGE = 6




class Player:
    def __init__(self, x, y, color, left_keys, right_keys, jump_key, attack_key, facing_right=True):
        self.x = x
        self.y = y
        self.vy = 0
        self.color = color
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.jump_key = jump_key
        self.attack_key = attack_key
        self.on_ground = True
        self.attacking = False
        self.attack_timer = 0
        self.hp = 5
        self.facing_right = facing_right
        self.anim_frame = 0

    def update(self):
        moving = False
        # 横移動
        if pyxel.btn(self.left_keys):
            self.x -= MOVE_SPEED
            self.facing_right = False
            moving = True
        if pyxel.btn(self.right_keys):
            self.x += MOVE_SPEED
            self.facing_right = True
            moving = True

        # アニメーションフレーム更新
        if moving:
            self.anim_frame += 1
        else:
            self.anim_frame = 0

        # ジャンプ
        if self.on_ground and pyxel.btnp(self.jump_key):
            self.vy = -JUMP_SPEED
            self.on_ground = False

        # 重力
        self.vy += GRAVITY
        self.y += self.vy

        # 地面判定
        if self.y >= SCREEN_H - 20:
            self.y = SCREEN_H - 20
            self.vy = 0
            self.on_ground = True

        # 攻撃
        if pyxel.btnp(self.attack_key) and not self.attacking:
            self.attacking = True
            self.attack_timer = ATTACK_DURATION

        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False

        # 画面外制限
        self.x = max(0, min(self.x, SCREEN_W))

    def draw(self):
        # パーツの相対位置
        head_y = self.y - 16
        body_y = self.y - 8
        arm_offset = math.sin(self.anim_frame * 0.3) * 2
        leg_offset = math.sin(self.anim_frame * 0.3 + math.pi) * 2

        # 向きによる左右反転
        dir_mult = 1 if self.facing_right else -1

        # 頭
        pyxel.circ(self.x, head_y, 4, self.color)
        # 胴
        pyxel.rect(self.x - 3, body_y, 6, 8, self.color)
        # 腕
        pyxel.rect(self.x + dir_mult * 5, body_y + arm_offset, 4, 4, self.color)
        # 足
        pyxel.rect(self.x - 2, self.y + leg_offset, 4, 4, self.color)

        # 攻撃エフェクト
        if self.attacking:
            atk_x = self.x + dir_mult * 8
            pyxel.rect(atk_x, body_y, ATTACK_RANGE, 4, 7)

    def check_attack_hit(self, opponent):
        if self.attacking:
            dir_mult = 1 if self.facing_right else -1
            hitbox_x1 = self.x + dir_mult * 8
            hitbox_x2 = hitbox_x1 + dir_mult * ATTACK_RANGE
            if hitbox_x1 > hitbox_x2:
                hitbox_x1, hitbox_x2 = hitbox_x2, hitbox_x1

            hitbox_y1 = self.y - 8
            hitbox_y2 = hitbox_y1 + 8

            if (hitbox_x1 < opponent.x + 4 and
                hitbox_x2 > opponent.x - 4 and
                hitbox_y1 < opponent.y and
                hitbox_y2 > opponent.y - 16):
                opponent.hp = max(0, opponent.hp - 1)

class Game:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Joy Mecha Fight Style 1vs1")
        self.p1 = Player(40, SCREEN_H - 20, 8, pyxel.KEY_A, pyxel.KEY_D, pyxel.KEY_W, pyxel.KEY_SPACE, facing_right=True)
        self.p2 = Player(120, SCREEN_H - 20, 11, pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_RETURN, facing_right=False)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.p1.update()
        self.p2.update()
        self.p1.check_attack_hit(self.p2)
        self.p2.check_attack_hit(self.p1)

    def draw(self):
        pyxel.cls(0)
        self.p1.draw()
        self.p2.draw()
        pyxel.text(5, 5, f"P1 HP: {self.p1.hp}", 7)
        pyxel.text(SCREEN_W - 50, 5, f"P2 HP: {self.p2.hp}", 7)

        if self.p1.hp == 0:
            pyxel.text(SCREEN_W // 2 - 20, SCREEN_H // 2, "P2 WINS!", 10)
        elif self.p2.hp == 0:
            pyxel.text(SCREEN_W // 2 - 20, SCREEN_H // 2, "P1 WINS!", 10)

if __name__ == "__main__":
    Game()





