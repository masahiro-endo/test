
import pyxel as px
from enum import Enum, auto

from constant import *
import appconfig as gbl
from basestate import *
from actor import *
from method import *
from map.stage_1 import *





class STATE(Enum):
    TITLE = auto()
    STAGE1 = auto()
    GAMEOVER = auto()






class SceneStates(BaseContext):
    def __init__(self, parent):
        self.parent = parent
        self.table = {
            STATE.TITLE  : SceneState_Title(self),
            STATE.STAGE1 : SceneState_Stage1(self),
            STATE.GAMEOVER  : SceneState_GameOver(self),
        }
        self.changeState(STATE.TITLE)

    def update(self):
        self.currentState.update()
    def draw(self):
        self.currentState.draw()

    def Title(self):
        self.changeState(STATE.TITLE)
    def Stage1(self):
        self.changeState(STATE.STAGE1)
    def GameOver(self):
        self.changeState(STATE.GAMEOVER)









class SceneState_Title(BaseState):
    def __init__(self, parent):
        self.state = STATE.TITLE
        self.parent = parent.parent
        self.scene = parent

    def update(self):
        pass
    def draw(self):
        pass



class SceneState_Stage1(BaseState):
    def __init__(self, parent):
        self.state = STATE.STAGE1
        self.parent = parent.parent
        self.scene = parent
        self.enemylist = stage1.EnemyList
        self.tick = 0

    def update(self):
        if px.frame_count % 30 == 0: 
            self.tick += 1

        for i, e in enumerate(self.enemylist):
            bgn, end, interval, cls, data, tick = e
            if px.frame_count < bgn:
                pass
            if (bgn < px.frame_count and px.frame_count < end):
                if tick % interval == 0:
                    cls.spawn(*data)
                self.enemylist[i][-1] += 1
            elif px.frame_count > end:
                self.enemylist.pop(i)

        Meth.detect_collision()

    def draw(self):
        # 背景
        # px.circ(40, 50, 20 + self.tick, px.COLOR_BROWN)
        pass


class SceneState_GameOver(BaseState):
    def __init__(self, parent):
        self.state = STATE.GAMEOVER
        self.parent = parent.parent
        self.scene = parent

    def update(self):
        pass
    def draw(self):
        pass

