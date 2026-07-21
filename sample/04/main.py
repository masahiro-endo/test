
import pyxel as px

import appconfig as gbl
from module.UI import *
from module.actorparty import *
from module.state.scenestate import *
from resource.mapevent import *

import os
import sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))








class AppModel():
    def __init__(self):
        pass



class AppViewModel():
    def __init__(self, model):
        self.model = model

        self.config = gbl.global_setting()
        self.config.resource = MapResources()
        self.config.party = PlayerParty()

        self.config.scenestack = deque([SceneStates()])
        self.scene = gbl.scene_state()
        self.stack = gbl.scene_stack()

    def update(self):
        self.stack[0].update()

        # btn = get_btn_state()

        # # 十字キー押しっぱなし防止
        # if self.wait and (btn[BTN.UP] or btn[BTN.DWN] or btn[BTN.RHT] or btn[BTN.LFT]):
        #     return
        # self.wait = False
        # # カーソルがある場合カーソル処理を優先
        # if self.cur:
        #     cur = self.cur
        #     ret = cur.update(btn)
        #     # ショップの場合は左右キーを押したときにウィンドウを再表示
        #     # if btn[BTN.RHT] or btn[BTN.LFT]:
        #     #     if cur.key == "spells":
        #     #         self.MENU_SPL()
        #     #     elif cur.key == "shop":
        #     #         self.shop_show()
        #     #     elif cur.key == "bt_spells":
        #     #         self.battle_spells()
        #     # ABボタンを押してなければ終了
        #     if ret is None:
        #         return
        #     elif cur.key == "boss1":
        #         self.cur = None
        #         Window.close()
        #         if ret == 0:
        #             self.battle_start(5, "boss1")
        #     # イベント（ボス戦2）の選択肢
        #     elif cur.key == "boss2":
        #         self.cur = None
        #         Window.close()
        #         if ret == 0:
        #             self.battle_start(6, "boss2")
        #     # イベント（ボス戦3）の選択肢
        #     elif cur.key == "boss3":
        #         self.cur = None
        #         Window.close()
        #         if ret == 0:
        #             self.battle_start(7, "boss3")

        # 入力処理
        # AI処理
        # 衝突判定

        # View 用データ取得　関数定義


class AppView:
    def __init__(self, view_model):
        self.vm = view_model
        self.vm.scene.Main()
        self.vm.stack.appendleft(SceneState_Extend([f"encount !!"]))


        px.init(
            128, 160, title="Pyxel Sample", quit_key=px.KEY_NONE, display_scale=2
        )
        px.load("assets.pyxres")
        vm.config.BDF = px.Font("k8x12S.bdf")

        px.run(self.update, self.draw)


    def update(self):
        self.vm.update()

    def draw(self):
        px.cls(px.COLOR_BLACK)
        for scn in reversed(self.vm.stack):
            scn.draw()

        for key in Window.all:
            Window.all[key].draw()
        
        # プレイヤー
        # コイン
        # 敵
        # スコア表示



if __name__ == "__main__":
    model = AppModel()
    vm = AppViewModel(model)
    AppView(vm)
