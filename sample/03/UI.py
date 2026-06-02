import pyxel



class MouseManager:

    def __init__(self):
        self.prev_state = {
            pyxel.MOUSE_LEFT_BUTTON: False,
            pyxel.MOUSE_RIGHT_BUTTON: False,
            pyxel.MOUSE_MIDDLE_BUTTON: False
        }

    def update(self):
        self.current_state = {
            btn: pyxel.btn(btn)
            for btn in self.prev_state
        }

    def pressed(self, btn):
        return not self.prev_state[btn] and self.current_state[btn]

    def held(self, btn):
        return self.current_state[btn]

    def released(self, btn):
        return self.prev_state[btn] and not self.current_state[btn]

    def end_frame(self):
        self.prev_state = self.current_state.copy()


# ===== Pyxel ゲーム部分 =====
mouse = MouseManager()

def update():
    mouse.update()

    # 左クリック押した瞬間
    if mouse.pressed(pyxel.MOUSE_LEFT_BUTTON):
        print("左クリック押した瞬間")

    # 左クリック放した瞬間
    if mouse.released(pyxel.MOUSE_LEFT_BUTTON):
        print("左クリック放した瞬間")

    # 右クリック押しっぱなし
    if mouse.held(pyxel.MOUSE_RIGHT_BUTTON):
        print("右クリック押しっぱなし")

    mouse.end_frame()

def draw():
    pyxel.cls(0)
    pyxel.text(10, 10, "左クリック: 押す/放す検出", 7)
    pyxel.text(10, 20, "右クリック: 押しっぱなし検出", 7)

pyxel.init(160, 120, title="Mouse Event Manager")
pyxel.mouse(True)
pyxel.run(update, draw)




