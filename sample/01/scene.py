import pyxel
from enum import Enum, auto



class SCENE(Enum):
    Title = auto()
    Main = auto()
    End = auto()

class COMMAND(Enum):
    Insert = auto()
    Pop = auto()
    Push = auto()

class StateReturn():
    def __init__(self, scene, cmd):
        self.scene = scene
        self.command = cmd




class SceneManager():
    
    def __init__(self):
        self.scene = {
            SCENE.Title: TitleScene(self),
            SCENE.Main: MainScene(self),
            SCENE.End: EndScene(self),
        }
        self.currentScene = None
        self.changeState(self.scene[SCENE.Title])

    def update(self):
        res = self.currentScene.update()
        if (res != None): 
            self.changeState(res.scene)

    def draw(self):
        self.currentScene.draw()

    def changeState(self, nextScene):
        if (self.currentScene != None): 
            self.currentScene.exit()

        self.currentScene = nextScene
        self.currentScene.enter()


class BaseScene():
    def update(self) -> StateReturn:
        pass

    def draw(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

class TitleScene(BaseScene):
    def __init__(self, parent):
        self.parent = parent

    def update(self) -> StateReturn:
        res = None
        if pyxel.btnp(pyxel.KEY_SPACE):
            res = StateReturn(self.parent.scene[SCENE.Main], COMMAND.Push)
        return res

    def draw(self):
        pyxel.text(75,  0, "     [Title]     ", 14)
        pyxel.text(75, 75, "press [space] key", 14)


class MainScene(BaseScene):
    def __init__(self, parent):
        self.parent = parent

    def update(self) -> StateReturn:
        res = None
        if pyxel.btnp(pyxel.KEY_SPACE):
            res = StateReturn(self.parent.scene[SCENE.End], COMMAND.Push)
        return res

    def draw(self):
        pyxel.text(75, 0, "now playing...", 14)


class EndScene(BaseScene):
    def __init__(self, parent):
        self.parent = parent

    def update(self) -> StateReturn:
        res = None
        if pyxel.btnp(pyxel.KEY_SPACE):
            res = StateReturn(self.parent.scene[SCENE.Title], COMMAND.Push)
        return res

    def draw(self):
        pyxel.text(60, 0, "thank you for playing!", 14)
