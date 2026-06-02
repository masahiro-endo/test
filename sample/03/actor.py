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

    def init_pos(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.number_eyes = random.randint(1, 6)

    def update(self):
        self.context.update()

    def Idle(self):
        self.context.changeState(STATE.Idle)

    def Roll(self):
        self.context.changeState(STATE.Roll)





class STATE(Enum):
    Idle = auto()
    Roll = auto()
    Release = auto()





class ActorState_Idle(BaseState):

    def __init__(self, actor):
        self.state = STATE.Idle
        self.actor = actor

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.actor.Roll

    def draw(self):
        pass

class ActorState_Roll(BaseState):

    def __init__(self, actor):
        self.state = STATE.Roll
        self.actor = actor

    def enter(self):
        pass

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.actor.Release
        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
            self.actor.Idle

    def draw(self):
        pass

class ActorState_Release(BaseState):

    def __init__(self, actor):
        self.state = STATE.Release
        self.actor = actor

    def enter(self):
        pass

    def update(self):
        pass

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

    def changeState(self, nextState):
        next = self.table[nextState]
        if (self.currentState != None): 
            self.currentState.exit()

        self.currentState = next
        self.currentState.enter()





class Die:
    def __init__(self):
        self.init()
    
    def init(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.face_value = 1
        self.active = False
        self.is_roll = False 
        self.fcnt = 0
        self.frames_until_throw = 0
        self.frames_end_roll = 0
        self.roll_behavior = "standard"		# "standard", "bouncy"
    
    def get_value(self):
        return self.face_value
    
    def prepare_to_roll(self, x, y, frames_until_throw, frames_end_roll, roll_behavior="standard"):
        self.active = True
        self.face_value = random.randint(1, 6)
        self.x = x
        self.y = y
        self.init_x = x
        self.init_y = y
        self.vx = -1.0 + random.random() * 2
        self.vy = -4.0 * random.random() - 2.0
        self.frames_until_throw = frames_until_throw
        self.frames_end_roll = frames_end_roll
        self.roll_behavior = roll_behavior
        
    def update(self):
        self.fcnt += 1
        if self.fcnt > self.frames_until_throw:
            if self.is_roll:
                if self.roll_behavior == "standard": self.roll_standard()
                elif self.roll_behavior == "bouncy": self.roll_bouncy()
        elif self.fcnt == self.frames_until_throw:
            self.is_roll = True
        else:
            return

    def roll_standard(self):
        if self.fcnt % 3 == 0:
            self.face_value = pyxel.rndi(1, 6)
        if self.fcnt >= self.frames_end_roll:
            self.is_roll = False       

    def roll_bouncy(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.35
        if not (0 < self.x < pyxel.width - 8):
            self.vx = -self.vx
        if self.y > pyxel.height - 16:
            self.y = pyxel.height - 16
            if self.vy < 2:
                self.is_roll = False
                self.x = self.init_x
                self.y = self.init_y
            else:
                self.vy = -self.vy * 0.5                
        
        if self.fcnt % 3 == 0:
            self.face_value = pyxel.rndi(1, 6)
        

    def draw(self):
        pyxel.blt(self.x, self.y, 0,
                  dice_dict[self.face_value-1][0],
                  dice_dict[self.face_value-1][1],
                  8, 8)







