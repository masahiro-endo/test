import pyxel
from enum import Enum, auto
from module.basestate import *
from UI import *
from actor import *
import appconfig as gbl
from module.mapstate import *
from module.battlestate import *





class SceneStates():
    def __init__(self):
        self.context = SceneStateContext(self, STATE.Main)

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




class SceneStateContext(BaseContext):
    
    def __init__(self, parent, initState):
        self.parent = parent
        self.table = {
            STATE.Title: SceneState_Title(self),
            STATE.Main: SceneState_Main(self),
            STATE.Battle: SceneState_Battle(self),
            STATE.End: SceneState_End(self),
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
        self.cursor = Cursor("welcome", [1, 5, 10], 12)

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
        self.state = STATE.Main
        self.scene = parent.parent
        self.cursor = None
        self.pl = gbl.get_party().pl
        self.battlephase = BattleStates(self)
        self.battlelog = []   

    def enter(self):
        self.battle_start(0)

    def update(self):
        self.battlephase.update()

        btn = get_btn_state()
        if btn["a"] or btn["b"]:
            # どちらかが倒れた
            if self.pl.hp <= 0:
                self.scene.End()
            elif self.ms.hp <= 0:
                self.battle_win()
            # 攻守が入れ替わる
            elif self.bt_my_turn:
                self.battle_monster_action()
            else:
                # self.battle_command()
                self.battlephase.Command_wait()

    def draw(self):
        self.battlephase.draw()

        # バトル用draw処理（モンスターグラフィック表示）
        u = self.ms.img % 4 * 64
        v = self.ms.img // 4 * 64 + 64
        px.blt(0, 0, 0, u, v, 64, 64)

        for key in Window.all:
            Window.all[key].draw()
        
        if self.battlephase.currentState.cursor:
            self.battlephase.currentState.cursor.draw()


    def battle_start(self, ms_id, evt=None):
        data = get_resource().monsters[ms_id]
        # self.scene = "battle"
        self.ms = Actor(*data)
        self.bt_evt = evt
        self.bt_my_turn = True
        msg_pre = [f"{self.ms.name}が あらわれた"]
        # 先行判定
        if self.pl.spd * px.rndf(1.0, 2.0) >= self.ms.spd * px.rndf(1.0, 2.0):
            # self.battle_command(msg_pre)
            self.battlephase.Command_wait()
        else:
            self.bt_msg = msg_pre + ["てきに せんてをとられた"]
            self.battle_showwindow()
        # self.wait = True
        # self.play_bgm(0)

    def battle_command(self, msg_pre=[]):
        self.bt_my_turn = True
        self.bt_msg = msg_pre + ["どうする？", " たたかう じゅもん にげる"]
        y = 8 + len(self.bt_msg) * 2
        self.cursor = Cursor("bt_command", [1, 6, 11], y)
        self.battle_showwindow()

    # バトル用ウィンドウ生成
    def battle_showwindow(self):
        pl = self.pl
        t = [pl.name, f"HP {pad(pl.hp,3)}", f"MP  {pad(pl.mp,2)}"]
        Window.open("bt_stat", 8, 0, 16, 8, t)
        Window.open("bt_msg", 0, 8, 16, 16, self.bt_msg)

    # バトル用呪文リスト
    def battle_spells(self):
        spells = self.available_spells(True)
        pos = self.cursor.pos if self.cursor else 0
        mp = get_resource().spells[spells[pos]].get_mp(self.pl)
        t1 = " "
        list_x = []
        for spl_id in spells:
            list_x.append(len(t1))
            t1 += self.spells[spl_id].name + " "
        self.bt_msg = ["なにを つかいますか？", t1, f" MP {pad(mp,2)}"]
        if not self.cursor:
            self.cursor = Cursor("bt_spells", list_x, 12, -1)
        self.battle_showwindow()

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
        

        self.battle_showwindow()

    # ダメージ処理
    def battle_damage(self, target, dmg):
        self.bt_msg += [f"{target.name}に {dmg}ダメージ"]
        target.hp = max(target.hp - dmg, 0)
        if self.bt_my_turn and target.hp <= 0:
            self.bt_msg += [f"{target.name}を たおした"]

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
        # MPがある敵はファイアを使う
        spl = get_resource().spells[SPELL.FIRE]
        if self.ms.mp >= spl.mp and px.rndi(0, 1) == 0:
            self.ms.mp -= spl.mp
            self.bt_msg = [f"{self.ms.name}は{spl.name}をとなえた"]
            dmg = px.rndi(12, 18)  # 敵のファイアは少し弱め
            self.battle_damage(self.pl, dmg)
            self.battle_showwindow()
        else:
            self.battle_attack(msg_pre)

    # 勝利
    def battle_win(self):
        t = ["たたかいに かった"]
        if self.bt_evt == "boss1":
            t += [f"「{get_resource().spells[SPELL.HEAL].name}」を おぼえた"]
            self.flags.append("sp2")
        elif self.bt_evt == "boss2":
            t += [f"「{get_resource().spells[SPELL.BURST].name}」を おぼえた"]
            self.flags.append("sp3")
        elif self.bt_evt == "boss3":
            self.flags.append("4-3")
            t = ["ひほうを てにいれた！"]
        else:
            gold = int(self.ms.gold * px.rndf(0.7, 1.0) + 0.99)
            gbl.get_party().add_gold(gold)
            t += [f"{gold}G てにいれた"]
        Window.message(t)
        self.scene.Main()


class SceneState_End(BaseState):
    def __init__(self, parent):
        self.state = STATE.End
        self.scene = parent.parent

    def enter(self):
        pt = gbl.get_party()
        pt.game_over()

    def update(self):
        btn = get_btn_state()
        pt = gbl.get_party()
        if btn["a"] or btn["b"]:
            pt.gold = pt.gold // 2
            pt.pl.hp = 1
            self.scene.Main()

    def draw(self):
        for key in Window.all:
            Window.all[key].draw()
        
