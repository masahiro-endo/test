import pyxel

# ============================================================
# Commands
# ============================================================
class Command:
    pass

class PushState(Command):
    def __init__(self, state):
        self.state = state

class PopState(Command):
    pass

class GotoLabel(Command):
    def __init__(self, label):
        self.label = label


# ============================================================
# Base State + Context
# ============================================================
class State:
    def __init__(self, ctx):
        self.ctx = ctx

    def update(self):
        return None

    def draw(self):
        pass


class Context:
    def __init__(self):
        self.vars = {}       # global flags and variables
        self.text_speed = 2  # typewriter speed


# ============================================================
# Text State
# Now supports embedded commands such as:
#   {flag set KEY}
#   {flag clear KEY}
#   {jump LABEL}
#   {if FLAG LABEL}
# ============================================================
class TextState(State):
    def __init__(self, ctx, script, label):
        super().__init__(ctx)
        if label not in script:
            raise ValueError("Missing label: " + str(label))

        self.script = script
        self.label = label
        self.lines = script[label]
        self.index = 0
        self.char_timer = 0
        self.display_text = ""

    def update(self):
        if self.index >= len(self.lines):
            return PopState()

        raw = self.lines[self.index]

        # Handle inline commands like {flag set love}
        if raw.startswith("{") and raw.endswith("}"):
            return self._handle_command(raw)

        # Typewriting text
        if self.char_timer < len(raw):
            if pyxel.frame_count % self.ctx.text_speed == 0:
                self.char_timer += 1
        else:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.index += 1
                self.char_timer = 0

        return None

    def draw(self):
        pyxel.cls(0)
        if self.index < len(self.lines):
            raw = self.lines[self.index]
            if not (raw.startswith("{") and raw.endswith("}")):
                pyxel.text(10, 10, raw[:self.char_timer], 7)
        pyxel.text(10, 120, "[SPACE]", 6)

    # Command handler
    def _handle_command(self, cmd):
        body = cmd[1:-1].strip().split()

        # Example: {flag set love}
        if body[0] == "flag":
            if len(body) != 3:
                raise ValueError("Invalid flag command")
            action, key = body[1], body[2]
            if action == "set":
                self.ctx.vars[key] = True
            elif action == "clear":
                self.ctx.vars[key] = False
            else:
                raise ValueError("Unknown flag action: " + action)
            self.index += 1
            return None

        # Example: {jump branch_a}
        if body[0] == "jump":
            if len(body) != 2:
                raise ValueError("Invalid jump command")
            return GotoLabel(body[1])

        # Example: {if love branch_love}
        if body[0] == "if":
            if len(body) != 3:
                raise ValueError("Invalid if command")
            flag, label = body[1], body[2]
            if self.ctx.vars.get(flag, False):
                return GotoLabel(label)
            self.index += 1
            return None

        raise ValueError("Unknown command: " + cmd)


# ============================================================
# Choice State
# Options can set flags or jump to labels
#    ("Tell her you care", {"set": "love", "goto": "love_branch"})
# ============================================================
class ChoiceState(State):
    def __init__(self, ctx, prompt, options):
        super().__init__(ctx)
        self.prompt = prompt
        self.options = options
        self.cursor = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.cursor = max(0, self.cursor - 1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.cursor = min(len(self.options) - 1, self.cursor + 1)

        if pyxel.btnp(pyxel.KEY_SPACE):
            text, actions = self.options[self.cursor]

            # Apply flag actions
            if "set" in actions:
                self.ctx.vars[actions["set"]] = True
            if "clear" in actions:
                self.ctx.vars[actions["clear"]] = False

            # Jump target
            if "goto" in actions:
                return PushState(
                    TextState(self.ctx, STORY_SCRIPT, actions["goto"])
                )

            return PopState()

        return None

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, self.prompt, 10)
        y = 40
        for i, (text, _) in enumerate(self.options):
            col = 11 if i == self.cursor else 7
            pyxel.text(20, y, text, col)
            y += 12


# ============================================================
# Main App
# ============================================================
class App:
    def __init__(self):
        pyxel.init(160, 140)
        self.ctx = Context()
        self.stack = []

        self.push(TextState(self.ctx, STORY_SCRIPT, "start"))
        pyxel.run(self.update, self.draw)

    def push(self, state):
        self.stack.append(state)

    def pop(self):
        if self.stack:
            self.stack.pop()

    def update(self):
        if not self.stack:
            return

        st = self.stack[-1]
        try:
            cmd = st.update()
        except Exception as e:
            print("Error:", e)
            return

        if isinstance(cmd, PushState):
            self.push(cmd.state)
        elif isinstance(cmd, PopState):
            self.pop()
        elif isinstance(cmd, GotoLabel):
            self.pop()
            self.push(TextState(self.ctx, STORY_SCRIPT, cmd.label))

    def draw(self):
        if self.stack:
            self.stack[-1].draw()


# ============================================================
# Story Script
# Embedded commands use:
#   {flag set KEY}
#   {flag clear KEY}
#   {if KEY LABEL}
#   {jump LABEL}
# ============================================================
STORY_SCRIPT = {
    "start": [
        "You meet her on the hill...",
        "She smiles softly at you.",
        "{flag clear love}",
        "Do you want to tell her something?",
        # Push choice state
    ],

    "after_choice": [
        "{if love love_scene}",
        "You walk away silently...",
        "Maybe next time.",
        "END",
    ],

    "love_scene": [
        "Her eyes widen in surprise...",
        "She blushes deeply.",
        "She seems happy.",
        "END",
    ],
}

# Insert choice trigger into start-end logic
def patched_start_update(self):
    if self.index < len(self.lines):
        raw = self.lines[self.index]
        if raw.startswith("{") and raw.endswith("}"):
            return self._handle_command(raw)

        if self.char_timer < len(raw):
            if pyxel.frame_count % self.ctx.text_speed == 0:
                self.char_timer += 1
        else:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.index += 1
                self.char_timer = 0
    else:
        # After finishing "start", show choices
        if self.label == "start":
            return PushState(
                ChoiceState(
                    self.ctx,
                    "What do you tell her?",
                    [
                        ("Tell her you like her", {"set": "love", "goto": "after_choice"}),
                        ("Stay quiet", {"goto": "after_choice"}),
                    ]
                )
            )
        return PopState()
    return None

TextState.update = patched_start_update


# Run the app
App()