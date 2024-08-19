
from pgzero.builtins import *
import pygame
import math
import random
from enum import Enum, auto
import global_value as g
from typing import Any, Dict
from proj_control import *




class CHARA(Enum):
    EXPLOSION = 0
    PLAYER_SHOT = 1
    PLAYER = 2
    ENEMY_SHOT = 3
    ENEMY_1 = 4
    ENEMY_2 = 5
    ENEMY_BOSS = 6
    DEBRIS = 7

class SPEED(Enum):
    SLOW = 4
    NORMAL = 8
    FAST = 12
    RANDOM = 12


# キャラクター情報
class CharaData:
    def __init__(self, filename, hp ,enemy):
        self.imagename = filename  # 画像ファイル名
        self.hp = hp               # ヒットポイント
        self.is_enemy = enemy      # 敵フラグ True

class Info:
    charas: Dict[Enum, Any] = {
            CHARA.EXPLOSION  : CharaData,
            CHARA.PLAYER_SHOT: CharaData,
            CHARA.PLAYER     : CharaData,
            CHARA.ENEMY_SHOT : CharaData,
            CHARA.ENEMY_1    : CharaData,
            CHARA.ENEMY_2    : CharaData,
            CHARA.ENEMY_BOSS : CharaData,
            CHARA.DEBRIS     : CharaData,
    }

Info.charas[CHARA.EXPLOSION]   = CharaData("star.png", 1, True)
Info.charas[CHARA.PLAYER_SHOT] = CharaData("mushroom_red.png", 1, False)
Info.charas[CHARA.PLAYER]      = CharaData("alien.png", 3, False)
Info.charas[CHARA.ENEMY_SHOT]  = CharaData("fireball.png", 1, True)
Info.charas[CHARA.ENEMY_1]     = CharaData("fly_fly1.png", 1, True)
Info.charas[CHARA.ENEMY_2]     = CharaData("fish_swim1.png", 2, True)
Info.charas[CHARA.ENEMY_BOSS]  = CharaData("snail_walk1.png", 10, True)
Info.charas[CHARA.DEBRIS]      = CharaData("rock_moss_alt.png", 100, True)



# スプライト(ゲーム背景とは別に動く画像)のクラス。Actorクラスを継承
# クラスでない記述例は、上記の7静体
class Spclass(Actor):
    def __init__(self, x, y, angle, num: Enum):
        Actor.__init__(self, Info.charas[num].imagename, (x, y))
        self.angle = angle       # 角度
        self.hp = Info.charas[num].hp # ヒットポイント
        self.count = 0           # カウンタ
        self.num = num           # キャラクタNo

    def damage(self):
        self.hp-=1

    def dispose(self):
        self.x = g.OUTSIDE
        self.hp = -1


# 爆発マークのクラス。Spclassクラスを継承
class Explosion(Spclass):
    COUNT_LIVE = 20

    def update(self):
        # カウント20超えると、表示を消滅する
        if self.count > self.COUNT_LIVE: 
            self.dispose()


# 自機弾のクラス。Spclassクラスを継承
class Shot(Spclass):
    def __init__(self, x, y, angle, num: CHARA, speed: SPEED):
        super().__init__(x, y, angle, num) 
        self.speed = speed.value

    def update(self):
        # 弾の弾道や速度を決める(関数に入れて戻り値)
        self.pos = spritemove_right(self.pos, self.angle, self.speed) 

        # 敵との衝突範囲を判定
        hitbox = Rect((self.x-15, self.y-15), (30, 30))
        for sp in reversed(g.objects):
            if not Info.charas[sp.num].is_enemy:
                continue
            if sp.colliderect(hitbox): # アタリ判定内に入ると爆発
                g.objects.append(Explosion(sp.x, sp.y, 0, CHARA.EXPLOSION))
                self.dispose()
                break


# 自機のクラス。Spclassクラスを継承
class Player(Spclass):

    class COUNT():
        LAUNCH = 1
        DAMAGE = 20

    class STATE(Enum):
        INVINCIBLE = auto()
        CONTROLABLE = auto()
        UNCONTROLABLE = auto()
        LAUNCH = auto()
        NORMAL = auto()
        DAMAGE = auto()

    _state = None


    def change_normal(self):
        self._state = self.STATE.NORMAL
        self.image = 'alien.png'

    def __init__(self, x, y, angle, num: CHARA):
        super().__init__(x, y, angle, num) 
        self._state = self.STATE.LAUNCH
        clock.schedule_interval(self.change_normal, self.COUNT.LAUNCH)
    
    def __del__(self):
        g.playerRemain -= 1


    def update(self):
        if self._state==self.STATE.LAUNCH:
            self.x += 4
            return
        
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        # キーボードで機体を操作する。Pygame zeroではこれが可読性良い
        if keyboard.up   : self.y -= 4
        if keyboard.down : self.y += 4
        if keyboard.left : self.x -= 4
        if keyboard.right: self.x += 4
        if self.x < 35: self.x = 35
        if self.y < 35: self.y = 35
        if self.x > (WIDTH-35 ): self.x = WIDTH-35
        if self.y > (HEIGHT-35): self.y = HEIGHT-35
        if keyboard.space!=0 and (self.count % 16)==0:
            # 鉄砲音を鳴らす
            # sounds.eep.play()
            # 5方向へ弾を打つ(Shot関数に代入してその戻り値)
            g.objects.append(Shot(self.x, self.y,  -90, CHARA.PLAYER_SHOT, SPEED.NORMAL))
            g.objects.append(Shot(self.x, self.y,  -60, CHARA.PLAYER_SHOT, SPEED.NORMAL))
            g.objects.append(Shot(self.x, self.y,  -30, CHARA.PLAYER_SHOT, SPEED.NORMAL))
            g.objects.append(Shot(self.x, self.y,  0, CHARA.PLAYER_SHOT, SPEED.NORMAL))
            g.objects.append(Shot(self.x, self.y,  30, CHARA.PLAYER_SHOT, SPEED.NORMAL))

        # 衝突判定
        hitbox = Rect((self.x-10,self.y-10), (20,20))
        for sp in reversed(g.objects):
            if Info.charas[sp.num].is_enemy:
                # 隕石にぶつかるとしぼう
                if sp.colliderect(hitbox):
                    if sp.num.value==CHARA.DEBRIS:
                        self.dispose()
                    else:
                        sp.damage()
                        self.damage()
                        self.image = 'alien_hurt.png'
                        clock.schedule_interval(self.change_normal, 1)
                        break


# 敵弾のクラス。Spclassクラスを継承
class EnemyShot(Spclass):
    def __init__(self, x, y, angle, num: CHARA, speed: SPEED):
        super().__init__(x, y, angle, num) 
        self.speed = speed.value

    def update(self):
        self.pos = spritemove_left(self.pos, self.angle, self.speed) # 弾の角度や速度
        # for sp in g.objects:
        #     if sp.colliderect(pipe_bottom):
        #         sp.hp -= 1
        #         break

# 敵のクラス。Spclassクラスを継承
class Enemy(Spclass):
    def update(self):
        self.x -= 2
        self.y -= int((self.count % 200) / 100) * 2  - 1 # ジグザグ移動
        
        if random.randrange(80) != 0: return # 弾の出現率
        px, py = g.player.pos
        # rad = math.atan2(py - self.y, px - self.x) # 敵と自機の方角
        rad = math.atan2(self.y - py, self.x - px) # 敵と自機の方角
        newangle = math.degrees(rad) # ラジアンから角度へ変換
        newsp = EnemyShot(self.x, self.y, newangle, CHARA.ENEMY_SHOT, SPEED.SLOW)
        g.objects.append(newsp)

# ボスのクラス。Spclassクラスを継承
class Boss(Spclass):
    def update(self):
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        if self.count < 100:
            self.y += 1
        else:
            rad = math.radians(self.count - 100)
            self.y = (HEIGHT / 2) + (math.sin(rad) * 200) # 上下に動く
        if self.count > 150 and (self.count % 5) == 0:
            newangle = (self.count * 4) % 360 # 全方向へ
            g.objects.append(EnemyShot(self.x, self.y, newangle, CHARA.ENEMY_SHOT, SPEED.FAST))


class Debris(Spclass):
    def __init__(self, x, y, angle, num: CHARA):
        super().__init__(x, y, angle, num) 
        self.speed = random.randrange(SPEED.SLOW.value, SPEED.FAST.value, 1)

    def update(self):
        self.pos = spritemove_left(self.pos, self.angle, self.speed)

