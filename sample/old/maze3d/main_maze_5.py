
import pyxel as px

import appconfig as gbl
from context import *
from actor import *
from map import *
from method import *







class App:

    def __init__(self):

        px.init(192, 128)
        # px.init(256, 192, fps=5)

        gbl._party = PlayerParty()
        gbl._map = dungeonB1._map

        px.run(self.update, self.draw)


    def update(self):
        gbl._party.update()

    def draw(self):
        px.cls(0)
        self.__drawMaze()
        gbl._party.draw()


    def __draw_grid(self):
        # 迷路の枠線
        px.rectb(DRAW_OFFSET_X - 1, DRAW_OFFSET_Y - 1, 
                    81, 81, 
                    px.COLOR_DARK_BLUE)

        # 一辺 80
        # 簡便のため「５」刻みとする
        # 40 ( 5, 15, 10, 5)
        #    (10, 25, 30, 35) ( 45, 50, 55, 70)

        # 地面部のグリッド
        if self.is_dark_area():
            px.rect(DRAW_OFFSET_X, DRAW_OFFSET_Y,
                       79, 79, 
                       px.COLOR_DARK_BLUE)
        else:
            # 下半分　横線
            # px.line( 0 + DRAW_OFFSET_X, 45 + DRAW_OFFSET_Y, 
            #         80 + DRAW_OFFSET_X, 45 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            # px.line( 0 + DRAW_OFFSET_X, 50 + DRAW_OFFSET_Y, 
            #         80 + DRAW_OFFSET_X, 50 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            px.line( 0 + DRAW_OFFSET_X, 55 + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 55 + DRAW_OFFSET_Y, 
                    px.COLOR_DARK_BLUE)
            px.line( 0 + DRAW_OFFSET_X, 70 + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 70 + DRAW_OFFSET_Y, 
                    px.COLOR_DARK_BLUE)

            # 下半分　集中線
            #  |0|1|4|3|2|
            #    |5|7|6|
            #    |8|A|9|
            #    |B|D|C|
            _depth = 1
            _depth_len = WALL_LENGTH[_depth + 1]

            _depth_vx = WALL_LEFT[7][0] # １つ奥のマス　右隣り「4」
            _depth_vy = WALL_LEFT[7][1] + _depth_len
            px.line(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y, 
                     0 + DRAW_OFFSET_X, 80 + DRAW_OFFSET_Y, 
                     px.COLOR_DARK_BLUE) # 中心 → 左下
            
            _depth_vx = WALL_LEFT[6][0]
            _depth_vy = WALL_LEFT[6][1] + _depth_len
            px.line(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 80 + DRAW_OFFSET_Y, 
                    px.COLOR_DARK_BLUE) # 中心 → 右下

        if self.is_sky():
            # 満天の星空
            self.__draw_Stars()
        else:
            # 天井部のグリッド
           #    (10, 25, 30, 35) ( 45, 50, 55, 70)
            px.line( 0 + DRAW_OFFSET_X, 10 + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 10 + DRAW_OFFSET_Y, 
                    px.COLOR_DARK_BLUE)
            px.line( 0 + DRAW_OFFSET_X, 25 + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 25 + DRAW_OFFSET_Y, 
                    px.COLOR_DARK_BLUE)
            # px.line( 0 + DRAW_OFFSET_X, 30 + DRAW_OFFSET_Y, 
            #         80 + DRAW_OFFSET_X, 30 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            # px.line( 0 + DRAW_OFFSET_X, 35 + DRAW_OFFSET_Y, 
            #         80 + DRAW_OFFSET_X, 35 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)

            _depth_vx = WALL_LEFT[7][0] # １つ奥のマス　右隣り「4」
            _depth_vy = WALL_LEFT[7][1] 
            px.line(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y, 
                     0 + DRAW_OFFSET_X, 0 + DRAW_OFFSET_Y, 
                     px.COLOR_DARK_BLUE)

            _depth_vx = WALL_LEFT[6][0]
            _depth_vy = WALL_LEFT[6][1] 
            px.line(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 0 + DRAW_OFFSET_Y, 
                    px.COLOR_DARK_BLUE)


    def is_sky(self):
        return True

    def is_dark_area(self):
        return False


    def __drawMaze(self):

        self.__draw_grid()

        for i in range(14):
            map_x = gbl._party.x + POS_X[gbl._party.direction][i]
            map_y = gbl._party.y + POS_Y[gbl._party.direction][i]
            if map_x < 0 or map_x > 5 or map_y < 0 or map_y > 5:
                tile = MAPTILE.WALL
            else:
                tile = gbl._map[map_y][map_x]
#            print(str(map_x) + ":" + str(map_y) + "=" + str(data))

            #  |0|1|4|3|2|
            #    |5|7|6|
            #    |8|A|9|
            #    |B|D|C|

            if i in [0, 1, 2, 3, 4]:
                _depth = 3
            elif i in [ 5,  6,  7]:
                _depth = 2
            elif i in [ 8,  9, 10]:
                _depth = 1
            elif i in [11, 12, 13]:
                _depth = 0

            _color = WALL_COLOR[_depth]
            if tile == MAPTILE.DOOR:
                _color = WALL_COLOR[MAPTILE.DOOR]

            self.__drawWall(i, tile, _color)

        self.__draw_Minimap()



    def __drawWall(self, num, tile,clr=None):

        if tile == MAPTILE.NONE:
            return

        # 中央を最後に処理するように順序を変更
        #  |0|1|4|3|2|
        #    |5|7|6|
        #    |8|A|9|
        #    |B|D|C|

        # 最奥５マス　→　３マス 端の２マスを除く
        #    (10, 25, 30, 35) ( 45, 50, 55, 70)
        #    (--, 15, 25, 35) ( 45, 55, 65, --)

        # 一辺が「10」のマスを５つ
        #         15--25--35--45--55---
        #         |   |   |   |   |   |
        #         ---------------------

        _depth = 3
        _x = WALL_LEFT[num][0]
        _y = WALL_LEFT[num][1]
        _w     = WALL_LENGTH[_depth]
        _h     = WALL_LENGTH[_depth]
        _color = WALL_COLOR[_depth] if not clr else clr 
        _depth_len = WALL_LENGTH[_depth + 1]
        if num == 0:
            pass
        if num == 1:
            # |\  tri
            # | | rect
            # |/  tri
            _depth_vx = WALL_TERMINAL[4][0] # １つ奥のマス　右隣り「4」
            _depth_vy = WALL_TERMINAL[1][1] 

            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _w, _h,
                        _color)

            #現マス　右上座標 から反時計回り
            _vx = _x + _w 
            _points = [
                (_vx       + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y),
                (_vx       + DRAW_OFFSET_X, _y + _h   + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y),
            ]
            Meth.draw_filled_polygon(_points, _color)

        if num == 2:
            pass
        if num == 3:
            #  /| tri
            # | | rect
            #  \| tri
            _depth_vx = WALL_TERMINAL[3][0] #１つ奥のマス　左上座標
            _depth_vy = WALL_TERMINAL[3][1] 

            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _w, _h,
                        _color)

            #現マス　左上座標 から時計回り
            _points = [
                (_x        + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y),
                (_x        + DRAW_OFFSET_X, _y + _h   + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y),
            ]
            Meth.draw_filled_polygon(_points, _color)


        if num == 4:
            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _w, _h,
                        _color)



        #２ブロック先の３マス
        #    (10, 25, 30, 35) ( 45, 50, 55, 70)
        #    (--, --, 10, 30) ( 50, --, --, --)

        # 一辺が「20」のマスを３つ
        #         10--30--50---
        #         |   |   |   |
        #         -------------

        _depth = 2
        _w     = WALL_LENGTH[_depth]
        _h     = WALL_LENGTH[_depth]
        _color = WALL_COLOR[_depth] if not clr else clr 
        _depth_len = WALL_LENGTH[_depth + 1]
        if num == 5:
            # |\  tri
            # | | rect
            # |/  tri
            _depth_vx = WALL_LEFT[4][0] # １つ奥のマス　右隣り「4」
            _depth_vy = WALL_LEFT[1][1] 

            _cut_x = 0
            _cut_w = _w + _x
            px.rect(_cut_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _cut_w, _h,
                        _color)

            #現マス　右上座標 から反時計回り
            _vx = _x + _w 
            _points = [
                (_vx       + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y),
                (_vx       + DRAW_OFFSET_X, _y + _h   + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y),
            ]
            Meth.draw_filled_polygon(_points, _color)

        if num == 6:
            #  /| tri
            # | | rect
            #  \| tri
            _depth_vx = WALL_LEFT[3][0] #１つ奥のマス　左上座標
            _depth_vy = WALL_LEFT[3][1] 

            # 見切れる部分を除く
            _cut_w = 80 - _x
            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _cut_w, _h,
                        _color)

            #現マス　左上座標 から時計回り
            _points = [
                (_x        + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y),
                (_x        + DRAW_OFFSET_X, _y + _h   + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y),
            ]
            Meth.draw_filled_polygon(_points, _color)

        if num == 7:
            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _w, _h,
                        _color)



        #１ブロック先の３マス
        #    (10, 25, 30, 35) ( 45, 50, 55, 70)
        #    (--, --, -5, 25) ( 55, --, --, --)

        # 一辺が「30」のマスを３つ
        #        -05--25--55---
        #         |   |   |   |
        #         -------------

        _depth = 1
        _w     = WALL_LENGTH[_depth]
        _h     = WALL_LENGTH[_depth]
        _color = WALL_COLOR[_depth] if not clr else clr 
        _depth_len = WALL_LENGTH[_depth + 1]
        if num == 8:
            # |\  tri
            # | | rect
            # |/  tri
            _depth_vx = WALL_LEFT[7][0] # １つ奥のマス　右隣り「7」
            _depth_vy = WALL_LEFT[5][1] 

            # 見切れる部分を除く
            _cut_x = 0
            _cut_w = _w + _x
            px.rect(_cut_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _cut_w, _h,
                        _color)
            
            #現マス　右上座標 から反時計回り
            _vx = _x + _w 
            _points = [
                (_vx       + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y),
                (_vx       + DRAW_OFFSET_X, _y + _h   + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y),
            ]
            Meth.draw_filled_polygon(_points, _color)

        if num == 9:
            #  /| tri
            # | | rect
            #  \| tri
            _depth_vx = WALL_LEFT[6][0] #１つ奥のマス　左上座標
            _depth_vy = WALL_LEFT[6][1] 

            # 見切れる部分を除く
            _cut_w = 80 - _x
            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _cut_w, _h,
                        _color)

            #現マス　左上座標 から時計回り
            _points = [
                (_x        + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y),
                (_x        + DRAW_OFFSET_X, _y + _h   + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y),
            ]
            Meth.draw_filled_polygon(_points, _color)

        if num == 10:
            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _w, _h,
                        _color)

            # 扉の縁取り
            if tile == MAPTILE.DOOR:
                _frame = 10
                px.line(_x + _frame + DRAW_OFFSET_X, _y + _frame + DRAW_OFFSET_Y,
                        _x + _frame + DRAW_OFFSET_X, _y + _h     + DRAW_OFFSET_Y,
                        px.COLOR_BLACK)
                px.line(_x + _frame      + DRAW_OFFSET_X, _y + _frame + DRAW_OFFSET_Y,
                        _x + _w - _frame + DRAW_OFFSET_X, _y + _frame + DRAW_OFFSET_Y,
                        px.COLOR_BLACK)
                px.line(_x + _w - _frame + DRAW_OFFSET_X, _y + _frame + DRAW_OFFSET_Y,
                        _x + _w - _frame + DRAW_OFFSET_X, _y + _h     + DRAW_OFFSET_Y,
                        px.COLOR_BLACK)


        # 最前３マス
        #    (10, 25, 30, 35) ( 45, 50, 55, 70)
        #    (--, --,-50, 10) ( 70, --, --, --)

        # 一辺が「60」のマスを３つ
        #        -50--10--70---
        #         |   |   |   |
        #         -------------

        _depth = 0
        _w     = WALL_LENGTH[_depth]
        _h     = WALL_LENGTH[_depth]
        _color = WALL_COLOR[_depth] if not clr else clr 
        _depth_len = WALL_LENGTH[_depth + 1]
        if num == 11:
            # |\  tri
            # | | rect
            # |/  tri
            _depth_vx = WALL_LEFT[10][0] # １つ奥のマス　右隣り「A」
            _depth_vy = WALL_LEFT[8][1] 

            # px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
            #             _w, _h,
            #             _color)

            #現マス　右上座標 から反時計回り
            _vx = _x + _w 
            _points = [
                (_vx       + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y),
                (_vx       + DRAW_OFFSET_X, _y + _h   + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y),
            ]
            Meth.draw_filled_polygon(_points, _color)

        if num == 12:
            #  /| tri
            # | | rect
            #  \| tri
            _depth_vx = WALL_LEFT[9][0] #１つ奥のマス　左上座標
            _depth_vy = WALL_LEFT[9][1] 

            # px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
            #             _w, _h,
            #             _color)

            #現マス　左上座標 から時計回り
            _points = [
                (_x        + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y),
                (_x        + DRAW_OFFSET_X, _y + _h   + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y),
                (_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y),
            ]
            Meth.draw_filled_polygon(_points, _color)

        if num == 13:
            # 自身の立ち位置への描画は意味がない
            # px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
            #             _w, _h,
            #             _color)
            pass



    def __draw_Stars(self):
        for star in stars[gbl._party.direction]:
            star.draw()

    def __draw_Minimap(self):
        scale = 4
        offset_x = 2
        offset_y = 2
        for my, row in enumerate(gbl._map):
            for mx, wall in enumerate(row):
                color = px.COLOR_WHITE if gbl._map[my][mx] == 1 else px.COLOR_BLACK
                px.rect(mx * scale + offset_x, my * scale + offset_y, scale, scale, color)

        # Player position
        pl_x = gbl._party.x * scale + offset_x + (scale // 2)
        pl_y = gbl._party.y * scale + offset_y + (scale // 2)
        px.circ(pl_x, pl_y, 1, 8)




if __name__ == "__main__":
    App()





