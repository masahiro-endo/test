import pyxel
from enum import Enum, auto
from basestate import *
from UI import *
from actor import *
import appconfig as gbl
from mapfield import *






class Screen():
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

    def End(self):
        self.context.changeState(STATE.End)



class STATE(Enum):
    Title = auto()
    Main = auto()
    Battle = auto()
    End = auto()





class SceneStateContext():
    
    def __init__(self, parent, initState):
        self.parent = parent
        self.table = {
            STATE.Title: SceneState_Title(self),
            STATE.Main: SceneState_Main(self),
            STATE.Battle: SceneState_Battle(self),
            STATE.End: SceneState_End(self),
        }
        self.currentScene = None
        self.changeState(initState)

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





class SceneState_Title(BaseState):
    def __init__(self, parent):
        self.state = STATE.Title
        self.scene = parent.parent

        message_window([" New Cont Exit", " (Zキー or Aボタン)"])
        self.cur = Cursor("welcome", [1, 5, 10], 12)

    def update(self):
        ret = self.cur.update()

        if ret == 0: # New
            config = gbl.get_settings()
            config.map = Map_Field()
            config.party = Party()
            self.scene.Main()
        elif ret == 1:  #（Continue)の場合、すでにセーブデータをロードしているので何もしない
            pass
        elif ret == 2: # Exit
            px.quit()


    def draw(self):
        draw_text(3, 2, "")
        draw_text(6, 4, "TEST")

        for key in Window.all:
            Window.all[key].draw()
            
        self.cur.draw()

    def exit(self):
        Window.close()


class SceneState_Main(BaseState):
    def __init__(self, parent):
        self.state = STATE.Main
        self.scene = parent

        self.map = Map_Field()

    def update(self):
        self.map.update()

    def draw(self):
        self.map.draw()

        for key in Window.all:
            Window.all[key].draw()
            


class SceneState_Battle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Main
        self.scene = parent.parent

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene.End()

    def draw(self):
        pyxel.text(75, 0, "now playing...", 14)


class SceneState_End(BaseState):
    def __init__(self, parent):
        self.state = STATE.End
        self.scene = parent.parent

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene.Title()

    def draw(self):
        pyxel.text(60, 0, "thank you for playing!", 14)
