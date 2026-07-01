
import pyxel as px
from enum import Enum, Flag, IntEnum, auto
import appconfig as gbl
from UI import *





class OBS(IntEnum):
    DOOR = 0
    TREASURE = auto()
    NPC = auto()


class ACTOR(Flag):
    ISPLAYER = True
    ISENEMY = False




# フィールド用障害物（kind = 0:ドア 1:宝箱 2:人）
class Obstacle:
    def __init__(self, evt, x, y, z, kind, val=0, resp = None):
        self.evt = evt
        self.x = x
        self.y = y
        self.z = z
        self.kind = kind
        self.val = val
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
    def __init__(self, evt, x, y, z, resp = None):
        self.kind = OBS.DOOR
        super().__init__(evt, x, y, z, self.kind, 0, resp)
    def refernce_grid(self):
        return (2, 1)

class Chest(Obstacle):
    def __init__(self, evt, x, y, z, val=0, resp = None):
        self.kind = OBS.TREASURE
        super().__init__(evt, x, y, z, self.kind, val, resp)
    def refernce_grid(self):
        return (3, 1)

class NPC(Obstacle):
    def __init__(self, evt, x, y, z, resp = None):
        self.kind = OBS.NPC
        super().__init__(evt, x, y, z, self.kind, 0, resp)
    def refernce_grid(self):
        return (2 + (px.frame_count % 30) // 15, 2)





class MapEvents:

    @staticmethod
    def get_obs_key(pos3d):
        x, y, z = pos3d
        for key, ob in gbl.map_resource.obstacles:
            if (ob.x, ob.y, ob.z) == (x, y, z):
                return key
        return ""

    @staticmethod
    def open_chest(pt, ob):
        t = ["たからばこだ！"]
        if ob.val:
            t += [f"{ob.val}G てにいれた"]
            pt.add_gold(ob.val)
        else:
            t += [f"カギを てにいれた"]
            pt.keys += 1
        Window.message(t)
        pt.flags.append(ob.evt)

    @staticmethod
    def unlock_the_door(pt, evt):
        if pt.keys:
            # px.play(3, 33)
            Window.message(["カギを あけた"])
            pt.flags.append(evt)
            pt.keys -= 1
            pt.wait = True
        else:
            Window.message(["カギを もっていない"])

    @staticmethod
    def talk_only_npc(evt):
        if evt in gbl.map_resource().talks:
            Window.message(gbl.map_resource.talks[evt])


    @staticmethod
    def talk_npc_0F1(pt, evt):
        if "4-3" in pt.flags:
            Window.message(["ぜひ Pyxelを", "マスターしてくれ"])
        else:
            MapEvents.talk_only_npc(evt)

    @staticmethod
    def talk_npc_0F3():
        gbl.scene.currentMap.Shop()

    @staticmethod
    def talk_npc_1F2(pt, evt):
        if evt == "1-2" and not "sp1" in pt.flags:
            Window.message(["リターンの じゅもんを", "さずけよう"])
            pt.flags.append("sp1")

    @staticmethod
    def talk_npc_2F5(pt, evt):
        if evt == "2-5" and not "sp2" in pt.flags:
            Window.message(["じゅんびは よいか？", " はい  いいえ"])
            gbl.current_cursor = Cursor("boss1", [1, 5], 14, 1)

    @staticmethod
    def talk_npc_3F1(pt, evt):
        if evt == "3-1" and not "sp3" in pt.flags:
            Window.message(["おれと たたかうのか？", " はい  いいえ"])
            gbl.current_cursor = Cursor("boss2", [1, 5], 14, 1)

    @staticmethod
    def talk_npc_4F3(evt):
        if evt == "4-3":
            Window.message(["この ひほうが ほしいか？", " はい  いいえ"])
            gbl.current_cursor = Cursor("boss3", [1, 5], 14, 1)




class MapResources:

    KEY = 0

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MapResources, cls).__new__(cls)
            # 障害物（ドア、宝箱、NPC）データ
            cls._instance.obstacles = {
                "0-1" :   NPC("0-1"  , 8, 19, 0,      MapEvents.talk_npc_0F1),
                "0-2" :   NPC("0-2"  , 3, 19, 0,      MapEvents.talk_only_npc),
                "0-3" :   NPC("0-3"  , 8, 28, 0,      MapEvents.talk_npc_0F3),
                "0-4" :   NPC("0-4"  ,12, 19, 0,      MapEvents.talk_only_npc),
                "0-5" :   NPC("0-5"  ,12, 28, 0,      MapEvents.talk_only_npc),
                "0-7" : Chest("0-7"  ,11, 17, 0, 100, MapEvents.open_chest),
                "0-8" :  Door("0-8"  , 4, 25, 0,      MapEvents.unlock_the_door),
                "0-9" :   NPC("0-9"  , 5, 27, 0,      MapEvents.talk_only_npc),
                "1-1" :  Door("1-1"  , 4,  6, 1,      MapEvents.unlock_the_door),  # ドア1（直行）
                "1-2" :   NPC("1-2"  ,27,  3, 1,      MapEvents.talk_npc_1F2),
                "1-3" : Chest("1-3"  , 7, 21, 1,  50, MapEvents.open_chest),
                "1-4" : Chest("1-4"  , 8, 12, 1,   6, MapEvents.open_chest),
                "1-5" : Chest("1-5"  ,12, 12, 1, 110, MapEvents.open_chest),
                "1-6" : Chest("1-6"  ,16, 24, 1,  80, MapEvents.open_chest),
                "1-7" : Chest("1-7"  ,24, 10, 1, cls.KEY, MapEvents.open_chest),  # カギ1
                "1-8" :  Door("1-8"  ,13,  8, 1,      MapEvents.unlock_the_door),  # ドア2（宝部屋）
                "1-9" : Chest("1-9"  , 8,  7, 1, 100, MapEvents.open_chest),
                "1-10": Chest("1-10" ,11,  7, 1, 100, MapEvents.open_chest),
                "1-11": Chest("1-11" , 8,  9, 1, 100, MapEvents.open_chest),
                "1-12": Chest("1-12" ,11,  9, 1, 100, MapEvents.open_chest),
                "2-1" : Chest("2-1"  ,17, 10, 2, 170, MapEvents.open_chest),
                "2-2" : Chest("2-2"  ,17, 20, 2,  73, MapEvents.open_chest),
                "2-3" : Chest("2-3"  ,21, 10, 2,  25, MapEvents.open_chest),
                "2-4" : Chest("2-4"  ,21, 20, 2, 256, MapEvents.open_chest),
                "2-5" :   NPC("2-5"  ,21,  4, 2,      MapEvents.talk_npc_2F5),
                "2-6" : Chest("2-6"  ,28, 28, 2, cls.KEY, MapEvents.open_chest),  # カギ2
                "2-7" :  Door("2-7"  ,23,  4, 2,      MapEvents.unlock_the_door),  # ドア3（ヒール）
                "3-1" :   NPC("3-1"  , 6, 22, 3,      MapEvents.talk_npc_3F1),
                "3-2" :  Door("3-2"  , 4,  6, 3,      MapEvents.unlock_the_door),  # ドア4（直行）
                "3-3" : Chest("3-3"  ,24, 12, 3, cls.KEY, MapEvents.open_chest),  # カギ3
                "3-4" : Chest("3-4"  ,25, 12, 3,1000, MapEvents.open_chest),
                "3-5" :  Door("3-5"  , 4, 10, 3,      MapEvents.unlock_the_door),  # ドア5
                "4-1" : Chest("4-1"  ,16, 11, 4, cls.KEY, MapEvents.open_chest),  # カギ4
                "4-2" : Chest("4-2"  ,18, 25, 4, cls.KEY, MapEvents.open_chest),  # カギ5
                "4-3" :   NPC("4-3"  , 4, 27, 4,      MapEvents.talk_npc_4F3),
            }
            # 会話イベントデータ
            cls._instance.talks = {
                "0-1": ["ちか5かいに ねむる", "ひほうを さがしてまいれ"],
                "0-2": ["いずみのみずを のむと", "HPとMPが かいふくするぞ"],
                "0-4": ["XキーかBボタンで", "メニューを ひらけるぞ"],
                "0-5": ["とびらを あけるには", "カギが ひつようだ"],
                "0-9": ["このさきには", "モンスターが でるぜ"],
                "1-2": ["おまえには もう", "おしえることは ないよ"],
                "2-5": ["まいった！"],
                "3-1": ["チクショウ！"],
            }
            # モンスターデータ
            cls._instance.monsters = (
                ["かぼちゃ", 12, 0, 6, 12, ACTOR.ISENEMY, 0, 0, 20],
                ["こおに", 24, 0, 10, 13, ACTOR.ISENEMY, 0, 1, 40],
                ["おにび", 32, 2, 14, 18, ACTOR.ISENEMY, 1, 2, 80],
                ["ゆうれい", 40, 0, 17, 32, ACTOR.ISENEMY, 0, 3, 160],
                ["にんじゃ", 64, 0, 34, 28, ACTOR.ISENEMY, 0, 4, 320],
                ["まどうし", 120, 4, 8, 15, ACTOR.ISENEMY, 0, 5, 0],
                ["だてんし", 200, 0, 20, 27, ACTOR.ISENEMY, 1, 6, 0],
                ["めがみ", 400, 0, 99, 99, ACTOR.ISENEMY, 0, 7, 0],
            )

        return cls._instance




