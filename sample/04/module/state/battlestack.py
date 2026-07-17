
from collections import deque

import appconfig as gbl
from module.actor import *
from module.state.basestate import *
from module.state.optionstate import *





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
    

class BattleStack_Log(BaseState, Singleton):
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





class SelectObserver(Observer):
    def update(self, subject):
        if isinstance(subject, OptionState):
            print(f"[Log] 選択肢が {subject.sel_index} に変更されました")


# 1プレーヤーの行動に必要な、個々の選択肢を、
# ひとまとめにしてスタックする

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




class BattleStack_Confirm(OptionState):
    def __init__(self, parent):
        self.state = PHASE.CONFIRM
        self.battle = parent
        self.enter()

    def enter(self):
        COMMAND_TREE = {
            'はい'  : [self.battle.handle_execute_phase],
            'いいえ': [self.battle.stack_wait_commands],
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














