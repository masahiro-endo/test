
from enum import Enum, IntEnum, auto




class BTN(IntEnum):
    NONE= 0
    UP  = auto()
    DWN = auto()
    LFT = auto()
    RHT = auto()
    A_Z = auto()
    B_X = auto()
    SEL = auto()





class EFCT(Enum):
    ATK = 'atk'
    DMG = 'dmg'
    BUF = 'buf'
    EXP = 'exp'
    LOAD = 'load'
    DONE = 'done'




