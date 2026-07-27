
from collections import deque

import appconfig as gbl
from module.actor import *
from module.state.basestate import *
from module.state.optionstate import *
from module.state.battleeffect import *





class PHASE(Enum):
    INPUT = auto()
    TARGET = auto()
    CONFIRM = auto()
    EXECUTE = auto()






class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
    

class BattleStack_BaseLog(BaseState):
    def __init__(self, parent):
        self.battle = parent
        self.log = deque()

    def update(self):
        push = Meth.get_btn_state()

        if push[BTN.A_Z] or push[BTN.B_X]:
            self.log.popleft()
            if not self.is_remain():
                # 自身をスタックから除外する
                self.battle.comand.popleft()

    def draw(self):
        super().draw()
        self.show_log()


    def push(self, texts):
        self.log.append(texts)
    def pop(self):
        if not self.is_remain():
            return
        self.log.popleft()

    def is_remain(self):
        return True if len(self.log) > 0 else False

    def show_log(self):
        texts  = self.log[0] if self.is_remain() else ''
        for pos, text in enumerate(texts):
            Meth.draw_text(1, 10 + pos * 2, text)



# 戦闘ログ表示
class BattleStack_Log(BattleStack_BaseLog):
    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        super().update()

    def draw(self):
        super().draw()

    @classmethod
    def replicate(cls, parent, log):
        ins = cls(parent)
        ins.push(log)
        return ins




class SelectObserver(Observer):
    def update(self, subject):
        if isinstance(subject, OptionState):
            print(f"[Log] 選択肢が {subject.sel_index} に変更されました")



# 行動選択
class BattleStack_Action(OptionState):
    def __init__(self, parent, actor):
        self.state = PHASE.INPUT
        self.battle = parent
        self.actor = actor
        self.enter()

    def enter(self):
        COMMAND_TREE = {
        }
        sub_tree = self.update_sub_tree()
        sub_tree.update(**COMMAND_TREE)
        super().__init__(sub_tree)
        self.attach(SelectObserver())

    def update(self):
        super().update()
        self.handle_input_phase()

    def draw(self):
        super().draw()
        bt_msg = [f"{self.actor.name}'の こうどう？"]
        self.show_message(bt_msg)


    def update_sub_tree(self):
        sub_tree = {}
        
        for i, skls in enumerate(self.actor.skills):
            skl_name, skl_func = skls
            sub_tree[skl_name] = [None, skls]

        # ヒールなどの「味方」側なら、
        # 選択肢を味方名を切り替え
        # actor.action.headto

        return sub_tree

    def handle_input_phase(self):
        push = Meth.get_btn_state()

        if push[BTN.A_Z] or push[BTN.B_X]:
            self.actor.action = self.sel_value[1][1]
            self.battle.comand.popleft() # 自身をpop()する



# ターゲット選択
class BattleStack_Target(OptionState):
    def __init__(self, parent, actor):
        self.state = PHASE.TARGET
        self.battle = parent
        self.actor = actor
        self.enter()

    def enter(self):
        COMMAND_TREE = {
        }
        sub_tree = self.update_sub_tree()
        sub_tree.update(**COMMAND_TREE)
        super().__init__(sub_tree)
        self.attach(SelectObserver())

        gbl.current_cursor = self


    def update(self):
        super().update()
        self.handle_target_phase()

    def draw(self):
        super().draw()
        bt_msg = [f"Select Target"]
        self.show_message(bt_msg)

    def update_sub_tree(self):
        sub_tree = {}
        
        # 「敵」に対する行動なら、選択肢はパーティー単位
        # for i, data in enumerate(self.battle.mspt):
        race = self.battle.mspt.race
        sub_tree[race] = [None, self.battle.mspt]

        # ヒールなどの「味方」側なら、
        # 選択肢を味方名を切り替え
        # actor.action.headto

        return sub_tree

    def handle_target_phase(self):
        push = Meth.get_btn_state()

        if push[BTN.A_Z] or push[BTN.B_X]:
            self.actor.target = self.sel_value[1][1]
            self.battle.comand.popleft() # 自身をpop()する



# 実行可否
class BattleStack_Confirm(OptionState):
    def __init__(self, parent):
        self.state = PHASE.CONFIRM
        self.battle = parent
        self.enter()

    def enter(self):
        COMMAND_TREE = {
            'はい'  : [self.battle.handle_execute_phase],
            'いいえ': [self.battle.reset_stack_wait_commands],
        }

        super().__init__(COMMAND_TREE)
        self.attach(SelectObserver())

        gbl.current_cursor = self

    def update(self):
        self.handle_confirm_phase()
        super().update()

    def draw(self):
        super().draw()
        bt_msg = [f"実行しますか？"]
        self.show_message(bt_msg)


    def handle_confirm_phase(self):
        push = Meth.get_btn_state()

        if push[BTN.A_Z] or push[BTN.B_X]:
            self.battle.comand.popleft() # 自身をpop()する



# １ターンの終端　分岐
class BattleStack_Term(BattleStack_BaseLog, Singleton):

    def __init__(self, parent):
        self.battle = parent
        self.log = deque()

    def __call__(self):
        self.terminal_log()
        return self

    def update(self):
        push = Meth.get_btn_state()

        if push[BTN.A_Z] or push[BTN.B_X]:
            self.log.popleft()
            if not self.is_remain():
                self.branch_path()
                # 自身をスタックから除外する
                self.battle.comand.popleft()

    def draw(self):
        super().draw()
 
    def is_enemy_win(self):
        return not any(c.is_alive() and c.is_player for c in self.battle.all_chars())
    def is_player_win(self):
        return not any(c.is_alive() and not c.is_player for c in self.battle.all_chars())

    def branch_path(self):

        if self.is_enemy_win():
            # game_over()内ではなく、ここでHPを「１」に戻さないと、
            # ここに分岐しない
            for i, actor in enumerate(self.battle.pt):
                actor.hp = 1
            gbl.scene_state().Main()
            self.battle.pt.get_start_location()

        elif self.is_player_win():
            gbl.scene_state().Main()
        else:
            self.battle.reset_stack_wait_commands()

    def terminal_log(self):
        log = []
        if self.is_enemy_win():
            log += self.game_over()
        elif self.is_player_win():
            log += self.victory()
        else:
            log += self.next_turn()
        self.push(log)

    def next_turn(self):
        return [f"次のターン"]

    def victory(self):
        gld = 0
        for i, actor in enumerate(self.battle.mspt):
            gld += int(actor.gold * px.rndf(0.7, 1.0) + 0.99)
        self.battle.pt.add_gold(gld)

        return [f"たたかいに かった",f"{gld}G てにいれた"]


    def game_over(self):
        self.battle.pt.gold = self.battle.pt.gold // 2

        return [f"{"あなた"}たちは", "いしきを うしなった"]







# 視覚効果
class BattleStack_Effect(BaseState):

    def __init__(self, parent, type):
        self.battle = parent
        self.type = type
        self.active = []

    def enter(self):
        self.active.insert(0,Effect_Buffer([f"now loading..."]))

        if self.type == EFCT.DAMAGE:
            efct = Effect_Shake(self)
        elif self.type == EFCT.SLASH:
            efct = Effect_Slash(self)
        efct.enter()
        self.active.append(efct)

    def update(self):

        if not self.active:
            self.enter()

        self.active[0].update()

        if EFCT.DONE in self.active:
            # 自身をスタックから除外する
            self.battle.comand.popleft()

    def draw(self):
        self.active[0].draw()





# 値の確定
class BattleStack_Period(BaseState):
    def __init__(self, parent, *args, **kwargs):
        self.battle = parent
        self.func = args[0]
        self.user = args[1]
        self.targ = args[2]
        if 'dmg' in kwargs:
            self.dmg = kwargs['dmg']


    def update(self):
        self.func(self.targ, self.dmg)
        # 自身をスタックから除外する
        self.battle.comand.popleft()

        # check_vitalは、結果をappendleft()する。
        # self.battle.comand.popleft()の前に書くと、
        # 本クラス自身でなく、結果をpopleft()してしまう。
        self.user.vm.check_vital(self.targ, self.battle)
        self.user.action = ('', None)
        self.user.target = None




# 一人ずつ処理するため、待機用
# handle_execute_phase()内で一気に積み上げることも考えたが、
# 途中の生存判定など面倒だったので、
# 一人づつ処理するための区切りを設ける
class BattleStack_Delim(BaseState):
    def __init__(self, parent):
        self.battle = parent

    def update(self):
        # 次のactorのstackを積み上げる
        self.battle.exec_next_actor()

        # 自身をスタックから除外する
        self.battle.comand.popleft()



