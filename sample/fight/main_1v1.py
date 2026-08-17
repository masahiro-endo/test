
import pyxel

# Game constants
SCREEN_WIDTH = 220
SCREEN_HEIGHT = 150
GROUND_Y = 120
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 24
MOVE_SPEED = 2
JUMP_SPEED = -6
GRAVITY = 0.4
ATTACK_RANGE = 14
ATTACK_COOLDOWN = 20
KNOCKBACK = 3
MAX_HP = 5
ROUND_RESET_DELAY = 90  # frames (~1.5 seconds at 60fps)

class Player:
    def __init__(self, x, color, left_key, right_key, jump_key, attack_key, face_dir=1):
        self.spawn_x = x
        self.x = x
        self.y = GROUND_Y - PLAYER_HEIGHT
        self.vy = 0
        self.color = color
        self.left_key = left_key
        self.right_key = right_key
        self.jump_key = jump_key
        self.attack_key = attack_key
        self.face_dir = face_dir
        self.is_attacking = False
        self.attack_timer = 0
        self.hp = MAX_HP
        self.state = "idle"
        self.anim_frame = 0

    def reset(self):
        self.x = self.spawn_x
        self.y = GROUND_Y - PLAYER_HEIGHT
        self.vy = 0
        self.hp = MAX_HP
        self.is_attacking = False
        self.attack_timer = 0
        self.state = "idle"
        self.anim_frame = 0

    def update(self, opponent):
        # Face opponent
        if opponent.x > self.x:
            self.face_dir = 1
        else:
            self.face_dir = -1

        moving = False
        if pyxel.btn(self.left_key):
            self.x -= MOVE_SPEED
            moving = True
        if pyxel.btn(self.right_key):
            self.x += MOVE_SPEED
            moving = True

        # Jump
        if pyxel.btnp(self.jump_key) and self.on_ground():
            self.vy = JUMP_SPEED
            self.state = "jump"

        # Gravity
        self.vy += GRAVITY
        self.y += self.vy

        # Ground collision
        if self.y >= GROUND_Y - PLAYER_HEIGHT:
            self.y = GROUND_Y - PLAYER_HEIGHT
            self.vy = 0

        # Attack
        if pyxel.btnp(self.attack_key) and self.attack_timer == 0:
            self.is_attacking = True
            self.attack_timer = ATTACK_COOLDOWN
            self.state = "attack"

        # Attack cooldown
        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.is_attacking = False

        # State update
        if self.on_ground() and not self.is_attacking:
            if moving:
                self.state = "walk"
            else:
                self.state = "idle"

        # Keep inside screen
        self.x = max(0, min(SCREEN_WIDTH - PLAYER_WIDTH, self.x))

        # Animation frame update
        self.anim_frame = (self.anim_frame + 1) % 20

    def on_ground(self):
        return self.y >= GROUND_Y - PLAYER_HEIGHT

    def hit(self, attacker_dir):
        self.hp = max(0, self.hp - 1)
        self.state = "hit"
        self.x += attacker_dir * KNOCKBACK

    def draw(self):
        # Animation variations
        if self.state == "idle":
            body_h = PLAYER_HEIGHT
        elif self.state == "walk":
            body_h = PLAYER_HEIGHT - (self.anim_frame // 5 % 2)  # small bobbing
        elif self.state == "jump":
            body_h = PLAYER_HEIGHT
        elif self.state == "attack":
            body_h = PLAYER_HEIGHT
        elif self.state == "hit":
            body_h = PLAYER_HEIGHT - 2
        else:
            body_h = PLAYER_HEIGHT

        # Draw body
        pyxel.rect(self.x, self.y, PLAYER_WIDTH, body_h, self.color)

        # Draw eyes
        eye_x = self.x + (3 if self.face_dir == 1 else PLAYER_WIDTH - 5)
        pyxel.rect(eye_x, self.y + 5, 2, 2, 7)

        # Draw attack hitbox
        if self.is_attacking:
            atk_x = self.x + (PLAYER_WIDTH if self.face_dir == 1 else -ATTACK_RANGE)
            pyxel.rect(atk_x, self.y + 8, ATTACK_RANGE, 4, 10)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Street Fighter Style")
        self.p1 = Player(50, 8, pyxel.KEY_A, pyxel.KEY_D, pyxel.KEY_W, pyxel.KEY_SPACE, face_dir=1)
        self.p2 = Player(150, 11, pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_RETURN, face_dir=-1)
        self.round_over = False
        self.winner = None
        self.reset_timer = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.round_over:
            self.reset_timer -= 1
            if self.reset_timer <= 0:
                self.p1.reset()
                self.p2.reset()
                self.round_over = False
                self.winner = None
            return

        self.p1.update(self.p2)
        self.p2.update(self.p1)
        self.check_attacks()

        # Win condition
        if self.p1.hp == 0:
            self.end_round("P2")
        elif self.p2.hp == 0:
            self.end_round("P1")

    def end_round(self, winner):
        self.round_over = True
        self.winner = winner
        self.reset_timer = ROUND_RESET_DELAY

    def check_attacks(self):
        # Player 1 attacking Player 2
        if self.p1.is_attacking:
            if self.attack_hit(self.p1, self.p2):
                self.p2.hit(self.p1.face_dir)

        # Player 2 attacking Player 1
        if self.p2.is_attacking:
            if self.attack_hit(self.p2, self.p1):
                self.p1.hit(self.p2.face_dir)

    def attack_hit(self, attacker, defender):
        if attacker.face_dir == 1:
            return (attacker.x + PLAYER_WIDTH <= defender.x <= attacker.x + PLAYER_WIDTH + ATTACK_RANGE
                    and abs(attacker.y - defender.y) < PLAYER_HEIGHT)
        else:
            return (defender.x + PLAYER_WIDTH >= attacker.x - ATTACK_RANGE >= defender.x
                    and abs(attacker.y - defender.y) < PLAYER_HEIGHT)

    def draw(self):
        pyxel.cls(0)
        # Ground
        pyxel.rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y, 3)

        # Draw players
        self.p1.draw()
        self.p2.draw()

        # Draw HP bars
        pyxel.text(5, 5, f"P1 HP: {self.p1.hp}", 7)
        pyxel.text(SCREEN_WIDTH - 40, 5, f"P2 HP: {self.p2.hp}", 7)




if __name__ == "__main__":
    App()


