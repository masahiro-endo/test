
from enum import Enum, auto
from basestate import *
from UI import *
from actor import *
import appconfig as gbl
from module.mapstate import *
from module.battlebehavior import *





class SceneStates():
    def __init__(self):
        self.context = SceneStateContext(self, STATE.Title)

    def update(self):
        self.context.update()
    def draw(self):
        self.context.draw()

    def Title(self):
        self.context.changeState(STATE.Title)
    def Main(self):
        self.context.changeState(STATE.Main)
    def Battle(self):
        self.context.changeState(STATE.Battle)
    def GameOver(self):
        self.context.changeState(STATE.GameOver)




class STATE(Enum):
    Title = auto()
    Main = auto()
    Battle = auto()
    GameOver = auto()




class SceneStateContext(BaseContext):
    
    def __init__(self, parent, initState):
        self.parent = parent
        self.table = {
            STATE.Title: SceneState_Title(self),
            STATE.Main: SceneState_Main(self),
            STATE.Battle: SceneState_Battle(self),
            STATE.GameOver: SceneState_GameOver(self),
        }
        self.changeState(initState)

    def update(self):
        self.currentState.update()
    def draw(self):
        self.currentState.draw()






class SceneState_Title(BaseState):
    def __init__(self, parent):
        self.state = STATE.Title
        self.scene = parent.parent

        Window.message([" New Cont Exit", " (push [Z] Key)"])
        self.cursor = Cursor(CURSOR_KEY.WELCOME, [1, 5, 10], TITLE_SEL.Cancel)

    def update(self):
        ret = self.cursor.update()

        if ret == TITLE_SEL.New:
            self.scene.Main()
        elif ret == TITLE_SEL.Continue:
            # すでにセーブデータをロードしているので何もしない
            pass
        elif ret == TITLE_SEL.Exit:
            px.quit()

    def draw(self):
        Meth.draw_text(3, 2, "")
        Meth.draw_text(6, 4, "TEST")

    def exit(self):
        self.cursor.dispose()
        Window.close()




class SceneState_Main(BaseState):
    def __init__(self, parent):
        self.state = STATE.Main
        self.scene = parent

        self.map = MapStates(self)

    def enter(self):
        Window.clear()
        self.map.Field()

    def update(self):
        self.map.update()

    def draw(self):
        self.map.draw()

            


class SceneState_Battle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Battle
        self.scene = parent.parent
        self.cursor = None

        self.logic = BattleBehavior(self)

    def enter(self):
        self.logic.enter_action()

    def update(self):
        self.logic.update()

    def draw(self):
        self.logic.draw()



class SceneState_GameOver(BaseState):
    def __init__(self, parent):
        self.state = STATE.GameOver
        self.scene = parent.parent

    def enter(self):
        self.game_over()

    def update(self):
        btn = Meth.get_btn_state()

        if btn["a"] or btn["b"]:
            self.scene.Main()
            pt.get_start_location()

    def draw(self):
        pass
        
    def game_over(self):
        pt.gold = pt.gold // 2
        pt.pl.hp = 1

        Window.clear()
        Window.message([f"{pt.pl.name}は", "いしきを うしなった"])

