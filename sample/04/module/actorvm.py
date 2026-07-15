
import pyxel as px
from typing import List
from module.UI import *
from resource.mapevent import * 
from resource.tileevent import * 






# 呪文インデックス定数
class SPELL(IntEnum):
    FIRE = 0
    RETURN = auto()
    HEAL = auto()
    BURST = auto()




# ViewModel
class ActorViewModel():

    def __init__(self, model):
        self.model = model

    def is_attack_by_suprise(self, char):
        return not self.is_fasterthan(char)

    def is_faster_than(self, char):
        return True if self.spd * px.rndf(1.0, 2.0) >= char.spd * px.rndf(1.0, 2.0) else False

    def is_remain_mp(self, spl):
        return True if self.mp >= spl.mp and px.rndi(0, 1) == 0 else False

    # 攻撃
    def normal_attack(self, target):
        log = []
        # クリティカル判定（10%）
        critical = px.rndf(0.0, 1.0) < 0.1

        log += [f"{self.name}の こうげき"]

        def __hit_rate(target):
            hit_rate = max(min(self.spd / target.spd, 1.5), 0.25)
            hit_rate = min(hit_rate - px.rndf(0.0, 1.0), 1.0)
            return hit_rate

        rate = __hit_rate(target)
        if rate > 0.0:
            dmg = self.take_damage(target)
            log += [f"{target.name}に {dmg}ダメージ"]
            log += self.check_alive(target)
        else:
            log += [f"{target.name}は みをかわした"]
        return log

    # ダメージ処理
    def take_damage(self, target):
        dmg = int(self.atk * px.rndi(0, 3) + 0.99)
        target.hp = max(target.hp - dmg, 0)
        return dmg

    def check_alive(self, target):
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


