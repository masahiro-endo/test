


class BaseContext():

    table = {}
    currentState = None

    def update(self):
        pass

    def draw(self):
        pass

    def changeState(self, nextState):
        tbl = self.table[nextState]
        if self.currentState: 
            self.currentState.exit()

        self.currentState = tbl
        self.currentState.enter()



class BaseState():

    def update(self):
        pass

    def draw(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass



