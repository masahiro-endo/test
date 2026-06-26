
import pyxel as px
from enum import Enum, IntEnum, auto
import appconfig as gbl




class GameMap:

    class TILE(IntEnum):
        WALL = 0
        SPRING = auto()
        UPSTAIR = auto()
        DOWNSTAIR = auto()
        EXTRAEVENT = auto()
        NOTHING = auto()

    #POS    イメージバンク内で、該当タイルが定義されている座標
    #LETTER タイルの種類を表すための独自定義
    table = {
        TILE.WALL       : {"POS":(0, 2), "LETTER":  "-"},
        TILE.SPRING     : {"POS":(2, 2), "LETTER":  "@"},
        TILE.UPSTAIR    : {"POS":(4, 0), "LETTER":  "<"},
        TILE.DOWNSTAIR  : {"POS":(6, 0), "LETTER":  ">"},
        TILE.EXTRAEVENT : {"POS":None,  "LETTER": "detect another part"},
        TILE.NOTHING    : {"POS":None,  "LETTER": ""},
    }

    @staticmethod
    def get_map_event(pt):

        x = pt.x + pt.dx
        y = pt.y + pt.dy

        tm = px.tilemaps[pt.z].pget(x * 2, y * 2)
        for _, row in GameMap.table:
            if tm == row["POS"]:
                return row["LETTER"]
        
        for key, ob in gbl.resource().obstacles:
            if not key in gbl.player_party.flags and (ob.x, ob.y, ob.z) == (x, y, pt.z):
                return key
            
        return GameMap.table[GameMap.TILE.NOTHING]["LETTER"]




class OBS(IntEnum):
    DOOR = 0
    TREASURE = auto()
    NPC = auto()


class ACTOR(Enum):
    ISPLAYER = True
    ISENEMY = False




# フィールド用障害物（kind = 0:ドア 1:宝箱 2:人）
class Obstacle:
    def __init__(self, x, y, z, kind=0, val=0):
        self.x = x
        self.y = y
        self.z = z
        self.kind = kind
        self.val = val

    def draw(self, pl_x, pl_y, pl_z):
        ox = self.x * 16 - pl_x
        oy = self.y * 16 - pl_y
        if abs(ox) < 64 and abs(oy) < 64 and abs(self.z == pl_z):
            if self.kind == OBS.DOOR:
                u, v = 2, 1
            elif self.kind == OBS.TREASURE:
                u, v = 3, 1
            else:
                u, v = 2 + (px.frame_count % 30) // 15, 2
            px.blt(56 + ox, 48 + oy, 0, u * 16, v * 16, 16, 16, 1)




class MapResources:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MapResources, cls).__new__(cls)
            # 障害物（ドア、宝箱、NPC）データ
            cls._instance.obstacles = {
                "0-1": Obstacle(8, 19, 0, OBS.NPC),
                "0-2": Obstacle(3, 19, 0, OBS.NPC),
                "0-3": Obstacle(8, 28, 0, OBS.NPC),
                "0-4": Obstacle(12, 19, 0, OBS.NPC),
                "0-5": Obstacle(12, 28, 0, OBS.NPC),
                "0-6": Obstacle(11, 16, 0, OBS.TREASURE),
                "0-7": Obstacle(11, 17, 0, OBS.TREASURE, 100),
                "0-8": Obstacle(4, 25, 0, OBS.DOOR),
                "0-9": Obstacle(5, 27, 0, OBS.NPC),
                "1-1": Obstacle(4, 6, 1, OBS.DOOR),  # ドア1（直行）
                "1-2": Obstacle(27, 3, 1, OBS.NPC),
                "1-3": Obstacle(7, 21, 1, OBS.TREASURE, 50),
                "1-4": Obstacle(8, 12, 1, OBS.TREASURE, 6),
                "1-5": Obstacle(12, 12, 1, OBS.TREASURE, 110),
                "1-6": Obstacle(16, 24, 1, OBS.TREASURE, 80),
                "1-7": Obstacle(24, 10, 1, OBS.TREASURE),  # カギ1
                "1-8": Obstacle(13, 8, 1, OBS.DOOR),  # ドア2（宝部屋）
                "1-9": Obstacle(8, 7, 1, OBS.TREASURE, 100),
                "1-10": Obstacle(11, 7, 1, OBS.TREASURE, 100),
                "1-11": Obstacle(8, 9, 1, OBS.TREASURE, 100),
                "1-12": Obstacle(11, 9, 1, OBS.TREASURE, 100),
                "2-1": Obstacle(17, 10, 2, OBS.TREASURE, 170),
                "2-2": Obstacle(17, 20, 2, OBS.TREASURE, 73),
                "2-3": Obstacle(21, 10, 2, OBS.TREASURE, 25),
                "2-4": Obstacle(21, 20, 2, OBS.TREASURE, 256),
                "2-5": Obstacle(21, 4, 2, OBS.NPC),
                "2-6": Obstacle(28, 28, 2, OBS.TREASURE),  # カギ2
                "2-7": Obstacle(23, 4, 2, OBS.DOOR),  # ドア3（ヒール）
                "3-1": Obstacle(6, 22, 3, OBS.NPC),
                "3-2": Obstacle(4, 6, 3, OBS.DOOR),  # ドア4（直行）
                "3-3": Obstacle(24, 12, 3, OBS.TREASURE),  # カギ3
                "3-4": Obstacle(25, 12, 3, OBS.TREASURE, 1000),
                "3-5": Obstacle(4, 10, 3, OBS.DOOR),  # ドア5
                "4-1": Obstacle(16, 11, 4, OBS.TREASURE),  # カギ4
                "4-2": Obstacle(18, 25, 4, OBS.TREASURE),  # カギ5
                "4-3": Obstacle(4, 27, 4, OBS.NPC),
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




