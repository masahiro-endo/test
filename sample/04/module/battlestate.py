import pyxel
from enum import Enum, auto
from module.basestate import *
from UI import *
import appconfig as gbl
from actor import *
from collections import deque




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

    def enter(self):
        pt = gbl.get_party()
        ms_id = pt.get_enemy_race()
        self.battle_encount(ms_id)

    def battle_encount(self, ms_id, evt=None):
        data = get_resource().monsters[ms_id]
        self.battle.ms = Actor(*data)
        self.battle.bt_evt = evt
        self.battle.bt_my_turn = True
        msg_pre = [f"{self.battle.ms.name}が あらわれた"]

        # 先行判定
        if self.battle.pl.is_fasterthan(self.battle.ms):
            self.statecommand.Command_wait()
        else:
            self.bt_msg = msg_pre + ["てきに せんてをとられた"]
            self.battle.pushlog(self.bt_msg)
            self.statecommand.BattleLog()


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
            self.dispose_cursor()
            self.battle.battle_attack()
        elif ret == BATTLE_SEL.Spell:
            self.statecommand.Spell()
        elif ret == BATTLE_SEL.Run:
            self.statecommand.Run()

    def dispose_cursor(self):
        self.cursor = None

    # コマンド選択
    def battle_command(self, msg_pre=[]):
        self.battle.bt_my_turn = True
        self.battle.bt_msg = msg_pre + ["どうする？", " たたかう じゅもん にげる"]
        y = 8 + len(self.battle.bt_msg) * 2
        self.cursor = Cursor(CURSOR_KEY.BATTLE_COMMAND, [1, 6, 11], y)
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
        if ret is None:
            return

        if ret >= 0:
            pt = gbl.get_party()
            spl_id = pt.available_spells(True)[ret]
            spl = get_resource().spells[spl_id]
            mp = spl.get_mp(pt.pl)
            if mp and mp <= pt.pl.mp:
                pt.pl.mp -= mp
                self.cursor = None
                self.battle.bt_msg = [f"{pt.pl.name}は {spl.name}をとなえた"]
                if spl_id == SPELL.FIRE:
                    dmg = 0 if self.battle.ms.resist else px.rndi(24, 30)
                    self.battle.battle_damage(self.battle.ms, dmg)
                elif spl_id == SPELL.HEAL:
                    ret = pt.use_heal(mp)
                    self.battle.bt_msg += [f"{ret}HP かいふくした"]
                elif spl_id == SPELL.BURST:
                    dmg = 0
                    for _ in range(mp):
                        dmg += px.rndi(8, 12)
                    self.battle.battle_damage(self.battle.ms, dmg)
                self.battle.battle_showwindow()
        else:
            self.statecommand.Command_wait()
            self.cursor.pos = SPELL.RETURN

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
        rate = 1.0 + self.battle.pl.spd / self.battle.ms.spd
        if rate > px.rndf(0.0, 2.0):
            self.battle.scene.Main()
            Window.clear()
            Window.message(["にげのびた..."])
        else:
            self.battle.bt_msg = ["にげられなかった"]
            self.battle.battle_showwindow()


class BattleState_BattleLog(BaseState):
    def __init__(self, parent):
        self.state = STATE.BattleLog
        self.battle = parent.parent
        self.statecommand = parent
        self.cursor = None
        self.battlelog = deque()

    def enter(self):
        self.battlelog = self.battle.battlelog
        self.show_battlelog()
        
    def show_battlelog(self):
        pt = gbl.get_party()
        Window.open(WINDOW_KEY.BATTLESTS, 8, 0, 16, 8, pt.battlestatus())
        if self.is_remain():
            Window.open(WINDOW_KEY.BATTLEMSG, 0, 8, 16, 16, self.battlelog[0])

    def is_remain(self):
        return True if len(self.battlelog) > 0 else False

    def update(self):
        btn = get_btn_state()

        if btn["a"] or btn["b"]:
            self.poplog()

            # どちらかが倒れた
            if self.battle.is_players_win():
                self.statecommand.Result()
            elif self.battle.is_enemies_win():
                self.battle.scene.GameOver()
            # 攻守が入れ替わる
            elif self.battle.bt_my_turn:
                self.battle.battle_monster_action()
            else:
                # self.battle_command()
                self.statecommand.Command_wait()

    def draw(self):
        pass

    def pushlog(self, log):
        self.battlelog.append(log)

    def poplog(self):
        if len(self.battlelog) <= 0:
            return
        self.battlelog.pop()

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

    def enter(self):
        self.battle_win()
        
    def update(self):
        pass

    def draw(self):
        pass

    # 勝利
    def battle_win(self):
        pt = gbl.get_party()

        t = ["たたかいに かった"]
        if self.battle.bt_evt == "boss1":
            t += [f"「{get_resource().spells[SPELL.HEAL].name}」を おぼえた"]
            pt.flags.append("sp2")
        elif self.battle.bt_evt == "boss2":
            t += [f"「{get_resource().spells[SPELL.BURST].name}」を おぼえた"]
            pt.flags.append("sp3")
        elif self.battle.bt_evt == "boss3":
            pt.flags.append("4-3")
            t = ["ひほうを てにいれた！"]
        else:
            gold = int(self.battle.ms.gold * px.rndf(0.7, 1.0) + 0.99)
            pt.add_gold(gold)
            t += [f"{gold}G てにいれた"]
        
        self.battle.scene.Main()
        Window.clear()
        Window.message(t)



