import pyxel
from enum import Enum, auto
from basestate import *



class Scene():
    def __init__(self):
        self.context = SceneStateContext(self, STATE.Title)

    def update(self):
        self.context.update()

    def Title(self):
        self.context.changeState(STATE.Title)

    def Main(self):
        self.context.changeState(STATE.Main)

    def End(self):
        self.context.changeState(STATE.End)



class STATE(Enum):
    Title = auto()
    Main = auto()
    End = auto()





class SceneStateContext():
    
    def __init__(self, scene, initState):
        self.state = initState
        self.scene = scene
        self.table = {
            STATE.Title: SceneState_Title(self),
            STATE.Main: SceneState_Main(self),
            STATE.End: SceneState_End(self),
        }
        self.currentScene = None
        self.changeState(STATE.Title)

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
        self.scene = parent

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene.Main()

    def draw(self):
        pyxel.text(75,  0, "     [Title]     ", 14)
        pyxel.text(75, 75, "press [space] key", 14)


class SceneState_Main(BaseState):
    def __init__(self, parent):
        self.state = STATE.Main
        self.scene = parent

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene.End()

    def draw(self):
        pyxel.text(75, 0, "now playing...", 14)


class SceneState_End(BaseState):
    def __init__(self, parent):
        self.state = STATE.End
        self.scene = parent

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene.Title()

    def draw(self):
        pyxel.text(60, 0, "thank you for playing!", 14)
