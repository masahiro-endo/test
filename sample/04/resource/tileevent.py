
import pyxel as px
from enum import Enum, Flag, IntEnum, auto
import appconfig as gbl
from UI import *
from resource.mapevent import *


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
    NOTHING = auto()




class TileEvents:

    @staticmethod
    def drink_spring_water(pt):
        t = ["かいふくの いずみだ", "HP MP かいふく！"]
        Window.message(t)
        for member in enumerate(pt):
            member.hp = member.mhp
            member.mp = member.mmp

    @staticmethod
    def step_updown_stairs(pt, evt):
        mrk = MapTiles.table[TILE.DOWNSTAIR]['SYMBOL']
        pt.z += 1 if evt == mrk else -1

        # エンディング判定
        if pt.z == 0 and "4-3" in pt.flags and not "end" in pt.flags:
            Window.message(["ゲームクリア！"])
            pt.flags.append("end")
        else:
            Window.message([f"ちか{pt.z+1}かい"])



class MapTiles:
    friend: 'MapEvents' 

    #POS    イメージバンク内で、該当タイルが定義されている座標
    #LETTER タイルの種類を表すための独自定義
    table = {
        TILE.WALL       : {'POS':(0, 2), 'SYMBOL': '-', 'WALKABLE':  False, 'EVENT':  None},
        TILE.SPRING     : {'POS':(2, 2), 'SYMBOL': '@', 'WALKABLE':  False, 'EVENT':  TileEvents.drink_spring_water},
        TILE.UPSTAIR    : {'POS':(4, 0), 'SYMBOL': '<', 'WALKABLE':  True , 'EVENT':  TileEvents.step_updown_stairs},
        TILE.DOWNSTAIR  : {'POS':(6, 0), 'SYMBOL': '>', 'WALKABLE':  True , 'EVENT':  TileEvents.step_updown_stairs},
        TILE.DOOR       : {'POS':(4, 1), 'SYMBOL': '#', 'WALKABLE':  True , 'EVENT':  None},
        TILE.CHEST      : {'POS':(6, 1), 'SYMBOL': '$', 'WALKABLE':  False, 'EVENT':  None},
        TILE.NOTHING    : {'POS':None  , 'SYMBOL': '' , 'WALKABLE':  True , 'EVENT':  None},
    }

    @staticmethod
    def is_exist_table(pos):
        x, y, z = pos
        tm = px.tilemaps[z].pget(x * 2, y * 2)
        for _, row in MapTiles.table.items():
            if tm == row['POS']:
                return row
        return None
    
    @staticmethod
    def get_property(pos, prop):
        row = MapTiles.is_exist_table(pos)
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
        evt = MapTiles.get_event(*args, **kwargs)
        if evt:
            evt(*args, **kwargs)

    @staticmethod
    def is_event_already_flaged(pt, key):
            return True if key in pt.flags else False

    @staticmethod
    def exec_response_spring(*args, **kwargs):
        pt = kwargs.items('pt')
        pos = kwargs.items('pos')
        mrk = MapTiles.get_symbol(pos)

        if mrk == MapTiles.table[TILE.SPRING]['SYMBOL']:
            MapTiles.exec_response(pos, pt)

    @staticmethod
    def exec_response_stairs(*args, **kwargs):
        pt = kwargs.items('pt')
        pos = kwargs.items('pos')

        mrk = MapTiles.get_symbol(pos)
        up = MapTiles.table[TILE.UPSTAIR]['SYMBOL']
        dwn = MapTiles.table[TILE.DOWNSTAIR]['SYMBOL']

        if mrk in (up,dwn):
            MapTiles.exec_response(*args, **kwargs)


