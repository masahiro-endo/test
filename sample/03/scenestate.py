import pyxel
from enum import Enum, auto
from basestate import *
from UI import *
from actor import *
import appconfig






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
    
    def __init__(self, scene, initState):
        self.state = initState
        self.scene = scene
        self.table = {
            STATE.Title: SceneState_Title(self),
            STATE.Main: SceneState_Main(self),
            STATE.Battle: SceneState_Battle(self),
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
        self.context = parent

        message_window([" New Cont Exit", " (Zキー or Aボタン)"])
        self.cur = Cursor("welcome", [1, 5, 10], 12)

    def update(self):
        ret = self.cur.update()

        if ret == 0: # New
            pt = appconfig.get_party()
            pt = Party()
            self.context.scene.Main()
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

        (self.x, self.y, self.z) = (8, 21, 0)

    def update(self):
        get_screen().party.update()

    def draw(self):
            pt = get_screen().party

            x, y = (self.x * 16 + pt.dx, self.y * 16 + pt.dy)
            px.bltm(8, 0, self.z, x - 48, y - 48, 112, 112)
            # 障害物（NPC含む）
            for key in get_resource().obstacles:
                if not key in pt.flags:
                    ob = get_resource().obstacles[key]
                    ob.draw(x, y, self.z)
            # マスク
            px.blt(0, -8, 0, 64, 0, 64, 64, 1)
            px.blt(64, -8, 0, 64, 0, -64, 64, 1)
            px.blt(0, 56, 0, 64, 0, 64, -64, 1)
            px.blt(64, 56, 0, 64, 0, -64, -64, 1)
            # 主人公
            (u, v) = ((px.frame_count % 30) // 15 * 16, 2 * 16)
            px.blt(56, 48, 0, u, v, 16, 16, 1)
            # ステータス表示
            px.rect(0, 112, 128, 16, 0)
            t = f"HP{pad(pt.pl.hp,3)} MP{pad(pt.pl.mp,2)} {pad(pt.gold,4)}G"
            draw_text(0, 14, t)


class SceneState_Battle(BaseState):
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
