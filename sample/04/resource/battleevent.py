
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
    def visual_effect(target, battle, **kwargs):
        amnt = 0
        efct = ''
        for val in kwargs.values():
            amnt = val if val > amnt else amnt
        if amnt == 0:
            return

        if 'dmg' in kwargs:
            efct = EFCT.DMG if target.is_player else EFCT.ATK
        elif 'rcv' in kwargs:
            efct = EFCT.BUF
        elif 'aoe' in kwargs:
            efct = EFCT.AOE

        battle.stack_effect(efct)


    # 1アクションにつき、最大３つをstack
    # first　log       戦闘ログ　ダメージ計算
    # middle effect    視覚効果
    # last   permanent ダメージ反映
    @staticmethod
    def single_attack(user, target, battle):
        dmg = user.vm.attack(target, battle)
        kwargs = {'dmg': dmg}
        SkillMeth.visual_effect(target, battle, **kwargs)
        battle.stack_permanent(user.vm.set_normal_damage, user, target, **kwargs)

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
        if not user.vm.ready_heal(target, battle):
            return
        #最優先や末尾だとエフェクトのタイミングが合わない
        SkillMeth.visual_effect(target, battle, rcv=999)
        rcv = user.vm.use_heal(target, battle)
        kwargs = {'rcv': rcv}
        battle.stack_permanent(user.vm.set_heal_support, user, target, **kwargs)

    @staticmethod
    def aoe(user, target, battle):
        if not user.vm.ready_aoe(target, battle):
            return
        #最優先や末尾だとエフェクトのタイミングが合わない
        SkillMeth.visual_effect(target, battle, aoe=999)
        for targ in target:
            if targ.is_alive():
                dmg = user.vm.use_aoe(targ, battle)
                kwargs = {'aoe': dmg}
                battle.stack_permanent(user.vm.set_normal_damage, user, targ, **kwargs)

    @staticmethod
    def escape(user, target, battle):
        if not user.vm.try_escape(target, battle):
            return
        battle.stack_btlrun()







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





