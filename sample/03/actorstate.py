import pyxel
from enum import Enum, auto
from basestate import *
from UI import *
from actor import *





class ActorState():
    def __init__(self):
        self.context = ActorStateContext(self, STATE.Idle)

    def update(self):
        self.context.update()

    def draw(self):
        self.context.draw()

    def Title(self):
        self.context.changeState(STATE.Idle)

    def Main(self):
        self.context.changeState(STATE.Moving)

    def Battle(self):
        self.context.changeState(STATE.Battle)



class STATE(Enum):
    Idle = auto()
    Move = auto()
    Battle = auto()





class ActorStateContext():
    
    def __init__(self, scene, initState):
        self.state = initState
        self.scene = scene
        self.table = {
            STATE.Idle: ActorState_Idle(self),
            STATE.Move: ActorState_Move(self),
            STATE.Battle: ActorState_Battle(self),
        }
        self.currentScene = None
        self.changeState(STATE.Idle)

    def update(self):
        self.currentScene.update()

    def draw(self):
        self.currentScene.draw()

    def changeState(self, nextState):
        tbl = self.table[nextState]
        if (self.currentScene != None): 
            self.currentScene.exit()

        self.currentScene = tbl
        self.currentScene.enter()



class ActorState_Idle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Idle
        self.context = parent

    def update(self):
        btn = get_btn_state()
        pt = get_character().party

        pt.dy = btn["d"] - btn["u"]
        pt.dx = btn["r"] - btn["l"] if not self.dy else 0
        if pt.dy or pt.dx:
            pt.move_start()
            self.scene.Move()

        elif btn["a"]:
            Window.close()
        elif btn["b"]:  # メニュー呼び出し
            pt.menu_show()
            pt.scene = "menu"


class ActorState_Move(BaseState):
    def __init__(self, parent):
        self.state = STATE.Move
        self.scene = parent

    def update(self):
        btn = get_btn_state()
        pt = get_character().party

        pt.dy += pt.spd * ((pt.dy > 0) - (pt.dy < 0))
        pt.dx += pt.spd * ((pt.dx > 0) - (pt.dx < 0))
        # 移動終了
        if (pt.dy % 16, pt.dx % 16) == (0, 0):
            self.scene.Idle()


    def draw(self):
        pyxel.text(75, 0, "now playing...", 14)


class ActorState_Battle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Battle
        self.scene = parent

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene.End()

    def draw(self):
        pyxel.text(75, 0, "now playing...", 14)






