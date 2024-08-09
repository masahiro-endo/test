
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


##### 関数
# 指定した角度に移動
# 引数を極座標系定義で受け取り、直行座標系へ変換する
def axis_polar_to_rect(angle):
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)

def spritemove(pos, angle, speed, direction: Enum):
    x, y = axis_polar_to_rect(angle)
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

def spritemove_right(pos, angle, speed):
    return spritemove(pos, angle, speed,Direction.RIGHT)

def spritemove_left(pos, angle, speed):
    return spritemove(pos, angle, speed,Direction.LEFT)




def player_isDead()->bool:
    res = False
    if not (g.player in g.objects):
        res = True
    return res

def player_isRemain()->bool:
    res = False
    if g.playerRemain > 0:
        res = True
    return res



def trans_gameOver():
    g.game_state = SCENE.GAMEOVER
    g.out_time = time.time() - g.start # ゲームオーバーまでの時間を計算

    g.sceneStack.popleft()
    g.sceneStack.appendleft(GameOverScene())

