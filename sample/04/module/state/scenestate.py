
from enum import Enum, auto
import appconfig as gbl
from module.UI import Window
from module.battlemanner import *
from module.state.basestate import *
from module.state.optionstate import *
from module.state.mapstate import *





class SceneStates():
    def __init__(self):
        self.context = SceneStateContext(self, STATE.Demo)

    def update(self):
        self.context.update()
    def draw(self):
        self.context.draw()

    def Demo(self):
        self.context.changeState(STATE.Demo)
    def Title(self):
        self.context.changeState(STATE.Title)
    def Main(self):
        self.context.changeState(STATE.Main)
    def Battle(self):
        self.context.changeState(STATE.Battle)
    def GameOver(self):
        self.context.changeState(STATE.GameOver)
    def Test(self):
        self.context.changeState(STATE.Test)




class STATE(Enum):
    Demo = auto()
    Title = auto()
    Main = auto()
    Battle = auto()
    GameOver = auto()
    Test = auto()




class SceneStateContext(BaseContext):
    
    def __init__(self, parent, initState):
        self.parent = parent
        self.table = {
            STATE.Demo    : SceneState_Demo(self),
            STATE.Title   : SceneState_Title(self),
            STATE.Main    : SceneState_Main(self),
            STATE.Battle  : SceneState_Battle(self),
            STATE.GameOver: SceneState_GameOver(self),
            STATE.Test    : SceneState_Test_Battle(self),
        }
        self.changeState(initState)

    def update(self):
        self.currentState.update()
    def draw(self):
        self.currentState.draw()








class SceneState_Demo(BaseState):
    def __init__(self, parent):
        self.state = STATE.Demo
        self.scene = parent.parent
        self.color = px.COLOR_CYAN
        self.sec = 1.4

    def update(self):
        pass
    def draw(self):
        self.draw_eyecatch()

    def draw_eyecatch(self):
        Meth.draw_text(5, 5, "pyxel", self.blink_color())

        if px.frame_count > (60 * self.sec):
            self.scene.Title()

    def blink_color(self):
        if (px.frame_count // 15) % 2 == 0:
            return px.COLOR_DARK_BLUE if self.color == px.COLOR_CYAN else px.COLOR_CYAN
        else:
            return px.COLOR_CYAN



class SceneState_Title(OptionState):

    def __init__(self, parent):
        self.state = STATE.Title
        self.scene = parent.parent
        # self.cursor = None


    def enter(self):
        # __init__() に記述すると、
        # gblクラス生成前で実行エラーがでるため、
        # ここに記述することでチェックを遅らせる。
        COMMAND_TREE = {
            'New' : [gbl.scene_state().Main],
            'Cont': [None],
            'Exit': [px.quit],
        }

        super().__init__(COMMAND_TREE)


    def update(self):
        super().update()
                    
    def draw(self):
        super().draw()
        Meth.draw_text(3, 2, "")
        Meth.draw_text(6, 4, "TEST")

    def exit(self):
        Window.close()




class SceneState_Main(BaseState):
    def __init__(self, parent):
        self.state = STATE.Main
        self.scene = parent.parent

        self.map = MapStates(self)

    def enter(self):
        Window.clear()
        self.map.Field()

    def update(self):
        self.map.update()

    def draw(self):
        self.map.draw()

            


class SceneState_Battle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Battle
        self.scene = parent.parent
        self.cursor = None

        # self.logic = BattleBehavior(self)

    def enter(self):
        self.logic.enter_action()

    def update(self):
        self.logic.update()

    def draw(self):
        self.logic.draw()



class SceneState_GameOver(BaseState):
    def __init__(self, parent):
        self.state = STATE.GameOver
        self.scene = parent.parent

    def enter(self):
        self.pt = gbl.player_party()
        self.game_over()

    def update(self):
        push = Meth.get_btn_state()

        if push[BTN.A_Z] or push[BTN.B_X]:
            self.scene.Main()
            self.pt.get_start_location()

    def draw(self):
        pass
        
    def game_over(self):
        self.pt.gold = self.pt.gold // 2
        self.pt[0].hp = 1

        Window.clear()
        Window.message([f"{self.pt[0].name}は", "いしきを うしなった"])






# StateContextから独立し、単体で用いる。
# main.py\SceneStackに、pushleft()する。
# draw処理はscenes[-1]で担わせ、
# scene[0]である本クラスでupdate処理を奪う。
class SceneState_Extend(BaseState):
    def __init__(self, texts):
        self.texts = texts

    def update(self):
        push = Meth.get_btn_state()
        for btn in push:
            if push[btn]:
                gbl.scene_state().Test()
                sprite = gbl.scene_stack().popleft()
                del sprite # # 自身を del する

    def draw(self):
        self.draw_pause()

    def draw_pause(self):
        for pos, text in enumerate(self.texts):
            x, y = (3, 6 + pos * 2)
            self.draw_rect(x, y, len(text), 2) #背景
            Meth.draw_text(x, y, text, px.COLOR_ORANGE)

    def draw_rect(self, x, y, w, h, clr=px.COLOR_BLACK):
        # 描画座標は x8
        px.rect(x * 8 - 4 , y * 8 + 4 , w * 8 , h * 8 ,clr)





class SceneState_Test(OptionState):

    COMMAND_TREE = {
        "たたかう": {
            "通常攻撃": None,
            "スキル": {
                "単体攻撃": None,
                "全体攻撃": None
            },
            "魔法": {
                "回復": None,
                "攻撃": None
            }
        },
        "どうぐ": {
            "回復アイテム": None,
            "攻撃アイテム": None
        },
        "にげる": None,
        "防御": None
    }

    def __init__(self, parent):
        super().__init__(self.COMMAND_TREE)
        self.state = STATE.Test
        self.scene = parent.parent

    def update(self):
        super().update()
                    
    def draw(self):
        super().draw()





class SceneState_Test_Battle(BaseState):

    def __init__(self, parent):
        self.state = STATE.Test
        self.scene = parent.parent
        self.manner = BattleManner(self)

    def update(self):
        self.manner.update()
                    
    def draw(self):
        self.manner.draw()
