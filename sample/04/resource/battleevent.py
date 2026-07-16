
import random
from enum import Enum, Flag, IntEnum, auto

from module.actorparty import *










class SkillMeth:

    @staticmethod
    def choice_single(target):
        if isinstance(target, Party):
            targets = [p for p in target if p.is_alive()]
            if targets:
                return random.choice(targets)
        return target

    @staticmethod
    def normal_attack(user, target):
        log  = []
        target = SkillMeth.choice_single(target)
        log += user.vm.attack(target)
        return log

    @staticmethod
    def poison_attack(user, target):
        log  = []
        target = SkillMeth.choice_single(target)
        log += user.vm.attack(target)
        if target.is_alive() and random.random() < 0.5:
            log += target.vm.add_status("poison", 3)
        return log

    @staticmethod
    def paralyze_attack(user, target):
        log  = []
        target = SkillMeth.choice_single(target)
        log += user.vm.attack(target)
        if target.is_alive() and random.random() < 0.4:
            log += target.vm.add_status("paralyze", 3)
        return log

    @staticmethod
    def heal(user, target):
        log  = []
        amount = random.randint(8, 15)
        target.hp = min(target.mhp, target.hp + amount)
        log += [f"{user.name} は 回復を唱えた！"]
        log += [f"{target.name} は {amount} 回復した！"]
        return log

    @staticmethod
    def aoe(user, target):
        log  = []
        log += [f"{user.name} の全体攻撃！"]
        for target in target.party:
            if target.is_alive():
                log += user.vm.attack(target)


    def normal_magic(user, target, battle):
        pass
    def ice_magic(user, target, battle):
        pass





class BattleAction:
    def __init__(self, parent):
        pass


# 個別行動
class BattleTurn:
    def __init__(self, actor, target, action):
        self.actor = actor
        self.target = target
        self.action = action

    def __lt__(self, other):
        return self.actor.btl_spd < other.actor.btl_spd

    


# 敵・味方 全員の行動一巡
# ラウンド開始直前に、味方全員分の行動を選択情報を保持。
# 敵ＡＩ分を追加した上で、ソートをかけ一気に処理を行う。
class BattleRound:
    def __init__(self, parent):
        self.turn_queue = []

    def push_turn(self, **kwargs):
        priority = kwargs['priority']
        if priority:
            self.queue.appendleft(kwargs)
        else:
            self.queue.append(kwargs)

    def run(self):
        while self.queue:
            kwargs = self.queue.popleft()
            func = kwargs['func']
            func(**kwargs)

    def ai_choose_action(self, allies, enemies):
        if self.hp < self.max_hp // 3 and random.random() < 0.3:
            target = random.choice([a for a in allies if a.is_alive()])
            return ("heal", target)
        elif random.random() < 0.2:
            return ("magic", enemies)
        else:
            target = random.choice([e for e in enemies if e.is_alive()])
            return ("attack", target)

    def start_turn(self):
        all_chars = [c for c in self.players + self.enemies if c.is_alive()]
        all_chars.sort(key=lambda c: c.speed, reverse=True)

        for char in all_chars:
            if char.is_alive():
                self.push_turn(self.take_action, char)


    def take_action(self, actor):
        if not actor.is_alive():
            return

        # 状態異常チェック
        if not actor.process_status():
            return

        # ターゲット選択
        if actor.is_player:
            targets = [e for e in self.enemies if e.is_alive()]
        else:
            targets = [p for p in self.players if p.is_alive()]

        if not targets:
            return

        target = random.choice(targets)

        # スキル選択（ランダム）
        skill_name, skill_func = random.choice(actor.skills)
        print(f"🌀 {actor.name} は {skill_name} を使った！")
        skill_func(actor, target, self)

        # 割り込み例：クリティカル
        if random.random() < 0.2:
            print(f"🔥 {actor.name} のクリティカル！追加攻撃！")
            self.push_event(self.take_action, actor, priority=True)

        # ターン終了時の状態異常処理
        actor.end_turn_status()










class SKL(Flag):
    FLD = 'FIELD'
    BTL = 'BATTLE'


class Skill:
    def __init__(self, name, cost, usable_place=None, desc=None):
        self.name = name
        self.cost = cost
        self.usable_place = usable_place if usable_place else []  # (履行可能場所・条件)
        self.desc = desc if desc else []

class Arts(Skill):
    def __init__(self, name, sp, place, desc):
        super().__init__(name, sp, place, desc)

class Spell(Skill):
    def __init__(self, name, mp, place, desc):
        super().__init__(name, mp, place, desc)



class SkillResources:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SkillResources, cls).__new__(cls)
            # 呪文データ
            cls._instance.spells = (
                [ 'ファイア', 2, [SKL.BTL]         , ['ちいさな ひのたまを', 'てきにぶつけて ダメージ'] ],
                [ 'リターン', 6, [SKL.FLD, SKL.BTL], ['スタートいちに', 'テレポートする'] ],
                [ 'ヒール'  , 0, [SKL.FLD, SKL.BTL], ['HPを かいふく', 'かいふくしたぶんMPをつかう'] ],
                [ 'バースト', 0, [SKL.BTL]         , ['すべての まりょくを', 'てきにぶつけて だいダメージ'] ],
            )

        return cls._instance





