import pyxel as px
import json
import copy
from UI import *
from actor import *
import appconfig as gbl
from module.scenestate import *



IS_WEB = True

try:
    from js import window
except:
    IS_WEB = False






# -------------------------
# Model: ゲーム状態
# -------------------------
class GameModel:
    def __init__(self):
        pass



# -------------------------
# ViewModel: ロジック制御
# -------------------------
class GameViewModel:
    def __init__(self, model: GameModel):
        self.model = model

        self.config = gbl.get_settings()
        self.config.party = Model_Party()

        self.config.screen = SceneStates()
        self.screen = gbl.get_screen()
        self.screen.Main()

        self.cur = None
        self.wait = False
        self.bgm = None
        self.scene = ""

    def update(self):
        self.screen.update()
        btn = get_btn_state()

        # 十字キー押しっぱなし防止
        if self.wait and (btn["u"] or btn["d"] or btn["r"] or btn["l"]):
            return
        self.wait = False
        # カーソルがある場合カーソル処理を優先
        if self.cur:
            cur = self.cur
            ret = cur.update(btn)
            # ショップの場合は左右キーを押したときにウィンドウを再表示
            if btn["r"] or btn["l"]:
                if cur.key == "spells":
                    self.menu_spells()
                elif cur.key == "shop":
                    self.shop_show()
                elif cur.key == "bt_spells":
                    self.battle_spells()
            # ABボタンを押してなければ終了
            if ret is None:
                return
            elif cur.key == "boss1":
                self.cur = None
                Window.close()
                if ret == 0:
                    self.battle_start(5, "boss1")
            # イベント（ボス戦2）の選択肢
            elif cur.key == "boss2":
                self.cur = None
                Window.close()
                if ret == 0:
                    self.battle_start(6, "boss2")
            # イベント（ボス戦3）の選択肢
            elif cur.key == "boss3":
                self.cur = None
                Window.close()
                if ret == 0:
                    self.battle_start(7, "boss3")

        # 入力処理
        # AI処理
        # 衝突判定

        # View 用データ取得　関数定義




# -------------------------
# View: 描画とイベントループ
# -------------------------
class GameView:
    def __init__(self, view_model: GameViewModel):
        self.vm = view_model

        px.init(
            128, 128, title="Pyxel Sample RPG", quit_key=px.KEY_NONE, display_scale=2
        )
        px.load("assets.pyxres")
        vm.config.BDF = px.Font("k8x12S.bdf")

        px.run(self.update, self.draw)

    def update(self):
        self.vm.update()

    def draw(self):
        px.cls(0)
        self.vm.screen.draw()


        # プレイヤー
        # コイン
        # 敵
        # スコア表示

        # ウィンドウ
        # for key in Window.all:
        #     Window.all[key].draw()
        # カーソル
        # if self.cur:
        #     self.cur.draw()




# -------------------------
# 実行
# -------------------------
if __name__ == "__main__":
    model = GameModel()  # 敵5体
    vm = GameViewModel(model)
    GameView(vm)
