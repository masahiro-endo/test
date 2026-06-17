import pyxel
from enum import Enum, auto
from module.basestate import *
from UI import *
import appconfig as gbl
from actor import *





class BattleStates(BaseContext):
    def __init__(self, parent):
        self.parent = parent
        self.table = {
            STATE.Encount: BattleState_Encount(self),
            STATE.CommandWait: BattleState_CommandWait(self),
            STATE.Attack: BattleState_Attack(self),
            STATE.Spell: BattleState_Spell(self),
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

    def update(self):
        pass
    def draw(self):
        pass


class BattleState_CommandWait(BaseState):
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
            self.disable_cursor()
            self.battle.battle_attack()
        elif ret == BATTLE_SEL.Spell:
            self.statecommand.Spell()
        elif ret == BATTLE_SEL.Run:
            self.statecommand.Run()

    def disable_cursor(self):
        self.cursor = None

    # コマンド選択
    def battle_command(self, msg_pre=[]):
        self.battle.bt_my_turn = True
        self.battle.bt_msg = msg_pre + ["どうする？", " たたかう じゅもん にげる"]
        y = 8 + len(self.battle.bt_msg) * 2
        self.cursor = Cursor("bt_command", [1, 6, 11], y)
        self.battle.battle_showwindow()




class BattleState_Attack(BaseState):
    def __init__(self, parent):
        self.state = STATE.Attack
        self.battle = parent.parent
        self.statecommand = parent

    def update(self):
        pass
    def draw(self):
        pass


class BattleState_Spell(BaseState):
    def __init__(self, parent):
        self.state = STATE.Spell
        self.battle = parent.parent
        self.statecommand = parent
        self.cursor = None

    def enter(self):
        self.battle_spells()

    def update(self):
        if self.cursor is None:
            return

        ret = self.cursor.update()
        if ret >= 0:
            pt = gbl.get_party()
            spl_id = pt.available_spells(True)[ret]
            spl = self.spells[spl_id]
            mp = spl.get_mp(pt.pl)
            if mp and mp <= pt.pl.mp:
                pt.pl.mp -= mp
                self.cursor = None
                self.battle.bt_msg = [f"{pt.pl.name}は {spl.name}をとなえた"]
                if spl_id == SPELL.FIRE:
                    dmg = 0 if self.battle.ms.resist else px.rndi(24, 30)
                    self.battle_damage(self.ms, dmg)
                elif spl_id == SPELL.HEAL:
                    ret = pt.use_heal(mp)
                    self.battle.bt_msg += [f"{ret}HP かいふくした"]
                elif spl_id == SPELL.BURST:
                    dmg = 0
                    for _ in range(mp):
                        dmg += px.rndi(8, 12)
                    self.battle_damage(self.battle.ms, dmg)
                self.battle.battle_showwindow()
        else:
            self.statecommand.Command_wait()
            self.cursor.pos = SPELL.CLOSE

    def draw(self):
        pass

    # バトル用呪文リスト
    def battle_spells(self):
        pt = gbl.get_party()
        spells = pt.available_spells(True)
        pos = self.cursor.pos if self.cursor else 0
        mp = get_resource().spells[spells[pos]].get_mp(pt.pl)
        t1 = " "
        list_x = []
        for spl_id in spells:
            list_x.append(len(t1))
            t1 += get_resource().spells[spl_id].name + " "
        self.battle.bt_msg = ["なにを つかいますか？", t1, f" MP {pad(mp,2)}"]
        if not self.cursor:
            self.cursor = Cursor("bt_spells", list_x, 12, -1)
        self.battle.battle_showwindow()


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
        rate = 1.0 + self.pl.spd / self.ms.spd
        if rate > px.rndf(0.0, 2.0):
            self.battle.scene.Main()
            Window.message(["にげのびた..."])
        else:
            self.battle.bt_msg = ["にげられなかった"]
            self.battle.battle_showwindow()


class BattleState_BattleLog(BaseState):
    def __init__(self, parent):
        self.state = STATE.Attack
        self.battle = parent.parent
        self.statecommand = parent
        self.battlelog = []

    def update(self):
        pass
    def draw(self):
        pass

    def pushlog(self, state):
        tbl = self.table[state]
        curr = self.current()
        if curr: 
            curr.exit()

        self._stack.append(tbl)
        curr = self.current()
        if curr: 
            curr.enter()

    def poplog(self):
        curr = self.current()
        if curr: 
            curr.exit()

        self._stack.pop()
        curr = self.current()
        if curr: 
            curr.enter()

    def current(self):
        if not self.battlelog:
            return None
        return self.battlelog[-1]



class BattleState_Result(BaseState):
    def __init__(self, parent):
        self.state = STATE.Result
        self.battle = parent.parent
        self.statecommand = parent
        self.cursor = None

    def update(self):
        # どちらかが倒れた
        if self.battle.pl.hp <= 0:
            self.battle.scene.End()
        elif self.battle.ms.hp <= 0:
            self.battle.battle_win()
        # 攻守が入れ替わる
        elif self.battle.bt_my_turn:
            self.battle.battle_monster_action()
        else:
            self.statecommand.Command_wait()

    def draw(self):
        pass

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



