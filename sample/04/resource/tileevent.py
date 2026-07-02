
import pyxel as px
from enum import Enum, Flag, IntEnum, auto
import appconfig as gbl
from UI import *
from resource.mapevent import *
from functools import partial


#システム上の、タイル基本サイズは 8x8
BASE_TILE_SIZE = 8
#本ゲームの基本サイズは,16
TILE_SIZE = BASE_TILE_SIZE * 2




class TILE(IntEnum):
    WALL = 0
    SPRING = auto()
    UPSTAIR = auto()
    DOWNSTAIR = auto()
    DOOR = auto()
    CHEST = auto()
    NPC1 = auto()
    NPC2 = auto()
    NOTHING = auto()




class TileEvents:

    @staticmethod
    def drink_spring_water(*args, **kwargs):
        pt = kwargs['pt']
        t = ["かいふくの いずみだ", "HP MP かいふく！"]
        Window.message(t)
        for _, mem in enumerate(pt):
            mem.hp = mem.mhp
            mem.mp = mem.mmp

    @staticmethod
    def step_updown_stairs(*args, **kwargs):
        pt = kwargs['pt']
        evt = kwargs['evt']
        mrk = MapTiles.table[TILE.DOWNSTAIR]['SYMBOL']
        pt.z += 1 if evt == mrk else -1

        # エンディング判定
        if pt.z == 0 and "4-3" in pt.flags and not "end" in pt.flags:
            Window.message(["ゲームクリア！"])
            pt.flags.append("end")
        else:
            Window.message([f"ちか{pt.z+1}かい"])



class MapTiles:

    #POS    イメージバンク内で、該当タイルが定義されている座標
    #LETTER タイルの種類を表すための独自定義
    table = {
        TILE.WALL       : {'POS':(0, 2), 'SYMBOL': '-', 'WALKABLE':  False, 'EVENT':  None},
        TILE.SPRING     : {'POS':(2, 2), 'SYMBOL': '@', 'WALKABLE':  False, 'EVENT':  TileEvents.drink_spring_water},
        TILE.UPSTAIR    : {'POS':(4, 0), 'SYMBOL': '<', 'WALKABLE':  True , 'EVENT':  TileEvents.step_updown_stairs},
        TILE.DOWNSTAIR  : {'POS':(6, 0), 'SYMBOL': '>', 'WALKABLE':  True , 'EVENT':  TileEvents.step_updown_stairs},
        TILE.NOTHING    : {'POS':None  , 'SYMBOL': '' , 'WALKABLE':  True , 'EVENT':  None},
    }

    @staticmethod
    def is_defined(pos):
        x, y, z = pos
        # NPC・扉・宝箱は、タイルマップに直書きしていないため、
        # px.tilemaps()　で検知できない。
        tm = px.tilemaps[z].pget(x * 2, y * 2)
        for _, row in MapTiles.table.items():
            if tm == row['POS']:
                return row
        return None
    
    @staticmethod
    def get_property(pos, prop):
        row = MapTiles.is_defined(pos)
        if row:
            return row[prop]
        return MapTiles.table[TILE.NOTHING][prop]

    @staticmethod
    def get_symbol(pos):
        return MapTiles.get_property(pos, 'SYMBOL')

    @staticmethod
    def is_walkable(pos):
        return MapTiles.get_property(pos, 'WALKABLE')

    @staticmethod
    def get_event(pos):
        return MapTiles.get_property(pos, 'EVENT')

    @staticmethod
    def exec_response(*args, **kwargs):
        pos = kwargs['pos']
        evt = MapTiles.get_event(pos)
        if evt:
            evt(*args, **kwargs)

    @staticmethod
    def is_event_already_flaged(pt, key):
            return True if key in pt.flags else False

    @staticmethod
    def exec_response_spring(*args, **kwargs):
        pos = kwargs['pos']
        pt = kwargs['pt']
        mrk = MapTiles.get_symbol(pos)

        if mrk == MapTiles.table[TILE.SPRING]['SYMBOL']:
            MapTiles.exec_response(*args, **kwargs)

    @staticmethod
    def exec_response_stairs(**kwargs):
        pos = kwargs['pos']
        pt = kwargs['pt']

        mrk = MapTiles.get_symbol(pos)
        up = MapTiles.table[TILE.UPSTAIR]['SYMBOL']
        dwn = MapTiles.table[TILE.DOWNSTAIR]['SYMBOL']

        if mrk in (up,dwn):
            partial(MapTiles.exec_response(**kwargs),evt=mrk)


