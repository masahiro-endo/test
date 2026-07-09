from enum import Enum, auto
import appconfig as gbl
from module.UI import *
from module.state.basestate import *
from resource.tileevent import *




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
        push = Meth.get_btn_state()
        pl = self.actor

        pl.dy = push[BTN.DWN] - push[BTN.UP]
        pl.dx = push[BTN.RHT] - push[BTN.LFT] if not pl.dy else 0
        if pl.dy or pl.dx:
            self.action.Move()
        elif push[BTN.A_Z]:
            Window.close()
        elif push[BTN.B_X]:  # メニュー呼び出し
            gbl.scene_state().context.currentState.map.FieldMenu()
            # pt.menu_show()
            # pt.scene = "menu"



class ActorState_Move(BaseState):
    def __init__(self, parent):
        self.state = STATE.Move
        self.actor = parent.parent
        self.action = parent

    def enter(self):
        self.actor.try_move_forward()

    def update(self):
        pt = self.actor

        pt.dy += pt.spd * ((pt.dy > 0) - (pt.dy < 0))
        pt.dx += pt.spd * ((pt.dx > 0) - (pt.dx < 0))
        # 移動終了
        sz = TILE_SIZE
        if (pt.dy % sz, pt.dx % sz) == (0, 0):
            self.action.Idle()

    def draw(self):
        pass

    def exit(self):
        self.actor.move_end()



class ActorState_Battle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Battle
        self.actor = parent.parent
        self.statecommand = parent

    def update(self):
        pass

    def draw(self):
        pass






