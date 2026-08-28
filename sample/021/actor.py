
import pyxel as px
import math
import random
import uuid

import appconfig as gbl
from constant import * 








class Bullet:
    SIZE = 4
    def __init__(self, owner_id, x, y, dx, dy, col=7):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = col
        self.active = True
        self.owner_id = owner_id

    def update(self):
        self.x += self.dx
        self.y += self.dy
        # 画面外で無効化
        if self.is_offscreen():
            self.active = False

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_offscreen(self):
        # 画面外で無効化
        if (self.x < -Bullet.SIZE or self.x > WIDTH  + Bullet.SIZE or 
            self.y < -Bullet.SIZE or self.y > HEIGHT + Bullet.SIZE):
            return True
        return False


    @classmethod
    def chase_player(cls, target, actor):
            dx = target.x - actor.x
            dy = target.y - actor.y
            dist = math.sqrt(dx**2 + dy**2) or 1
            speed = 1.5
            gbl.bullets.append(cls(actor.id, 
                                   actor.x, actor.y, 
                                   dx/dist * speed, dy/dist * speed))

    @classmethod
    def player_bullet(cls):
            speed = 10
            gbl.bullets.append(cls(gbl.player.id, 
                                   gbl.player.x + (Player.SIZE//2), gbl.player.y + (Player.SIZE//2),
                                    0, -speed))



# 爆発エフェクトクラス
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0  # 爆発の経過フレーム

    def update(self):
        self.timer += 1

    def draw(self):
        # 爆発を円で簡易表現（本来はスプライトでもOK）
        px.circ(self.x, self.y, self.timer, 8 + self.timer % 8)

    def is_finished(self):
        return self.timer > 10  # 爆発終了条件




class Sparks_spread:
    def __init__(self, x, y, angle, speed, life, color):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = life
        self.color = color
        self.timer = 0  # 爆発の経過フレーム

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.timer += 1

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_finished(self):
        return self.timer > self.life

    @classmethod
    def spawn(cls, cnt,  actor):
        for _ in range(cnt):  # パーティクル数
            #angle = random.uniform(0, math.tau)  # 0〜2π
            angle = random.uniform(-math.tau*(1/8), -math.tau*(3/8))  # 0〜2π
            speed = random.uniform(1.0, 2.0)
            life = random.randint(10, 20)
            color = random.choice([8, 9, 10])  # 赤系
            dx = actor.x + (actor.size//2)
            dy = actor.y + (actor.size//2)
            gbl.explosions.append(cls(dx, dy, angle, speed, life, color))



class Sparks_parabola:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-4, -2)
        self.life = random.randint(10, 30)  # 寿命フレーム
        self.color = random.choice([px.COLOR_YELLOW, px.COLOR_ORANGE, px.COLOR_RED])
        self.timer = 0  # 爆発の経過フレーム

    def update(self):
        # 重力加速度
        self.vy += 0.2
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_finished(self):
        return self.life <= 0

    @classmethod
    def spawn(cls, cnt,  actor):
        for _ in range(cnt):  # パーティクル数
            radius = actor.size//2
            dx = actor.x + radius + random.randint(-radius, radius)
            dy = actor.y + radius + random.randint(-radius, radius)
            gbl.explosions.append(cls(dx, dy))



class Star:
    SIZE = 1
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(0, HEIGHT - 1)
        self.speed = random.choice([0.5, 1, 1.5])
        self.color = random.choice([5, 6, 7])

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT - 1)
            self.speed = random.choice([0.5, 1, 1.5])
            self.color = random.choice([5, 6, 7])

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_offscreen(self):
        if (self.x < -Star.SIZE or self.x > WIDTH  + Star.SIZE or 
            self.y < -Star.SIZE or self.y > HEIGHT + Star.SIZE):
            return True
        return False



class Terrain:
    # """上下の壁や障害物をスクロールさせる"""
    def __init__(self):
        self.segments = []
        self.generate_initial()

    def generate_initial(self):
        # 初期地形を生成
        for x in range(WIDTH // 8 + 2):
            self.segments.append(self.random_segment())

    def random_segment(self):
        # 上下の壁の高さをランダム生成
        top_height = random.randint(0, 20)
        bottom_height = random.randint(0, 20)
        return (top_height, bottom_height)

    def update(self):
        # 左にスクロール
        if px.frame_count % 8 == 0:  # スクロール速度
            self.segments.pop(0)
            self.segments.append(self.random_segment())

    def draw(self):
        for i, (top, bottom) in enumerate(self.segments):
            x = i * 8
            if top > 0:
                px.rect(x, 0, 8, top, 3)  # 上の壁
            if bottom > 0:
                px.rect(x, HEIGHT - bottom, 8, bottom, 3)  # 下の壁

    def check_collision(self, px, py, pw, ph):
        for i, (top, bottom) in enumerate(self.segments):
            x = i * 8
            if x < px + pw and x + 8 > px:
                if py < top or py + ph > HEIGHT - bottom:
                    return True
        return False





class Bomb:
    DURATION = 20  # 爆発表示フレーム数
    def __init__(self):
        self.active = True
        self.timer = Bomb.DURATION
        self.x = gbl.player.x - (Player.SIZE//2)
        self.y = gbl.player.y - (Player.SIZE//2)
        self.radius = 0

    def update(self):
        # ボムタイマー更新 & 敵巻き込み処理
        if self.active:
            self.timer -= 1
            self.radius = (Bomb.DURATION - self.timer) * 2
            self.check_bomb_hit()
            if self.timer <= 0:
                self.active = False

    def draw(self):
        # ボム描画
        if self.active:
            radius = (Bomb.DURATION - self.timer) * 2
            px.circ(self.x + 4, self.y, radius, 8)   # 外側
            px.circ(self.x + 4, self.y, radius // 2, 10)  # 中心光

    def is_collision(self, obj):
            dist_sq = (obj.x - self.x) ** 2 + (obj.x - self.y) ** 2
            if dist_sq <= self.radius ** 2:
                return True
            return False

    def check_bomb_hit(self):
        # """爆発範囲にいる敵を消す"""
        for e in gbl.enemies:
            if self.is_collision(e):
                e.sudden_death()
                gbl.enemies.remove(e)
                gbl.explosions.append(Explosion(e.x + (e.size//2), e.y + (e.size//2)))

        for b in gbl.enemies:
            if self.is_collision(b):
                gbl.bullets.remove(b)




class Player:
    SIZE = 4
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT -10
        self.speed = 2
        self.alive = True
        self.id = uuid.uuid4()
        self.bombs = []
        self.bomb_stock = 3

    def update(self):
        if not self.alive:
            return
        if px.btn(px.KEY_UP):
            self.y -= self.speed
        if px.btn(px.KEY_DOWN):
            self.y += self.speed
        if px.btn(px.KEY_LEFT):
            self.x -= self.speed
        if px.btn(px.KEY_RIGHT):
            self.x += self.speed

        if px.btnp(px.KEY_SPACE,hold=10, repeat=3):
            Bullet.player_bullet()
        if px.btn(px.KEY_B) and self.bomb_stock > 0:
            # 連続使用不可
            if not self.bombs:
                self.bombs.append(Bomb())
                self.bomb_stock -= 1

        self.x = max(0, min(WIDTH - Player.SIZE, self.x))
        self.y = max(0, min(HEIGHT - Player.SIZE, self.y))

        for b in self.bombs:
            b.update()
        self.bombs = [b for b in self.bombs if b.active]

    def draw(self):
        for bomb in self.bombs:
            bomb.draw()

        if self.alive:
            px.rect(self.x, self.y, Player.SIZE, Player.SIZE, 11)



