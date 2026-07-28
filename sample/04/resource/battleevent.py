
import random
from enum import Enum, Flag, IntEnum, auto

from module.constant import EFCT







class SKLTYP(Enum):
    ATTK = 'attack'
    SUPP = 'support'
    DEFE = 'defence'
    SPEC = 'special'
    NODE = 'subcate'







class SkillMeth:

    @staticmethod
    def choice_one(target):
        # 循環参照対策
        # if isinstance(target, BaseParty):
        if isinstance(target.type, list):
            targets = [p for p in target if p.is_alive()]
            if targets:
                return random.choice(targets)
        return target

    @staticmethod
    def visual_effect(func, user, target, battle, **kwargs):
        efct = ''
        if 'dmg' in kwargs:
            dmg = kwargs['dmg']
            if dmg > 0:
                if target.is_player:
                    efct = EFCT.DMG
                else:
                    efct = EFCT.ATK
        elif 'rcv' in kwargs:
            rcv = kwargs['rcv']
            if rcv > 0:
                efct = EFCT.BUF
        if efct:
            battle.stack_effect(efct)
            battle.stack_reflect(func, user, target, **kwargs)


    # 1アクションにつき、最大３つをstack
    # first　log     戦闘ログ　ダメージ算出
    # middle effect  視覚効果
    # last   reflect ダメージ反映
    @staticmethod
    def single_attack(user, target, battle):
        dmg = user.vm.attack(target, battle)
        SkillMeth.visual_effect(user.vm.set_normal_damage, user, target, battle, **{'dmg': dmg})

    def normal_attack(user, target, battle):
        target = SkillMeth.choice_one(target)
        SkillMeth.single_attack(user, target, battle)
        # 生存判定はダメージ反映後
        # user.vm.check_vital(target, battle)

    @staticmethod
    def poison_attack(user, target, battle):
        target = SkillMeth.choice_one(target)
        SkillMeth.single_attack(user, target, battle)
        # 単体に限定していないと.is_alive()でエラー
        if target.is_alive() and random.random() < 0.5:
            target.vm.add_status("poison", 3, battle)

    @staticmethod
    def paralyze_attack(user, target, battle):
        target = SkillMeth.choice_one(target)
        SkillMeth.single_attack(user, target, battle)
        if target.is_alive() and random.random() < 0.4:
            target.vm.add_status("paralyze", 3)

    @staticmethod
    def heal(user, target, battle):
        rcv = user.vm.heal(target, battle)
        SkillMeth.visual_effect(user.vm.set_heal_support, user, target, battle, **{'rcv': rcv})

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




class SKLResour:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SKLResour, cls).__new__(cls)
            cls._instance.skills = (
                ("攻撃", SkillMeth.normal_attack, SKLTYP.ATTK), 
                ("呪文", SkillMeth.poison_attack, SKLTYP.ATTK),
                ("回復", SkillMeth.heal, SKLTYP.SUPP),
                ("防御", SkillMeth.heal, SKLTYP.DEFE),
                ("逃走", SkillMeth.heal, SKLTYP.SPEC),
            )

        return cls._instance









class SPLAREA(Flag):
    FLD = 'FIELD'
    BTL = 'BATTLE'


class SpellResources:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SpellResources, cls).__new__(cls)
            # 呪文データ
            cls._instance.spells = (
                [ 'ファイア', 2, [SPLAREA.BTL]             , ['ちいさな ひのたまを', 'てきにぶつけて ダメージ'] ],
                [ 'リターン', 6, [SPLAREA.FLD, SPLAREA.BTL], ['スタートいちに', 'テレポートする'] ],
                [ 'ヒール'  , 0, [SPLAREA.FLD, SPLAREA.BTL], ['HPを かいふく', 'かいふくしたぶんMPをつかう'] ],
                [ 'バースト', 0, [SPLAREA.BTL]             , ['すべての まりょくを', 'てきにぶつけて だいダメージ'] ],
            )

        return cls._instance





