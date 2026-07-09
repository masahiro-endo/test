import pyxel as px
from typing import List
from module.UI import *
from module.state.actorstate import *
from resource.mapevent import * 
from resource.tileevent import * 






# 呪文インデックス定数
class SPELL(IntEnum):
    FIRE = 0
    RETURN = auto()
    HEAL = auto()
    BURST = auto()







# 戦闘用キャラクタ（自分とモンスター）
class Character():
    def __init__(self, parent, name, hp, mp, atk, spd, is_player,resist=0, img=None, gold=0, skills=None):
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
        
        self.action = None
        self.bad_status = {}  # {"poison": 残りターン, "paralyze": 残りターン}
        self.skills = skills if skills else []  # (スキル名, 関数)

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
        # クリティカル判定（10%）
        critical = px.rndf(0.0, 1.0) < 0.1

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


    def add_status(self, status_name, turns):
        """状態異常を付与"""
        self.status[status_name] = turns
        print(f"⚠ {self.name} は {status_name} 状態になった！（{turns}ターン）")

    def process_status(self):
        """ターン開始時の状態異常処理"""
        # 麻痺判定
        if "paralyze" in self.status:
            if random.random() < 0.5:  # 50%で行動不能
                print(f"💥 {self.name} は麻痺で動けない！")
                self.status["paralyze"] -= 1
                if self.status["paralyze"] <= 0:
                    del self.status["paralyze"]
                return False  # 行動スキップ

        return True

    def end_turn_status(self):
        """ターン終了時の状態異常処理"""
        if "poison" in self.status:
            dmg = max(1, self.max_hp // 10)
            self.hp = max(0, self.hp - dmg)
            print(f"☠ {self.name} は毒で {dmg} ダメージ！（残りHP: {self.hp}）")
            self.status["poison"] -= 1
            if self.status["poison"] <= 0:
                del self.status["poison"]

    def attack(self, target):
        damage = random.randint(self.attack_power - 2, self.attack_power + 2)
        target.hp = max(0, target.hp - damage)
        print(f"{self.name} の攻撃！ {target.name} に {damage} ダメージ！")
        return damage


class Player(Character):
    def __init__(self, parent, name, hp, mp, atk, spd, resist=0, img=None, gold=0, skills=None):
        self.is_player = True
        super().__init__(parent, name, hp, mp, atk, spd, self.is_player,resist, img, gold, skills)

class Enemy(Character):
    def __init__(self, parent, name, hp, mp, atk, spd, resist=0, img=None, gold=0, skills=None):
        self.race = name
        self.is_player = False
        super().__init__(parent, name, hp, mp, atk, spd, self.is_player,resist, img, gold, skills)





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
        self.add_member(Player(self, "あなた", 30,  6, 12, 12))
        self.add_member(Player(self, "メンバ", 15, 50,  5,  5))
        self.gold = 0
        self.keys = 0    # カギの数
        self.flags = []  # フラグ（宝箱、扉などの判定用）
        self.enc = 0     # エンカウント
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
        if gbl.scene_state(): gbl.scene_state().Main()
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
        z = self.get_current_floor()
        return (x, y, z)


    def try_move_forward(self):
        # Tileの定義位置は、イメージバンクが関わるため、
        # 座標にはz軸も必要
        pos = self.pos_3d()
        evt = MapMeth.get_obs_key(pos)
        obj = MapTiles.is_defined(pos) and not MapTiles.is_walkable(pos)
        # 扉開放や宝箱取得時点でフラグを保持し、
        # 以降は通過を許す
        if obj or (evt and not evt in self.flags): 
            self.fire_event_in_front()
        else:
            self.move_step()

    # 移動（１マス）開始
    def move_step(self):
        self.dx *= self.spd
        self.dy *= self.spd
        self.moving = True
        Window.close()

    def fire_event_in_front(self):
        pos = self.pos_3d() # 踏み出し直後の座標を保持
        self.dx, self.dy = (0, 0)
            
        # 進行先タイルに紐づくイベント処理 泉
        MapTiles.response_spring(**{'pos': pos, 'pt': self})

        evt = MapMeth.get_obs_key(pos)
        if evt and not evt in self.flags:
            ob = gbl.map_resource().obstacles[evt]
            ob.response(**{'evt': evt, 'pos': pos, 'pt': self, 'ob': ob })


    # 移動（１ステップ）終了
    def move_end(self):
        self.y += self.dy // 16 
        self.x += self.dx // 16
        self.dy = 0
        self.dx = 0
        self.moving = False

        # 移動後のタイルに紐づくイベント処理 階段
        pos = self.pos_3d()
        MapTiles.response_stairs(**{'pos': pos, 'pt': self})

        self.recover_health_gradually()
        self.roll_encount()

    def recover_health_gradually(self):
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
            gbl.current_scene().Battle()

    def get_enemy_random(self):
            return self.get_current_floor() - (1 if px.rndi(0, 3) < 3 else 0)


    def field_status(self):
        return [
            f"HP {Meth.pad(self[0].hp,3)}/{Meth.pad(self[0].mhp,3)}",
            f"MP  {Meth.pad(self[0].mp,2)}/ {Meth.pad(self[0].mmp,2)}",
            f"ちから {Meth.pad(self[0].atk,2)}  はやさ {Meth.pad(self[0].spd,2)}",
            f" {Meth.pad(self.gold,4)}G  カギ {Meth.pad(self.keys,2)}こ",
        ]

    def battle_status(self):
        return [self.name, f"HP {Meth.pad(self.hp,3)}", f"MP  {Meth.pad(self.mp,2)}"]




class EnemyParty(Party):
    
    opt = ['A','B','C','D','E','F']

    def __init__(self):
        super().__init__()

    def add_member(self, chr):
        self._member.append(chr)
        # 複数体の場合は、甲乙丙を付与
        # 異種族混在は不可。Party を分けるか？
        for i, mem in enumerate(self._member):
            mem.name = mem.race + self.opt[i]

