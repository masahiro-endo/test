import pyxel
from enum import Enum, auto
from basestate import *
from UI import *
import appconfig as gbl
from actor import *




class BattleStates(BaseContext):
    def __init__(self, parent):
        self.parent = parent
        self.table = {
            STATE.Encount: BattleState_Encount(self),
            STATE.CommandWait: BattleState_Wait_Command(self),
            STATE.Attack: BattleState_Attack(self),
            STATE.Spell: BattleState_choice_Spell(self),
            STATE.Run: BattleState_Run(self),
            STATE.BattleLog: BattleState_BattleLog(self),
            STATE.Result: BattleState_Result(self),
        }
        self.currentState = None
        self.changeState(STATE.Encount)

    def update(self):
        self.currentState.update()
    def draw(self):
        self.currentState.draw()

    def Encount(self):
        self.changeState(STATE.Encount)
    def Command_wait(self):
        self.changeState(STATE.CommandWait)
    def Attack(self):
        self.changeState(STATE.Attack)
    def Spell(self):
        self.changeState(STATE.Spell)
    def Run(self):
        self.changeState(STATE.Run)
    def BattleLog(self):
        self.changeState(STATE.BattleLog)
    def Result(self):
        self.changeState(STATE.Result)




class STATE(Enum):
    Encount = auto()
    CommandWait = auto()
    Attack = auto()
    Spell = auto()
    Run = auto()
    BattleLog = auto()
    Result = auto()




class BattleState_Encount(BaseState):
    def __init__(self, parent):
        self.state = STATE.Encount
        self.battle = parent.parent
        self.statecommand = parent
        self.cursor = None

    def enter(self):
        # pt = gbl.get_party()
        # ms_id = pt.get_enemy_race()
        # self.battle_encount(ms_id)
        pass

    def battle_encount(self, ms_id, evt=None):
        self.battle.bt_evt = evt

        data = gbl.resource().monsters[ms_id]
        self.battle.ms = Actor(*data)
        bt_msg = [f"{self.battle.ms.name}が あらわれた"]

        # 先制判定
        if self.battle.pl.is_fasterthan(self.battle.ms):
            self.statecommand.Command_wait()
        else:
            bt_msg += ["てきに せんてをとられた"]
            self.battle.pushlog(bt_msg)

            self.statecommand.BattleLog()

    def update(self):
        pass
    def draw(self):
        pass


class BattleState_Wait_Command(BaseState):
    def __init__(self, parent):
        self.state = STATE.CommandWait
        self.battle = parent.parent
        self.statecommand = parent
        self.cursor = None

    def enter(self):
        self.battle_command()
    
    def update(self):
        if self.cursor is None:
            return

        ret = self.cursor.update()
        if ret == BATTLE_SEL.Attack:
            self.cursor.dispose()
            self.statecommand.Attack()
        elif ret == BATTLE_SEL.Spell:
            self.statecommand.Spell()
        elif ret == BATTLE_SEL.Run:
            self.statecommand.Run()

    def battle_command(self, msg_pre=[]):
        bt_msg = []
        bt_msg = msg_pre + ["どうする？", " たたかう じゅもん にげる"]
        y = 8 + len(bt_msg) * 2
        self.cursor = Cursor(CURSOR_KEY.BATTLE_COMMAND, [1, 6, 11], y)
        Window.battlemessage(bt_msg)

    def exit(self):
        self.cursor.dispose()


class BattleState_Attack(BaseState):
    def __init__(self, parent):
        self.state = STATE.Attack
        self.battle = parent.parent
        self.statecommand = parent

    def enter(self):
        bt_msg = self.battle.pt[0].battlelog_action_atk(self.battle.mspt[0])
        self.battle.pushlog(bt_msg)
        self.battle.end_action()

    def update(self):
        pass
    def draw(self):
        pass



class BattleState_choice_Spell(BaseState):
    def __init__(self, parent):
        self.state = STATE.Spell
        self.battle = parent.parent
        self.statecommand = parent
        self.cursor = None

    def enter(self):
        self.battle_list_spells()

    def update(self):
        if self.cursor is None:
            return

        ret = self.cursor.update()
        if ret is None:
            return

        if ret >= 0:
            self.battlelog_cast_spell(self.battle.ms, ret)
            self.battle.end_action()
        else:
            self.statecommand.Command_wait()

    def draw(self):
        pass

    def exit(self):
        self.cursor.dispose()

    def battlelog_cast_spell(self, target, sel_id, msg_pre=[]):
        pt = gbl.player_party()
        spl_id = pt.available_spells(True)[sel_id]
        spl = gbl.resource().spells[spl_id]
        cost = spl.mp

        if cost and cost <= pt.pl.mp:
            pt.pl.mp -= cost
            self.cursor.dispose()
            bt_msg = [f"{pt.pl.name}は {spl.name}をとなえた"]
            bt_msg += pt.pl.battlelog_spell_effect(target, spl_id, cost)
            self.battle.pushlog(bt_msg)
            self.battle.end_action()

    # バトル用呪文リスト
    def battle_list_spells(self):
        pt = gbl.get_party()
        list_x, t1, list_mp = pt.available_spells_cursor()

        pos = self.cursor.pos if self.cursor else 0
        cost = list_mp[pos].mp

        bt_msg = ["なにを つかいますか？", t1, f" MP {Meth.pad(cost,2)}"]
        self.cursor = Cursor(CURSOR_KEY.BATTLE_SPELLS, list_x, 12, SPELL_SEL.Cancel)
        Window.battlemessage(bt_msg)

    def available_spells_cursor(self, pl):
        spells = pl.available_spells(True)
        t1 = " "
        list_x = []
        list_mp = []
        for spl_id in spells:
            spl = gbl.resource().spells[spl_id]
            list_x.append(len(t1))
            t1 += spl.name + " "
            list_mp.append(spl.mp)
        return list_x, t1, list_mp



class BattleState_Run(BaseState):
    def __init__(self, parent):
        self.state = STATE.Run
        self.battle = parent.parent
        self.statecommand = parent

    def enter(self):
        self.battle_run()
        
    def update(self):
        pass
    def draw(self):
        pass

    # 逃げる
    def battle_run(self):
        bt_msg = []
        rate = 1.0 + self.battle.pl.spd / self.battle.ms.spd
        if rate > px.rndf(0.0, 2.0):
            bt_msg = ["にげのびた..."]
            self.battle.scene.Main()
            Window.clear()
            Window.message(bt_msg)
            self.battle.scene.Main()
        else:
            bt_msg = ["にげられなかった"]
            self.battle.pushlog(bt_msg)
            self.battle.end_action()


class BattleState_BattleLog(BaseState):
    def __init__(self, parent):
        self.state = STATE.BattleLog
        self.battle = parent.parent
        self.statecommand = parent
        self.cursor = None

    def enter(self):
        Window.battlemessage(self.battle.battlelog[0])
        
    def update(self):
        btn = Meth.get_btn_state()

        if btn["a"] or btn["b"]:
            self.battle.poplog()
            if self.log_is_remain():
                Window.battlemessage(self.battle.battlelog[0])
            else:
                if self.battle.is_win() or self.battle.is_lose():
                    self.statecommand.Result()
                else:
                    self.battle.next_turn()

    def draw(self):
        pass

    def log_is_remain(self):
        return True if len(self.battle.battlelog) > 0 else False



class BattleState_Result(BaseState):
    def __init__(self, parent):
        self.state = STATE.Result
        self.battle = parent.parent
        self.statecommand = parent
        self.cursor = None

    def enter(self):
        if self.battle.is_win():
            self.battle_win()
        else:
            self.battle.scene.GameOver()
        
    def update(self):
        pass

    def draw(self):
        pass

    # 勝利
    def battle_win(self):
        pt = self.battle.pt
        ms = self.battle.mspt._member[0]

        t = ["たたかいに かった"]
        if self.battle.bt_evt == "boss1":
            t += [f"「{gbl.resource().spells[SPELL.HEAL].name}」を おぼえた"]
            pt.flags.append("sp2")
        elif self.battle.bt_evt == "boss2":
            t += [f"「{gbl.resource().spells[SPELL.BURST].name}」を おぼえた"]
            pt.flags.append("sp3")
        elif self.battle.bt_evt == "boss3":
            pt.flags.append("4-3")
            t = ["ひほうを てにいれた！"]
        else:
            gold = int(ms.gold * px.rndf(0.7, 1.0) + 0.99)
            pt.add_gold(gold)
            t += [f"{gold}G てにいれた"]
        
        gbl.scene().Main()
        Window.clear()
        Window.message(t)



