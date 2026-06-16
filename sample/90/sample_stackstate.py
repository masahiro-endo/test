import json
import os
import sys
import pyxel
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))


# ----------------------------------------------------------------------
# Utility: load dialog.json safely
# ----------------------------------------------------------------------

def load_dialog_tree(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Dialog file '{filename}' not found.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Basic validation
        if not isinstance(data, dict):
            raise ValueError("Dialog file root must be a JSON object.")

        for key, node in data.items():
            if "speaker" not in node or "text" not in node:
                raise ValueError(f"Node '{key}' must have 'speaker' and 'text'.")

            if not isinstance(node["text"], list):
                raise ValueError(f"Node '{key}'.text must be a list of strings.")

            node.setdefault("portrait", 7)
            node.setdefault("choices", [])
            node.setdefault("next", None)

        return data

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


# ----------------------------------------------------------------------
# State Commands
# ----------------------------------------------------------------------

class StateCommand: pass

class PushState(StateCommand):
    def __init__(self, state):
        self.state = state

class PopState(StateCommand):
    pass


# ----------------------------------------------------------------------
# Base State
# ----------------------------------------------------------------------

class State:
    def on_enter(self): pass
    def on_exit(self): pass
    def update(self): return None
    def draw(self): pass


# ----------------------------------------------------------------------
# Portrait rendering (placeholder)
# ----------------------------------------------------------------------

def draw_portrait(x, y, color):
    pyxel.rect(x, y, 32, 32, color)
    pyxel.rectb(x, y, 32, 32, 7)


# ----------------------------------------------------------------------
# Dialog Tree Player
# ----------------------------------------------------------------------

class DialogTreeState(State):
    def __init__(self, dialog_tree, start_key):
        self.tree = dialog_tree
        self._go_to(start_key)

    def _go_to(self, key):
        if key not in self.tree:
            raise ValueError(f"Dialog node '{key}' not found.")
        self.key = key
        self.node = self.tree[key]
        self.line_index = 0
        self.showing_choices = False
        self.choice_index = 0

    def update(self):
        # Choice mode
        if self.showing_choices:
            if pyxel.btnp(pyxel.KEY_UP):
                self.choice_index = max(0, self.choice_index - 1)
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.choice_index = min(len(self.node["choices"]) - 1, self.choice_index + 1)
            if pyxel.btnp(pyxel.KEY_SPACE):
                # Apply choice
                _, next_key = self.node["choices"][self.choice_index]
                if next_key is None:
                    return PopState()
                self._go_to(next_key)
            return None

        # Text mode
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.line_index += 1
            if self.line_index >= len(self.node["text"]):
                if self.node["choices"]:
                    self.showing_choices = True
                else:
                    nxt = self.node["next"]
                    if nxt is None:
                        return PopState()
                    self._go_to(nxt)
        return None

    def draw(self):
        pyxel.rect(0, 60, 120, 60, 0)

        # Speaker
        pyxel.text(5, 62, f"{self.node['speaker']}:", 10)

        # Portrait
        draw_portrait(5, 75, self.node["portrait"])

        # Text or choices
        if not self.showing_choices:
            pyxel.text(45, 75, self.node["text"][self.line_index], 7)
            pyxel.text(100, 110, ">>>", 10)
        else:
            for i, (label, _) in enumerate(self.node["choices"]):
                color = 10 if i == self.choice_index else 7
                pyxel.text(45, 75 + i * 12, label, color)


# ----------------------------------------------------------------------
# Title and Game States
# ----------------------------------------------------------------------

class TitleState(State):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            return PushState(GameState())
        return None

    def draw(self):
        pyxel.cls(1)
        pyxel.text(40, 40, "TITLE", 7)
        pyxel.text(15, 60, "Press SPACE to Start", 10)


class GameState(State):
    def update(self):
        if pyxel.btnp(pyxel.KEY_C):
            # Start dialog tree from "start"
            return PushState(DialogTreeState(dialog_tree, "start"))
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            return PopState()
        return None

    def draw(self):
        pyxel.cls(3)
        pyxel.text(10, 10, "GAME PLAY", 7)
        pyxel.text(10, 30, "Press C for Dialog Tree", 10)
        pyxel.text(10, 50, "Press ESC to Title", 10)


# ----------------------------------------------------------------------
# State Machine
# ----------------------------------------------------------------------

class StateMachine:
    def __init__(self, initial_state):
        self.stack = []
        self.push_state(initial_state)

    def push_state(self, state):
        if not isinstance(state, State):
            raise TypeError("push_state requires a State")
        self.stack.append(state)
        state.on_enter()

    def pop_state(self):
        if self.stack:
            self.stack.pop().on_exit()

    def current(self):
        return self.stack[-1] if self.stack else None

    def update(self):
        cur = self.current()
        if not cur:
            return
        cmd = cur.update()
        if isinstance(cmd, PushState):
            self.push_state(cmd.state)
        elif isinstance(cmd, PopState):
            self.pop_state()

    def draw(self):
        cur = self.current()
        if cur:
            cur.draw()


# ----------------------------------------------------------------------
# Pyxel App
# ----------------------------------------------------------------------

class App:
    def __init__(self):
        global dialog_tree

        # Load JSON
        dialog_tree = load_dialog_tree("dialog.json")

        pyxel.init(120, 120, title="JSON Dialog Tree")
        self.fsm = StateMachine(TitleState())
        pyxel.run(self.update, self.draw)

    def update(self):
        self.fsm.update()

    def draw(self):
        self.fsm.draw()


app = None

if __name__ == "__main__":
    try:
        app = App()
    except Exception as e:
        print("Error:", e)
