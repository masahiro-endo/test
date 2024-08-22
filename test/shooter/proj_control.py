
from pgzero.builtins import *
import math
from enum import Enum, auto
import global_value as g
from typing import Any, Dict



class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Ctl:
    ##### 関数
    # 指定した角度に移動
    # 引数を極座標系定義で受け取り、直行座標系へ変換する
    @staticmethod
    def axis_polar_to_rect(angle):
        rad = math.radians(angle)
        return math.cos(rad), math.sin(rad)

    @staticmethod
    def spritemove(pos, angle, speed, direction: Enum):
        x, y = Ctl.axis_polar_to_rect(angle)
        x = speed  * x
        y = speed  * y
        px, py = pos

        if direction==Direction.RIGHT:
            px += x
            py += y
        if direction==Direction.LEFT:
            px -= x
            py -= y

        return px, py

    @staticmethod
    def spritemove_right(pos, angle, speed):
        return Ctl.spritemove(pos, angle, speed,Direction.RIGHT)

    @staticmethod
    def spritemove_left(pos, angle, speed):
        return Ctl.spritemove(pos, angle, speed,Direction.LEFT)





