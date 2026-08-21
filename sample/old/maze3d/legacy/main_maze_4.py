
import pyxel as px

from context import * 
from actor import *





class App:

    def __init__(self):

        px.init(192, 128)
        # px.init(256, 192, fps=5)

        # リソースをロード
        # px.load("./assets/onyxofblack.pyxres", True, False, False, False)

        # 変数定義
        # 自分の最初の座標と方向
        self.x = 1
        self.y = 1
        self.direction = DIRECTION_SOUTH

        # マップ
        # 0 = 通路
        # 1 = 壁
        # 外周は必ず壁とする
        self.map = [
            [ 1, 1, 1, 1, 1, 1],
            [ 1, 0, 0, 0, 1, 1],
            [ 1, 0, 1, 0, 1, 1],
            [ 1, 0, 1, 0, 0, 1],
            [ 1, 0, 1, 1, 0, 1],
            [ 1, 0, 0, 0, 0, 1],
            [ 1, 1, 1, 1, 1, 1]
        ]

        # pyxel実行
        px.run(self.update, self.draw)


    def update(self):
        self.__update_move()

    #
    # キー入力で方向・座標変更
    #
    def __update_move(self):
        # 上：前進する
        if px.btnp(px.KEY_UP):
            # 前が壁であるかチェック
            if self.map[self.y + VY[self.direction]][self.x + VX[self.direction]] == 0:
                self.x = self.x + VX[self.direction]
                self.y = self.y + VY[self.direction]

        # 右：右回転する
        if px.btnp(px.KEY_RIGHT):
            self.direction = self.direction + 1
            if self.direction > DIRECTION_WEST:
                self.direction = DIRECTION_NORTH
        
        # 左：左回転する
        if px.btnp(px.KEY_LEFT):
            self.direction = self.direction - 1
            if self.direction < DIRECTION_NORTH:
                self.direction = DIRECTION_WEST

        
    def draw(self):
        px.cls(0)

        # 迷路の枠線
        px.rectb(DRAW_OFFSET_X - 1, DRAW_OFFSET_Y -
                    1, 81, 81, px.COLOR_DARK_BLUE)

        # 一辺 80
        # 簡便のため「５」刻みとする
        # 40 ( 5, 15, 10, 5)
        #    (10, 25, 30, 35) ( 45, 50, 55, 70)

        # 地面部のグリッド
        if self.is_sky():
            px.rect(DRAW_OFFSET_X, DRAW_OFFSET_Y,
                       79, 79, px.COLOR_DARK_BLUE)
            # 満天の星空
            self.draw_stars()
        else:
            # 下半分　横線
            _screen_len_full = 80
            # px.line( 0 + DRAW_OFFSET_X, 45 + DRAW_OFFSET_Y, 
            #         80 + DRAW_OFFSET_X, 45 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            # px.line( 0 + DRAW_OFFSET_X, 50 + DRAW_OFFSET_Y, 
            #         80 + DRAW_OFFSET_X, 50 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            px.line( 0 + DRAW_OFFSET_X, 55 + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 55 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            px.line( 0 + DRAW_OFFSET_X, 70 + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 70 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)

            # 下半分　集中線
            #  |0|1|4|3|2|
            #    |5|7|6|
            #    |8|A|9|
            #    |B|D|C|
            _depth = 3
            _depth_len = WALL_LENGTH[_depth + 1]

            _depth_vx = WALL_LEFT[4][0] # １つ奥のマス　右隣り「4」
            _depth_vy = WALL_LEFT[4][1] + _depth_len
            px.line(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y, 
                     0 + DRAW_OFFSET_X, 80 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE) # 中心 → 左下
            
            _depth_vx = WALL_LEFT[3][0]
            _depth_vy = WALL_LEFT[3][1] + _depth_len
            px.line(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 80 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE) # 中心 → 右下

        if self.is_outer():
            # 満天の星空
            self.draw_stars()
        else:
            # 天井部のグリッド
           #    (10, 25, 30, 35) ( 45, 50, 55, 70)
            px.line( 0 + DRAW_OFFSET_X, 10 + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 10 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            px.line( 0 + DRAW_OFFSET_X, 25 + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 25 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            # px.line( 0 + DRAW_OFFSET_X, 30 + DRAW_OFFSET_Y, 
            #         80 + DRAW_OFFSET_X, 30 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)
            # px.line( 0 + DRAW_OFFSET_X, 35 + DRAW_OFFSET_Y, 
            #         80 + DRAW_OFFSET_X, 35 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)

            _depth_vx = WALL_LEFT[4][0] # １つ奥のマス　右隣り「4」
            _depth_vy = WALL_LEFT[4][1] 
            px.line(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y, 
                     0 + DRAW_OFFSET_X, 0 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)

            _depth_vx = WALL_LEFT[3][0]
            _depth_vy = WALL_LEFT[3][1] 
            px.line(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y, 
                    80 + DRAW_OFFSET_X, 0 + DRAW_OFFSET_Y, px.COLOR_DARK_BLUE)



        for i in range(14):
            map_x = self.x + POS_X[self.direction][i]
            map_y = self.y + POS_Y[self.direction][i]
            if map_x < 0 or map_x > 5 or map_y < 0 or map_y > 5:
                data = 1
            else:
                data = self.map[map_y][map_x]
#            print(str(map_x) + ":" + str(map_y) + "=" + str(data))

            if data == 1:
                self.__drawMaze(i)

        # test
        # self.__drawPlayer(0,  1, 0, 0, 0, 0)
        # self.__drawPlayer(1, 34, 0, 0, 0, 0)
        # self.__drawPlayer(2, 88, 0, 0, 0, 0)
        # self.__drawPlayer(3,100, 0, 0, 0, 0)
        self.draw_minimap()

    def is_sky(self):
        return False
    def is_outer(self):
        return True


    def __drawMaze(self, num):

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
        _color = WALL_COLOR[_depth]
        _depth_len = WALL_LENGTH[_depth + 1]
        if num == 0:
            pass
        if num == 1:
            _depth_vx = WALL_TERMINAL[4][0] # １つ奥のマス　右隣り「4」
            _depth_vy = WALL_TERMINAL[1][1] 

            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _w, _h,
                        _color)

            # 側壁の中四角
            _vx = _x + _w #現マス　右上座標
            px.rect(_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                       _depth_vx - _vx, _depth_len,
                        _color)
            # 側壁の上三角
            px.tri(_x + _w   + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y,
                   _x + _w   + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                        _color)
            # 側壁の下三角
            px.tri(_x + _w   + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                   _x + _w   + DRAW_OFFSET_X, _y + _w                + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                        _color)

        if num == 2:
            pass
        if num == 3:
            _depth_vx = WALL_TERMINAL[3][0] #１つ奥のマス　左上座標
            _depth_vy = WALL_TERMINAL[3][1] 

            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _w, _h,
                        _color)

            # 側壁の中四角
            px.rect(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                         _x - _depth_vx, _depth_len,
                        _color)
            # 側壁の上三角 
            px.tri(_x        + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y,
                   _x        + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                        _color)
            # 側壁の下三角
            px.tri(_x        + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                   _x        + DRAW_OFFSET_X, _y + _h                + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                        _color)

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

        #  |0|1|4|3|2|
        #    |5|7|6|
        #    |8|A|9|
        #    |B|D|C|

        _depth = 2
        _w     = WALL_LENGTH[_depth]
        _h     = WALL_LENGTH[_depth]
        _color = WALL_COLOR[_depth]
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

            # 側壁の中四角
            _vx = _x + _w #現マス　右上座標
            px.rect(_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                       _depth_vx - _vx, _depth_len,
                        _color)
            # 側壁の上三角
            px.tri(_x + _w   + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y,
                   _x + _w   + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                        _color)
            # 側壁の下三角
            px.tri(_x + _w   + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                   _x + _w   + DRAW_OFFSET_X, _y + _w                + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                        _color)

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

            # 側壁の中四角
            px.rect(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                         _x - _depth_vx, _depth_len,
                        _color)
            # 側壁の上三角 
            px.tri(_x        + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y,
                   _x        + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                        _color)
            # 側壁の下三角
            px.tri(_x        + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                   _x        + DRAW_OFFSET_X, _y + _h                + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                        _color)

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

        #  |0|1|4|3|2|
        #    |5|7|6|
        #    |8|A|9|
        #    |B|D|C|

        _depth = 1
        _w     = WALL_LENGTH[_depth]
        _h     = WALL_LENGTH[_depth]
        _color = WALL_COLOR[_depth]
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
            
            # 側壁の中四角
            _vx = _x + _w #現マス　右上座標
            px.rect(_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                       _depth_vx - _vx, _depth_len,
                        _color)
            # 側壁の上三角
            px.tri(_x + _w   + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y,
                   _x + _w   + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                        _color)
            # 側壁の下三角
            px.tri(_x + _w   + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                   _x + _w   + DRAW_OFFSET_X, _y + _w                + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                        _color)

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

            # 側壁の中四角
            px.rect(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                         _x - _depth_vx, _depth_len,
                        _color)
            # 側壁の上三角 
            px.tri(_x        + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y,
                   _x        + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                        _color)
            # 側壁の下三角
            px.tri(_x        + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                   _x        + DRAW_OFFSET_X, _y + _h                + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                        _color)

        if num == 10:
            px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
                        _w, _h,
                        _color)

        # 最前３マス
        #    (10, 25, 30, 35) ( 45, 50, 55, 70)
        #    (--, --,-50, 10) ( 70, --, --, --)

        # 一辺が「60」のマスを３つ
        #        -50--10--70---
        #         |   |   |   |
        #         -------------

        #  |0|1|4|3|2|
        #    |5|7|6|
        #    |8|A|9|
        #    |B|D|C|

        _depth = 0
        _w     = WALL_LENGTH[_depth]
        _h     = WALL_LENGTH[_depth]
        _color = WALL_COLOR[_depth]
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

            _vx = _x + _w #現マス　右上座標
            px.rect(_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                       _depth_vx - _vx, _depth_len,
                        _color)
            # 側壁の上三角
            px.tri(_x + _w   + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y,
                   _x + _w   + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                        _color)
            # 側壁の下三角
            px.tri(_x + _w   + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                   _x + _w   + DRAW_OFFSET_X, _y + _w                + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                        _color)


        if num == 12:
            #  /| tri
            # | | rect
            #  \| tri
            _depth_vx = WALL_LEFT[9][0] #１つ奥のマス　左上座標
            _depth_vy = WALL_LEFT[9][1] 

            # px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
            #             _w, _h,
            #             _color)

            margin = 1 # 何故か足りないので
            # 側壁の中四角
            px.rect(_depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                         _x - _depth_vx + margin, _depth_len,
                        _color)
            # 側壁の上三角 
            px.tri(_x        + DRAW_OFFSET_X, _y        + DRAW_OFFSET_Y,
                   _x        + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + DRAW_OFFSET_Y,
                        _color)
            # 側壁の下三角
            px.tri(_x        + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                   _x        + DRAW_OFFSET_X, _y + _h                + DRAW_OFFSET_Y,
                   _depth_vx + DRAW_OFFSET_X, _depth_vy + _depth_len + DRAW_OFFSET_Y,
                        _color)


        if num == 13:
            # 自身の立ち位置への描画は意味がない
            # px.rect(_x + DRAW_OFFSET_X, _y + DRAW_OFFSET_Y,
            #             _w, _h,
            #             _color)
            pass





    def __drawPlayer(self, number, head, helm, body, weapon, shield):

        px.blt( 12, (number * 20) +  2, 1,  (head % 32) * 8,  int(head / 32) * 8,  8,  8, 0) # 頭
        px.blt( 12, (number * 20) + 10, 1,  32, 32,  8, 16, 0) # 体
        px.blt(  4, (number * 20) +  2, 1,   0, 48,  8, 16, 0) # 武器
        px.rect( 24, (number * 20) + 12, 16, 3,  5)
        px.rect( 24, (number * 20) + 15, 30, 1,  6)


    def draw_stars(self):
        for star in stars[self.direction]:
            star.draw()


    def draw_minimap(self):
        scale = 4
        offset_x = 2
        offset_y = 2
        for my, row in enumerate(self.map):
            for mx, wall in enumerate(row):
                color = 7 if self.map[my][mx] == 1 else 0
                px.rect(mx * scale + offset_x, my * scale + offset_y, scale, scale, color)

        # Player position
        pl_x = self.x * scale + offset_x + (scale // 2)
        pl_y = self.y * scale + offset_y + (scale // 2)
        px.circ(pl_x, pl_y, 1, 8)


if __name__ == "__main__":
    App()
