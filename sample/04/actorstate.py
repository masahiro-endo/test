import pyxel
from enum import Enum, auto
from basestate import *
from UI import *
import appconfig as gbl





class ActorStates():
    def __init__(self):
        self.context = ActorStateContext(self, STATE.Idle)

    def update(self):
        self.context.update()

    def draw(self):
        self.context.draw()

    def Idle(self):
        self.context.changeState(STATE.Idle)

    def Move(self):
        self.context.changeState(STATE.Move)

    def Battle(self):
        self.context.changeState(STATE.Battle)



class STATE(Enum):
    Idle = auto()
    Move = auto()
    Battle = auto()





class ActorStateContext():
    
    def __init__(self, parent, initState):
        self.parent = parent
        self.table = {
            STATE.Idle: ActorState_Idle(self),
            STATE.Move: ActorState_Move(self),
            STATE.Battle: ActorState_Battle(self),
        }
        self.currentState = None
        self.changeState(initState)

    def update(self):
        self.currentState.update()

    def draw(self):
        self.currentState.draw()

    def changeState(self, nextState):
        tbl = self.table[nextState]
        if (self.currentState != None): 
            self.currentState.exit()

        self.currentState = tbl
        self.currentState.enter()



class ActorState_Idle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Idle
        self.actor = parent.parent

    def update(self):
        btn = get_btn_state()
        pt = gbl.get_party()

        pt.dy = btn["d"] - btn["u"]
        pt.dx = btn["r"] - btn["l"] if not pt.dy else 0
        if pt.dy or pt.dx:
            mp = gbl.get_map()
            mp.move_start()
            self.actor.Move()

        elif btn["a"]:
            Window.close()
        elif btn["b"]:  # メニュー呼び出し
            pt.menu_show()
            pt.scene = "menu"


class ActorState_Move(BaseState):
    def __init__(self, parent):
        self.state = STATE.Move
        self.actor = parent.parent

    def update(self):
        pt = gbl.get_party()

        pt.dy += pt.spd * ((pt.dy > 0) - (pt.dy < 0))
        pt.dx += pt.spd * ((pt.dx > 0) - (pt.dx < 0))
        # 移動終了
        if (pt.dy % 16, pt.dx % 16) == (0, 0):
            self.actor.Idle()
            mp = gbl.get_map()
            mp.move_end()


    def draw(self):
        pass


class ActorState_Battle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Battle
        self.actor = parent.parent

    def update(self):
        pass

    def draw(self):
        pass






