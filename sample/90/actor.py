import pyxel
from enum import Enum, auto
from basestate import *



class Actor():
    def __init__(self):
        self.context = ActorStateContext(self, STATE.Idle)

    def update(self):
        self.context.update()

    def Idle(self):
        self.context.changeState(STATE.Idle)

    def Walk(self):
        self.context.changeState(STATE.Walk)

    def Attack(self):
        self.context.changeState(STATE.Attack)




class STATE(Enum):
    Idle = auto()
    Walk = auto()
    Attack = auto()





class ActorState_Idle(BaseState):

    def __init__(self, actor):
        self.state = STATE.Idle
        self.actor = actor

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.actor.Walk

    def draw(self):
        pass

class ActorState_Walk(BaseState):

    def __init__(self, actor):
        self.state = STATE.Walk
        self.actor = actor

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.actor.Attack

    def draw(self):
        pass

class ActorState_Attack(BaseState):

    def __init__(self, actor):
        self.state = STATE.Attack
        self.actor = actor

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.actor.Idle

    def draw(self):
        pass


class ActorStateContext():

    def __init__(self, actor, initState):
        self.state = initState
        self.actor = actor
        self.table = {
            STATE.Idle: ActorState_Idle(actor),
            STATE.Walk: ActorState_Walk(actor),
            STATE.Attack: ActorState_Attack(actor),
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


