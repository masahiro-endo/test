
import pyxel as px

from module.constant import *
from module.UI import Meth
from module.state.observer import *
from module.state.basestate import *









class OptionState(BaseState, Subject):

    def __init__(self, tree=None):
        super().__init__()
        self.tree = tree if tree else {'': []} #ダミー
        self.command_stack = [self.tree] # 階層をスタックで管理
        self._sel_i = auto()
        self._sel_v = None
        self.sel_index = 0
        self.is_leaf = False


    # 内部変数「_sel_i」と、プロパティ名「sel_index」を
    # 一致させてしまうと無限再帰
    @property
    def sel_index(self):
        return self._sel_i
    @sel_index.setter
    def sel_index(self, value):
        if value != self._sel_i:
            self._sel_i = value
            self.change_value()
            self.notify()

    @property
    def sel_value(self):
        return self._sel_v
    @sel_value.setter
    def sel_value(self, value):
        if value != self._sel_v:
            self._sel_v = value

    def enter(self):
        super().__init__()
        # 「閉じる」は、treeの要素をpop()しているので、
        # 開きなおす度に、初期化しないとエラーが起きる。
        self.command_stack = [self.tree]
        self.sel_index = 0

    def update(self):
        push = Meth.get_btn_state()

        if push[BTN.LFT]:
            self.sel_index = (self.sel_index - 1) % (len(self.command_stack[-1]) )
        elif push[BTN.RHT]:
            self.sel_index = (self.sel_index + 1) % (len(self.command_stack[-1]) )
        elif push[BTN.A_Z]:
            self.handle_selection()
        elif push[BTN.B_X]:
            self.command_stack.pop()
            self.sel_index = 0
            
    def draw(self):
        self.draw_commands()


    def change_value(self):
        current_tree = self.command_stack[-1]
        options = list(current_tree.items())
        self.sel_value = options[self.sel_index]
        pass

    def draw_commands(self):
        current_tree = self.command_stack[-1]
        options = list(current_tree.keys())

        # 選択肢文字数の合計
        slen = 0
        for i, cmd in enumerate(options):
            clr = px.COLOR_YELLOW if i == self.sel_index else px.COLOR_WHITE
            Meth.draw_text(1 + (slen + i), 14, cmd, clr)
            slen += len(cmd)

        # # 最上位なら「終了」、分岐に入っていたら「戻る」
        # i += 1
        # back_text = "終了" if len(self.command_stack) == 1 else "戻る"
        # clr = px.COLOR_YELLOW if self.sel_index == len(options) else px.COLOR_WHITE
        # Meth.draw_text(1 + (slen + i), 14, back_text, clr)


    def handle_selection(self):
        current_tree = self.command_stack[-1]
        options = list(current_tree.keys())

        if self.sel_index == len(options):
            # 最上位なら「終了」、分岐に入っていたら「戻る」
            if len(self.command_stack) == 1:
                px.quit()
            else:
                self.command_stack.pop()
                self.sel_index = 0
        else:
            selected_cmd = options[self.sel_index]
            sub_tree = current_tree[selected_cmd]
            if isinstance(sub_tree, dict):
                self.is_leaf = False
                # self.command_stack.append()した時の変数内部は、
                # 小項目を抜き出しているというよりは
                # 末尾要素に小項目を追加している
                #     command_stack[0] = {
                #         "たたかう": {
                #             "通常攻撃": None,
                #             "魔法": {
                #                 "回復": None,
                #                 "攻撃": None
                #             }
                #         },
                #     }
                #     command_stack[1] = {
                #         "魔法": {
                #             "回復": None,
                #             "攻撃": None
                #         }
                #     }

                self.command_stack.append(sub_tree)
                self.sel_index = 0
            else:
                self.is_leaf = True
                # ()は実行時に付与する。
                if not sub_tree:
                    return
                args = len( list(sub_tree) )
                if args == 0: 
                    pass
                elif args == 1:
                    if sub_tree[0]:
                        sub_tree[0]()
                else:
                    if sub_tree[0]:
                        sub_tree[0](**sub_tree[1])


    def show_message(self, texts):
        for pos, text in enumerate(texts):
            Meth.draw_text(1, 10 + pos * 2, text)

    def dict_depth(self, dic):
        if not isinstance(dic, dict) or not dic:
            return 0
        return 1 + max(self.dict_depth(v) for v in dic.values())

