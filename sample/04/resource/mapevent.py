
import pyxel as px
from enum import Enum, Flag, IntEnum, auto
import appconfig as gbl
from module.UI import *
from resource.battleevent import *





class OBS(IntEnum):
    DOOR = 0
    CHEST = auto()
    NPC = auto()

class TRE(IntEnum):
    EMPTY = 0
    KEY = auto()
    GOLD = auto()




class Obstacle:
    def __init__(self, pos3, kind, resp=None):
        self.x, self.y, self.z = pos3
        self.kind = kind
        self.resp = resp

    def draw(self, pl_x, pl_y, pl_z):
        ox = self.x * 16 - pl_x
        oy = self.y * 16 - pl_y
        if abs(ox) < 64 and abs(oy) < 64 and abs(self.z == pl_z):
            (u, v) = self.refernce_grid()
            # blt(x, y, imgbank, u, v, w, h, [colkey])
            sz = 16 #TILE_SIZE
            px.blt(56 + ox, 48 + oy, 0, u * sz, v * sz, sz, sz, 1)

    def refernce_grid(self):
        pass

    # 可変長引数で、wrapper関数 
    def response(self, *args, **kwargs):
        if self.resp:
            self.resp(*args, **kwargs)


class Door(Obstacle):
    def __init__(self, pos, resp=None):
        self.kind = OBS.DOOR
        super().__init__(pos, self.kind, resp)
    def refernce_grid(self):
        return (2, 1)

class Chest(Obstacle):
    def __init__(self, pos, resp=None, content=None):
        self.kind = OBS.CHEST
        self.content = content
        super().__init__(pos, self.kind, resp)
    def refernce_grid(self):
        return (3, 1)

class NPC(Obstacle):
    def __init__(self, pos, resp=None):
        self.kind = OBS.NPC
        super().__init__(pos, self.kind, resp)
    def refernce_grid(self):
        return (2 + (px.frame_count % 30) // 15, 2)





class Treasure:
    def __init__(self, clas,  disc):
        self.clas = clas
        self.disc = disc
    def effect(self):
        pass

class DoorKey(Treasure):
    def __init__(self, disc):
        self.clas = TRE.KEY
        super().__init__(self.clas, disc)
    def effect(self, *args, **kwargs):
        pt = kwargs['pt']
        pt.keys += 1

class Gold(Treasure):
    def __init__(self, amount):
        self.clas = TRE.GOLD
        self.amount = amount
        self.disc = str(amount) + 'G'
        super().__init__(self.clas, self.disc)
    def effect(self, *args, **kwargs):
        pt = kwargs['pt']
        pt.add_gold(self.amount)



class MapMeth:

    @staticmethod
    def get_obs_key(pos3):
        x, y, z = pos3
        for key, ob in gbl.map_resource().obstacles.items():
            if (ob.x, ob.y, ob.z) == (x, y, z):
                return key
        return ""

    @staticmethod
    def open_chest(*args, **kwargs):
        pt = kwargs['pt']
        ob = kwargs['ob']

        t = ["たからばこだ！"]
        t += [f"{ob.desc}を てにいれた"]
        ob.content.effect(*args, **kwargs)

        Window.message(t)
        pt.flags.append(ob.evt)

    @staticmethod
    def unlock_the_door(*args, **kwargs):
        pt = kwargs['pt']
        evt = kwargs['evt']
        if pt.keys:
            # px.play(3, 33)
            Window.message(["カギを あけた"])
            pt.flags.append(evt)
            pt.keys -= 1
            pt.wait = True
        else:
            Window.message(["カギを もっていない"])

    @staticmethod
    def talk_only_npc(*args, **kwargs):
        evt = kwargs['evt']
        if evt in gbl.map_resource().talks.keys():
            Window.message(gbl.map_resource().talks[evt])


    @staticmethod
    def talk_npc_0F1(*args, **kwargs):
        pt = kwargs['pt']
        if "4-3" in pt.flags:
            Window.message(["ぜひ Pyxelを", "マスターしてくれ"])
        else:
            MapMeth.talk_only_npc(*args, **kwargs)

    @staticmethod
    def talk_npc_0F3(*args, **kwargs):
        gbl.current_scene().context.currentState.map.Shop()

    @staticmethod
    def talk_npc_1F2(*args, **kwargs):
        pt = kwargs['pt']
        evt = kwargs['evt']
        if evt == "1-2" and not "sp1" in pt.flags:
            Window.message(["リターンの じゅもんを", "さずけよう"])
            pt.flags.append("sp1")

    @staticmethod
    def talk_npc_2F5(*args, **kwargs):
        pt = kwargs['pt']
        evt = kwargs['evt']
        if evt == "2-5" and not "sp2" in pt.flags:
            Window.message(["じゅんびは よいか？", " はい  いいえ"])
            gbl.current_cursor = Cursor("boss1", [1, 5], 14, 1)

    @staticmethod
    def talk_npc_3F1(*args, **kwargs):
        pt = kwargs['pt']
        evt = kwargs['evt']
        if evt == "3-1" and not "sp3" in pt.flags:
            Window.message(["おれと たたかうのか？", " はい  いいえ"])
            gbl.current_cursor = Cursor("boss2", [1, 5], 14, 1)

    @staticmethod
    def talk_npc_4F3(*args, **kwargs):
        evt = kwargs['evt']
        if evt == "4-3":
            Window.message(["この ひほうが ほしいか？", " はい  いいえ"])
            gbl.current_cursor = Cursor("boss3", [1, 5], 14, 1)




class MapResources:

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MapResources, cls).__new__(cls)
            # 障害物（ドア、宝箱、NPC）データ
            cls._instance.obstacles = {
                '0-1':   NPC( ( 8, 19, 0), MapMeth.talk_npc_0F1),
                '0-2':   NPC( ( 3, 19, 0), MapMeth.talk_only_npc),
                '0-3':   NPC( ( 8, 28, 0), MapMeth.talk_npc_0F3),
                '0-4':   NPC( (12, 19, 0), MapMeth.talk_only_npc),
                '0-5':   NPC( (12, 28, 0), MapMeth.talk_only_npc),
                '0-6': Chest( (11, 16, 0), MapMeth.open_chest, DoorKey('ゼロのカギ')),  # カギ0
                '0-7': Chest( (11, 17, 0), MapMeth.open_chest, Gold(100) ),
                '0-8':  Door( ( 4, 25, 0), MapMeth.unlock_the_door),
                '0-9':   NPC( ( 5, 27, 0), MapMeth.talk_only_npc),
                '1-1':  Door( ( 4,  6, 1), MapMeth.unlock_the_door),  # ドア1（直行）
                '1-2':   NPC( (27,  3, 1), MapMeth.talk_npc_1F2),
                '1-3': Chest( ( 7, 21, 1), MapMeth.open_chest, Gold( 50) ),
                '1-4': Chest( ( 8, 12, 1), MapMeth.open_chest, Gold(  6) ),
                '1-5': Chest( (12, 12, 1), MapMeth.open_chest, Gold(110) ),
                '1-6': Chest( (16, 24, 1), MapMeth.open_chest, Gold( 80) ),
                '1-7': Chest( (24, 10, 1), MapMeth.open_chest, DoorKey('イチのカギ') ),  # カギ1
                '1-8':  Door( (13,  8, 1), MapMeth.unlock_the_door),  # ドア2（宝部屋）
                '1-9': Chest( ( 8,  7, 1), MapMeth.open_chest, Gold(100) ),
                '1-10':Chest( (11,  7, 1), MapMeth.open_chest, Gold(100) ),
                '1-11':Chest( ( 8,  9, 1), MapMeth.open_chest, Gold(100) ),
                '1-12':Chest( (11,  9, 1), MapMeth.open_chest, Gold(100) ),
                '2-1': Chest( (17, 10, 2), MapMeth.open_chest, Gold(170) ),
                '2-2': Chest( (17, 20, 2), MapMeth.open_chest, Gold( 73) ),
                '2-3': Chest( (21, 10, 2), MapMeth.open_chest, Gold( 25) ),
                '2-4': Chest( (21, 20, 2), MapMeth.open_chest, Gold(256) ),
                '2-5':   NPC( (21,  4, 2), MapMeth.talk_npc_2F5),
                '2-6': Chest( (28, 28, 2), MapMeth.open_chest, DoorKey('ニのカギ') ),  # カギ2
                '2-7':  Door( (23,  4, 2), MapMeth.unlock_the_door),  # ドア3（ヒール）
                '3-1':   NPC( ( 6, 22, 3), MapMeth.talk_npc_3F1),
                '3-2':  Door( ( 4,  6, 3), MapMeth.unlock_the_door),  # ドア4（直行）
                '3-3': Chest( (24, 12, 3), MapMeth.open_chest, DoorKey('サンのカギ') ),  # カギ3
                '3-4': Chest( (25, 12, 3), MapMeth.open_chest, Gold(1000) ),
                '3-5':  Door( ( 4, 10, 3), MapMeth.unlock_the_door),  # ドア5
                '4-1': Chest( (16, 11, 4), MapMeth.open_chest, DoorKey('ヨンのカギ') ),  # カギ4
                '4-2': Chest( (18, 25, 4), MapMeth.open_chest, DoorKey('ゴのカギ') ),  # カギ5
                '4-3':   NPC( ( 4, 27, 4), MapMeth.talk_npc_4F3),
            }
            # 会話イベントデータ
            cls._instance.talks = {
                '0-1': ['ちか5かいに ねむる', 'ひほうを さがしてまいれ'],
                '0-2': ['いずみのみずを のむと', 'HPとMPが かいふくするぞ'],
                '0-4': ['XキーかBボタンで', 'メニューを ひらけるぞ'],
                '0-5': ['とびらを あけるには', 'カギが ひつようだ'],
                '0-9': ['このさきには', 'モンスターが でるぜ'],
                '1-2': ['おまえには もう', 'おしえることは ないよ'],
                '2-5': ['まいった！'],
                '3-1': ['チクショウ！'],
            }
            # モンスターデータ
            # name, hp, mp, atk, spd, resist, img, gold, skills
            # クラス化すると、循環参照を考慮せねばならないので配列で
            # Character生成時の、引数リストとして、下記配列行を渡す。
            cls._instance.monsters = (
                ['かぼちゃ',  12, 0,  6, 12, 0, 0,  20, [("攻撃", SkillMeth.normal_attack, SKLTYP.ATTK)] ],
                ['こおに'  ,  24, 0, 10, 13, 0, 1,  40, [("攻撃", SkillMeth.normal_attack, SKLTYP.ATTK)] ],
                ['おにび'  ,  32, 2, 14, 18, 1, 2,  80, [("攻撃", SkillMeth.normal_attack, SKLTYP.ATTK)] ],
                ['ゆうれい',  40, 0, 17, 32, 0, 3, 160, [("麻痺攻撃", SkillMeth.paralyze_attack, SKLTYP.ATTK)] ],
                ['にんじゃ',  64, 0, 34, 28, 0, 4, 320, [("攻撃", SkillMeth.normal_attack, SKLTYP.ATTK), ("毒攻撃", SkillMeth.poison_attack, SKLTYP.ATTK)] ],
                ['まどうし', 120, 4,  8, 15, 0, 5,   0, [("魔法", SkillMeth.normal_attack, SKLTYP.ATTK) ] ],
                ['だてんし', 200, 0, 20, 27, 1, 6,   0, [("氷魔法", SkillMeth.normal_attack, SKLTYP.ATTK)  ] ],
                ['めがみ'  , 400, 0, 99, 99, 0, 7,   0, [("全体魔法", SkillMeth.aoe, SKLTYP.ATTK)] ],
            )

        return cls._instance




