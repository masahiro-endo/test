import pyxel
import random
from enum import Enum, auto
from basestate import *

# 3-2. Stateパターンを構成する3つの役者
# Stateパターンは、主に次の3つで構成されます。

# State（状態）：振る舞いを定義する
# Context：現在の状態を保持・切り替える
# User（利用者）：Contextを使う側（Playerなど）
# ここで重要なのは、 「状態を切り替える責務」をState自身に持たせないことです。

# 状態遷移の判断はContextが行い、 Stateは自分の振る舞いだけに集中します。


dice_dict = [
    (8*0, 128),
    (8*1, 128),
    (8*2, 128),
    (8*3, 128),
    (8*4, 128),
    (8*5, 128)
]


class Actor():
    def __init__(self):
        self.context = ActorStateContext(self, STATE.Idle)

    def init_pos(self, x=0, y=0, ut=0, er=0):
        self.x = x
        self.y = y
        self.vx = -1.0 + random.random() * 2
        self.vy = -4.0 * random.random() - 2.0
        self.frames_until_throw = ut
        self.frames_end_roll = er

        self.number_eyes = random.randint(1, 6)
    
    def bounce(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.35
        if not (0 < self.x < pyxel.width - 8):
            self.vx = -self.vx
        if self.y > pyxel.height - 16:
            self.y = pyxel.height - 16
            if self.vy < 2:
                self.x = self.init_x
                self.y = self.init_y
            else:
                self.vy = -self.vy * 0.5                
        
    def update(self):
        self.context.update()

    def draw(self):
        self.context.draw()
        pyxel.blt(self.x, self.y, 0,
                  dice_dict[self.number_eyes-1][0],
                  dice_dict[self.number_eyes-1][1],
                  8, 8)

    def Idle(self):
        self.context.changeState(STATE.Idle)

    def Roll(self):
        self.context.changeState(STATE.Roll)

    def Release(self):
        self.context.changeState(STATE.Release)




class STATE(Enum):
    Idle = auto()
    Roll = auto()
    Release = auto()





class ActorState_Idle(BaseState):

    def __init__(self, actor):
        self.state = STATE.Idle
        self.actor = actor

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.actor.Roll

    def draw(self):
        pass

class ActorState_Roll(BaseState):

    def __init__(self, actor):
        self.state = STATE.Roll
        self.actor = actor
        self.tick = 0

    def enter(self):
        pass

    def update(self):
        self.tick += 1
        if self.tick % 3 == 0:
            self.actor.number_eyes = random.randint(1, 6)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.actor.Release
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.actor.Idle

    def draw(self):
        pass

class ActorState_Release(BaseState):

    def __init__(self, actor):
        self.state = STATE.Release
        self.actor = actor
        self.tick = 0

    def enter(self):
        pass

    def update(self):
        self.tick += 1
        self.actor.bounce()

        if self.tick % 3 == 0:
            self.actor.number_eyes = random.randint(1, 6)

    def draw(self):
        pass



class ActorStateContext():

    def __init__(self, actor, initState):
        self.state = initState
        self.actor = actor
        self.table = {
            STATE.Idle: ActorState_Idle(actor),
            STATE.Roll: ActorState_Roll(actor),
            STATE.Release: ActorState_Release(actor),
        }
        self.currentState = None
        self.changeState(STATE.Idle)

    def update(self):
        self.currentState.update()

    def draw(self):
        self.currentState.draw()

    def changeState(self, nextState):
        next = self.table[nextState]
        if (self.currentState != None): 
            self.currentState.exit()

        self.currentState = next
        self.currentState.enter()





class Game:
    class Setting:
        class DisplayResolution():
            CUSTOM = (160, 120)
            VGA = (640, 480)
            SVGA = (800, 600)
            XGA = (1024, 768)
        
        class ActorPosition():
            Default = (80, 50)





class GameMaster():

    def __init__(self):
        pass

    def grab_dice(self, cnt):
        self.dice = [Actor() for i in range(cnt)]
        x, y = Game.Setting.ActorPosition.Default

        i = 0
        for die in self.dice:
            frm_ut = random.randint(5, 20)
            frm_er = 30 + i*12
            die.init_pos(x + i*9, y, frm_ut, frm_er)
            i += 1
        
    def update(self):
        for die in self.dice:
            die.update()
                
    def draw(self):
        for die in self.dice:
            die.draw()



