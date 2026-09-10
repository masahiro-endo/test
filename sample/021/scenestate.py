
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


class SceneState_Extend(BaseState):
    PLAYABLE = 120
    def __init__(self, texts):
        self.texts = texts
        self.tick = 0

    def update(self):
        self.tick += 1
        if self.tick > SceneState_Extend.PLAYABLE:
            gbl.stack.popleft()

    def draw(self):
        self.draw_pause()

    def draw_pause(self):
        for row, text in enumerate(self.texts):
            x, y = (self.center_text_x(text), self.center_text_y() + (row * 6))
            self.draw_rect(x, y, len(text), 2) #背景矩形
            px.text(x, y, text, px.COLOR_WHITE)

    def center_text_x(text):
        text_width = len(text) * 4  # 1文字4px
        return (WIDTH - text_width) // 2

    def center_text_y():
        text_height = 6  # 1文字6px
        return (HEIGHT - text_height) // 2

    def draw_rect(self, x, y, w, h, clr=px.COLOR_ORANGE):
        # 描画座標は x8
        px.rect(x * 8 - 4 , y * 8 + 4 , w * 8 , h * 8 ,clr)





class SceneState_Stage1(BaseState):
    def __init__(self, parent):
        self.state = STATE.STAGE1
        self.parent = parent.parent
        self.scene = parent
        self.enemylist = stage1.EnemyList
        self.tick = 0
        # gbl.stars =  [Star() for _ in range(20)] 

    def enter(self):
        gbl.stack.appendleft(SceneState_Extend([f"stage 1"]))


    def update(self):
        if px.frame_count % 30 == 0: 
            self.tick += 1

        # if random.randrange(600)==0: # デブリ出現
        #     gbl.obstacles.append(Debris())

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

        gbl.player.update()

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

