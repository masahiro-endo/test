import pyxel
from collections import deque
from enum import IntEnum, Enum, auto
from typing import Any, Dict



class BaseScene:

    def __init__(self):
        pass

    def Enter(self):
        pass

    def Update(self):
        pass

    def Exit(self):
        pass

class TitleScene(BaseScene):
   def Draw(self):
        pyxel.text(75, 0, "Title", 14)

class MainScene(BaseScene):
   def Draw(self):
        pyxel.text(75, 0, "Main", 14)

class EndScene(BaseScene):
   def Draw(self):
        pyxel.text(75, 0, "End", 14)


class GameManager:

    class SCENE(IntEnum):
        TITLE = auto()
        MAIN = auto()
        END = auto()

    currentScene = None
    scenes = None

    def __init__(self):
        self.scenes = {
            GameManager.SCENE.TITLE    : TitleScene(),
            GameManager.SCENE.MAIN    : MainScene(),
            GameManager.SCENE.END    : EndScene(),
        }
        self.switchScene(self.scenes[GameManager.SCENE.TITLE])

    def Update(self):
        self.currentScene.Update()

    def Draw(self):
        self.currentScene.Draw()

    def switchScene(self, newScene):
        if (self.currentScene != None): 
            self.currentScene.Exit()

        self.currentScene = newScene
        self.currentScene.Enter()


