
import pyxel as px
from UI import *
from actor import *
import appconfig as gbl
from module.scenestate import *
from resource.mapevent import *
import os
import sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))








class GameModel:
    def __init__(self):
        pass



class GameViewModel:
    def __init__(self, model: GameModel):
        self.model = model

        self.config = gbl.global_setting()
        self.config.party = PlayerParty()

        self.config.resource = MapResources()
        self.config.scene = SceneStates()
        self.scene = gbl.scene()

    def update(self):
        self.scene.update()

        # btn = get_btn_state()

        # # 十字キー押しっぱなし防止
        # if self.wait and (btn["u"] or btn["d"] or btn["r"] or btn["l"]):
        #     return
        # self.wait = False
        # # カーソルがある場合カーソル処理を優先
        # if self.cur:
        #     cur = self.cur
        #     ret = cur.update(btn)
        #     # ショップの場合は左右キーを押したときにウィンドウを再表示
        #     # if btn["r"] or btn["l"]:
        #     #     if cur.key == "spells":
        #     #         self.menu_spells()
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



class GameView:
    def __init__(self, view_model: GameViewModel):
        self.vm = view_model
        self.vm.scene.Battle()

        px.init(
            128, 128, title="Pyxel Sample RPG", quit_key=px.KEY_NONE, display_scale=2
        )
        px.load("assets.pyxres")
        vm.config.BDF = px.Font("k8x12S.bdf")

        px.run(self.update, self.draw)

    def update(self):
        self.vm.update()

    def draw(self):
        px.cls(pyxel.COLOR_BLACK)
        self.vm.scene.draw()

        for key in Window.all:
            Window.all[key].draw()
        
        # プレイヤー
        # コイン
        # 敵
        # スコア表示



if __name__ == "__main__":
    model = GameModel()
    vm = GameViewModel(model)
    GameView(vm)
