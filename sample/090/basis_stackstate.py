# push down state
import pyxel




class BaseState:
    def update(self):
        pass

    def draw(self):
        pass


class StateManager:
    def __init__(self):
        self._stack = []

    def push(self, state):
        # Accept only BaseState instances
        if not isinstance(state, BaseState):
            raise TypeError("State must inherit from BaseState")
        self._stack.append(state)

    def pop(self):
        if not self._stack:
            raise RuntimeError("State stack is empty. Cannot pop.")
        self._stack.pop()

    def current(self):
        if not self._stack:
            return None
        return self._stack[-1]



class TitleState(BaseState):
    def __init__(self, manager):
        self.manager = manager

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.manager.push(GameState(self.manager))

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(1)
        pyxel.text(40, 40, "TITLE SCREEN", 7)
        pyxel.text(32, 70, "SPACE: PUSH GAME STATE", 10)
        pyxel.text(40, 90, "Q: QUIT", 8)


class GameState(BaseState):
    def __init__(self, manager):
        self.manager = manager
        self.x = 60

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.manager.pop()

        if pyxel.btnp(pyxel.KEY_M):
            self.manager.push(MenuState(self.manager))

        if pyxel.btnp(pyxel.KEY_P):
            self.manager.push(PauseState(self.manager))


    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, "GAME STATE", 11)
        pyxel.text(10, 25, "ESC: POP TO TITLE", 8)
        pyxel.rect(self.x, 80, 8, 8, 9)


class MenuState(BaseState):
    def __init__(self, manager):
        self.manager = manager

    def enter(self):
        print("[Menu] Entered menu.")

    def exit(self):
        print("[Menu] Exiting menu.")

    def update(self):
        if pyxel.btnp(pyxel.KEY_M):
            self.manager.pop()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, "MENU STATE", 11)


class PauseState(BaseState):
    def __init__(self, manager):
        self.manager = manager

    def enter(self):
        print("[Pause] Game paused.")

    def exit(self):
        print("[Pause] Resuming game.")

    def update(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.manager.pop()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, "PAUSE STATE", 11)



class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel State/Context/Stack Demo")

        self.manager = StateManager()
        self.manager.push(TitleState(self.manager))

        pyxel.run(self.update, self.draw)

    def update(self):
        current = self.manager.current()
        if current:
            current.update()
        else:
            pyxel.quit()  # no states → exit safely

    def draw(self):
        current = self.manager.current()
        if current:
            current.draw()


# Run the app
if __name__ == "__main__":
    try:
        App()
    except Exception as e:
        print("Error:", e)
