
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


    def add_status(self, status_name, turns, battle):
        log = []
        self.mdl.status[status_name] = turns
        log += [f" {self.mdl.name} は {status_name} 状態になった！（{turns}ターン）"]
        if log:
            battle.stack_btllog(log)

    def process_status(self, battle):
        log = []
        badsts = [ 
                {'name':'paralyze' , 'desc': f"{self.mdl.name} は麻痺で動けない！", 'rate': 0.5}, 
                {'name':'confusion', 'desc': f"{self.mdl.name} は混乱している！"  , 'rate': 0.5},
        ]
        for bad in badsts:
            if bad['name'] in self.mdl.status:
                if random.random() < bad['rate']:  # 一定確率で行動不能
                    log += [f"{bad['desc']}"]
                    self.mdl.status[bad['name']] -= 1
                    if self.mdl.status[bad['name']] <= 0:
                        del self.mdl.status[bad['name']]
        if log:
            battle.stack_btllog(log)


    def end_turn_status(self, battle):
        log = []
        badsts = [ 
                {'name':'poison', 'desc': "毒"  , 'dmg': self.calc_chip_damage}, 
                {'name':'bleed' , 'desc': "出血", 'dmg': self.calc_chip_damage},
        ]
        for bad in badsts:
            if bad['name'] in self.mdl.status:
                dmg = self.calc_chip_damage()
                log += [f"{self.mdl.name} は"]
                log += [f"{bad['desc']}" + f"で {dmg} ダメージ！"]
                self.mdl.status[bad['name']] -= 1
                if self.mdl.status[bad['name']] <= 0:
                    del self.mdl.status[bad['name']]
        if log:
            battle.stack_btllog(log)
            SkillMeth.visual_effect(self.mdl.vm.set_chip_damage, self.mdl, self.mdl, battle, **{'dmg': dmg})

    def calc_chip_damage(self):
        dmg = max(1, self.mdl.mhp // 10)
        return dmg
    def set_chip_damage(self, target, dmg):
        target.hp = max(target.hp - dmg, 0)


    def use_mp(self, cost):
        if self.mdl.mp >= cost:
            self.mdl.mp -= cost
            return True
        return False

    def heal(self, target, battle):
        spells = [
            {'name': 'ヒール', 'type': 'support', 'power': 20, 'mp': 2, 'desc': 'HPが回復した！'},
        ]
        log = []
        rcv = 0

        log += [f"{self.mdl.name} は {spells[0]['name']}を唱えた！"]

        if self.mdl.use_mp(spells[0]['mp']):
            rcv = self.calc_heal_support()
            log += [f"{target.name} は {rcv} {spells[0]['desc']}"]
        else:
            log += [f"MPが足りない！"]

        if log:
            battle.stack_btllog(log)
        return rcv


    def calc_heal_support(self):
        recov = random.randint(8, 15)
        return recov
    def set_heal_support(self, target, recov):
        target.hp = min(target.mhp, target.hp + recov)

