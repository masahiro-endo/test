import pyxel
from enum import Enum, auto
from module.basestate import *
from UI import *
from actor import *
import appconfig as gbl
from module.mapstate import *
from module.battlestate import *
import heapq
import random





class SceneStates():
    def __init__(self):
        self.context = SceneStateContext(self, STATE.Battle)

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

    def GameOver(self):
        self.context.changeState(STATE.GameOver)




class STATE(Enum):
    Title = auto()
    Main = auto()
    Battle = auto()
    GameOver = auto()




class SceneStateContext(BaseContext):
    
    def __init__(self, parent, initState):
        self.parent = parent
        self.table = {
            STATE.Title: SceneState_Title(self),
            STATE.Main: SceneState_Main(self),
            STATE.Battle: SceneState_Battle(self),
            STATE.GameOver: SceneState_GameOver(self),
        }
        self.changeState(initState)

    def update(self):
        self.currentState.update()

    def draw(self):
        self.currentState.draw()






class SceneState_Title(BaseState):
    def __init__(self, parent):
        self.state = STATE.Title
        self.scene = parent.parent

        Window.message([" New Cont Exit", " (push [Z] Key)"])
        self.cursor = Cursor(CURSOR_KEY.WELCOME, [1, 5, 10], TITLE_SEL.Cancel)

    def update(self):
        ret = self.cursor.update()

        if ret == TITLE_SEL.New:
            self.scene.Main()
        elif ret == TITLE_SEL.Continue:  # すでにセーブデータをロードしているので何もしない
            pass
        elif ret == TITLE_SEL.Exit:
            px.quit()

    def draw(self):
        draw_text(3, 2, "")
        draw_text(6, 4, "TEST")

        for key in Window.all:
            Window.all[key].draw()
        
        self.cursor.draw()

    def exit(self):
        Window.close()




class SceneState_Main(BaseState):
    def __init__(self, parent):
        self.state = STATE.Main
        self.scene = parent

        self.map = MapStates(self)

    def enter(self):
        Window.clear()
        self.map.Field()

    def update(self):
        self.map.update()

    def draw(self):
        self.map.draw()

        for key in Window.all:
            Window.all[key].draw()
        
        if self.map.currentState.cursor:
            self.map.currentState.cursor.draw()
            


class SceneState_Battle(BaseState):
    def __init__(self, parent):
        self.state = STATE.Battle
        self.scene = parent.parent
        self.cursor = None

        self.pl = gbl.get_party().pl
        self.battlelog = deque()
        self.turn_queue = []
        self.action = BattleStates(self)

    def fill_turn_queue(self):
        self.turn_queue.clear()
        for char in self.pl + self.ms:
            if char.is_alive():
                char.btl_spd = char.spd * px.rndf(1.0, 2.0)
                heapq.heappush(self.turn_queue, (-char.btl_spd, char))

    def next_turn(self):
        if not self.turn_queue:
            self.fill_turn_queue()
        _, self.current_actor = heapq.heappop(self.turn_queue)

        if not self.current_actor.is_alive():
            self.next_turn()
            return

        if self.current_actor.is_player:
            self.state = "PLAYER_CMD"
            self.selected_cmd = 0
            self.selected_target = 0
        else:
            self.state = "ENEMY_ACT"

    def pushlog(self, log):
        self.battlelog.append(log)

    def poplog(self):
        if len(self.battlelog) <= 0:
            return
        self.battlelog.pop()

    def currentlog(self):
        if not self.battlelog:
            return None
        return self.battlelog[-1]

    def enter(self):
        self.action.Encount()

    def update(self):
        self.action.update()

    def draw(self):
        self.action.draw()

        # バトル用draw処理（モンスターグラフィック表示）
        u = self.ms.img % 4 * 64
        v = self.ms.img // 4 * 64 + 64
        px.blt(0, 0, 0, u, v, 64, 64)

        for key in Window.all:
            Window.all[key].draw()
        
        if self.action.currentState.cursor:
            self.action.currentState.cursor.draw()



    # バトル用ウィンドウ生成
    def battle_showwindow(self):
        pt = gbl.get_party()
        Window.open(WINDOW_KEY.BATTLESTS, 8, 0, 16, 8, pt.battlestatus())
        Window.open(WINDOW_KEY.BATTLEMSG, 0, 8, 16, 16, self.bt_msg)


    # 攻撃
    def battle_attack(self, msg_pre=[]):
        # 攻撃する人、される人を設定
        if self.bt_my_turn:
            attacker = self.pl
            target = self.ms
        else:
            attacker = self.ms
            target = self.pl
        self.bt_msg = msg_pre + [f"{attacker.name}の こうげき"]
        hit_rate = max(min(attacker.spd / target.spd, 1.5), 0.25)
        hit_rate = min(hit_rate - px.rndf(0.0, 1.0), 1.0)
        if hit_rate > 0.0:
            dmg = int(attacker.atk * (1 + hit_rate) / 2 + 0.99)
            self.battle_damage(target, dmg)
        else:  # 回避された
            self.bt_msg += [f"{target.name}は みをかわした"]

        self.pushlog(self.bt_msg)
        self.action.BattleLog()
        # self.battle_showwindow()

    # ダメージ処理
    def battle_damage(self, target, dmg):
        self.bt_msg += [f"{target.name}に {dmg}ダメージ"]
        target.hp = max(target.hp - dmg, 0)
        if self.bt_my_turn and not target.is_alive():
            self.bt_msg += [f"{target.name}を たおした"]
        self.pushlog(self.bt_msg)

    def is_players_win(self):
        pt = gbl.get_party()
        return pt.get_alive_actors() and not self.ms.is_alive()

    def is_enemies_win(self):
        return not self.is_players_win()

    # 逃げる
    def battle_run(self):
        rate = 1.0 + self.pl.spd / self.ms.spd
        if rate > px.rndf(0.0, 2.0):
            self.scene.Main()
            Window.message(["にげのびた..."])
        else:
            self.bt_msg = ["にげられなかった"]
            self.battle_showwindow()

    # 敵の行動
    def battle_monster_action(self, msg_pre=[]):
        self.bt_my_turn = False
        
        pt = gbl.get_party()
        target = random.choice(pt.get_alive_actors())

        # MPがある敵はファイアを使う
        spl = get_resource().spells[SPELL.FIRE]
        if self.ms.is_able_cast(spl):
            self.ms.mp -= spl.mp
            self.bt_msg = [f"{self.ms.name}は{spl.name}をとなえた"]
            dmg = px.rndi(12, 18)  # 敵のファイアは少し弱め
            self.battle_damage(target, dmg)
            # self.battle_showwindow()
        else:
            self.battle_attack(msg_pre)



class SceneState_GameOver(BaseState):
    def __init__(self, parent):
        self.state = STATE.GameOver
        self.scene = parent.parent

    def enter(self):
        self.game_over()

    def game_over(self):
        pt = gbl.get_party()
        Window.clear()
        Window.message([f"{pt.pl.name}は", "いしきを うしなった"])

    def update(self):
        btn = get_btn_state()
        pt = gbl.get_party()
        if btn["a"] or btn["b"]:
            pt.gold = pt.gold // 2
            pt.pl.hp = 1
            self.scene.Main()
            pt.get_start_location()

    def draw(self):
        for key in Window.all:
            Window.all[key].draw()
        
