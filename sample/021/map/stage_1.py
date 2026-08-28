
import pyxel as px
import math
import random
from typing import override

import appconfig as gbl
from constant import * 
from actor import * 
from map.baseactor import *






# 指定座標を通過する編隊
class EnemyLine(BaseEnemy):
    SIZE = 4

    def __init__(self, path, speed, spacing):
        super().__init__(EnemyLine.SIZE)
        self.path = path
        self.x, self.y = path[0]
        self.y += spacing
        self.speed = speed
        self.angle = 0  # 回転角度（度数法）
        self.target_index = 1  # 次の目的地インデックス

    def update(self):
        if self.is_dead():
            return

        # 毎フレーム角度を更新（0〜360度でループ）
        self.angle = (self.angle + 10) % 360

        target_x, target_y = self.path[self.target_index]
        
        # 目的地までの距離を計算
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)  # √(dx² + dy²)

        if dist > 0:
            # 移動量を計算（正規化して速度を掛ける）
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed

            # X方向移動
            if abs(self.x - target_x) > abs(move_x):
                self.x += move_x 
            else:
                self.x = target_x
            
            # Y方向移動
            if abs(self.y - target_y) > (move_y):
                self.y += move_y 
            else:
                self.y = target_y
        
        # 目的地に到達したら次のポイントへ
        if (self.x, self.y) == (target_x, target_y):
            self.target_index = (self.target_index + 1) % len(self.path)

    def draw(self):
        # px.rect(self.x, self.y, 8, 8, 8)
        # 画像を回転描画
        # x, y: 描画位置（画面座標）
        # u, v: 画像の左上座標（.pyxres内）
        # w, h: 幅と高さ
        # colkey: 透明色
        # scale: 拡大縮小倍率
        # rotate: 回転角度（度数法）
        px.blt(
            x=self.x, y=self.y,  # 中心座標
            img=0, u=0, v=0, w=EnemyLine.SIZE, h=EnemyLine.SIZE,
            colkey=0,
            scale=1,
            rotate=self.angle)
        px.text(self.x, self.y, str(self.hp), px.COLOR_WHITE)

    @classmethod
    def spawn(cls, *args):
        path = args[0]
        speed = args[1]
        spacing = args[2]
        for i in range(5):
            e = cls(
                path, 
                speed,
                (i * spacing)
            )
            gbl.enemies.append(e)





class EnemyEscape(BaseEnemy):
    SIZE = 8
    SPEED = 1.0
    WAIT_MIN = 30   # 停滞時間の最小フレーム
    WAIT_MAX = 90   # 停滞時間の最大フレーム
    SPAWN_INTERVAL = 60   # 敵出現間隔（フレーム）

    def __init__(self, x, y):
        super().__init__(EnemyEscape.SIZE)
        self.x = x
        self.y = y
        self.timer = 0
        self.wait_time = random.randint(EnemyEscape.WAIT_MIN, EnemyEscape.WAIT_MAX)
        self.state = "wait"  # "wait" → "escape" → "gone"
        self.hp = random.randint(2, 5)  # 耐久値（2〜5）

    def update(self):
        self.timer += 1

        if self.state == "wait":
            if self.timer >= self.wait_time:
                self.state = "escape"
                self.fire_bullet()


        elif self.state == "escape":
            # プレイヤーから離れる方向に移動
            dx = self.x - gbl.player.x
            dy = self.y - gbl.player.y
            dist = math.sqrt(dx**2 + dy**2) or 1
            self.x += (dx / dist) * EnemyEscape.SPEED
            self.y += (dy / dist) * EnemyEscape.SPEED

            # 画面外に出たら消える
            if self.is_offscreen():
                self.state = "gone"

    def draw(self):
        if self.state != "gone":
            color = 8 if self.state == "wait" else 2  # 待機中は青、逃走中は赤
            px.rect(self.x, self.y, EnemyEscape.SIZE, EnemyEscape.SIZE, color)
            px.text(self.x, self.y, str(self.hp), px.COLOR_WHITE)

    @classmethod
    def spawn(cls, *args):
        # 画面の端からランダムに出現
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = random.randint(0, WIDTH), 0
        elif side == "bottom":
            x, y = random.randint(0, WIDTH), HEIGHT - 8
        elif side == "left":
            x, y = 0, random.randint(0, HEIGHT)
        else:  # right
            x, y = WIDTH - 8, random.randint(0, HEIGHT)

        gbl.enemies.append(cls(x + (Player.SIZE//2), y + (Player.SIZE//2)))

    def fire_bullet(self):
            Bullet.chase_player(gbl.player, self)






class EnemyBoss(BaseEnemy):
    SIZE = 16
    HP_BASE = 60
    BULLET_SPEED = 1.5
    DIFFICULTY = 200

    def __init__(self, x, y):
        super().__init__(EnemyBoss.SIZE)
        self.x = x
        self.y = y
        self.maxhp = EnemyBoss.HP_BASE + (gbl.score // 5 if gbl.score > EnemyBoss.DIFFICULTY else 0)
        self.hp = self.maxhp
        self.phase = 1
        self.dx = 1
        self.direction_interval = 60
        self.change_direction()
        self.damage_interval = random.randint(60, 100)


    def update(self):
        # フェーズごとの移動速度
        speed = {1: 1, 2: 1.5, 3: 2}[self.phase]
        # self.x += speed * (1 if px.frame_count // 30 % 2 == 0 else -1)
        # self.y = max(0, min(WIDTH - EnemyBoss.SIZE, self.x))
        if px.frame_count // self.direction_interval % 2 == 0:
            self.change_direction()

        self.x += speed * self.dx
        self.x = max(0, min(WIDTH - EnemyBoss.SIZE, self.x))
        self.dx *= -1 if self.x in [0, WIDTH - EnemyBoss.SIZE] else 1


        # 攻撃パターン
        if self.phase == 1:
            if px.frame_count % 25 == 0:
                self.fire_bullet(0, EnemyBoss.BULLET_SPEED)

        elif self.phase == 2:
            if px.frame_count % 20 == 0:
                self.fire_bullet(-0.5, EnemyBoss.BULLET_SPEED)
                self.fire_bullet(0, EnemyBoss.BULLET_SPEED)
                self.fire_bullet(0.5, EnemyBoss.BULLET_SPEED)

            if px.frame_count // self.damage_interval % 2 == 0:
                Sparks_parabola.spawn(random.randint(1, 5), self)
                self.damage_interval = random.randint(60, 100)

        elif self.phase == 3:
            if px.frame_count % 15 == 0:
                for angle in range(0, 360, 45):
                    rad = math.radians(angle)
                    dx = math.cos(rad) * EnemyBoss.BULLET_SPEED
                    dy = math.sin(rad) * EnemyBoss.BULLET_SPEED
                    self.fire_bullet(dx, dy)

            if px.frame_count // self.damage_interval % 2 == 0:
                Sparks_parabola.spawn(random.randint(3, 5), self)
                self.damage_interval = random.randint(30, 60)

        self.update_boss_phase()

        if self.is_dead():
            self.effect_death()

    def draw(self):
            color = px.COLOR_DARK_BLUE
            if self.phase == 2:
                color = px.COLOR_GREEN
            elif self.phase == 3:
                color = px.COLOR_RED

            px.rect(self.x, self.y, EnemyBoss.SIZE, EnemyBoss.SIZE, color)
            px.text(self.x, self.y, str(self.hp), px.COLOR_WHITE)
            px.text(self.x, self.y + 4, f"phas{str(self.phase)}", px.COLOR_WHITE)

    def update_boss_phase(self):
        # HP割合でフェーズ変更
        hp_ratio = self.hp / self.maxhp
        if hp_ratio <= 0.33:
            self.phase = 3
        elif hp_ratio <= 0.66:
            self.phase = 2

    def change_direction(self):
        self.dx = random.choice([-1, 1])
        self.direction_interval = random.randint(60, 100)

    def fire_bullet(self, dx, dy):
        gbl.bullets.append(Bullet(self.id, 
                                self.x + (EnemyBoss.SIZE//2), self.y + (EnemyBoss.SIZE//2),
                                dx, dy))

    @classmethod
    def spawn(cls, *args):
        bx = args[0]
        by = args[1]
        gbl.enemies.append(cls(bx, by))




class stage1:

    # 経路（敵が通る座標のリスト）
    # begin, end, interval, class, args, tick
    # EnemyList = [
    #     [100, 600, 10000, EnemyBoss, [WIDTH // 2 - 16, 10], 0],
    # ]
    EnemyList = [
        [100, 200, 200, EnemyLine, [[(10 , -3), (10, 90), (40, 50), (40, - 10)], 1.5, 10], 0],
        [100, 500, EnemyEscape.SPAWN_INTERVAL,  EnemyEscape, [], 0],
        [200, 300, 200, EnemyLine, [[(100 , -3), (100, 90), (50, 40), (50, - 10)], 1.5, 10], 0],
        [300, 400, 200, EnemyLine, [[(10 , -3), (10, 90), (60, 50), (60, - 10)], 1.5, 10], 0],
        [500, 600, 10000, EnemyBoss, [WIDTH // 2 - 16, 10], 0],
    ]










