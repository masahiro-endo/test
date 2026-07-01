import pyxel as px
from UI import *
from module.actorstate import *
from typing import List
from observer import *
from resource.mapevent import * 
from resource.tileevent import * 






# 呪文インデックス定数
class SPELL(IntEnum):
    FIRE = 0
    RETURN = auto()
    HEAL = auto()
    BURST = auto()







# 戦闘用キャラクタ（自分とモンスター）
class Actor(Subject):
    def __init__(self, parent, name, hp, mp, atk, spd, is_player,resist=0, img=None, gold=0):
        super().__init__()
        self.party = parent
        self.name = name
        self.mhp = hp
        self.hp = hp
        self.mmp = mp
        self.mp = mp
        self.atk = atk
        self.spd = spd
        self.btl_spd = spd
        self.is_player = is_player
        self.resist = resist  # 呪文（ファイア）耐性
        self.img = img  # モンスターの場合の画像イメージ
        self.gold = gold  # 勝利時報酬

    def __lt__(self, other):
        return self.btl_spd < other.btl_spd

    def is_alive(self):
        return self.hp > 0

    def is_attack_by_suprise(self, char):
        return not self.is_fasterthan(char)

    def is_faster_than(self, char):
        return True if self.spd * px.rndf(1.0, 2.0) >= char.spd * px.rndf(1.0, 2.0) else False

    def has_remain_mp(self, spl):
        return True if self.mp >= spl.mp and px.rndi(0, 1) == 0 else False

    # 攻撃
    def battlelog_action_atk(self, target, msg_pre=[]):

        def get_hit_rate(target):
            hit_rate = max(min(self.spd / target.spd, 1.5), 0.25)
            hit_rate = min(hit_rate - px.rndf(0.0, 1.0), 1.0)
            return hit_rate

        bt_msg = msg_pre + [f"{self.name}の こうげき"]

        hit_rate = get_hit_rate(target)
        if hit_rate > 0.0:
            dmg = int(self.atk * (1 + hit_rate) / 2 + 0.99)
            bt_msg += self.battlelog_take_dmg(target, dmg)
            bt_msg += self.battlelog_action_res(target)

        else:  # 回避された
            bt_msg += [f"{target.name}は みをかわした"]
        return bt_msg

    # ダメージ処理
    def battlelog_take_dmg(self, target, dmg):
        bt_msg = []
        bt_msg += [f"{target.name}に {dmg}ダメージ"]
        target.hp = max(target.hp - dmg, 0)
        return bt_msg

    def battlelog_action_res(self, target):
        bt_msg = []
        if not target.is_alive():
            if not target.is_player:
                bt_msg += [f"{target.name}を たおした"]
            else:
                bt_msg += [f"{target.name}は たおれた"]
        return bt_msg

    def battlelog_spell_effect(self, target, spl_id, cost=0):

        def use_heal(person, mp):
            hp = min(person.hp + mp * 5, person.mhp)
            ret = hp - person.hp
            person.hp += ret
            return ret

        if spl_id == SPELL.FIRE:
            dmg = 0 if target.resist else px.rndi(24, 30)
            bt_msg += self.battlelog_take_damage(target, dmg)
        elif spl_id == SPELL.HEAL:
            ret = use_heal(cost)
            bt_msg += [f"{ret}HP かいふくした"]
        elif spl_id == SPELL.BURST:
            dmg = 0
            for _ in range(cost):
                dmg += px.rndi(8, 12)
            bt_msg += self.battlelog_take_damage(target, dmg)
        return bt_msg



    def status(self):
        return [
            f"HP {Meth.pad(self.hp,3)}/{Meth.pad(self.mhp,3)}",
            f"MP  {Meth.pad(self.mp,2)}/ {Meth.pad(self.mmp,2)}",
            f"ちから {Meth.pad(self.atk,2)}  はやさ {Meth.pad(self.spd,2)}",
            f" {Meth.pad(self.gold,4)}G  カギ {Meth.pad(self.keys,2)}こ",
        ]

    def battle_status(self):
        return [self.name, f"HP {Meth.pad(self.hp,3)}", f"MP  {Meth.pad(self.mp,2)}"]




class Party():
    def __init__(self):
        self._member = []

    def __len__(self):
        return len(self._member)
    
    def __getitem__(self, index):
        return self._member[index]
    
    def __setitem__(self, index, value):
        self._member[index] = value
    #in
    def __contains__(self, item):
        return item in self._member
    
    def __iter__(self):
        return iter(self._member)

    def add_member(self, chr):
        chr.attach(LogObserver())
        self._member.append(chr)

    def remove_member(self, idx):
        try:
            del self._member[idx]
        except:
            raise Exception("the specified member doesn't exist.：" + str(idx))

    def clear_member(self):
        self._member.clear()
        
    def get_alive_actors(self):
        return [p for p in self._member if p.is_alive()]





class PlayerParty(Party):

    def __init__(self):
        super().__init__()
        self.add_member(Actor(self, "あなた", 30, 6, 12, 12, ACTOR.ISPLAYER))

        self.pl = self._member[0]
        self.gold = 0
        self.keys = 0  # カギの数
        self.flags = []  # フラグ（宝箱、扉などの判定用）
        self.enc = 0  # エンカウント
        self.frames = 0
        self.action = ActorStates(self)

        self.get_start_location()
        (self.dx, self.dy, self.spd) = (0, 0, 4)

    def update(self):
        self.action.update()

    def draw(self):
        self.action.draw()

    def get_current_floor(self):
        return self.z

    def use_return(self):
        if gbl.scene(): gbl.scene().Main()
        (self.x, self.y, self.z) = (8, 21, 0)
        # self.play_bgm(2)

    # 現在使える呪文
    def available_spells(self, on_battle=False):
        ret = [SPELL.FIRE]  # ファイアは最初から
        if not on_battle and "sp1" in self.flags:
            ret.append(SPELL.RETURN)
        if "sp2" in self.flags:
            ret.append(SPELL.HEAL)
        if "sp3" in self.flags:
            ret.append(SPELL.BURST)
        return ret

    def get_start_location(self):
        self.use_return()

    def add_gold(self, gold):
        self.gold = min(self.gold + gold, 9999)

    def pos_try_move(self):
        x = self.x + self.dx
        y = self.y + self.dy
        return (x, y)

    def pos_3d(self):
        (x, y) = self.pos_try_move()
        z = self.get_current_floor
        return (x, y, z)


    def try_move_forward(self):
        # Tileの定義位置は、イメージバンクが関わるため、
        # 座標にはz軸も必要
        pos = self.pos_3d()
        evt = MapTiles.get_obs_key(pos)

        if not evt or MapTiles.is_walkable(pos): 
            self.move_step()
        else:
            self.fire_event_in_front()

    # 移動（１マス）開始
    def move_step(self):
        self.dx *= self.spd
        self.dy *= self.spd
        self.moving = True
        Window.close()

    def fire_event_in_front(self):
        self.dx, self.dy = (0, 0)
            
        # 進行先タイルに紐づくイベントを発火 泉
        pos = self.pos_3d()
        MapTiles.exec_response_spring(pos=pos, pt=self)

        evt = MapResources.get_obs_key(self.pos_3d())
        if evt in MapResources.obstacles and not evt in self.flags:
            ob = MapResources.obstacles[evt]
            ob.response(pt=self,evt=evt,ob=ob)


    # 移動（１ステップ）終了
    def move_end(self):
        self.y += self.dy // 16 
        self.x += self.dx // 16
        self.dy = 0
        self.dx = 0
        self.moving = False

        # 移動後のタイルに紐づくイベントを発火 階段
        pos = self.pos_3d()
        MapTiles.exec_response_stairs(pos=pos, pt=self)

        self.recovery_gradually()
        
        self.roll_encount()

    def recovery_gradually(self):
        if (self.x + self.y) % 2 == 0:
            self.pl.hp = min(self.pl.hp + 1, self.pl.mhp)

    def roll_encount(self):
        # 地下1階、ひほう取得〜エンディングは敵がでない
        if self.z == 0 or ("4-3" in self.flags and not "end" in self.flags):
            return
        self.enc += 1

        if self.enc > 12 and px.rndi(0, 7) == 0:
            self.enc = 0
            # ms_id = self.get_enemy_race()
            # self.battle_start(ms_id)
            gbl.get_screen().Battle()

    def get_enemy_random(self):
            return self.get_current_floor() - (1 if px.rndi(0, 3) < 3 else 0)


class EnemyParty(Party):
    def __init__(self):
        super().__init__()





