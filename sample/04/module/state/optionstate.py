
import pyxel as px

from module.constant import *
from module.UI import Meth
from module.state.basestate import *










class OptionState(BaseState):

    def __init__(self, tree):
        self.command_stack = [tree]  # 階層をスタックで管理
        self.sel_index = 0
        self.sel_value = None

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
                self.command_stack.append(sub_tree)
                self.sel_index = 0
            else:
                # ()は実行に付与する。
                args = len( list(sub_tree) )
                if args == 1:
                    sub_tree[0]()
                else:
                    sub_tree[0](**sub_tree[1])
