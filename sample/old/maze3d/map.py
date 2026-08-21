
from enum import Enum, IntEnum, auto




class MAPTILE(IntEnum):
    NONE = 0
    WALL = 1
    DEPTH2 =2
    DEPTH3 =3
    DOOR = 4




class dungeonB1:

    _map = [
        [ 1, 1, 1, 1, 1, 1],
        [ 1, 0, 0, 0, 1, 1],
        [ 1, 0, 1, 0, 1, 1],
        [ 1, 0, 1, 0, 0, 1],
        [ 1, 0, 1, 1, 0, 1],
        [ 1, 4, 0, 0, 0, 1],
        [ 1, 1, 1, 1, 1, 1]
    ]


