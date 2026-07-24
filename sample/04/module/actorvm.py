
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
        self.mdl = model

    def is_attack_by_suprise(self, char):
        return not self.is_fasterthan(char)

    def is_faster_than(self, char):
        return True if self.mdl.spd * px.rndf(1.0, 2.0) >= char.spd * px.rndf(1.0, 2.0) else False

    def is_remain_mp(self, spl):
        return True if self.mdl.mp >= spl.mp and px.rndi(0, 1) == 0 else False


    def attack(self, target, battle):
        log = []
        dmg = 0
        # クリティカル判定（10%）
        critical = px.rndf(0.0, 1.0) < 0.1

        log += [f"{self.mdl.name}の こうげき"]

        def __hit_rate(target):
            hit_rate = max(min(self.mdl.spd / target.spd, 1.5), 0.25)
            hit_rate = min(hit_rate - px.rndf(0.0, 1.0), 1.0)
            return hit_rate

        rate = __hit_rate(target)
        if rate > 0.0:
            dmg = self.calc_narmal_damage(target)
            log += [f"{target.name}に {dmg}ダメージ"]
        else:
            log += [f"{target.name}は みをかわした"]

        if log:
            battle.stack_btllog(log)
        return dmg

    # 時間差の視覚効果用に、
    # 値の計算と反映を分割する
    def calc_narmal_damage(self, target):
        dmg = int(self.mdl.atk * px.rndi(0, 3) + 0.99)
        return dmg
    def set_normal_damage(self, target, dmg):
        target.hp = max(target.hp - dmg, 0)


    def check_vital(self, target, battle):
        log = []
        if not target.is_alive():
            if not target.is_player:
                log += [f"{target.name}を たおした"]
            else:
                log += [f"{target.name}は たおれた"]
        if log:
            battle.stack_btllog(log, True)

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


    def add_status(self, status_name, turns, battle):
        log = []
        self.mdl.status[status_name] = turns
        log += [f" {self.mdl.name} は {status_name} 状態になった！（{turns}ターン）"]
        if log:
            battle.stack_btllog(log)

    def process_status(self, battle):
        log = []
        if "paralyze" in self.mdl.status:
            if random.random() < 0.5:  # 50%で行動不能
                log += [f"{self.mdl.name} は麻痺で動けない！"]
                self.mdl.status["paralyze"] -= 1
                if self.mdl.status["paralyze"] <= 0:
                    del self.mdl.status["paralyze"]
        if log:
            battle.stack_btllog(log)


    def end_turn_status(self, battle):
        log = []
        if "poison" in self.mdl.status:
            dmg = self.calc_poison_damage()
            log += [f"{self.mdl.name} は毒で {dmg} ダメージ！（残りHP: {self.mdl.hp}）"]
            self.mdl.status["poison"] -= 1
            if self.mdl.status["poison"] <= 0:
                del self.mdl.status["poison"]
        if log:
            battle.stack_btllog(log)
            SkillMeth.visual_effect(self.mdl.vm.set_poison_damage, self.mdl, self.mdl, battle, **{'dmg': dmg})

    def calc_poison_damage(self):
        dmg = max(1, self.mdl.mhp // 10)
        return dmg
    def set_poison_damage(self, target, dmg):
        target.hp = max(target.hp - dmg, 0)

