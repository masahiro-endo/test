import pyxel
from enum import Enum, auto
from basestate import *
from UI import *
from actor import *
import appconfig as gbl





class MapState():
    def __init__(self):
        self.context = MapStateContext(self, STATE.Field)

    def update(self):
        self.context.update()

    def draw(self):
        self.context.draw()

    def Field(self):
        self.context.changeState(STATE.Field)

    def Shop(self):
        self.context.changeState(STATE.Shop)



class STATE(Enum):
    Field = auto()
    Shop = auto()





class MapStateContext():
    
    def __init__(self, parent, initState):
        self.parent = parent
        self.table = {
            STATE.Field: MapState_Field(self),
            STATE.Shop: MapState_Shop(self),
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



class MapState_Field(BaseState):
    def __init__(self, parent):
        self.state = STATE.Field
        self.context = parent

    def update(self):
        pass

    def draw(self):
        pass


class MapState_Shop(BaseState):
    def __init__(self, parent):
        self.state = STATE.Shop
        self.scene = parent

    def update(self):
        pass

    def draw(self):
        pyxel.text(75, 0, "now playing...", 14)







