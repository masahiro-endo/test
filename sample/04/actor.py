import pyxel as px
from UI import *
from module.actorstate import *
from typing import List
from observer import *
from resource.mapresource import * 






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
    @property
    def is_enemy(self):
        return self.is_player

    def is_attack_by_suprise(self, char):
        return not self.is_fasterthan(char)

    def is_faster_than(self, char):
        return True if self.spd * px.rndf(1.0, 2.0) >= char.spd * px.rndf(1.0, 2.0) else False

    def has_remain_mp(self, spl):
        return True if self.mp >= spl.mp and px.rndi(0, 1) == 0 else False

    # 攻撃
    def battlelog_action_atk(self, target, msg_pre=[]):

        def get_hit_rate(self, target):
            hit_rate = max(min(self.spd / target.spd, 1.5), 0.25)
            hit_rate = min(hit_rate - px.rndf(0.0, 1.0), 1.0)
            return hit_rate

        bt_msg = msg_pre + [f"{self.name}の こうげき"]

        hit_rate = get_hit_rate(target)
        if hit_rate > 0.0:
            dmg = int(self.atk * (1 + hit_rate) / 2 + 0.99)
            bt_msg += self.battlelog_take_damage(target, dmg)
        else:  # 回避された
            bt_msg += [f"{target.name}は みをかわした"]
        return bt_msg

    # ダメージ処理
    def battlelog_take_dmg(self, target, dmg):
        bt_msg = []
        bt_msg += [f"{target.name}に {dmg}ダメージ"]
        target.hp = max(target.hp - dmg, 0)
        if not target.is_alive():
            bt_msg += [f"{target.name}を たおした"]
        return bt_msg

    def battlelog_spell_effect(self, target, spl_id, cost=0):

        def use_heal(self, mp):
            hp = min(self.pl.hp + mp * 5, self.pl.mhp)
            ret = hp - self.pl.hp
            self.pl.hp += ret
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

    def get_positon(self):
        return (self.x + self.dx, self.y + self.dy)

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




    # 移動（１ステップ）開始
    def move_start(self):
        # self.notify()

        # 移動先のイベントを取得
        evt = GameMap.get_map_event(self)
        letter_up = GameMap.table[GameMap.TILE.UPSTAIR]["LETTER"]
        letter_dwn = GameMap.table[GameMap.TILE.DOWNSTAIR]["LETTER"]
        obs = (letter_up, letter_dwn)
        if not evt or evt in obs: 
            self.dx *= self.spd
            self.dy *= self.spd
            self.moving = True
            Window.close()
            return
        
        self.dx, self.dy = (0, 0)
        if evt == "@":  # 泉
            # px.play(3, 32)
            Window.message(["かいふくの いずみだ", "HP MP かいふく！"])
            self.pl.hp = self.pl.mhp
            self.pl.mp = self.pl.mmp

        if evt in gbl.resource().obstacles:
            ob = gbl.resource().obstacles[evt]
            # 扉
            if ob.kind == 0:
                if self.keys:
                    px.play(3, 33)
                    Window.message(["カギを あけた"])
                    self.flags.append(evt)
                    self.keys -= 1
                    self.wait = True
                else:
                    Window.message(["カギを もっていない"])
            # 宝箱
            elif ob.kind == 1:
                t = ["たからばこだ！"]
                if ob.val:
                    t.append(f"{ob.val}G てにいれた")
                    self.add_gold(ob.val)
                else:
                    t.append(f"カギを てにいれた")
                    self.keys += 1
                Window.message(t)
                self.flags.append(evt)
                # px.play(3, 35)
            # NPC
            if evt == "0-1" and "4-3" in self.flags:
                Window.message(["ぜひ Pyxelを", "マスターしてくれ"])
            elif evt == "0-3":
                gbl.get_screen().currentMap.Shop()
                # Window.message(["パワーアップするかい？", " HP MP ちから はやさ"])
                # self.cur = Cursor("shop", [1, 4, 7, 11], 14, -1)
                # Window.shop_show()
            elif evt == "1-2" and not "sp1" in self.flags:
                Window.message(["リターンの じゅもんを", "さずけよう"])
                self.flags.append("sp1")
            elif evt == "2-5" and not "sp2" in self.flags:
                Window.message(["じゅんびは よいか？", " はい  いいえ"])
                self.cur = Cursor("boss1", [1, 5], 14, 1)
            elif evt == "3-1" and not "sp3" in self.flags:
                Window.message(["おれと たたかうのか？", " はい  いいえ"])
                self.cur = Cursor("boss2", [1, 5], 14, 1)
            elif evt == "4-3":
                Window.message(["この ひほうが ほしいか？", " はい  いいえ"])
                self.cur = Cursor("boss3", [1, 5], 14, 1)
            # 会話のみ
            elif evt in gbl.resource().talks:
                Window.message(gbl.resource().talks[evt])

    # 移動（１ステップ）終了
    def move_end(self):
        self.y += self.dy // 16 
        self.x += self.dx // 16
        self.dy = 0
        self.dx = 0
        self.moving = False

        evt = self.get_map_event

        if evt in ("<", ">"):  # 階段
            self.z += 1 if evt == ">" else -1
            # エンディング判定
            if self.z == 0 and "4-3" in self.flags and not "end" in self.flags:
                s = self.frames // 30
                m = s // 60
                s %= 60
                Window.message(["ゲームクリア！", f"タイム：{m}ふん{s}びょう"])
                self.flags.append("end")
            else:
                Window.message([f"ちか{self.z+1}かい"])
            # self.field_bgm()
            # px.play(3, 34)
            self.wait = True
            return
        if (self.x + self.y) % 2 == 0:
            self.pl.hp = min(self.pl.hp + 1, self.pl.mhp)
        # 地下1階、ひほう取得〜エンディングは敵がでない
        if self.z == 0 or ("4-3" in self.flags and not "end" in self.flags):
            return
        self.enc += 1
        self.roll_encount()

    def roll_encount(self):
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





