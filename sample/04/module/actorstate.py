import pyxel
from enum import Enum, auto
from module.basestate import *
from UI import *
import appconfig as gbl





class ActorStates(BaseContext):
    def __init__(self, parent):
        self.parent = parent
        self.table = {
            STATE.Idle: ActorState_Idle(self),
            STATE.Move: ActorState_Move(self),
            STATE.Battle: ActorState_Battle(self),
        }
        self.currentState = None
        self.changeState(STATE.Idle)

    def update(self):
        self.currentState.update()

    def draw(self):
        self.currentState.update()

    def Idle(self):
        self.changeState(STATE.Idle)

    def Move(self):
        self.changeState(STATE.Move)

    def Battle(self):
        self.changeState(STATE.Battle)



class STATE(Enum):
    Idle = auto()
    Move = auto()
    Battle = auto()






class ActorState_Idle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Idle
        self.actor = parent.parent
        self.action = parent
    
    def update(self):
        btn = get_btn_state()
        pt = self.actor

        pt.dy = btn["d"] - btn["u"]
        pt.dx = btn["r"] - btn["l"] if not pt.dy else 0
        if pt.dy or pt.dx:
            self.action.Move()
            self.actor.move_start()
        elif btn["a"]:
            Window.close()
        elif btn["b"]:  # メニュー呼び出し
            gbl.get_screen().context.currentState.map.Menu()
            # pt.menu_show()
            # pt.scene = "menu"



class ActorState_Move(BaseState):
    def __init__(self, parent):
        self.state = STATE.Move
        self.actor = parent.parent
        self.action = parent

    def update(self):
        pt = self.actor

        pt.dy += pt.spd * ((pt.dy > 0) - (pt.dy < 0))
        pt.dx += pt.spd * ((pt.dx > 0) - (pt.dx < 0))
        # 移動終了
        if (pt.dy % 16, pt.dx % 16) == (0, 0):
            self.action.Idle()
            self.actor.move_end()


    def draw(self):
        pass


class ActorState_Battle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Battle
        self.actor = parent.parent
        self.statecommand = parent

    def update(self):
        pass

    def draw(self):
        pass






