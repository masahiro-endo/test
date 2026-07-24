
import random
from enum import Enum, Flag, IntEnum, auto











class SkillMeth:

    @staticmethod
    def choice_single(target):
        # 循環参照対策
        # if isinstance(target, BaseParty):
        if isinstance(target.type, list):
            targets = [p for p in target if p.is_alive()]
            if targets:
                return random.choice(targets)
        return target

    @staticmethod
    def visual_effect(func, user, target, battle, **kwargs):
        if 'dmg' in kwargs:
            dmg = kwargs['dmg']
            if dmg > 0:
                if target.is_player:
                    # とりあえず、プレイヤーがダメージを受けた時だけ
                    # 視覚効果を発動する
                    battle.stack_effect()
                battle.stack_reflect(func, user, target, **kwargs)

    # 1アクションにつき、最大３つをstack
    # first　log     戦闘ログ　ダメージ算出
    # middle effect  視覚効果
    # last   reflect ダメージ反映
    @staticmethod
    def normal_attack(user, target, battle):
        target = SkillMeth.choice_single(target)
        dmg = user.vm.attack(target, battle)
        SkillMeth.visual_effect(user.vm.set_normal_damage, user, target, battle, **{'dmg': dmg})
        # 生存判定はダメージ反映後
        # user.vm.check_vital(target, battle)

    @staticmethod
    def poison_attack(user, target, battle):
        SkillMeth.normal_attack(user, target, battle)
        if target.is_alive() and random.random() < 0.5:
            target.vm.add_status("poison", 3, battle)

    @staticmethod
    def paralyze_attack(user, target, battle):
        SkillMeth.normal_attack(user, target, battle)
        if target.is_alive() and random.random() < 0.4:
            target.vm.add_status("paralyze", 3)

    @staticmethod
    def heal(user, target, battle):
        log  = []
        amount = random.randint(8, 15)
        target.hp = min(target.mhp, target.hp + amount)
        log += [f"{user.name} は 回復を唱えた！"]
        log += [f"{target.name} は {amount} 回復した！"]
        return log

    @staticmethod
    def aoe(user, target, battle):
        log  = []
        log += [f"{user.name} の全体攻撃！"]
        for actor in target:
            if actor.is_alive():
                log += user.vm.attack(actor)
        return log


    def normal_magic(user, target, battle):
        pass
    def ice_magic(user, target, battle):
        pass







class SKL(Flag):
    FLD = 'FIELD'
    BTL = 'BATTLE'





class SpellResources:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SpellResources, cls).__new__(cls)
            # 呪文データ
            cls._instance.spells = (
                [ 'ファイア', 2, [SKL.BTL]         , ['ちいさな ひのたまを', 'てきにぶつけて ダメージ'] ],
                [ 'リターン', 6, [SKL.FLD, SKL.BTL], ['スタートいちに', 'テレポートする'] ],
                [ 'ヒール'  , 0, [SKL.FLD, SKL.BTL], ['HPを かいふく', 'かいふくしたぶんMPをつかう'] ],
                [ 'バースト', 0, [SKL.BTL]         , ['すべての まりょくを', 'てきにぶつけて だいダメージ'] ],
            )

        return cls._instance





